#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
Script: etl_estrella_completo.py
Proyecto: Data Warehouse Apuestas Deportivas (HEFESTO)
Esquema: ESTRELLA con campos derivados de arbitraje
Fecha: Noviembre 2025
============================================================
"""

import sqlite3
import mysql.connector
from mysql.connector import Error
import logging
from datetime import datetime
from collections import defaultdict

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🔧 CONFIGURACIÓN
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

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
    'password': 'pepe1234',  # ✅ Tu contraseña
    'database': 'apuestas_dw',
    'charset': 'utf8mb4'
}

# Ruta al archivo SQLite
SQLITE_PATH = r"C:\Users\santi\OneDrive\Documentos\Documentos\2025\BD2\BD2_Hefesto_ApuetasDeportivas\database.sqlite"

# Mapeo de casas de apuestas (código → id_casa)
CASAS_APUESTAS = {
    'B365': 1,  'BW': 2,   'IW': 3,   'LB': 4,   'PS': 5,
    'WH': 6,    'SJ': 7,   'VC': 8,   'GB': 9,   'BS': 10
}

# Mapeo de estrategias
ESTRATEGIAS = {
    'ALWAYS_H': 1,
    'ALWAYS_A': 2,
    'FOLLOW_FAV': 3,
    'UNDERDOG': 4
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🔹 FUNCIONES DE CONEXIÓN
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def conectar_sqlite():
    """Conectar a SQLite"""
    try:
        conn = sqlite3.connect(SQLITE_PATH)
        logger.info(f"✅ Conectado a SQLite: {SQLITE_PATH}")
        return conn
    except Exception as e:
        logger.error(f"❌ Error conectando a SQLite: {e}")
        raise

def conectar_mysql():
    """Conectar a MySQL"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        logger.info(f"✅ Conectado a MySQL: {DB_CONFIG['database']}")
        return conn
    except Error as e:
        logger.error(f"❌ Error conectando a MySQL: {e}")
        raise

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🔹 FUNCIONES DE CARGA DE DIMENSIONES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def cargar_dim_fecha(sqlite_conn, mysql_conn):
    """Cargar DIM_FECHA desde fechas únicas de Match"""
    logger.info("📅 Cargando DIM_FECHA...")

    sqlite_cursor = sqlite_conn.cursor()
    mysql_cursor = mysql_conn.cursor()

    # Obtener fechas únicas
    sqlite_cursor.execute("""
        SELECT DISTINCT date
        FROM Match
        WHERE date IS NOT NULL
        ORDER BY date
    """)

    fechas = sqlite_cursor.fetchall()
    logger.info(f"   Encontradas {len(fechas)} fechas únicas")

    contador = 0
    for (fecha_str,) in fechas:
        try:
            # Parsear fecha
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d %H:%M:%S')

            # Determinar temporada (ej: 2015-08-01 → 2015/16)
            if fecha.month >= 8:
                temporada = f"{fecha.year}/{str(fecha.year + 1)[-2:]}"
            else:
                temporada = f"{fecha.year - 1}/{str(fecha.year)[-2:]}"

            # Determinar trimestre
            trimestre = (fecha.month - 1) // 3 + 1

            # Nombres
            meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                     'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
            dias_semana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']

            nombre_mes = meses[fecha.month - 1]
            nombre_dia = dias_semana[fecha.weekday()]
            es_fin_semana = 1 if fecha.weekday() >= 5 else 0

            # Insertar
            mysql_cursor.execute("""
                INSERT INTO DIM_FECHA
                (fecha, dia, mes, anio, trimestre, nombre_mes, nombre_dia_semana,
                 temporada, es_fin_semana)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE id_fecha=id_fecha
            """, (
                fecha.date(), fecha.day, fecha.month, fecha.year, trimestre,
                nombre_mes, nombre_dia, temporada, es_fin_semana
            ))

            contador += 1

        except Exception as e:
            logger.warning(f"   Error procesando fecha {fecha_str}: {e}")

    mysql_conn.commit()
    logger.info(f"   ✅ {contador} fechas insertadas")

    sqlite_cursor.close()
    mysql_cursor.close()

