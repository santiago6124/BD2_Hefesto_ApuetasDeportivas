# ⚡ DASHBOARD 3: OPORTUNIDADES DE ARBITRAJE
## Guía Detallada con Campos Reales de Power BI

**Objetivo**: Detectar y analizar oportunidades de arbitraje en apuestas deportivas.

**Tiempo Estimado**: 40-50 minutos

---

## 🎨 DISEÑO DEL DASHBOARD

### Layout Recomendado

```
┌─────────────────────────────────────────────────────────────────┐
│  ⚡ Detección de Oportunidades de Arbitraje                     │
├──────────────┬──────────────┬──────────────┬───────────────────┤
│  KPI 1       │  KPI 2       │  KPI 3       │  KPI 4            │
│  Oportun.    │  % Partidos  │  Beneficio   │  Total Partidos   │
│  Arbitraje   │  con Arb.    │  Promedio    │  Analizados       │
├──────────────┴──────────────┴──────────────┴───────────────────┤
│  TABLA: Oportunidades por Liga                                  │
├────────────────────────────────┬─────────────────────────────────┤
│  BARRAS APILADAS:              │  COLUMNAS AGRUPADAS:           │
│  Oportunidades por Liga/Temp.  │  Distribución Beneficio        │
├────────────────────────────────┴─────────────────────────────────┤
│  LÍNEAS DOBLES: Evolución Temporal (Cantidad + Beneficio)       │
├──────────────────────────────────────────────────────────────────┤
│  TABLA: Top 10 Partidos con Mayor Beneficio                     │
├──────────────────┬──────────────────┬───────────────────────────┤
│ FILTRO: Temp.    │ FILTRO: Liga     │ FILTRO: Solo Arbitraje   │
└──────────────────┴──────────────────┴───────────────────────────┘
```

---

## 📋 PASO 1: PREPARACIÓN

### 1.1 Crear Nueva Página

1. Parte inferior → **`+`** Nueva página
2. Clic derecho → **Renombrar** → `3 - Oportunidades de Arbitraje`

### 1.2 Crear Columna Calculada (IMPORTANTE)

**Antes de crear visuales**, necesitas crear una columna calculada para el histograma.

#### Crear "Rango Beneficio Arbitraje"

1. En panel **Datos**, clic derecho en tabla `apuestas_dw fact_apuestas`
2. Seleccionar **Nueva columna**
3. Pegar este código:

```dax
Rango Beneficio Arbitraje =
SWITCH(
    TRUE(),
    'apuestas_dw fact_apuestas'[arbitraje_beneficio] = 0, "Sin arbitraje",
    'apuestas_dw fact_apuestas'[arbitraje_beneficio] <= 1, "0-1%",
    'apuestas_dw fact_apuestas'[arbitraje_beneficio] <= 2, "1-2%",
    'apuestas_dw fact_apuestas'[arbitraje_beneficio] <= 3, "2-3%",
    'apuestas_dw fact_apuestas'[arbitraje_beneficio] <= 5, "3-5%",
    ">5%"
)
```

4. Presionar **Enter**
5. Power BI calculará la columna (~30 segundos)

**Resultado**: Nueva columna en `fact_apuestas` que categoriza el beneficio de arbitraje.

---

## 📝 PASO 2: TÍTULO DEL DASHBOARD

1. **Insertar** → **Cuadro de texto**
2. Texto: `⚡ Detección de Oportunidades de Arbitraje`
3. Formato:
   - Fuente: Segoe UI Bold, 22pt
   - Color: `#2C3E50`
   - Alineación: Centro
   - Ancho: 100%

---

## 📊 PASO 3: KPI CARDS (4 Tarjetas)

### 3.1 KPI Card 1: Total Oportunidades

#### Crear y Configurar
1. **Visualizaciones** → **Tarjeta**
2. Posición: Esquina superior izquierda

#### Campo
```
📊 Campos de Tarjeta
├─ Campos
   └─ Medidas > Oportunidades Arbitraje
```

#### Formato
- **Etiqueta de categoría**: `Oportunidades Detectadas`
- **Tamaño valor**: 32pt (grande)
- **Color valor**: `#00A36C` (verde brillante)
- **Prefijo**: `⚡ ` (rayo)
- **Color fondo**: `#E8F5E9` (verde claro)
- **Borde**: 2px, `#4CAF50`

---

### 3.2 KPI Card 2: % Partidos con Arbitraje

