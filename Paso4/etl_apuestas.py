#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
Script: etl_apuestas_FIXED.py
Proyecto: Data Warehouse Apuestas Deportivas (HEFESTO)
Autor: Facundo Ortega
Descripción: Proceso ETL corregido para poblar fact_apuestas
============================================================
"""

import mysql.connector
from mysql.connector import Error
import logging
from datetime import datetime

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🔧 CONFIGURACIÓN
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Configuración MySQL
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'aloalo',  # ⚠️ CAMBIAR
    'database': 'apuestas_dw',
    'charset': 'utf8mb4'
}

# Mapeo casas de apuestas (código -> id_casa)
CASAS_APUESTAS = {
    'B365': 1,  # Bet365
    'BW': 2,    # Bet&Win
    'IW': 3,    # Interwetten
    'PS': 4     # Pinnacle Sports
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🔹 FUNCIONES AUXILIARES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def conectar_db():
    """Establece conexión con MySQL"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            logger.info("✅ Conexión a MySQL establecida")
            return conn
    except Error as e:
        logger.error(f"❌ Error de conexión: {e}")
        return None

def obtener_id_fecha(fecha_str):
    """
    Convierte fecha string a id_fecha (YYYYMMDD)
    Ejemplo: '2015-08-15' -> 20150815
    """
    try:
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d %H:%M:%S')
        return int(fecha.strftime('%Y%m%d'))
    except:
        return None

def calcular_resultado(goles_local, goles_visitante):
    """
    Calcula resultado del partido
    H = Home (local gana)
    D = Draw (empate)
    A = Away (visitante gana)
    """
    if goles_local > goles_visitante:
        return 'H'
    elif goles_local < goles_visitante:
        return 'A'
    else:
        return 'D'

