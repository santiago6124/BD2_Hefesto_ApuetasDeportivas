# 🔍 DIAGNÓSTICO Y EJECUCIÓN DEL DATA WAREHOUSE

**Fecha**: Noviembre 2025
**Estado Actual**: Base de datos `apuestas_dw` NO creada
**Acción Requerida**: Ejecutar scripts del Paso 4

---

## ❌ PROBLEMA DETECTADO

La base de datos `apuestas_dw` no existe en tu servidor MySQL.

**Bases de datos actuales encontradas**:
```
- clase 3
- db_backup_test
- empleados
- gimnasio_db
- information_schema
- mi_db
- mysql
- northwind
- peliculas
- performance_schema
- sakila
- sys
- teoricodb
- world
```

**Falta**: `apuestas_dw` (necesaria para Power BI)

---

## ✅ SOLUCIÓN: EJECUTAR PASO 4 COMPLETO

### Opción A: Ejecución Automática (Recomendada)

Te voy a crear un script batch que ejecute todo automáticamente.

### Opción B: Ejecución Manual Paso a Paso

---

## PASO 1: PREPARAR ARCHIVOS CSV

### 1.1 Verificar que existen los CSVs

```bash
dir "C:\Users\santi\OneDrive\Documentos\Documentos\2025\BD2\BD2_Hefesto_ApuetasDeportivas\Paso4\export_csv"
```

**Archivos esperados**:
- Country.csv
- League.csv
- Team.csv
- Match.csv

### 1.2 Si NO existen, ejecutar script de exportación

```bash
cd "C:\Users\santi\OneDrive\Documentos\Documentos\2025\BD2\BD2_Hefesto_ApuetasDeportivas\Paso4"

bash export_sqlite_to_csv.sh
```

---

## PASO 2: MODIFICAR SCRIPT SQL CON TUS RUTAS

### 2.1 Crear versión corregida del SQL

El archivo `create_staging_and_load.sql` tiene rutas de Linux que debes cambiar a Windows.

**Ruta actual (Linux)**:
```sql
LOAD DATA LOCAL INFILE '/home/facundo/Documents/...'
```

**Debe ser (Windows)**:
```sql
LOAD DATA LOCAL INFILE 'C:/Users/santi/OneDrive/Documentos/Documentos/2025/BD2/BD2_Hefesto_ApuetasDeportivas/Paso4/export_csv/Country.csv'
```

**Nota**: Usar `/` (forward slash) en lugar de `\` (backslash) en rutas de MySQL.

---

## PASO 3: EJECUTAR SCRIPT SQL

### Opción 3A: Desde línea de comandos

```bash
"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -ppepe1234 --local-infile=1 < "C:\Users\santi\OneDrive\Documentos\Documentos\2025\BD2\BD2_Hefesto_ApuetasDeportivas\Paso4\create_staging_and_load_FIXED.sql"
```

**Importante**: Flag `--local-infile=1` es necesario para cargar CSVs.

### Opción 3B: Desde MySQL Workbench

1. Abrir MySQL Workbench
2. Conectar a localhost (root / pepe1234)
3. `File > Open SQL Script`
4. Seleccionar `create_staging_and_load_FIXED.sql`
5. Ejecutar completo (⚡ icono de rayo)

### Opción 3C: Desde línea de comandos interactiva

```bash
"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -ppepe1234 --local-infile=1

mysql> source C:/Users/santi/OneDrive/Documentos/Documentos/2025/BD2/BD2_Hefesto_ApuetasDeportivas/Paso4/create_staging_and_load_FIXED.sql
```

---

## PASO 4: EJECUTAR SCRIPT PYTHON ETL

### 4.1 Modificar contraseña en etl_apuestas.py

Editar línea 33:
```python
# ANTES:
'password': 'aloalo',  # ⚠️ CAMBIAR

# DESPUÉS:
'password': 'pepe1234',
```

### 4.2 Instalar dependencias Python

```bash
pip install mysql-connector-python
```

### 4.3 Ejecutar script

```bash
cd "C:\Users\santi\OneDrive\Documentos\Documentos\2025\BD2\BD2_Hefesto_ApuetasDeportivas\Paso4"

python etl_apuestas.py
```

**Tiempo esperado**: 5-15 minutos para cargar ~903K registros.

---

## PASO 5: VERIFICAR CREACIÓN

### 5.1 Verificar base de datos existe

```bash
"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -ppepe1234 -e "SHOW DATABASES;"
```

**Debe aparecer**: `apuestas_dw`

### 5.2 Verificar tablas creadas

```bash
"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -ppepe1234 -e "USE apuestas_dw; SHOW TABLES;"
```

**Tablas esperadas** (7):
```
DIM_CASA_APUESTAS
DIM_EQUIPO
DIM_ESTRATEGIA
DIM_FECHA
DIM_LIGA
DIM_RESULTADO_TIPO
FACT_APUESTAS
```

### 5.3 Verificar conteo de registros

```bash
"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -ppepe1234 -e "USE apuestas_dw; SELECT COUNT(*) as total FROM FACT_APUESTAS;"
```

**Esperado**: ~903,680 registros (o similar)

---

## TROUBLESHOOTING COMÚN

### Error 1: "Access denied for user"

**Causa**: Contraseña incorrecta

**Solución**: Verificar contraseña MySQL:
```bash
"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -p
# Ingresar contraseña manualmente
```

### Error 2: "The used command is not allowed"

**Causa**: `local_infile` deshabilitado

**Solución**: Habilitar en MySQL:
```sql
SET GLOBAL local_infile = 1;
```

O agregar flag al ejecutar:
```bash
mysql -u root -ppepe1234 --local-infile=1
```

### Error 3: "Can't find file"

**Causa**: Ruta incorrecta a CSVs

**Solución**: Verificar ruta absoluta:
```bash
dir "C:\Users\santi\OneDrive\Documentos\Documentos\2025\BD2\BD2_Hefesto_ApuetasDeportivas\Paso4\export_csv\Country.csv"
```

Si existe, usar esa ruta exacta (con `/` en lugar de `\`).

### Error 4: "Unknown database 'apuestas_dw'"

**Causa**: Script no se ejecutó o falló

**Solución**: Ejecutar manualmente creación:
```sql
CREATE DATABASE apuestas_dw CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE apuestas_dw;
```

---

## SCRIPT BATCH AUTOMATIZADO

Voy a crear un script que haga todo automáticamente...