#### Campo
```
📊 Campos de Tarjeta
├─ Campos
   └─ Medidas > % Partidos Arbitraje
```

#### Formato
- **Etiqueta**: `% Partidos con Arbitraje`
- **Formato**: Porcentaje con 2 decimales
- **Color**: `#3498DB` (azul)
- **Fondo**: `#EBF5FB` (azul claro)

---

### 3.3 KPI Card 3: Beneficio Promedio

#### Campo
```
📊 Campos de Tarjeta
├─ Campos
   └─ Medidas > Beneficio Arbitraje Promedio
```

#### Formato
- **Etiqueta**: `Ganancia Garantizada Promedio`
- **Subtítulo**: `(Solo partidos con arbitraje)`
- **Formato**: Porcentaje con 2 decimales
- **Color**: `#F39C12` (naranja)
- **Fondo**: `#FEF5E7` (naranja claro)

---

### 3.4 KPI Card 4: Total Partidos Analizados

#### Campo
```
📊 Campos de Tarjeta
├─ Campos
   └─ Medidas > Total Partidos
```

#### Formato
- **Etiqueta**: `Total Partidos Analizados`
- **Formato**: Número con separador de miles
- **Color**: `#95A5A6` (gris)

---

## 📋 PASO 4: TABLA - OPORTUNIDADES POR LIGA

### 4.1 Crear Visual

1. **Visualizaciones** → **Tabla**
2. Posición: Debajo de KPIs
3. Ancho: 100%
4. Alto: ~200px

### 4.2 Configurar Campos

```
📊 Campos de Tabla
├─ Columnas
   ├─ [1] apuestas_dw dim_liga > nombre_liga
   ├─ [2] Medidas > Oportunidades Arbitraje
   ├─ [3] Medidas > % Partidos Arbitraje
   ├─ [4] Medidas > Beneficio Arbitraje Promedio
   └─ [5] Medidas > Total Partidos
```

### 4.3 Renombrar Columnas

- `nombre_liga` → `Liga`
- `Oportunidades Arbitraje` → `Oportunidades`
- `% Partidos Arbitraje` → `% con Arbitraje`
- `Beneficio Arbitraje Promedio` → `Beneficio Prom.`
- `Total Partidos` → `Partidos`

### 4.4 Formato Condicional

#### Columna "Oportunidades"
1. Clic derecho → **Formato condicional** → **Barras de datos**
2. Configurar:
```
Barras de Datos
├─ Color barra: #00A36C (verde)
├─ Solo barra: OFF
└─ Dirección: Izquierda a derecha
```

#### Columna "% con Arbitraje"
1. Clic derecho → **Formato condicional** → **Escalas de color**
2. Configurar:
```
Escalas de Color
├─ Mínimo: Menor → #FFFFFF (blanco)
├─ Centro: N/A
└─ Máximo: Mayor → #00A36C (verde)
```

### 4.5 Ordenar

1. Clic en **`...`** → **Ordenar por** → `Oportunidades` descendente

---

## 📊 PASO 5: GRÁFICO DE BARRAS APILADAS

### 5.1 Crear Visual

1. **Visualizaciones** → **Gráfico de barras apiladas** (horizontal)
2. Posición: Lado izquierdo, debajo de tabla
3. Tamaño: ~50% ancho

### 5.2 Configurar Campos

```
📊 Campos de Barras Apiladas
├─ Eje Y
│  └─ apuestas_dw dim_liga > nombre_liga
├─ Eje X
│  └─ Medidas > Oportunidades Arbitraje
├─ Leyenda
│  └─ apuestas_dw dim_fecha > temporada
└─ Información sobre herramientas
   └─ (opcional: agregar % Partidos Arbitraje)
```

### 5.3 Formato Visual

**Panel Formato visual**:

1. **Título**:
   - Texto: `Oportunidades por Liga y Temporada`

2. **Colores**:
   - **Tema**: Paleta de azules/verdes
   - O asignar colores manualmente por temporada

3. **Etiquetas de datos**:
   - Activar: Solo para Totales
   - Posición: Dentro del extremo

4. **Leyenda**:
   - Posición: Parte inferior
   - Orientación: Horizontal

5. **Eje Y**:
   - Ordenar: Por Total de Oportunidades (descendente)

---

## 📊 PASO 6: HISTOGRAMA - DISTRIBUCIÓN DE BENEFICIO

### 6.1 Crear Visual