def cargar_dim_liga(sqlite_conn, mysql_conn):
    """Cargar DIM_LIGA desde League y Country"""
    logger.info("⚽ Cargando DIM_LIGA...")

    sqlite_cursor = sqlite_conn.cursor()
    mysql_cursor = mysql_conn.cursor()

    # JOIN League con Country
    sqlite_cursor.execute("""
        SELECT DISTINCT l.id, l.name, c.name
        FROM League l
        JOIN Country c ON l.country_id = c.id
        ORDER BY l.id
    """)

    ligas = sqlite_cursor.fetchall()
    logger.info(f"   Encontradas {len(ligas)} ligas")

    for (id_liga, nombre_liga, pais) in ligas:
        mysql_cursor.execute("""
            INSERT INTO DIM_LIGA (codigo_liga, nombre_liga, pais, nivel_competicion)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE id_liga=id_liga
        """, (f"LIGA_{id_liga}", nombre_liga, pais, 1))

    mysql_conn.commit()
    logger.info(f"   ✅ {len(ligas)} ligas insertadas")

    sqlite_cursor.close()
    mysql_cursor.close()

def cargar_dim_equipo(sqlite_conn, mysql_conn):
    """Cargar DIM_EQUIPO con SCD Tipo 2"""
    logger.info("👥 Cargando DIM_EQUIPO...")

    sqlite_cursor = sqlite_conn.cursor()
    mysql_cursor = mysql_conn.cursor()

    # Obtener todos los equipos únicos
    sqlite_cursor.execute("""
        SELECT DISTINCT t.team_api_id, t.team_long_name, t.team_short_name
        FROM Team t
        ORDER BY t.team_api_id
    """)

    equipos = sqlite_cursor.fetchall()
    logger.info(f"   Encontrados {len(equipos)} equipos únicos")

    # Por simplicidad, crear una versión única por equipo
    # (En producción, aquí iría la lógica de SCD-2 con cambios de liga)
    for (codigo_equipo, nombre_largo, nombre_corto) in equipos:
        # Asignar a primera liga por defecto (ajustar según lógica real)
        mysql_cursor.execute("""
            INSERT INTO DIM_EQUIPO
            (codigo_equipo, nombre_equipo, nombre_corto, id_liga,
             fecha_inicio, fecha_fin, registro_actual)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (codigo_equipo, nombre_largo, nombre_corto, 1,
              '2008-01-01', None, True))

    mysql_conn.commit()
    logger.info(f"   ✅ {len(equipos)} equipos insertados")

    sqlite_cursor.close()
    mysql_cursor.close()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🔹 CARGA DE FACT_APUESTAS CON ARBITRAJE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def calcular_campos_arbitraje(cuotas_partido):
    """
    Calcular campos derivados de arbitraje para un partido

    Args:
        cuotas_partido: dict con todas las cuotas del partido
            {'B365': {'H': 1.85, 'D': 3.40, 'A': 4.20}, 'BW': {...}, ...}

    Returns:
        dict con campos derivados
    """
    # Encontrar cuotas máximas por resultado
    max_cuota_local = 0
    max_cuota_empate = 0
    max_cuota_visitante = 0
    casa_mejor_local = None
    casa_mejor_empate = None
    casa_mejor_visitante = None

    for casa, cuotas in cuotas_partido.items():
        if cuotas['H'] and cuotas['H'] > max_cuota_local:
            max_cuota_local = cuotas['H']
            casa_mejor_local = CASAS_APUESTAS.get(casa)

        if cuotas['D'] and cuotas['D'] > max_cuota_empate:
            max_cuota_empate = cuotas['D']
            casa_mejor_empate = CASAS_APUESTAS.get(casa)

        if cuotas['A'] and cuotas['A'] > max_cuota_visitante:
            max_cuota_visitante = cuotas['A']
            casa_mejor_visitante = CASAS_APUESTAS.get(casa)

    # Calcular porcentaje de arbitraje
    if max_cuota_local > 0 and max_cuota_empate > 0 and max_cuota_visitante > 0:
        porcentaje = (1/max_cuota_local + 1/max_cuota_empate + 1/max_cuota_visitante)
        es_oportunidad = porcentaje < 1.0
        beneficio = ((1/porcentaje) - 1) * 100 if es_oportunidad else 0
    else:
        porcentaje = None
        es_oportunidad = False
        beneficio = 0

    return {
        'arbitraje_cuota_local_max': max_cuota_local if max_cuota_local > 0 else None,
        'arbitraje_cuota_empate_max': max_cuota_empate if max_cuota_empate > 0 else None,
        'arbitraje_cuota_visitante_max': max_cuota_visitante if max_cuota_visitante > 0 else None,
        'arbitraje_casa_local_mejor': casa_mejor_local,
        'arbitraje_casa_empate_mejor': casa_mejor_empate,
        'arbitraje_casa_visitante_mejor': casa_mejor_visitante,
        'arbitraje_porcentaje': porcentaje,
        'arbitraje_es_oportunidad': es_oportunidad,
        'arbitraje_beneficio': beneficio
    }

def cargar_fact_apuestas(sqlite_conn, mysql_conn):
    """Cargar FACT_APUESTAS con campos derivados de arbitraje"""
    logger.info("📊 Cargando FACT_APUESTAS (esto puede tomar 10-20 minutos)...")

    sqlite_cursor = sqlite_conn.cursor()
    mysql_cursor = mysql_conn.cursor()

    # Crear mapeos de dimensiones
    logger.info("   Creando mapeos de dimensiones...")

    # Mapeo fecha
    mysql_cursor.execute("SELECT id_fecha, fecha FROM DIM_FECHA")
    map_fecha = {str(fecha): id_fecha for id_fecha, fecha in mysql_cursor.fetchall()}

    # Mapeo liga
    mysql_cursor.execute("SELECT id_liga, codigo_liga FROM DIM_LIGA")
    map_liga = {codigo: id_liga for id_liga, codigo in mysql_cursor.fetchall()}

    # Mapeo equipo
    mysql_cursor.execute("SELECT id_equipo, codigo_equipo FROM DIM_EQUIPO WHERE registro_actual = 1")
    map_equipo = {codigo: id_equipo for id_equipo, codigo in mysql_cursor.fetchall()}

    # Obtener partidos con cuotas completas
    logger.info("   Extrayendo partidos desde SQLite...")
    sqlite_cursor.execute("""
        SELECT
            m.id, m.date, m.league_id, m.home_team_api_id, m.away_team_api_id,
            m.home_team_goal, m.away_team_goal,
            m.B365H, m.B365D, m.B365A,
            m.BWH, m.BWD, m.BWA,
            m.IWH, m.IWD, m.IWA,
            m.LBH, m.LBD, m.LBA,
            m.PSH, m.PSD, m.PSA,
            m.WHH, m.WHD, m.WHA,
            m.SJH, m.SJD, m.SJA,
            m.VCH, m.VCD, m.VCA,
            m.GBH, m.GBD, m.GBA,
            m.BSH, m.BSD, m.BSA
        FROM Match m
        WHERE m.B365H IS NOT NULL
          AND m.BWH IS NOT NULL
          AND m.IWH IS NOT NULL
          AND m.home_team_goal IS NOT NULL
        ORDER BY m.date
    """)

    partidos = sqlite_cursor.fetchall()
    total_partidos = len(partidos)
    logger.info(f"   Procesando {total_partidos} partidos...")

    registros_insertados = 0
    partidos_procesados = 0
    batch_size = 1000
    registros_batch = []

    for partido in partidos:
        partidos_procesados += 1

        # Desempaquetar datos
        (id_partido, fecha_str, league_id, home_team_id, away_team_id,
         goles_local, goles_visitante,
         b365h, b365d, b365a, bwh, bwd, bwa, iwh, iwd, iwa,
         lbh, lbd, lba, psh, psd, psa, whh, whd, wha,
         sjh, sjd, sja, vch, vcd, vca, gbh, gbd, gba,
         bsh, bsd, bsa) = partido

        # Determinar resultado
        if goles_local > goles_visitante:
            resultado_real = 'H'
        elif goles_local < goles_visitante:
            resultado_real = 'A'
        else:
            resultado_real = 'D'

        # Mapear dimensiones
        fecha_key = fecha_str.split()[0]  # '2015-08-15'
        id_fecha = map_fecha.get(fecha_key)
        id_liga = map_liga.get(f"LIGA_{league_id}")
        id_equipo_local = map_equipo.get(home_team_id)
        id_equipo_visitante = map_equipo.get(away_team_id)

        if not all([id_fecha, id_liga, id_equipo_local, id_equipo_visitante]):
            continue

        # Organizar cuotas por casa
        cuotas_partido = {
            'B365': {'H': b365h, 'D': b365d, 'A': b365a},
            'BW': {'H': bwh, 'D': bwd, 'A': bwa},
            'IW': {'H': iwh, 'D': iwd, 'A': iwa},
            'LB': {'H': lbh, 'D': lbd, 'A': lba},
            'PS': {'H': psh, 'D': psd, 'A': psa},
            'WH': {'H': whh, 'D': whd, 'A': wha},
            'SJ': {'H': sjh, 'D': sjd, 'A': sja},
            'VC': {'H': vch, 'D': vcd, 'A': vca},
            'GB': {'H': gbh, 'D': gbd, 'A': gba},
            'BS': {'H': bsh, 'D': bsd, 'A': bsa}
        }

        # CALCULAR CAMPOS DERIVADOS DE ARBITRAJE (1 VEZ POR PARTIDO)
        campos_arbitraje = calcular_campos_arbitraje(cuotas_partido)

        # Generar registros para cada casa × estrategia × resultado
        for casa_codigo, id_casa in CASAS_APUESTAS.items():
            cuotas_casa = cuotas_partido[casa_codigo]

            if not all([cuotas_casa['H'], cuotas_casa['D'], cuotas_casa['A']]):
                continue

            for estrat_codigo, id_estrategia in ESTRATEGIAS.items():
                # Determinar qué se apostó según estrategia
                if estrat_codigo == 'ALWAYS_H':
                    resultado_apostado = 'H'
                    cuota_apostada = cuotas_casa['H']
                elif estrat_codigo == 'ALWAYS_A':
                    resultado_apostado = 'A'
                    cuota_apostada = cuotas_casa['A']
                elif estrat_codigo == 'FOLLOW_FAV':
                    # Apostar al favorito (menor cuota)
                    min_cuota = min(cuotas_casa['H'], cuotas_casa['D'], cuotas_casa['A'])
                    if cuotas_casa['H'] == min_cuota:
                        resultado_apostado = 'H'
                    elif cuotas_casa['D'] == min_cuota:
                        resultado_apostado = 'D'
                    else:
                        resultado_apostado = 'A'
                    cuota_apostada = min_cuota
                elif estrat_codigo == 'UNDERDOG':
                    # Apostar al underdog (mayor cuota)
                    max_cuota = max(cuotas_casa['H'], cuotas_casa['D'], cuotas_casa['A'])
                    if cuotas_casa['H'] == max_cuota:
                        resultado_apostado = 'H'
                    elif cuotas_casa['D'] == max_cuota:
                        resultado_apostado = 'D'
                    else:
                        resultado_apostado = 'A'
                    cuota_apostada = max_cuota

                # Calcular ganancia/pérdida
                inversion = 1.0
                if resultado_apostado == resultado_real:
                    ganancia = cuota_apostada * inversion
                    perdida = 0
                    aciertos = 1
                else:
                    ganancia = 0
                    perdida = inversion
                    aciertos = 0

                # Mapear tipo de resultado
                id_resultado_tipo = {'H': 1, 'D': 2, 'A': 3}[resultado_apostado]

                # Crear registro (DUPLICAR campos de arbitraje)
                registro = (
                    id_fecha, id_equipo_local, id_equipo_visitante, id_liga,
                    id_casa, id_estrategia, id_resultado_tipo,
                    id_partido, goles_local, goles_visitante, resultado_real,
                    cuota_apostada, cuotas_casa['H'], cuotas_casa['D'], cuotas_casa['A'],
                    ganancia, perdida, inversion, aciertos, 1,
                    # CAMPOS DERIVADOS DE ARBITRAJE (duplicados)
                    campos_arbitraje['arbitraje_cuota_local_max'],
                    campos_arbitraje['arbitraje_cuota_empate_max'],
                    campos_arbitraje['arbitraje_cuota_visitante_max'],
                    campos_arbitraje['arbitraje_casa_local_mejor'],
                    campos_arbitraje['arbitraje_casa_empate_mejor'],
                    campos_arbitraje['arbitraje_casa_visitante_mejor'],
                    campos_arbitraje['arbitraje_porcentaje'],
                    campos_arbitraje['arbitraje_es_oportunidad'],
                    campos_arbitraje['arbitraje_beneficio']
                )

                registros_batch.append(registro)

        # Insertar en batch
        if len(registros_batch) >= batch_size:
            mysql_cursor.executemany("""
                INSERT INTO FACT_APUESTAS (
                    id_fecha, id_equipo_local, id_equipo_visitante, id_liga,
                    id_casa_apuestas, id_estrategia, id_resultado_tipo,
                    id_partido, goles_local, goles_visitante, resultado_real,
                    cuota_apostada, cuota_local, cuota_empate, cuota_visitante,
                    ganancia_total, perdida_total, inversion, cant_aciertos, cant_apuestas,
                    arbitraje_cuota_local_max, arbitraje_cuota_empate_max, arbitraje_cuota_visitante_max,
                    arbitraje_casa_local_mejor, arbitraje_casa_empate_mejor, arbitraje_casa_visitante_mejor,
                    arbitraje_porcentaje, arbitraje_es_oportunidad, arbitraje_beneficio
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                          %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, registros_batch)

            mysql_conn.commit()
            registros_insertados += len(registros_batch)
            registros_batch = []

            # Log de progreso
            if partidos_procesados % 1000 == 0:
                progreso = (partidos_procesados / total_partidos) * 100
                logger.info(f"   Progreso: {partidos_procesados}/{total_partidos} partidos ({progreso:.1f}%) - {registros_insertados} registros")

    # Insertar registros restantes
    if registros_batch:
        mysql_cursor.executemany("""
            INSERT INTO FACT_APUESTAS (
                id_fecha, id_equipo_local, id_equipo_visitante, id_liga,
                id_casa_apuestas, id_estrategia, id_resultado_tipo,
                id_partido, goles_local, goles_visitante, resultado_real,
                cuota_apostada, cuota_local, cuota_empate, cuota_visitante,
                ganancia_total, perdida_total, inversion, cant_aciertos, cant_apuestas,
                arbitraje_cuota_local_max, arbitraje_cuota_empate_max, arbitraje_cuota_visitante_max,
                arbitraje_casa_local_mejor, arbitraje_casa_empate_mejor, arbitraje_casa_visitante_mejor,
                arbitraje_porcentaje, arbitraje_es_oportunidad, arbitraje_beneficio
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                      %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, registros_batch)
        mysql_conn.commit()
        registros_insertados += len(registros_batch)

    logger.info(f"   ✅ {registros_insertados} registros insertados en FACT_APUESTAS")

    sqlite_cursor.close()
    mysql_cursor.close()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🔹 FUNCIÓN PRINCIPAL
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def main():
    """Proceso ETL completo"""
    inicio = datetime.now()
    logger.info("=" * 60)
    logger.info("🚀 INICIANDO ETL - DATA WAREHOUSE APUESTAS DEPORTIVAS")
    logger.info("   Esquema: ESTRELLA con campos derivados de arbitraje")
    logger.info("=" * 60)

    try:
        # Conectar a bases de datos
        logger.info("\n📡 CONECTANDO A BASES DE DATOS...")
        sqlite_conn = conectar_sqlite()
        mysql_conn = conectar_mysql()

        # Cargar dimensiones
        logger.info("\n📥 CARGANDO DIMENSIONES...")
        cargar_dim_fecha(sqlite_conn, mysql_conn)
        cargar_dim_liga(sqlite_conn, mysql_conn)
        cargar_dim_equipo(sqlite_conn, mysql_conn)

        # Cargar tabla de hechos
        logger.info("\n📊 CARGANDO TABLA DE HECHOS...")
        cargar_fact_apuestas(sqlite_conn, mysql_conn)

        # Cerrar conexiones
        sqlite_conn.close()
        mysql_conn.close()

        # Resumen final
        fin = datetime.now()
        duracion = (fin - inicio).total_seconds()

        logger.info("\n" + "=" * 60)
        logger.info("✅ ETL COMPLETADO EXITOSAMENTE")
        logger.info(f"⏱️  Tiempo total: {duracion:.1f} segundos ({duracion/60:.1f} minutos)")
        logger.info("=" * 60)

        logger.info("\n🎯 SIGUIENTE PASO:")
        logger.info("   Ejecutar verificaciones en ESTADO_ACTUAL.md")
        logger.info("   Luego continuar con Power BI (Paso 5)")

    except Exception as e:
        logger.error(f"\n❌ ERROR DURANTE ETL: {e}")
        raise

if __name__ == "__main__":
    main()
