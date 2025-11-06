# 📊 ESTADO ACTUAL DEL DATA WAREHOUSE

**Fecha**: Noviembre 2025
**Última Verificación**: Ahora mismo

---

## ✅ COMPLETADO

### Base de Datos Creada
- ✅ Base de datos `apuestas_dw` creada correctamente
- ✅ Esquema ESTRELLA implementado
- ✅ 7 tablas creadas (1 hechos + 6 dimensiones)

### Tablas Verificadas

| Tabla | Registros | Estado | Comentario |
|-------|-----------|--------|------------|
| `DIM_CASA_APUESTAS` | 10 | ✅ Completa | 10 casas de apuestas |
| `DIM_ESTRATEGIA` | 4 | ✅ Completa | 4 estrategias de apuesta |
| `DIM_RESULTADO_TIPO` | 3 | ✅ Completa | 3 tipos (H/D/A) |
| `DIM_FECHA` | 0 | ⚠️ Vacía | Requiere carga ETL |
| `DIM_LIGA` | 0 | ⚠️ Vacía | Requiere carga ETL |
| `DIM_EQUIPO` | 0 | ⚠️ Vacía | Requiere carga ETL |
| `FACT_APUESTAS` | 0 | ⚠️ Vacía | Requiere carga ETL |

### Campos Derivados de Arbitraje Configurados

La tabla `FACT_APUESTAS` tiene los 8 campos derivados para arbitraje:
- ✅ `arbitraje_cuota_local_max`
- ✅ `arbitraje_cuota_empate_max`
- ✅ `arbitraje_cuota_visitante_max`
- ✅ `arbitraje_casa_local_mejor`
- ✅ `arbitraje_casa_empate_mejor`
- ✅ `arbitraje_casa_visitante_mejor`
- ✅ `arbitraje_porcentaje`
- ✅ `arbitraje_es_oportunidad`
- ✅ `arbitraje_beneficio`

### Índices Configurados
- ✅ Índices en FKs de todas las dimensiones
- ✅ Índice filtrado para arbitraje: `idx_fact_arbitraje`
- ✅ Índices de búsqueda en campos clave

---

## ⚠️ PENDIENTE: CARGA DE DATOS (ETL)

Para poder usar Power BI, necesitas cargar los datos históricos.

### Opción 1: Usar Database.sqlite Existente

Si tienes el archivo `database.sqlite` en la raíz del proyecto:

#### Paso A: Exportar a CSV (si no lo hiciste)

```bash
cd "C:\Users\santi\OneDrive\Documentos\Documentos\2025\BD2\BD2_Hefesto_ApuetasDeportivas"

# Verificar que existe database.sqlite
dir database.sqlite

# Si existe, ir a Paso4 y exportar
cd Paso4
bash export_sqlite_to_csv.sh
```

Esto creará la carpeta `export_csv/` con:
- Country.csv
- League.csv
- Team.csv
- Match.csv

#### Paso B: Verificar CSVs Generados

```bash
dir "C:\Users\santi\OneDrive\Documentos\Documentos\2025\BD2\BD2_Hefesto_ApuetasDeportivas\Paso4\export_csv"
```

**Archivos esperados**:
- Country.csv (~11 registros)
- League.csv (~11 registros)
- Team.csv (~300 registros)
- Match.csv (~25,979 registros)

#### Paso C: Ejecutar ETL Python

1. **Modificar contraseña** en `etl_apuestas.py`:

   Abrir archivo y cambiar línea 33:
   ```python
   'password': 'pepe1234',  # Tu contraseña
   ```

2. **Instalar dependencias**:
   ```bash
   pip install mysql-connector-python
   ```

3. **Ejecutar ETL**:
   ```bash
   cd "C:\Users\santi\OneDrive\Documentos\Documentos\2025\BD2\BD2_Hefesto_ApuetasDeportivas\Paso4"
   python etl_apuestas.py
   ```

**Tiempo estimado**: 10-20 minutos para procesar ~900K registros.

**Progreso esperado**:
```
[INFO] Conectando a MySQL...
[INFO] Poblando DIM_FECHA...
[INFO] Poblando DIM_LIGA...
[INFO] Poblando DIM_EQUIPO...
[INFO] Procesando partidos y generando apuestas...
[INFO] Calculando campos derivados de arbitraje...
[INFO] Insertando en FACT_APUESTAS...
[INFO] ✅ ETL completado: 903,680 registros insertados
```

### Opción 2: Usar Datos de Prueba (Rápido)

Si no tienes `database.sqlite` o quieres probar rápido, puedo generar un script con datos de prueba.

---

## 🔍 VERIFICACIÓN POST-ETL

Una vez completado el ETL, ejecuta estas verificaciones:

### Verificación 1: Conteo de Registros

```bash
"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -ppepe1234 -e "USE apuestas_dw; SELECT 'FACT_APUESTAS' as Tabla, COUNT(*) as Total FROM fact_apuestas;"
```

**Esperado**: ~903,680 registros (o ~226K si son 4 estrategias × partidos sin unpivot completo)

### Verificación 2: Dimensiones Pobladas