1. **Visualizaciones** → **Gráfico de columnas agrupadas**
2. Posición: Lado derecho de barras apiladas
3. Tamaño: ~50% ancho

### 6.2 Configurar Campos

```
📊 Campos de Columnas Agrupadas
├─ Eje X
│  └─ apuestas_dw fact_apuestas > Rango Beneficio Arbitraje
├─ Eje Y
│  └─ Medidas > Partidos con Arbitraje
├─ Leyenda
│  └─ (vacío - o agregar temporada para agrupar)
└─ Valores pequeños múltiples
   └─ (vacío)
```

**IMPORTANTE**: Este gráfico usa la columna calculada que creaste en Paso 1.2.

### 6.3 Ordenar Categorías

**El orden debe ser lógico**:
1. Sin arbitraje
2. 0-1%
3. 1-2%
4. 2-3%
5. 3-5%
6. >5%

**Para forzar orden correcto**:
1. Ir a vista **Datos** (ícono de tabla en barra izquierda)
2. Seleccionar columna `Rango Beneficio Arbitraje`
3. En barra superior: **Modelado** → **Ordenar por columna**
4. Crear nueva columna de ordenamiento o usar orden alfabético (ya está correcto)

### 6.4 Formato Visual

1. **Título**:
   - Texto: `Distribución del Beneficio de Arbitraje`
   - Subtítulo: `Frecuencia de oportunidades por rango`

2. **Colores**:
   - Degradado: Del rojo (sin arbitraje) al verde (>5%)
   - O color sólido: `#00A36C` (verde)

3. **Etiquetas de datos**:
   - Activar: ON
   - Formato: Número con separador de miles

4. **Eje X**:
   - Título: `Rango de Beneficio`
   - Etiquetas: Inclinación 45° si es necesario

5. **Eje Y**:
   - Título: `Cantidad de Partidos`

---

## 📈 PASO 7: GRÁFICO DE LÍNEAS DOBLE - EVOLUCIÓN TEMPORAL

### 7.1 Crear Visual

1. **Visualizaciones** → **Gráfico de líneas y columnas agrupadas**
2. Posición: Debajo de gráficos anteriores
3. Ancho: 100%
4. Alto: ~250px

**IMPORTANTE**: Este visual combina columnas (cantidad) + línea (porcentaje).

### 7.2 Configurar Campos

```
📊 Campos de Líneas y Columnas
├─ Eje X compartido
│  └─ apuestas_dw dim_fecha > fecha (agregar por Mes)
├─ Valores de columna
│  └─ Medidas > Oportunidades Arbitraje
├─ Valores de línea
│  └─ Medidas > Beneficio Arbitraje Promedio
└─ Leyenda
   └─ (vacío)
```

**Cómo agregar por Mes**:
1. Arrastrar `fecha` al Eje X
2. Clic en flecha dropdown junto a `fecha`
3. Seleccionar: `Mes` (no `Fecha` completa)

### 7.3 Formato Visual

1. **Título**:
   - Texto: `Evolución Temporal de Oportunidades de Arbitraje`

2. **Eje Y (Columnas - Izquierda)**:
   - Título: `Cantidad de Oportunidades`
   - Gridlines: ON

3. **Eje Y (Línea - Derecha)**:
   - Título: `Beneficio Promedio (%)`
   - Mínimo: 0
   - Máximo: Automático

4. **Columnas**:
   - Color: `#3498DB` (azul)
   - Transparencia: 30%

5. **Línea**:
   - Color: `#E67E22` (naranja)
   - Grosor: 3px
   - Marcadores: ON
   - Tamaño marcadores: 5

6. **Leyenda**:
   - Activar: ON
   - Posición: Superior

**Interpretación**: Las columnas muestran CANTIDAD de oportunidades, la línea muestra el BENEFICIO promedio de esas oportunidades.

---

## 📋 PASO 8: TABLA - TOP 10 PARTIDOS CON MAYOR BENEFICIO

### 8.1 Crear Medida Auxiliar

Primero necesitas crear una medida para mostrar los equipos de cada partido.

**Crear medida "Partido Local vs Visitante"**:

1. Clic derecho en tabla **Medidas** → **Nueva medida**
2. Pegar:

```dax
Partido Detalle =
VAR EquipoLocal =
    CALCULATE(
        SELECTEDVALUE('apuestas_dw dim_equipo'[nombre_equipo]),
        USERELATIONSHIP('apuestas_dw fact_apuestas'[id_equipo_local], 'apuestas_dw dim_equipo'[id_equipo])
    )
VAR EquipoVisitante =
    CALCULATE(
        SELECTEDVALUE('apuestas_dw dim_equipo'[nombre_equipo]),
        USERELATIONSHIP('apuestas_dw fact_apuestas'[id_equipo_visitante], 'apuestas_dw dim_equipo'[id_equipo])
    )
RETURN
    IF(
        NOT(ISBLANK(EquipoLocal)) && NOT(ISBLANK(EquipoVisitante)),
        EquipoLocal & " vs " & EquipoVisitante,
        BLANK()
    )
```

3. Enter

**NOTA**: Esta medida es compleja porque usa role-playing dimension (DIM_EQUIPO).

### 8.2 Crear Visual

1. **Visualizaciones** → **Tabla**
2. Posición: Debajo de gráfico de líneas
3. Ancho: 100%

### 8.3 Configurar Campos

```
📊 Campos de Tabla
├─ Columnas
   ├─ [1] Medidas > Partido Detalle
   ├─ [2] apuestas_dw dim_liga > nombre_liga
   ├─ [3] apuestas_dw dim_fecha > fecha
   ├─ [4] apuestas_dw fact_apuestas > arbitraje_beneficio
   ├─ [5] apuestas_dw fact_apuestas > arbitraje_cuota_local_max
   ├─ [6] apuestas_dw fact_apuestas > arbitraje_cuota_empate_max
   └─ [7] apuestas_dw fact_apuestas > arbitraje_cuota_visitante_max
```

### 8.4 Aplicar Filtro Top 10

1. Panel **Filtros** → **Filtros en este visual**
2. Arrastrar: `arbitraje_beneficio`
3. Tipo de filtro: `Top N`
4. Configurar:
   - **Mostrar elementos**: `Top 10`
   - **Por valor**: `arbitraje_beneficio`
5. **Aplicar filtro**

### 8.5 Renombrar Columnas

- `Partido Detalle` → `Partido`
- `nombre_liga` → `Liga`
- `fecha` → `Fecha`
- `arbitraje_beneficio` → `Beneficio %`
- `arbitraje_cuota_local_max` → `Cuota Local`
- `arbitraje_cuota_empate_max` → `Cuota Empate`
- `arbitraje_cuota_visitante_max` → `Cuota Visitante`

### 8.6 Formato

1. **Ordenar**: Por `Beneficio %` descendente
2. **Formato números**:
   - Beneficio %: Porcentaje con 2 decimales
   - Cuotas: Número con 2 decimales

3. **Estilo**:
   - Encabezados: Negrita, color `#2C3E50`
   - Alternar colores: ON

---

## 🎚️ PASO 9: SEGMENTACIONES (FILTROS)

### 9.1 Segmentación 1: Temporada

```
📊 Campo
└─ Campo
   └─ apuestas_dw dim_fecha > temporada
```

- **Estilo**: Desplegable
- **Título**: `Temporada`
- **Posición**: Inferior izquierda

---

### 9.2 Segmentación 2: Liga

```
📊 Campo
└─ Campo
   └─ apuestas_dw dim_liga > nombre_liga
```

- **Estilo**: Lista
- **Selección múltiple**: ON
- **Título**: `Liga`
- **Posición**: Inferior centro
- **Tamaño**: 250px × 180px

---

### 9.3 Segmentación 3: Solo con Arbitraje (Filtro Especial)

**Este filtro es BOOLEANO y muy importante**:

```
📊 Campo
└─ Campo
   └─ apuestas_dw fact_apuestas > arbitraje_es_oportunidad
```

#### Configurar Valor Predeterminado

1. Crear segmentación
2. **Panel Filtros** → Filtro de esta segmentación
3. **Tipo**: Lista (valores múltiples)
4. Marcar **SOLO** `TRUE` (desmarcar FALSE y Blank)
5. **Aplicar filtro**

#### Formato
- **Estilo**: Botones
- **Orientación**: Horizontal
- **Título**: `Mostrar solo oportunidades de arbitraje`
- **Valores**: TRUE, FALSE

**IMPORTANTE**: Por defecto, el dashboard debe mostrar SOLO partidos con arbitraje (TRUE). El usuario puede desactivar para ver todos.

---

## ✅ VERIFICACIÓN FINAL

### Checklist Dashboard 3