def validar_cuotas(cuotas):
    """Verifica que las cuotas sean válidas (>= 1.01)"""
    return all(c is not None and c >= 1.01 for c in cuotas)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🔹 PROCESO ETL PRINCIPAL
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def ejecutar_etl():
    """Proceso ETL completo"""
    
    conn = conectar_db()
    if not conn:
        return False
    
    cursor = conn.cursor(dictionary=True)
    
    try:
        logger.info("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        logger.info("🚀 INICIANDO PROCESO ETL")
        logger.info("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
        # ━━━ PASO 1: EXTRAER datos de staging ━━━
        logger.info("📥 PASO 1: Extrayendo datos de staging...")
        
        query_extract = """
        SELECT 
            m.id,
            m.date,
            m.league_id,
            m.home_team_api_id,
            m.away_team_api_id,
            m.home_team_goal,
            m.away_team_goal,
            m.B365H, m.B365D, m.B365A,
            m.BWH, m.BWD, m.BWA,
            m.IWH, m.IWD, m.IWA,
            m.PSH, m.PSD, m.PSA
        FROM stg_match m
        WHERE m.B365H IS NOT NULL 
          AND m.B365D IS NOT NULL 
          AND m.B365A IS NOT NULL
          AND m.home_team_goal IS NOT NULL
          AND m.away_team_goal IS NOT NULL
        """
        
        cursor.execute(query_extract)
        partidos = cursor.fetchall()
        total_partidos = len(partidos)
        
        logger.info(f"   ✓ {total_partidos} partidos extraídos")
        
        if total_partidos == 0:
            logger.warning("⚠️  No hay datos para procesar")
            return False
        
        # ━━━ PASO 2: TRANSFORMAR y CARGAR ━━━
        logger.info("🔄 PASO 2: Transformando e insertando registros...")
        
        registros_insertados = 0
        errores = 0
        
        # Desactivar autocommit para mejor performance
        conn.autocommit = False
        
        # Preparar statement de inserción
        insert_query = """
        INSERT INTO fact_apuestas 
        (id_fecha, id_casa, id_league, id_home_team, id_away_team,
         home_team_goal, away_team_goal, resultado,
         cuota_local, cuota_empate, cuota_visitante)
        VALUES 
        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        # Procesar cada partido
        for i, partido in enumerate(partidos, 1):
            try:
                # Extraer datos base
                id_fecha = obtener_id_fecha(str(partido['date']))
                id_league = partido['league_id']
                id_home = partido['home_team_api_id']
                id_away = partido['away_team_api_id']
                goles_h = partido['home_team_goal']
                goles_a = partido['away_team_goal']
                resultado = calcular_resultado(goles_h, goles_a)
                
                # Validar datos esenciales
                if not all([id_fecha, id_league, id_home, id_away]):
                    logger.warning(f"   ⚠️  Partido {partido['id']}: datos incompletos")
                    errores += 1
                    continue
                
                # Procesar cada casa de apuestas
                for codigo_casa, id_casa in CASAS_APUESTAS.items():
                    # Obtener cuotas
                    cuota_h = partido.get(f'{codigo_casa}H')
                    cuota_d = partido.get(f'{codigo_casa}D')
                    cuota_a = partido.get(f'{codigo_casa}A')
                    
                    # Validar cuotas
                    if not validar_cuotas([cuota_h, cuota_d, cuota_a]):
                        continue
                    
                    # Insertar registro
                    cursor.execute(insert_query, (
                        id_fecha, id_casa, id_league, id_home, id_away,
                        goles_h, goles_a, resultado,
                        float(cuota_h), float(cuota_d), float(cuota_a)
                    ))
                    registros_insertados += 1
                
                # Commit cada 1000 registros
                if i % 1000 == 0:
                    conn.commit()
                    logger.info(f"   ✓ Procesados {i}/{total_partidos} partidos ({registros_insertados} registros)")
            
            except Error as e:
                logger.error(f"   ❌ Error en partido {partido['id']}: {e}")
                errores += 1
                continue
        
        # Commit final
        conn.commit()
        
        # ━━━ PASO 3: VALIDACIÓN ━━━
        logger.info("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        logger.info("✅ PROCESO ETL COMPLETADO")
        logger.info("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        logger.info(f"📊 RESUMEN:")
        logger.info(f"   • Partidos procesados: {total_partidos}")
        logger.info(f"   • Registros insertados: {registros_insertados}")
        logger.info(f"   • Errores: {errores}")
        
        # Validación final
        cursor.execute("SELECT COUNT(*) as total FROM fact_apuestas")
        total_fact = cursor.fetchone()['total']
        logger.info(f"   • Total en fact_apuestas: {total_fact}")
        
        # Distribución por casa
        logger.info("\n📈 Distribución por casa de apuestas:")
        cursor.execute("""
        SELECT 
            c.nombre,
            COUNT(*) as registros
        FROM fact_apuestas f
        JOIN dim_casa_apuestas c ON f.id_casa = c.id_casa
        GROUP BY c.nombre
        ORDER BY registros DESC
        """)
        
        for row in cursor.fetchall():
            logger.info(f"   • {row['nombre']}: {row['registros']:,}")
        
        logger.info("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
        return True
        
    except Error as e:
        logger.error(f"❌ Error crítico en ETL: {e}")
        conn.rollback()
        return False
        
    finally:
        cursor.close()
        conn.close()
        logger.info("🔌 Conexión cerrada")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🔹 EJECUCIÓN PRINCIPAL
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

if __name__ == "__main__":
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║   ETL APUESTAS DEPORTIVAS - Data Warehouse HEFESTO       ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    # Confirmar ejecución
    respuesta = input("¿Ejecutar proceso ETL? (s/n): ")
    
    if respuesta.lower() == 's':
        inicio = datetime.now()
        exito = ejecutar_etl()
        fin = datetime.now()
        duracion = (fin - inicio).total_seconds()
        
        if exito:
            print(f"\n✅ ETL completado en {duracion:.2f} segundos")
        else:
            print(f"\n❌ ETL falló después de {duracion:.2f} segundos")
    else:
        print("❌ Proceso cancelado")