```bash
"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -ppepe1234 -e "USE apuestas_dw; SELECT 'DIM_FECHA' as Dim, COUNT(*) as Total FROM dim_fecha UNION ALL SELECT 'DIM_LIGA', COUNT(*) FROM dim_liga UNION ALL SELECT 'DIM_EQUIPO', COUNT(*) FROM dim_equipo;"
```

**Esperado**:
- DIM_FECHA: ~2,920 registros (fechas únicas)
- DIM_LIGA: 11 registros
- DIM_EQUIPO: ~400 registros (con SCD-2)

### Verificación 3: Campos Derivados de Arbitraje

```bash
"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -ppepe1234 -e "USE apuestas_dw; SELECT COUNT(*) as Partidos_Con_Arbitraje FROM fact_apuestas WHERE arbitraje_es_oportunidad = TRUE LIMIT 1;"
```

**Esperado**: > 0 (debería haber oportunidades de arbitraje)

### Verificación 4: Integridad Referencial

```bash
"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -ppepe1234 -e "USE apuestas_dw; SELECT COUNT(*) as Huerfanos FROM fact_apuestas f LEFT JOIN dim_fecha d ON f.id_fecha = d.id_fecha WHERE d.id_fecha IS NULL;"
```

**Esperado**: 0 (no debe haber registros huérfanos)

---

## 🎯 SIGUIENTE: POWER BI

Una vez que tengas datos cargados (verificaciones anteriores con resultados esperados), puedes proceder con Power BI:

### Checklist Pre-Power BI

- [ ] Base de datos `apuestas_dw` existe
- [ ] 7 tablas creadas
- [ ] `FACT_APUESTAS` tiene > 100,000 registros
- [ ] `DIM_FECHA` tiene > 1,000 registros
- [ ] `DIM_LIGA` tiene 11 registros
- [ ] `DIM_EQUIPO` tiene > 100 registros
- [ ] Campos derivados de arbitraje tienen valores (no todos NULL)
- [ ] MySQL corriendo en localhost:3306

### Conexión Power BI

Una vez completadas las verificaciones:

1. Abrir Power BI Desktop
2. `Obtener datos > MySQL database`
3. Servidor: `localhost`
4. Base de datos: `apuestas_dw`
5. Usuario: `root`
6. Contraseña: `pepe1234`
7. Seleccionar las 7 tablas
8. Importar datos

**Continuar con**: `README_POWERBI_PASO_A_PASO.md` (Paso 5 de la guía)

---

## 📁 ARCHIVOS CLAVE

### SQL Scripts
- `create_dw_WINDOWS.sql` ← **EJECUTADO** ✅
- `create_staging_and_load.sql` (original, requiere ajustes)

### Python Scripts
- `etl_apuestas.py` ← **PENDIENTE** (modificar contraseña y ejecutar)
- `export_sqlite_to_csv.sh` ← Ejecutar si tienes database.sqlite

### Documentación
- `DIAGNOSTICO_Y_EJECUCION.md` ← Guía completa de troubleshooting
- `ESTADO_ACTUAL.md` ← Este documento
- `../Paso5/README_POWERBI_PASO_A_PASO.md` ← Siguiente paso

---

## 🆘 SI ALGO FALLA

### Problema: No tengo database.sqlite

**Solución 1**: Descargar de Kaggle
- Dataset: "European Soccer Database"
- Link: https://www.kaggle.com/hugomathien/soccer
- Colocar en raíz del proyecto

**Solución 2**: Usar datos de prueba
- Puedo generar un script SQL con datos sintéticos para probar
- Menos realista pero funcional para Power BI

### Problema: Python no instalado

**Solución**: Instalar Python
1. Descargar: https://www.python.org/downloads/
2. Durante instalación: ✅ Marcar "Add Python to PATH"
3. Verificar: `python --version` en CMD

### Problema: MySQL no arranca

**Solución**: Verificar servicio
```bash
# Ver estado
net start | findstr MySQL

# Iniciar si está detenido
net start MySQL80
```

### Problema: Errores de permisos en MySQL

**Solución**: Verificar privilegios
```sql
GRANT ALL PRIVILEGES ON apuestas_dw.* TO 'root'@'localhost';
FLUSH PRIVILEGES;
```

---

## 📊 RESUMEN VISUAL

```
┌─────────────────────────────────────────────────────────┐
│          ESTADO DEL DATA WAREHOUSE                      │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ✅ COMPLETADO:                                         │
│     • Base de datos creada                              │
│     • Esquema estrella implementado                     │
│     • 3 dimensiones pequeñas pobladas                   │
│     • Campos derivados de arbitraje configurados        │
│                                                          │
│  ⚠️ PENDIENTE:                                          │
│     • Cargar DIM_FECHA, DIM_LIGA, DIM_EQUIPO          │
│     • Cargar FACT_APUESTAS (~900K registros)           │
│     • Calcular campos derivados de arbitraje            │
│                                                          │
│  🎯 SIGUIENTE PASO:                                     │
│     Ejecutar etl_apuestas.py (modificar contraseña)    │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

**Actualizado**: Noviembre 2025
**Estado**: Listo para carga de datos (ETL)
**Bloqueador**: Necesitas ejecutar `etl_apuestas.py` con tus datos