- [ ] Título visible: "⚡ Detección de Oportunidades de Arbitraje"
- [ ] Columna calculada `Rango Beneficio Arbitraje` creada
- [ ] 4 KPI cards funcionando:
  - [ ] Oportunidades muestra ~5,000-10,000 (varía)
  - [ ] % Partidos muestra ~10-30%
  - [ ] Beneficio Promedio muestra ~0.5-2%
  - [ ] Total Partidos muestra ~22,502
- [ ] Tabla por liga ordenada correctamente
- [ ] Gráfico barras apiladas muestra temporadas
- [ ] Histograma muestra distribución de beneficios
- [ ] Gráfico dual (columnas + línea) funciona
- [ ] Tabla Top 10 muestra partidos con mayor beneficio
- [ ] 3 segmentaciones activas:
  - [ ] Temporada funciona
  - [ ] Liga funciona
  - [ ] Filtro booleano arbitraje predeterminado en TRUE

### Valores Esperados

**Oportunidades detectadas**: ~5,000-10,000 partidos (20-40% del total)
**Beneficio promedio**: 0.5% - 2.5%
**Beneficio máximo**: 3% - 8% (casos excepcionales)

### Interpretación de Arbitraje

**¿Qué es arbitraje en apuestas?**
- Apostar a TODOS los resultados en casas diferentes
- Las cuotas combinadas garantizan ganancia sin importar resultado
- Beneficio pequeño pero sin riesgo

**Ejemplo práctico**:
```
Partido: Real Madrid vs Barcelona
Casa A: Local = 2.10
Casa B: Empate = 3.50
Casa C: Visitante = 4.00

Cálculo: 1/2.10 + 1/3.50 + 1/4.00 = 0.9857 < 1.0
Arbitraje: SÍ (beneficio ~1.4%)
```

---

## 🆘 SOLUCIÓN DE PROBLEMAS

### Problema: "Rango Beneficio Arbitraje" no aparece
**Causa**: Columna calculada no creada
**Solución**: Verificar Paso 1.2, crear columna en fact_apuestas

### Problema: "Partido Detalle" muestra BLANK
**Causa**: Medida compleja con role-playing dimension
**Solución**: Verificar que la medida usa USERELATIONSHIP correctamente

**Alternativa simple**: Usar solo `id_partido` en lugar de nombres de equipos

### Problema: Filtro booleano no funciona
**Causa**: Valores NULL o tipos incorrectos
**Solución**: En ETL, asegurar que `arbitraje_es_oportunidad` es TRUE/FALSE (no 1/0)

### Problema: Pocos datos en visuales
**Causa**: Filtro booleano está activo en TRUE
**Solución**: Desactivar filtro o cambiar a FALSE para ver todos los partidos

### Problema: Gráfico dual no muestra línea
**Causa**: Beneficio Promedio tiene valores muy pequeños comparados con cantidad
**Solución**: Verificar que Beneficio está en "Valores de línea" con eje Y secundario

---

## 💡 TIPS AVANZADOS

### Tip 1: Alertas de Arbitraje
Crear visual con formato condicional que resalte beneficios > 2%

### Tip 2: Drill-through a Detalle
Configurar página drill-through con detalles completos del partido:
- Cuotas de las 10 casas
- Distribución de inversión óptima
- Casa recomendada por resultado

### Tip 3: Bookmark para Comparación
Crear bookmark con filtro TRUE (solo arbitraje) y otro con FALSE (todos) para comparación rápida.

### Tip 4: Export to Excel
La tabla Top 10 se puede exportar a Excel para análisis detallado.

---

## 📊 INTERPRETACIÓN DE RESULTADOS

### ¿Qué es una buena oportunidad?

**Beneficio > 1%**: Excelente (poco común)
**Beneficio 0.5-1%**: Bueno (viable para inversión grande)
**Beneficio < 0.5%**: Marginal (requiere comisiones bajas)

### Factores que afectan arbitraje:

1. **Velocidad de actualización** de cuotas
2. **Límites de apuesta** por casa
3. **Comisiones de las casas**
4. **Liquidez** (capacidad de colocar apuestas grandes)

### Ligas con más oportunidades (típico):

- Premier League (alta liquidez)
- Champions League (muchas casas)
- Ligas menores (cuotas menos ajustadas)

---

📅 **Creado**: Noviembre 2025
📊 **Proyecto**: BD2_Hefesto_ApuestasDeportivas
📄 **Completado**: Los 3 Dashboards principales

**Siguiente**: TIPS_GENERALES_POWERBI.md (opcional)
