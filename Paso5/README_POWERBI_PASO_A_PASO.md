# 📊 POWER BI - GUÍA PASO A PASO
## Análisis de Apuestas Deportivas | Data Warehouse HEFESTO

**Fecha**: Noviembre 2025
**Objetivo**: Crear dashboards interactivos que respondan las 3 preguntas de negocio
**Esquema**: Estrella (1 tabla de hechos + 6 dimensiones)

---

## 📋 TABLA DE CONTENIDOS

1. [Requisitos Previos](#1-requisitos-previos)
2. [Paso 1: Verificar el Data Warehouse](#paso-1-verificar-el-data-warehouse)
3. [Paso 2: Instalar Power BI Desktop](#paso-2-instalar-power-bi-desktop)
4. [Paso 3: Conectar Power BI a MySQL](#paso-3-conectar-power-bi-a-mysql)
5. [Paso 4: Importar Tablas del DW](#paso-4-importar-tablas-del-dw)
6. [Paso 5: Configurar Relaciones](#paso-5-configurar-relaciones)
7. [Paso 6: Crear Medidas DAX](#paso-6-crear-medidas-dax)
8. [Paso 7: Dashboard 1 - Precisión de Casas](#paso-7-dashboard-1---precisión-de-casas)
9. [Paso 8: Dashboard 2 - ROI de Estrategias](#paso-8-dashboard-2---roi-de-estrategias)
10. [Paso 9: Dashboard 3 - Arbitraje](#paso-9-dashboard-3---arbitraje)
11. [Paso 10: Publicar y Compartir](#paso-10-publicar-y-compartir)
12. [Solución de Problemas](#solución-de-problemas)

---

## 1. REQUISITOS PREVIOS

### ✅ Checklist de Preparación

**Base de Datos**:
- [x] MySQL instalado y corriendo
- [x] Data Warehouse `apuestas_dw` creado
- [x] Tablas de dimensiones y hechos cargadas
- [x] Usuario con permisos de lectura

**Software**:
- [ ] Power BI Desktop instalado (gratuito)
- [ ] Conector MySQL para Power BI

**Datos Esperados**:
- `FACT_APUESTAS`: ~903,680 registros
- `DIM_FECHA`: ~2,920 registros
- `DIM_CASA_APUESTAS`: 10 registros
- `DIM_LIGA`: 11 registros
- `DIM_EQUIPO`: ~400 registros
- `DIM_ESTRATEGIA`: 4 registros
- `DIM_RESULTADO_TIPO`: 3 registros

---

## PASO 1: VERIFICAR EL DATA WAREHOUSE

### 1.1. Conectar a MySQL

```bash
# Abrir MySQL en terminal
mysql -u root -p

# Seleccionar base de datos
USE apuestas_dw;
```

### 1.2. Verificar Tablas Creadas

```sql
-- Ver todas las tablas
SHOW TABLES;
```

**Resultado Esperado**:
```
+------------------------+
| Tables_in_apuestas_dw  |
+------------------------+
| DIM_CASA_APUESTAS      |
| DIM_EQUIPO             |
| DIM_ESTRATEGIA         |
| DIM_FECHA              |
| DIM_LIGA               |
| DIM_RESULTADO_TIPO     |
| FACT_APUESTAS          |
+------------------------+
```

### 1.3. Verificar Conteo de Registros

```sql
-- Tabla de hechos
SELECT COUNT(*) as total_apuestas FROM FACT_APUESTAS;
-- Esperado: ~903,680

-- Dimensiones
SELECT 'DIM_FECHA' as tabla, COUNT(*) as registros FROM DIM_FECHA
UNION ALL
SELECT 'DIM_CASA_APUESTAS', COUNT(*) FROM DIM_CASA_APUESTAS
UNION ALL
SELECT 'DIM_LIGA', COUNT(*) FROM DIM_LIGA
UNION ALL
SELECT 'DIM_EQUIPO', COUNT(*) FROM DIM_EQUIPO
UNION ALL
SELECT 'DIM_ESTRATEGIA', COUNT(*) FROM DIM_ESTRATEGIA
UNION ALL
SELECT 'DIM_RESULTADO_TIPO', COUNT(*) FROM DIM_RESULTADO_TIPO;
```

### 1.4. Verificar Campos Derivados de Arbitraje

```sql
-- Verificar que existen campos de arbitraje
SELECT
    arbitraje_cuota_local_max,
    arbitraje_cuota_empate_max,
    arbitraje_cuota_visitante_max,
    arbitraje_porcentaje,
    arbitraje_es_oportunidad,
    arbitraje_beneficio
FROM FACT_APUESTAS
LIMIT 5;
```

**Si falta alguna tabla o campo**: Revisar Paso 4 (ETL) antes de continuar.

---

## PASO 2: INSTALAR POWER BI DESKTOP

### 2.1. Descargar Power BI Desktop

**Opción 1: Microsoft Store (Recomendado)**
1. Abrir Microsoft Store
2. Buscar "Power BI Desktop"
3. Clic en "Obtener" / "Instalar"
4. Esperar instalación automática

**Opción 2: Descarga Directa**
1. Ir a: https://powerbi.microsoft.com/desktop/
2. Clic en "Descargar gratis"
3. Ejecutar instalador `.exe`
4. Seguir wizard de instalación

### 2.2. Verificar Instalación

1. Abrir Power BI Desktop
2. Verificar versión: `Ayuda > Acerca de`
3. Versión recomendada: Noviembre 2025 o superior

### 2.3. Crear Cuenta Microsoft (si no tienes)

Power BI requiere una cuenta Microsoft para publicar reportes:
1. Ir a: https://signup.live.com/
2. Crear cuenta gratuita
3. Confirmar email

**Nota**: Para desarrollo local NO necesitas cuenta, solo para publicar en Power BI Service.

---

## PASO 3: CONECTAR POWER BI A MYSQL

### 3.1. Instalar Conector MySQL

Power BI Desktop incluye conector MySQL nativo, pero puede requerir drivers adicionales.

**Verificar si necesitas drivers**:
1. Abrir Power BI Desktop
2. `Obtener datos > Más > Base de datos > MySQL`
3. Si aparece error de driver → Instalar MySQL Connector/ODBC

**Instalar MySQL Connector/ODBC** (si es necesario):
1. Descargar: https://dev.mysql.com/downloads/connector/odbc/
2. Seleccionar: "Windows (x86, 64-bit), MSI Installer"
3. Ejecutar instalador
4. Reiniciar Power BI Desktop

### 3.2. Conectar a la Base de Datos

1. **Abrir Power BI Desktop**

2. **Obtener Datos**:
   - Clic en `Inicio > Obtener datos`
   - O: `Ctrl + Alt + D`

3. **Seleccionar Origen**:
   - Buscar: "MySQL"
   - Seleccionar: "Base de datos MySQL"
   - Clic en `Conectar`

4. **Configurar Conexión**:
   ```
   Servidor: localhost
   Base de datos: apuestas_dw
   ```
   - Clic en `Aceptar`

5. **Autenticación**:
   - Seleccionar: "Base de datos"
   - Usuario: `root` (o tu usuario MySQL)
   - Contraseña: [tu contraseña MySQL]
   - Clic en `Conectar`

6. **Modo de Conectividad**:
   - Seleccionar: `DirectQuery` (recomendado para datos grandes)
   - O: `Importar` (si el dataset es pequeño y quieres mejor performance)

**Diferencia DirectQuery vs Import**:
- **DirectQuery**: Queries en tiempo real a MySQL, siempre datos actualizados
- **Import**: Copia datos a Power BI, más rápido pero requiere refrescos manuales

**Recomendación**: Usa `Import` para este proyecto (datos estáticos históricos).

---

## PASO 4: IMPORTAR TABLAS DEL DW

### 4.1. Seleccionar Tablas

Después de conectar, verás el **Navegador** con todas las tablas de `apuestas_dw`.

**Seleccionar las siguientes 7 tablas** (marcar checkbox):
- ☑️ `FACT_APUESTAS`
- ☑️ `DIM_FECHA`
- ☑️ `DIM_CASA_APUESTAS`
- ☑️ `DIM_LIGA`
- ☑️ `DIM_EQUIPO`
- ☑️ `DIM_ESTRATEGIA`
- ☑️ `DIM_RESULTADO_TIPO`

### 4.2. Vista Previa de Datos

Para cada tabla:
1. Clic en el nombre de la tabla (no el checkbox)
2. Verificar que los datos se ven correctos en el panel derecho
3. Verificar cantidad aproximada de filas

### 4.3. Transformar Datos (Opcional pero Recomendado)

Antes de cargar, puedes limpiar/transformar datos:

1. Clic en `Transformar datos` (en lugar de `Cargar`)
2. Se abrirá **Power Query Editor**

**Transformaciones Recomendadas**:

#### Para `DIM_FECHA`:
```
1. Verificar que 'fecha' está en formato Date
2. Verificar campos: temporada, año, mes, trimestre
```

#### Para `FACT_APUESTAS`:
```
1. Verificar tipos de datos:
   - Campos numéricos (ganancia, pérdida, etc.) → Decimal
   - Campos booleanos (arbitraje_es_oportunidad) → True/False
   - FKs → Número entero

2. Renombrar columnas para mejor legibilidad (opcional):
   ganancia_total → Ganancia
   perdida_total → Pérdida
   arbitraje_es_oportunidad → Es Arbitraje
```

#### Para `DIM_CASA_APUESTAS`:
```
1. Verificar que 'nombre_completo' está como texto
```

### 4.4. Cargar Datos

1. Si estás en Power Query: Clic en `Cerrar y aplicar` (esquina superior izquierda)
2. Si estás en Navegador: Clic en `Cargar`

**Tiempo de Carga Esperado**:
- ~903K registros de FACT_APUESTAS: 2-5 minutos
- Dimensiones: <1 minuto cada una

**Barra de Progreso**: Verás progreso en la parte inferior de Power BI.

---

## PASO 5: CONFIGURAR RELACIONES

Power BI puede detectar relaciones automáticamente, pero es mejor verificarlas.

### 5.1. Abrir Vista de Modelo

1. Clic en icono de **Modelo** (lado izquierdo, tercer icono)
2. Verás todas las tablas como cajas conectadas

### 5.2. Verificar Relaciones Existentes

Power BI debería haber creado automáticamente:

```
DIM_FECHA.id_fecha -----> FACT_APUESTAS.id_fecha (1:*)
DIM_LIGA.id_liga -----> FACT_APUESTAS.id_liga (1:*)
DIM_CASA_APUESTAS.id_casa_apuestas -----> FACT_APUESTAS.id_casa_apuestas (1:*)
DIM_ESTRATEGIA.id_estrategia -----> FACT_APUESTAS.id_estrategia (1:*)
DIM_RESULTADO_TIPO.id_resultado_tipo -----> FACT_APUESTAS.id_resultado_tipo (1:*)
```

### 5.3. Crear Relaciones Faltantes Manualmente

**Para DIM_EQUIPO** (role-playing dimension):

1. **Relación 1 - Equipo Local**:
   - Arrastrar `DIM_EQUIPO.id_equipo` → `FACT_APUESTAS.id_equipo_local`
   - Cardinalidad: Muchos a uno (*:1)
   - Dirección filtro cruzado: Ambas
   - Activar relación: Sí (activa)

2. **Relación 2 - Equipo Visitante**:
   - Arrastrar `DIM_EQUIPO.id_equipo` → `FACT_APUESTAS.id_equipo_visitante`
   - Cardinalidad: Muchos a uno (*:1)
   - Dirección filtro cruzado: Ambas
   - Activar relación: No (inactiva, usaremos con USERELATIONSHIP)

**Importante**: Solo una relación puede estar activa por defecto entre dos tablas.

### 5.4. Configuración Avanzada de Relaciones

Para cada relación, hacer clic derecho > Propiedades:

**Verificar**:
- ✅ Dirección del filtro cruzado: `Ambas` (para todas)
- ✅ Cardinalidad: `Muchos a uno (*:1)` (desde FACT hacia DIM)
- ✅ Asumir integridad referencial: `Sí` (para mejor performance)

### 5.5. Organizar Diagrama

**Recomendación de Layout**:

```
        DIM_FECHA           DIM_LIGA
           |                   |
           |                   |
      DIM_EQUIPO          DIM_CASA_APUESTAS
           |                   |
           +-------+-----------+
                   |
              FACT_APUESTAS
                   |
           +-------+-----------+
           |                   |
      DIM_ESTRATEGIA    DIM_RESULTADO_TIPO
```

**Organizar**:
1. Arrastrar tablas para formar esquema estrella visual
2. `FACT_APUESTAS` en el centro
3. Dimensiones alrededor

---

## PASO 6: CREAR MEDIDAS DAX

Las medidas DAX son cálculos que Power BI ejecuta dinámicamente según filtros aplicados.

### 6.1. Crear Tabla de Medidas (Buena Práctica)

1. Clic derecho en panel de Campos
2. `Nueva tabla`
3. Escribir: `Medidas = {0}`
4. Enter
5. Ocultar la columna `Valor` (clic derecho > Ocultar)

### 6.2. Medidas para Pregunta 1: Precisión de Casas

#### Medida 1: Total Aciertos
```dax
Total Aciertos = SUM(FACT_APUESTAS[cant_aciertos])
```

#### Medida 2: Total Apuestas
```dax
Total Apuestas = SUM(FACT_APUESTAS[cant_apuestas])
```

#### Medida 3: Precisión %
```dax
Precisión % =
DIVIDE(
    [Total Aciertos],
    [Total Apuestas],
    0
) * 100
```

#### Medida 4: Formato Precisión
```dax
Precisión Texto =
FORMAT([Precisión %], "0.00") & "%"
```

### 6.3. Medidas para Pregunta 2: ROI de Estrategias

#### Medida 5: Ganancia Total
```dax
Ganancia Total = SUM(FACT_APUESTAS[ganancia_total])
```

#### Medida 6: Pérdida Total
```dax
Pérdida Total = SUM(FACT_APUESTAS[perdida_total])
```

#### Medida 7: Inversión Total
```dax
Inversión Total = SUM(FACT_APUESTAS[inversion])
```

#### Medida 8: Beneficio Neto
```dax
Beneficio Neto = [Ganancia Total] - [Pérdida Total]
```

#### Medida 9: ROI %
```dax
ROI % =
DIVIDE(
    [Beneficio Neto],
    [Inversión Total],
    0
) * 100
```

#### Medida 10: ROI Texto
```dax
ROI Texto =
FORMAT([ROI %], "+0.00;-0.00") & "%"
```

#### Medida 11: Color ROI (para formato condicional)
```dax
Color ROI =
SWITCH(
    TRUE(),
    [ROI %] > 5, "#00A36C",      // Verde oscuro
    [ROI %] > 0, "#90EE90",      // Verde claro
    [ROI %] > -5, "#FFD700",     // Amarillo
    "#FF6B6B"                     // Rojo
)
```

### 6.4. Medidas para Pregunta 3: Arbitraje

#### Medida 12: Total Partidos
```dax
Total Partidos =
CALCULATE(
    DISTINCTCOUNT(FACT_APUESTAS[id_fecha])
    + DISTINCTCOUNT(FACT_APUESTAS[id_equipo_local])
    + DISTINCTCOUNT(FACT_APUESTAS[id_equipo_visitante])
)
```

**Mejor versión (usando columna calculada concatenada)**:
Primero crear columna calculada en FACT_APUESTAS:
```dax
// Columna Calculada: ID_Partido
ID_Partido =
FACT_APUESTAS[id_fecha] & "-" &
FACT_APUESTAS[id_equipo_local] & "-" &
FACT_APUESTAS[id_equipo_visitante]
```

Luego la medida:
```dax
Total Partidos = DISTINCTCOUNT(FACT_APUESTAS[ID_Partido])
```

#### Medida 13: Partidos con Arbitraje
```dax
Partidos con Arbitraje =
CALCULATE(
    DISTINCTCOUNT(FACT_APUESTAS[ID_Partido]),
    FACT_APUESTAS[arbitraje_es_oportunidad] = TRUE
)
```

#### Medida 14: % Partidos con Arbitraje
```dax
% Partidos Arbitraje =
DIVIDE(
    [Partidos con Arbitraje],
    [Total Partidos],
    0
) * 100
```

#### Medida 15: Beneficio Arbitraje Promedio
```dax
Beneficio Arbitraje Promedio =
CALCULATE(
    AVERAGE(FACT_APUESTAS[arbitraje_beneficio]),
    FACT_APUESTAS[arbitraje_es_oportunidad] = TRUE
)
```

#### Medida 16: Contador Oportunidades
```dax
Oportunidades Arbitraje = [Partidos con Arbitraje]
```

### 6.5. Medidas Auxiliares

#### Medida 17: KPI Precisión (indicador visual)
```dax
KPI Precisión =
SWITCH(
    TRUE(),
    [Precisión %] >= 55, "🟢 Alta",
    [Precisión %] >= 50, "🟡 Media",
    "🔴 Baja"
)
```

#### Medida 18: Partidos Analizados
```dax
Partidos Analizados =
DISTINCTCOUNT(FACT_APUESTAS[ID_Partido])
```

---

## PASO 7: DASHBOARD 1 - PRECISIÓN DE CASAS

### 7.1. Crear Nueva Página

1. En la parte inferior, clic en `+` (nueva página)
2. Renombrar: "1 - Precisión por Casa"

### 7.2. Agregar Título

1. `Insertar > Cuadro de texto`
2. Escribir: "📊 Precisión de Casas de Apuestas"
3. Formato:
   - Fuente: Segoe UI Bold, 24pt
   - Color: #2C3E50
   - Alineación: Centro

### 7.3. Visual 1: Tabla Ranking de Precisión

**Crear Visual**:
1. Seleccionar: `Visualizaciones > Tabla`
2. Arrastrar campos:
   - **Filas**: `DIM_CASA_APUESTAS[nombre_completo]`
   - **Valores**:
     - `[Precisión %]`
     - `[Total Aciertos]`
     - `[Total Apuestas]`

**Formato**:
1. Clic en visual > `Formato visual`
2. **Valores**:
   - Precisión %: Formato personalizado `0.00` con símbolo `%`
   - Total Aciertos/Apuestas: Separador de miles
3. **Encabezados de columna**:
   - Renombrar: "Casa de Apuestas", "Precisión", "Aciertos", "Apuestas"
   - Color de fondo: #34495E
   - Color de texto: Blanco
4. **Ordenar**:
   - Clic en "..." > Ordenar por > Precisión % descendente

**Formato Condicional**:
1. Seleccionar columna "Precisión %"
2. Formato condicional > Escalas de color
   - Mínimo: 45% → Rojo (#FF6B6B)
   - Centro: 50% → Amarillo (#FFD700)
   - Máximo: 55% → Verde (#00A36C)

### 7.4. Visual 2: Gráfico de Barras Horizontales

**Crear Visual**:
1. `Visualizaciones > Gráfico de barras horizontales`
2. Campos:
   - **Eje Y**: `DIM_CASA_APUESTAS[nombre_completo]`
   - **Eje X**: `[Precisión %]`

**Formato**:
- Título: "Comparación de Precisión"
- Etiquetas de datos: Mostrar, formato "0.0%"
- Barras: Color degradado basado en valor
- Eje X: Rango 40% - 60%

### 7.5. Visual 3: Precisión por Liga

**Crear Visual**:
1. `Visualizaciones > Matriz`
2. Campos:
   - **Filas**: `DIM_LIGA[nombre_liga]`
   - **Columnas**: `DIM_CASA_APUESTAS[nombre_completo]`
   - **Valores**: `[Precisión %]`

**Formato**:
- Formato condicional en valores (escalas de color)
- Totales: Mostrar totales de fila y columna
- Tamaño texto: 11pt

### 7.6. Visual 4: KPI Cards

**Crear 3 Tarjetas KPI**:

**Card 1: Casa Más Precisa**
```dax
Casa Más Precisa =
CALCULATE(
    SELECTEDVALUE(DIM_CASA_APUESTAS[nombre_completo]),
    TOPN(1, ALL(DIM_CASA_APUESTAS), [Precisión %], DESC)
)
```
- Visual: Tarjeta
- Campo: `[Casa Más Precisa]`
- Subtítulo: "Casa Más Precisa"

**Card 2: Precisión Máxima**
- Visual: Tarjeta
- Campo: `[Precisión %]` con filtro TOPN
- Subtítulo: "Mejor Precisión"

**Card 3: Aciertos Totales**
- Visual: Tarjeta
- Campo: `[Total Aciertos]`
- Subtítulo: "Total Aciertos"

### 7.7. Visual 5: Evolución por Temporada

**Crear Visual**:
1. `Visualizaciones > Gráfico de líneas`
2. Campos:
   - **Eje X**: `DIM_FECHA[temporada]`
   - **Eje Y**: `[Precisión %]`
   - **Leyenda**: `DIM_CASA_APUESTAS[nombre_completo]`

**Formato**:
- Marcadores: Mostrar
- Título: "Evolución de Precisión por Temporada"
- Líneas: Grosor 3px

### 7.8. Agregar Segmentaciones (Filtros Interactivos)

**Segmentación 1: Liga**
1. `Visualizaciones > Segmentación`
2. Campo: `DIM_LIGA[nombre_liga]`
3. Estilo: Lista

**Segmentación 2: Temporada**
1. Campo: `DIM_FECHA[temporada]`
2. Estilo: Desplegable

**Segmentación 3: Tipo Resultado**
1. Campo: `DIM_RESULTADO_TIPO[tipo_resultado]`
2. Estilo: Botones

---

## PASO 8: DASHBOARD 2 - ROI DE ESTRATEGIAS

### 8.1. Crear Nueva Página

1. Clic en `+` nueva página
2. Renombrar: "2 - ROI por Estrategia"

### 8.2. Título Dashboard

```
Cuadro de texto: "💰 Rentabilidad por Estrategia de Apuesta (ROI)"
```

### 8.3. Visual 1: Tabla Resumen Estrategias

**Crear Tabla**:
1. Visual: Tabla
2. Campos:
   - **Filas**: `DIM_ESTRATEGIA[nombre_estrategia]`
   - **Valores**:
     - `[ROI %]`
     - `[Beneficio Neto]`
     - `[Inversión Total]`
     - `[Total Apuestas]`

**Formato Condicional**:
- ROI %: Barras de datos con escala rojo-amarillo-verde
- Beneficio Neto: Escalas de color (negativo rojo, positivo verde)

### 8.4. Visual 2: Gráfico de Cascada (Waterfall)

**Crear Visual**:
1. `Visualizaciones > Gráfico de cascada`
2. Campos:
   - **Categoría**: `DIM_ESTRATEGIA[nombre_estrategia]`
   - **Eje Y**: `[Beneficio Neto]`

**Formato**:
- Colores: Positivo verde, negativo rojo
- Etiquetas de datos: Mostrar
- Título: "Impacto de Cada Estrategia en Beneficio"

### 8.5. Visual 3: ROI por Liga y Estrategia

**Crear Matriz**:
1. Visual: Matriz
2. Campos:
   - **Filas**: `DIM_LIGA[nombre_liga]`
   - **Columnas**: `DIM_ESTRATEGIA[nombre_estrategia]`
   - **Valores**: `[ROI %]`

**Formato**:
- Formato condicional: Escalas de color
- Totales: Mostrar promedio

### 8.6. Visual 4: Gráfico de Dispersión ROI vs Precisión

**Crear Visual**:
1. `Visualizaciones > Gráfico de dispersión`
2. Campos:
   - **Eje X**: `[Precisión %]`
   - **Eje Y**: `[ROI %]`
   - **Detalles**: `DIM_ESTRATEGIA[nombre_estrategia]`
   - **Tamaño**: `[Inversión Total]`

**Formato**:
- Líneas de promedio: Activar eje X y Y
- Etiquetas: Mostrar nombres de estrategia
- Título: "Relación Precisión vs Rentabilidad"

### 8.7. Visual 5: Evolución ROI por Temporada

**Crear Gráfico de Área**:
1. Visual: Gráfico de áreas apiladas
2. Campos:
   - **Eje X**: `DIM_FECHA[temporada]`
   - **Eje Y**: `[ROI %]`
   - **Leyenda**: `DIM_ESTRATEGIA[nombre_estrategia]`

### 8.8. KPI Cards

**Card 1: Mejor Estrategia**
```dax
Mejor Estrategia =
CALCULATE(
    SELECTEDVALUE(DIM_ESTRATEGIA[nombre_estrategia]),
    TOPN(1, ALL(DIM_ESTRATEGIA), [ROI %], DESC)
)
```

**Card 2: ROI Máximo**
- Campo: `[ROI %]` filtrado por mejor estrategia

**Card 3: Beneficio Total**
- Campo: `[Beneficio Neto]` con formato moneda

---

## PASO 9: DASHBOARD 3 - ARBITRAJE

### 9.1. Crear Nueva Página

1. Nueva página: "3 - Oportunidades de Arbitraje"
2. Título: "⚡ Detección de Oportunidades de Arbitraje"

### 9.2. Visual 1: KPI Grid Principal

**Crear 4 Tarjetas KPI**:

**KPI 1: Total Oportunidades**
- Visual: Tarjeta
- Campo: `[Oportunidades Arbitraje]`
- Formato: Número grande con ícono ⚡
- Color: Verde (#00A36C)

**KPI 2: % Partidos con Arbitraje**
- Campo: `[% Partidos Arbitraje]`
- Formato: Porcentaje con 2 decimales

**KPI 3: Beneficio Promedio**
- Campo: `[Beneficio Arbitraje Promedio]`
- Formato: Porcentaje con 2 decimales
- Subtítulo: "Ganancia Garantizada Promedio"

**KPI 4: Total Partidos Analizados**
- Campo: `[Total Partidos]`
- Formato: Número con separador de miles

### 9.3. Visual 2: Tabla Detallada de Oportunidades por Liga

**Crear Tabla**:
1. Visual: Tabla
2. Campos:
   - **Filas**: `DIM_LIGA[nombre_liga]`
   - **Valores**:
     - `[Oportunidades Arbitraje]`
     - `[% Partidos Arbitraje]`
     - `[Beneficio Arbitraje Promedio]`
     - `[Total Partidos]`

**Ordenar**: Por Oportunidades Arbitraje descendente

### 9.4. Visual 3: Gráfico de Barras Apiladas

**Crear Visual**:
1. `Visualizaciones > Gráfico de barras apiladas`
2. Campos:
   - **Eje Y**: `DIM_LIGA[nombre_liga]`
   - **Eje X**: `[Oportunidades Arbitraje]`
   - **Leyenda**: `DIM_FECHA[temporada]`

**Formato**:
- Colores: Paleta de azules
- Etiquetas de datos: Mostrar totales

### 9.5. Visual 4: Distribución de Beneficio Arbitraje

**Crear Histograma**:
1. Visual: Gráfico de columnas agrupadas
2. Crear columna calculada primero:
```dax
// Columna Calculada en FACT_APUESTAS
Rango Beneficio Arbitraje =
SWITCH(
    TRUE(),
    FACT_APUESTAS[arbitraje_beneficio] = 0, "Sin arbitraje",
    FACT_APUESTAS[arbitraje_beneficio] <= 1, "0-1%",
    FACT_APUESTAS[arbitraje_beneficio] <= 2, "1-2%",
    FACT_APUESTAS[arbitraje_beneficio] <= 3, "2-3%",
    FACT_APUESTAS[arbitraje_beneficio] <= 5, "3-5%",
    ">5%"
)
```

3. Campos:
   - **Eje X**: `[Rango Beneficio Arbitraje]`
   - **Eje Y**: `[Partidos con Arbitraje]`

### 9.6. Visual 5: Evolución Temporal

**Crear Gráfico de Líneas**:
1. Visual: Gráfico de líneas
2. Campos:
   - **Eje X**: `DIM_FECHA[fecha]` (agregado por mes)
   - **Eje Y**: `[Oportunidades Arbitraje]`
   - **Línea secundaria**: `[Beneficio Arbitraje Promedio]`

**Formato**:
- Eje Y doble para mostrar cantidad y porcentaje
- Marcadores en líneas

### 9.7. Visual 6: Top 10 Partidos con Mayor Beneficio

**Crear Tabla**:
1. Visual: Tabla
2. Necesitas crear medida para obtener detalles:

```dax
// Medida para mostrar detalle partido
Detalle Partido =
VAR EquipoLocal = SELECTEDVALUE(DIM_EQUIPO[nombre_equipo])
VAR EquipoVisitante = SELECTEDVALUE(DIM_EQUIPO[nombre_equipo])
VAR FechaPartido = SELECTEDVALUE(DIM_FECHA[fecha])
RETURN
EquipoLocal & " vs " & EquipoVisitante & " (" & FechaPartido & ")"
```

3. Campos:
   - `[Detalle Partido]`
   - `DIM_LIGA[nombre_liga]`
   - `[Beneficio Arbitraje Promedio]`
4. Filtro Visual: Top 10 por beneficio

### 9.8. Segmentaciones

**Filtro 1: Temporada**
- Campo: `DIM_FECHA[temporada]`

**Filtro 2: Liga**
- Campo: `DIM_LIGA[nombre_liga]`

**Filtro 3: Solo con Arbitraje**
- Campo: `FACT_APUESTAS[arbitraje_es_oportunidad]`
- Valor predeterminado: TRUE

---

## PASO 10: PUBLICAR Y COMPARTIR

### 10.1. Guardar Archivo Local

1. `Archivo > Guardar como`
2. Nombre: `Apuestas_Deportivas_DW_Dashboard.pbix`
3. Ubicación: Carpeta del proyecto

### 10.2. Publicar en Power BI Service (Opcional)

**Requisitos**:
- Cuenta Microsoft
- Licencia Power BI (gratuita disponible)

**Pasos**:
1. `Inicio > Publicar`
2. Iniciar sesión con cuenta Microsoft
3. Seleccionar área de trabajo: "Mi área de trabajo"
4. Clic en `Seleccionar`
5. Esperar publicación (~2-5 min)
6. Clic en "Abrir en Power BI"

### 10.3. Configurar Actualización de Datos (Power BI Service)

1. En Power BI Service, ir a "Configuración" del dataset
2. `Configuración de gateway` > Configurar conexión MySQL
3. `Actualización programada`:
   - Frecuencia: Diaria (si datos se actualizan)
   - Hora: 6:00 AM
4. `Aplicar`

### 10.4. Compartir Dashboard

**Opción 1: Compartir Link**
1. Clic en `Compartir`
2. Ingresar emails de destinatarios
3. Permisos: Ver o Editar
4. `Compartir`

**Opción 2: Exportar a PDF**
1. `Archivo > Exportar > PDF`
2. Seleccionar páginas
3. Guardar archivo

**Opción 3: Insertar en Web (si es público)**
1. `Archivo > Insertar > Publicar en web`
2. Copiar código iframe
3. Pegar en sitio web

---

## SOLUCIÓN DE PROBLEMAS

### Problema 1: Error de Conexión MySQL

**Error**: "No se puede conectar al servidor MySQL"

**Soluciones**:
1. Verificar que MySQL está corriendo:
   ```bash
   # Windows
   net start MySQL80

   # O verificar en Servicios (services.msc)
   ```

2. Verificar puerto MySQL (default 3306):
   ```sql
   SHOW VARIABLES LIKE 'port';
   ```

3. Verificar firewall permite conexiones:
   - Windows Defender Firewall > Permitir aplicación > MySQL

4. Instalar MySQL Connector/ODBC:
   - https://dev.mysql.com/downloads/connector/odbc/

### Problema 2: Relaciones No Detectadas

**Síntoma**: Power BI no crea relaciones automáticamente

**Solución**:
1. Verificar nombres de columnas coinciden exactamente
2. Verificar tipos de datos son compatibles (ambos INT, ambos VARCHAR, etc.)
3. Crear relaciones manualmente en Vista de Modelo
4. Verificar que hay valores coincidentes entre tablas:
   ```sql
   -- En MySQL
   SELECT COUNT(*) FROM FACT_APUESTAS WHERE id_casa_apuestas NOT IN (SELECT id_casa_apuestas FROM DIM_CASA_APUESTAS);
   -- Resultado debe ser 0
   ```

### Problema 3: Performance Lenta

**Síntoma**: Dashboards tardan mucho en cargar

**Soluciones**:
1. **Usar Import en lugar de DirectQuery**:
   - Más rápido para datasets pequeños/medianos
   - Datos en memoria de Power BI

2. **Optimizar Medidas DAX**:
   - Evitar funciones CALCULATE anidadas
   - Usar variables VAR para cálculos repetidos
   - Ejemplo:
   ```dax
   // LENTO
   Medida = CALCULATE(SUM(...), FILTER(...)) + CALCULATE(SUM(...), FILTER(...))

   // RÁPIDO
   Medida =
   VAR Valor1 = CALCULATE(SUM(...), FILTER(...))
   VAR Valor2 = CALCULATE(SUM(...), FILTER(...))
   RETURN Valor1 + Valor2
   ```

3. **Crear Índices en MySQL**:
   ```sql
   -- En tu base de datos
   CREATE INDEX idx_fact_fecha ON FACT_APUESTAS(id_fecha);
   CREATE INDEX idx_fact_liga ON FACT_APUESTAS(id_liga);
   CREATE INDEX idx_fact_casa ON FACT_APUESTAS(id_casa_apuestas);
   ```

4. **Deshabilitar visuales complejos innecesarios**:
   - Menos visuales por página = más rápido
   - Limitar segmentaciones a las esenciales

### Problema 4: Campos de Arbitraje No Funcionan

**Síntoma**: Medidas de arbitraje muestran valores incorrectos o vacíos

**Verificar**:
1. Campos existen en FACT_APUESTAS:
   ```sql
   DESCRIBE FACT_APUESTAS;
   ```

2. Campos tienen valores:
   ```sql
   SELECT COUNT(*) FROM FACT_APUESTAS WHERE arbitraje_es_oportunidad = TRUE;
   -- Debería devolver ~23,000-46,000 (dependiendo de duplicación)
   ```

3. Tipo de dato correcto en Power BI:
   - `arbitraje_es_oportunidad` → True/False (booleano)
   - `arbitraje_beneficio` → Decimal
   - `arbitraje_porcentaje` → Decimal

4. Si faltan campos, revisar ETL (Paso 4) y regenerar datos.

### Problema 5: Role-Playing Dimension (Equipo) No Funciona

**Síntoma**: No puedes filtrar por equipo local Y visitante simultáneamente

**Solución**: Usar medida con USERELATIONSHIP

```dax
Aciertos Equipo Local =
CALCULATE(
    [Total Aciertos],
    USERELATIONSHIP(FACT_APUESTAS[id_equipo_local], DIM_EQUIPO[id_equipo])
)

Aciertos Equipo Visitante =
CALCULATE(
    [Total Aciertos],
    USERELATIONSHIP(FACT_APUESTAS[id_equipo_visitante], DIM_EQUIPO[id_equipo])
)

Aciertos Cualquier Equipo =
[Aciertos Equipo Local] + [Aciertos Equipo Visitante]
```

### Problema 6: Formato de Fechas Incorrecto

**Síntoma**: Fechas se muestran como números o formato incorrecto

**Solución**:
1. En Power Query Editor:
   - Seleccionar columna `fecha` en `DIM_FECHA`
   - `Transformar > Tipo de datos > Fecha`
   - `Cerrar y aplicar`

2. Verificar formato en visual:
   - Clic derecho en campo de fecha
   - `Formato` → Seleccionar formato deseado (dd/MM/yyyy)

### Problema 7: Medidas DAX con Errores

**Errores Comunes**:

1. **Error: "No se puede determinar la tabla"**
   - Solución: Especificar tabla: `FACT_APUESTAS[campo]` en lugar de solo `[campo]`

2. **Error: "Función no reconocida"**
   - Solución: Verificar mayúsculas (DAX es case-insensitive pero usa MAYÚSCULAS por convención)

3. **Error: "Tipo de datos no compatible"**
   - Solución: Usar CONVERT o VALUE para cambiar tipos:
   ```dax
   Medida Correcta = VALUE(FACT_APUESTAS[campo_texto])
   ```

4. **Valores incorrectos en agregaciones**:
   - Problema: Estás usando SUM en lugar de DISTINCTCOUNT
   - Solución para contar partidos únicos:
   ```dax
   // INCORRECTO (cuenta apuestas, no partidos)
   Partidos = COUNT(FACT_APUESTAS[id_fecha])

   // CORRECTO
   Partidos = DISTINCTCOUNT(FACT_APUESTAS[ID_Partido])
   ```

---

## CHECKLIST FINAL

### Antes de Presentar

- [ ] Todas las páginas tienen título descriptivo
- [ ] Todos los visuales tienen títulos claros
- [ ] Formato consistente en todo el reporte
- [ ] Colores corporativos/temáticos aplicados
- [ ] Segmentaciones funcionan correctamente
- [ ] Interactividad entre visuales funciona (cross-filtering)
- [ ] No hay errores en medidas DAX
- [ ] Datos actualizados y verificados
- [ ] Ortografía y gramática revisadas
- [ ] Archivo guardado con nombre descriptivo

### Pruebas de Funcionalidad

- [ ] **Dashboard 1**: Tabla de precisión muestra Top 10 casas
- [ ] **Dashboard 1**: Filtros de liga/temporada funcionan
- [ ] **Dashboard 2**: ROI se calcula correctamente (positivo/negativo)
- [ ] **Dashboard 2**: Gráfico de cascada muestra impacto por estrategia
- [ ] **Dashboard 3**: Oportunidades de arbitraje se cuentan por partido (no por apuesta)
- [ ] **Dashboard 3**: Beneficio promedio solo incluye partidos con arbitraje = TRUE
- [ ] **Navegación**: Puedes moverte entre páginas fácilmente

### Validación de Datos

- [ ] Totales coinciden con queries SQL directas
- [ ] No hay valores NULL inesperados
- [ ] Rangos de datos son razonables (precisión 40-60%, ROI -50% a +50%)
- [ ] Suma de partes = total global

---

## RECURSOS ADICIONALES

### Documentación Oficial

- **Power BI Documentation**: https://docs.microsoft.com/power-bi/
- **DAX Function Reference**: https://dax.guide/
- **Power BI Community**: https://community.powerbi.com/

### Tutoriales Recomendados

1. **Microsoft Learn - Power BI**:
   - https://learn.microsoft.com/training/powerbi/

2. **SQLBI - DAX Patterns**:
   - https://www.daxpatterns.com/

3. **Guy in a Cube (YouTube)**:
   - Canal de Microsoft con tutoriales Power BI

### Cursos Gratuitos

- **edX - Analyzing and Visualizing Data with Power BI**
- **Microsoft Virtual Academy - Power BI courses**

---

## PRÓXIMOS PASOS AVANZADOS

### Mejoras Opcionales

1. **Bookmarks y Navegación**:
   - Crear botones de navegación entre páginas
   - Bookmarks para diferentes vistas del mismo dashboard

2. **Drill-Through Pages**:
   - Páginas de detalle al hacer clic en elementos
   - Ejemplo: Clic en casa → Ver detalle solo de esa casa

3. **Tooltips Personalizados**:
   - Crear páginas de tooltip con información adicional
   - Se muestran al pasar mouse sobre visuales

4. **Row-Level Security (RLS)**:
   - Si compartes con múltiples usuarios
   - Filtrar datos por usuario (ej: cada casa solo ve sus datos)

5. **Parámetros What-If**:
   - Crear escenarios hipotéticos
   - Ejemplo: "¿Qué pasaría si la inversión fuera X?"

6. **Integración con R/Python**:
   - Visualizaciones avanzadas
   - Modelos predictivos en Power BI

---

## CONCLUSIÓN

Siguiendo esta guía paso a paso, habrás creado un sistema completo de Business Intelligence con:

✅ **3 Dashboards Interactivos** respondiendo las preguntas de negocio
✅ **Conexión Directa** al Data Warehouse MySQL
✅ **20+ Medidas DAX** para análisis avanzado
✅ **Visualizaciones Profesionales** con formato corporativo
✅ **Filtros Interactivos** para exploración dinámica

**Tiempo Estimado Total**: 4-6 horas (incluyendo aprendizaje de Power BI)

**¡Éxito con tu proyecto!** 🚀

---

**Documento Generado**: Noviembre 2025
**Versión**: 1.0
**Proyecto**: BD2_Hefesto_ApuestasDeportivas - Paso 5 (Visualización)
