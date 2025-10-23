# 📊 ANÁLISIS HEFESTO - Sistema de Apuestas Deportivas

## Proyecto: Data Warehouse para Análisis de Apuestas Deportivas

---

## 📑 Tabla de Contenidos

- [Contexto del Dataset](#-contexto-del-dataset)
- [Paso 1: Análisis de Requerimientos](#-paso-1-análisis-de-requerimientos)
  - [a) Preguntas de Negocio](#a--preguntas-de-negocio-identificadas)
  - [b) Indicadores y Perspectivas](#b--indicadores-y-perspectivas)
  - [c) Modelo Conceptual](#c--modelo-conceptual-hefesto)
- [Insights Clave](#-insights-clave-del-análisis)
- [Validación del Modelo](#-validación-del-modelo)
- [Próximos Pasos](#-próximos-pasos-en-hefesto)
- [Recomendaciones Técnicas](#-recomendaciones-técnicas)

---

## 📈 CONTEXTO DEL DATASET

### Descripción General

Base de datos SQLite con información histórica de partidos de fútbol europeo y datos de apuestas deportivas de múltiples casas.

### Estadísticas del Dataset

- **Total de partidos:** 25,979
- **Partidos con datos de apuestas:** 22,592 (87% cobertura)
- **Período temporal:** 2008-2016 (8 temporadas completas)
- **Casas de apuestas:** 10 operadores principales
- **Ligas europeas:** 11 competiciones
- **Jugadores registrados:** 11,060
- **Equipos:** ~300 equipos

### Casas de Apuestas Incluidas

| Casa de Apuestas | Cobertura | % del Total |
|------------------|-----------|-------------|
| Bet365 | 22,592 partidos | 86.96% |
| Betway | 22,575 partidos | 86.90% |
| Interwetten | 22,520 partidos | 86.69% |
| Ladbrokes | 22,556 partidos | 86.82% |
| William Hill | 22,571 partidos | 86.88% |
| VC Bet | 22,568 partidos | 86.87% |
| Stan James | 17,097 partidos | 65.81% |
| Gamebookers | 14,162 partidos | 54.51% |
| BetWin | 14,161 partidos | 54.51% |
| Pinnacle | 11,168 partidos | 42.99% |

### Ligas Incluidas

- 🏴󠁧󠁢󠁥󠁮󠁧󠁿 **England** - Premier League (3,040 partidos)
- 🇪🇸 **Spain** - La Liga (3,039 partidos)
- 🇫🇷 **France** - Ligue 1 (3,036 partidos)
- 🇮🇹 **Italy** - Serie A (3,011 partidos)
- 🇩🇪 **Germany** - Bundesliga (2,447 partidos)
- 🇳🇱 **Netherlands** - Eredivisie (2,445 partidos)
- 🇵🇹 **Portugal** - Primeira Liga (2,044 partidos)
- 🏴󠁧󠁢󠁳󠁣󠁴󠁿 **Scotland** - Premiership (1,824 partidos)
- 🇧🇪 **Belgium** - Pro League (1,706 partidos)
- 🇵🇱 **Poland** - Ekstraklasa
- 🇨🇭 **Switzerland** - Super League

---

## 🎯 PASO 1: ANÁLISIS DE REQUERIMIENTOS

Aplicación de la **Metodología HEFESTO** para el diseño de Data Warehouse.

---

## a) 🎯 PREGUNTAS DE NEGOCIO IDENTIFICADAS

### PREGUNTA 1: Análisis de Precisión Predictiva

> **¿Cuál es la precisión de las predicciones implícitas en las cuotas de cada casa de apuestas, analizada por liga, temporada y tipo de resultado?**

#### Justificación
Las cuotas más bajas indican el favorito según cada casa de apuestas. Con 22,592 partidos y resultados reales disponibles, podemos medir objetivamente qué casa predice mejor y en qué contextos específicos:
- Ligas competitivas vs. predecibles
- Partidos de local vs. visitante
- Temporadas y tendencias temporales
- Efectividad por tipo de resultado

#### Valor de Negocio
- Identificar casas de apuestas más precisas para estrategias de arbitraje
- Validar modelos predictivos propios contra el mercado
- Detectar ineficiencias en mercados específicos
- Evaluar calidad de información por fuente

---

### PREGUNTA 2: Evaluación de Estrategias de Apuesta

> **¿Cuál es el retorno de inversión (ROI) simulado de diferentes estrategias sistemáticas (apostar siempre al favorito, siempre al underdog, búsqueda de valor) por liga, temporada y casa de apuestas?**

#### Justificación
Con cuotas históricas y resultados reales podemos simular inversiones sistemáticas y calcular ROI real. Los datos muestran que:
- Favoritos locales ganan 54.52% del tiempo
- Favoritos visitantes ganan 50.67% del tiempo
- Empates son menos predecibles (31.55% cuando son favoritos)

#### Valor de Negocio
- Evaluar viabilidad económica de estrategias de apuestas automatizadas
- Identificar nichos rentables (ligas específicas, temporadas, tipos de apuesta)
- Calcular rentabilidad histórica de diferentes enfoques
- Optimizar gestión de bankroll y Kelly Criterion

---

### PREGUNTA 3: Oportunidades de Arbitraje Deportivo

> **¿Qué oportunidades de arbitraje deportivo (sure bets) existen al comparar cuotas entre casas de apuestas para el mismo partido, y cómo varían por liga y temporada?**

#### Justificación
Con 10 casas de apuestas ofreciendo cuotas para los mismos partidos, podemos detectar discrepancias que permiten apuestas sin riesgo. El arbitraje existe cuando la suma de las probabilidades implícitas es menor a 100%:

```
% Arbitraje = (1/CuotaLocal + 1/CuotaEmpate + 1/CuotaVisitante) < 1.0
```

#### Valor de Negocio
- Identificación de oportunidades de ganancia garantizada independiente del resultado
- Análisis de eficiencia de mercado por liga y temporada
- Detección de patrones temporales en oportunidades de arbitraje
- Evaluación de viabilidad de estrategias de arbitraje sistemático

---

## b) 📊 INDICADORES Y PERSPECTIVAS

### INDICADORES (Métricas Numéricas)

| Indicador | Tipo | Descripción | Fórmula/Fuente |
|-----------|------|-------------|----------------|
| **% Precisión** | No Aditivo | Porcentaje de aciertos en predicciones | `(Aciertos / Total) × 100` |
| **ROI %** | No Aditivo | Retorno de inversión porcentual | `((Ganancia - Inversión) / Inversión) × 100` |
| **Ganancia Total** | Aditivo | Suma de ganancias en apuestas exitosas | `SUM(cuota × inversión)` cuando acierta |
| **Pérdida Total** | Aditivo | Suma de pérdidas en apuestas fallidas | `SUM(inversión)` cuando falla |
| **% Arbitraje** | No Aditivo | Indicador de oportunidad de arbitraje | `(1/cuotaLocal + 1/cuotaEmpate + 1/cuotaVisitante) < 1` |
| **Cuota Promedio** | Semi-Aditivo | Cuota media ofrecida | `AVG(cuota)` por tipo de resultado |
| **Cant. Aciertos** | Aditivo | Número de predicciones correctas | `COUNT(*)` WHERE predicción = resultado |
| **Cant. Apuestas** | Aditivo | Total de apuestas realizadas | `COUNT(*)` |
| **Diferencia de Cuotas** | No Aditivo | Variación entre casas de apuestas | `MAX(cuota) - MIN(cuota)` por partido |

#### Clasificación por Aditividad

**Indicadores Aditivos** (se pueden sumar en todas las dimensiones):
- Ganancia Total
- Pérdida Total
- Cantidad de Aciertos
- Cantidad de Apuestas

**Indicadores Semi-Aditivos** (se pueden promediar, no sumar):
- Cuota Promedio

**Indicadores No Aditivos** (deben calcularse, no sumar ni promediar):
- % Precisión
- ROI %
- % Arbitraje
- Diferencia de Cuotas

> ⚠️ **Nota Técnica:** Los indicadores no aditivos deben implementarse como medidas calculadas en la capa semántica (Power BI/Tableau/Qlik) en lugar de almacenarse pre-calculados.

---

### PERSPECTIVAS (Dimensiones de Análisis)

| Perspectiva | Atributos | Jerarquía | Cardinalidad |
|-------------|-----------|-----------|--------------|
| **🏢 Casa de Apuestas** | Nombre, País, Tipo, Comisión | Casa → Región | 10 casas |
| **🏆 Liga** | Nombre, País, Nivel Competitivo | Liga → País | 11 ligas |
| **📅 Temporada/Tiempo** | Temporada, Año, Mes, Fecha, Jornada | Fecha → Mes → Año → Temporada | 8 temporadas (2008-2016) |
| **⚽ Tipo de Resultado** | Local/Empate/Visitante | Resultado Específico → Tipo | 3 tipos |
| **👥 Equipo** | Nombre, Liga, País, Posición Local/Visitante | Equipo → Liga → País | ~300 equipos |
| **🎯 Estrategia** | Favorito, Underdog, Empate, Búsqueda de Valor | Estrategia Específica → Categoría | 4+ estrategias |

#### Jerarquías Identificadas

1. **Jerarquía Geográfica-Competitiva:**
   ```
   Equipo → Liga → País
   ```

2. **Jerarquía Temporal:**
   ```
   Fecha → Mes → Año → Temporada
   Jornada → Temporada
   ```

3. **Jerarquía de Resultado:**
   ```
   Resultado Específico (1-0, 2-1, etc.) → Tipo (Local/Empate/Visitante)
   ```

4. **Jerarquía de Casa de Apuestas:**
   ```
   Casa Individual → Región Geográfica → Tipo de Operador
   ```

> 💡 **Beneficio OLAP:** Estas jerarquías permiten operaciones de drill-down (profundizar) y roll-up (consolidar) en análisis multidimensional.

---

## c) 🏗️ MODELO CONCEPTUAL HEFESTO

```
╔══════════════════════════╗                                ╔═══════════════════════════╗
║   PERSPECTIVAS           ║                                ║      INDICADORES          ║
║   (Dimensiones)          ║      ┌──────────────────┐     ║      (Métricas)           ║
╠══════════════════════════╣      │                  │     ╠═══════════════════════════╣
║                          ║─────>│                  │────>║ % Precisión (N.A.)        ║
║ 🏢 CASA DE APUESTAS      ║      │                  │     ║ ROI % (N.A.)              ║
║    • Bet365              ║─────>│                  │────>║ Ganancia Total (A)        ║
║    • Betway              ║      │     APUESTA      │     ║ Pérdida Total (A)         ║
║    • Pinnacle            ║─────>│     DEPORTIVA    │────>║ % Arbitraje (N.A.)        ║
║    • William Hill        ║      │                  │     ║ Cuota Promedio (S.A.)     ║
║    • Interwetten         ║─────>│                  │────>║ Cant. Aciertos (A)        ║
║    • Ladbrokes           ║      │   (FACT TABLE)   │     ║ Cant. Apuestas (A)        ║
║    • (+ 4 casas)         ║─────>│                  │────>║ Diferencia Cuotas (N.A.)  ║
║                          ║      │                  │     ║                           ║
║ 🏆 LIGA                  ║─────>│                  │     ║ LEYENDA:                  ║
║    • England (Premier)   ║      │                  │     ║ (A) = Aditivo             ║
║    • Spain (La Liga)     ║─────>│                  │     ║ (S.A) = Semi-Aditivo      ║
║    • Germany (Bundesliga)║      │                  │     ║ (N.A) = No Aditivo        ║
║    • Italy (Serie A)     ║─────>│                  │     ║                           ║
║    • France (Ligue 1)    ║      │                  │     ╚═══════════════════════════╝
║    • (+ 6 ligas)         ║─────>│                  │
║                          ║      └──────────────────┘
║ 📅 TEMPORADA/TIEMPO      ║
║    • 2008/2009           ║       GRANULARIDAD DEL HECHO:
║    • 2009/2010           ║       ────────────────────────
║    • 2010/2011           ║       1 fila = 1 apuesta de
║    • 2011/2012           ║       1 casa de apuestas en
║    • 2012/2013           ║       1 partido específico
║    • 2013/2014           ║
║    • 2014/2015           ║       CARDINALIDAD ESTIMADA:
║    • 2015/2016           ║       ────────────────────────
║                          ║       ~225,920 registros
║    Jerarquía:            ║       (22,592 partidos ×
║    Fecha→Mes→Año→Temp.   ║        10 casas promedio)
║                          ║
║ ⚽ TIPO DE RESULTADO      ║       TIPO DE ESQUEMA:
║    • Victoria Local      ║       ────────────────────────
║    • Empate              ║       Esquema ESTRELLA
║    • Victoria Visitante  ║       (Star Schema)
║                          ║
║ 👥 EQUIPO                ║       FUENTES DE DATOS:
║    • Equipo Local        ║       ────────────────────────
║    • Equipo Visitante    ║       • Match (tabla principal)
║                          ║       • Team (dimensión)
║    Jerarquía:            ║       • League (dimensión)
║    Equipo→Liga→País      ║       • Country (jerarquía)
║                          ║       • Fecha (derivada)
║ 🎯 ESTRATEGIA            ║
║    • Favorito            ║
║    • Underdog            ║
║    • Empate              ║
║    • Búsqueda de Valor   ║
║    • Martingala          ║
╚══════════════════════════╝
```

### Descripción del Modelo

**Proceso de Negocio Central:** APUESTA DEPORTIVA

**Granularidad:** Una fila en la tabla de hechos representa una apuesta realizada por una casa de apuestas específica en un partido específico.

**Cardinalidad Esperada:** ~225,920 registros (22,592 partidos × 10 casas de apuestas promedio)

**Tipo de Esquema:** Esquema Estrella (Star Schema) - óptimo para consultas OLAP y rendimiento de agregaciones.

---

## 🔍 INSIGHTS CLAVE DEL ANÁLISIS

### 1. Precisión de Predicciones (Datos Reales)

| Escenario | Precisión | Distribución |
|-----------|-----------|--------------|
| **Favorito Local** | 54.52% | 10,371 victorias de 16,232 partidos |
| **Favorito Visitante** | 50.67% | 3,118 victorias de 6,154 partidos |
| **Favorito Empate** | 31.55% | 65 empates de 206 partidos (muy raro) |

> 📊 **Interpretación:** Los favoritos locales tienen ventaja estadística del 54.52%, mientras que favoritos visitantes están prácticamente al 50/50, indicando que las cuotas capturan correctamente la ventaja de jugar en casa.

---

### 2. Distribución Global de Resultados

| Resultado | Cantidad | Porcentaje |
|-----------|----------|------------|
| **Victorias Locales** | 10,371 | 45.91% |
| **Empates** | 5,716 | 25.30% |
| **Victorias Visitantes** | 6,505 | 28.79% |

> 🏠 **Ventaja de Local:** El equipo local gana casi el doble que el visitante, confirmando la importancia del factor casa en el fútbol europeo.

---

### 3. Rangos de Cuotas (Bet365)

| Tipo de Cuota | Mínimo | Máximo | Promedio |
|---------------|--------|--------|----------|
| **Cuota Local (Home)** | 1.04 | 26.0 | 2.63 |
| **Cuota Empate (Draw)** | 1.4 | 17.0 | 3.84 |
| **Cuota Visitante (Away)** | 1.4 | 67.0 | 4.05 |

> ⚖️ **Observación:** Las cuotas visitantes son en promedio 54% más altas que las locales, reflejando la ventaja estadística del equipo de casa.

---

### 4. Cuotas Promedio por Resultado Real

| Resultado Real | Cuota Local Avg | Cuota Empate Avg | Cuota Visitante Avg |
|----------------|-----------------|------------------|---------------------|
| **Victoria Local** | 2.08 | 4.08 | 5.96 |
| **Empate** | 2.60 | 3.61 | 4.05 |
| **Victoria Visitante** | 3.54 | 3.65 | 3.14 |

> 💡 **Insight:** Cuando el local gana, su cuota promedio era 2.08 (probabilidad implícita 48%), sugiriendo que el mercado predice correctamente los favoritos.

---

### 5. Variación por Liga

| Liga | Partidos | Cuota Local Avg | Cuota Empate Avg | Cuota Visitante Avg |
|------|----------|-----------------|------------------|---------------------|
| **Spain** | 3,039 | 2.76 | 4.16 | 5.23 |
| **England** | 3,040 | 2.70 | 3.95 | 4.91 |
| **Netherlands** | 2,445 | 2.59 | 4.12 | 4.92 |
| **Germany** | 2,447 | 2.60 | 3.91 | 4.38 |
| **Italy** | 3,011 | 2.51 | 3.60 | 4.56 |
| **France** | 3,036 | 2.41 | 3.44 | 4.39 |

> 🏆 **Competitividad:** España e Inglaterra tienen las cuotas más altas, sugiriendo mayor competitividad e impredecibilidad. Francia e Italia tienen cuotas más bajas, indicando mayor predecibilidad.

---

### 6. Tendencias Temporales

| Temporada | Partidos | Victorias Local | Empates | Victorias Visitante |
|-----------|----------|-----------------|---------|---------------------|
| 2008/2009 | 2,898 | 1,356 (46.8%) | 725 (25.0%) | 817 (28.2%) |
| 2009/2010 | 2,806 | 1,323 (47.1%) | 718 (25.6%) | 765 (27.3%) |
| 2010/2011 | 2,835 | 1,320 (46.6%) | 727 (25.7%) | 788 (27.8%) |
| 2011/2012 | 2,813 | 1,317 (46.8%) | 713 (25.3%) | 783 (27.8%) |
| 2012/2013 | 2,832 | 1,259 (44.5%) | 744 (26.3%) | 829 (29.3%) |
| 2013/2014 | 2,599 | 1,205 (46.4%) | 620 (23.9%) | 774 (29.8%) |
| 2014/2015 | 2,904 | 1,303 (44.9%) | 736 (25.3%) | 865 (29.8%) |
| 2015/2016 | 2,905 | 1,288 (44.3%) | 733 (25.2%) | 884 (30.4%) |

> 📈 **Tendencia:** Se observa un incremento gradual en victorias visitantes del 28.2% (2008) al 30.4% (2016), sugiriendo una reducción en la ventaja de local a lo largo del tiempo.

---

## ✅ VALIDACIÓN DEL MODELO

### El Modelo Conceptual RESPONDE a las Preguntas de Negocio

#### ✅ PREGUNTA 1: Precisión de Predicciones

**Consulta Conceptual:**
```sql
SELECT
    Casa_Apuestas,
    Liga,
    Temporada,
    Tipo_Resultado,
    AVG(Precision_Pct) as precision_promedio,
    COUNT(*) as total_apuestas,
    SUM(Cant_Aciertos) as total_aciertos
FROM FACT_APUESTA_DEPORTIVA
GROUP BY Casa_Apuestas, Liga, Temporada, Tipo_Resultado
ORDER BY precision_promedio DESC
```

**Perspectivas Utilizadas:**
- Casa de Apuestas
- Liga
- Temporada
- Tipo de Resultado

**Indicadores Utilizados:**
- % Precisión
- Cantidad de Aciertos
- Cantidad de Apuestas

---

#### ✅ PREGUNTA 2: ROI de Estrategias

**Consulta Conceptual:**
```sql
SELECT
    Estrategia,
    Liga,
    Temporada,
    Casa_Apuestas,
    AVG(ROI_Pct) as roi_promedio,
    SUM(Ganancia_Total) as ganancia_acumulada,
    SUM(Perdida_Total) as perdida_acumulada,
    (SUM(Ganancia_Total) - SUM(Perdida_Total)) as beneficio_neto
FROM FACT_APUESTA_DEPORTIVA
GROUP BY Estrategia, Liga, Temporada, Casa_Apuestas
HAVING AVG(ROI_Pct) > 0
ORDER BY roi_promedio DESC
```

**Perspectivas Utilizadas:**
- Estrategia
- Liga
- Temporada
- Casa de Apuestas

**Indicadores Utilizados:**
- ROI %
- Ganancia Total
- Pérdida Total

---

#### ✅ PREGUNTA 3: Oportunidades de Arbitraje

**Consulta Conceptual:**
```sql
SELECT
    Partido_ID,
    Liga,
    Temporada,
    Fecha,
    COUNT(DISTINCT Casa_Apuestas) as casas_disponibles,
    MAX(Diferencia_Cuotas) as max_diferencia,
    AVG(Pct_Arbitraje) as oportunidad_arbitraje,
    MIN(Cuota_Promedio) as mejor_cuota_local,
    MAX(Cuota_Promedio) as peor_cuota_local
FROM FACT_APUESTA_DEPORTIVA
WHERE Pct_Arbitraje > 0
GROUP BY Partido_ID, Liga, Temporada, Fecha
HAVING casas_disponibles >= 3
ORDER BY oportunidad_arbitraje DESC
```

**Perspectivas Utilizadas:**
- Partido (derivada de Equipo + Tiempo)
- Liga
- Temporada
- Tiempo

**Indicadores Utilizados:**
- % Arbitraje
- Diferencia de Cuotas
- Cuota Promedio

---

## 🎯 PRÓXIMOS PASOS EN HEFESTO

| Paso | Nombre | Estado | Descripción |
|------|--------|--------|-------------|
| ✅ **1** | Análisis de Requerimientos | **COMPLETADO** | Preguntas, indicadores, perspectivas, modelo conceptual |
| ⏭️ **2** | Análisis de Fuentes OLTP | **Pendiente** | Mapeo detallado Match→Team→League→Country, análisis de calidad de datos |
| ⏭️ **3** | Modelo Lógico del DW | **Pendiente** | Diseño detallado de esquema estrella/copo de nieve, definición de claves |
| ⏭️ **4** | Integración de Datos | **Pendiente** | Procesos ETL (Extract, Transform, Load) para cargar DW |
| ⏭️ **5** | Implementación Física | **Pendiente** | Creación de base de datos física, índices, particiones |
| ⏭️ **6** | Explotación y Visualización | **Pendiente** | Consultas OLAP, dashboards BI (Power BI/Tableau) |

---

## 💡 RECOMENDACIONES TÉCNICAS

### 1. Diseño Dimensional

**Esquema Recomendado:** ⭐ **Esquema Estrella (Star Schema)**

**Justificación:**
- ✅ Óptimo rendimiento para consultas OLAP
- ✅ Simplicidad en joins (solo 1 nivel)
- ✅ Facilita comprensión para usuarios de negocio
- ✅ Mejor performance en agregaciones
- ✅ Compatible con herramientas BI modernas

**Alternativa:** Esquema Copo de Nieve solo si la normalización de dimensiones es crítica para almacenamiento.

---

### 2. Granularidad del Modelo

**Granularidad Recomendada:**
```
1 fila = 1 apuesta de 1 casa de apuestas en 1 partido específico
```

**Beneficios:**
- ✅ Máxima flexibilidad analítica
- ✅ Permite análisis detallado por casa
- ✅ Facilita detección de arbitraje
- ✅ Soporta drill-down hasta nivel atómico

**Consideración:** Mayor volumen de datos (~225K registros) pero hardware moderno lo maneja eficientemente.

---

### 3. Slowly Changing Dimensions (SCD)

**Tablas Candidatas para SCD Tipo 2:**

| Tabla | Tipo SCD | Justificación |
|-------|----------|---------------|
| **Player_Attributes** | Tipo 2 | Atributos cambian en el tiempo (ratings, habilidades) |
| **Team_Attributes** | Tipo 2 | Estrategias y estilos de juego evolucionan |
| **Team** | Tipo 1 | Nombre puede cambiar pero mantener identidad |
| **Casa_Apuestas** | Tipo 1 | Metadatos estáticos generalmente |

**Campos Adicionales para SCD Tipo 2:**
- `fecha_inicio_vigencia`
- `fecha_fin_vigencia`
- `version`
- `es_actual` (flag booleano)

---

### 4. Indicadores Calculados

**Implementación Recomendada:** Calcular en capa semántica, NO almacenar

**Indicadores a Calcular Dinámicamente:**
```sql
-- % Precisión
Precision_Pct = (SUM(Aciertos) / SUM(Total_Apuestas)) * 100

-- ROI %
ROI_Pct = ((SUM(Ganancia_Total) - SUM(Perdida_Total)) / SUM(Perdida_Total)) * 100

-- % Arbitraje
Pct_Arbitraje = (1/MIN(Cuota_Local) + 1/MIN(Cuota_Empate) + 1/MIN(Cuota_Visitante))

-- Diferencia de Cuotas
Diferencia_Cuotas = MAX(Cuota) - MIN(Cuota)
```

**Herramientas:**
- Power BI: DAX Measures
- Tableau: Calculated Fields
- Qlik: Master Measures

---

### 5. Índices y Optimización

**Índices Recomendados:**

```sql
-- Índices en tabla de hechos
CREATE INDEX idx_fecha ON FACT_APUESTA_DEPORTIVA(fecha);
CREATE INDEX idx_temporada ON FACT_APUESTA_DEPORTIVA(temporada_id);
CREATE INDEX idx_liga ON FACT_APUESTA_DEPORTIVA(liga_id);
CREATE INDEX idx_casa ON FACT_APUESTA_DEPORTIVA(casa_apuestas_id);

-- Índices compuestos para queries frecuentes
CREATE INDEX idx_temporada_liga ON FACT_APUESTA_DEPORTIVA(temporada_id, liga_id);
CREATE INDEX idx_fecha_liga ON FACT_APUESTA_DEPORTIVA(fecha, liga_id);

-- Índices en dimensiones
CREATE INDEX idx_dim_tiempo_fecha ON DIM_TIEMPO(fecha);
CREATE INDEX idx_dim_liga_pais ON DIM_LIGA(pais);
```

---

### 6. Particionamiento

**Estrategia de Particionamiento:** Por **Temporada** (particionamiento horizontal)

```sql
-- Ejemplo conceptual
PARTITION BY RANGE (temporada_id) (
    PARTITION p_2008_2009 VALUES LESS THAN (2009),
    PARTITION p_2009_2010 VALUES LESS THAN (2010),
    PARTITION p_2010_2011 VALUES LESS THAN (2011),
    ...
    PARTITION p_2015_2016 VALUES LESS THAN (2017),
    PARTITION p_futuro VALUES LESS THAN MAXVALUE
);
```

**Beneficios:**
- ✅ Mejora rendimiento de queries con filtro de temporada
- ✅ Facilita archivado de datos históricos
- ✅ Mantenimiento más eficiente

---

### 7. ETL - Consideraciones

**Proceso ETL Recomendado:**

#### Extract:
- Lectura directa de SQLite `database.sqlite`
- Validación de integridad referencial
- Detección de registros duplicados

#### Transform:
- **Limpieza:**
  - Normalización de nombres de equipos
  - Manejo de valores NULL en cuotas
  - Validación de rangos (cuotas > 1.0)

- **Derivación:**
  - Cálculo de favorito (MIN cuota)
  - Derivación de resultado (comparación goles)
  - Generación de dimensión tiempo

- **Enriquecimiento:**
  - Agregar clasificación de estrategia
  - Calcular métricas de arbitraje
  - Asignar categorías de liga

#### Load:
- Carga incremental por temporada
- Validación post-carga (conteos, sumas de control)
- Actualización de índices y estadísticas

**Herramientas Sugeridas:**
- **Python:** Pandas + SQLAlchemy
- **Talend Open Studio:** ETL visual
- **Apache Airflow:** Orquestación y scheduling
- **dbt (data build tool):** Transformaciones SQL

---

### 8. Calidad de Datos

**Validaciones Críticas:**

| Validación | Regla | Acción en Falla |
|------------|-------|-----------------|
| **Cuotas Válidas** | `cuota >= 1.01` | Rechazar registro |
| **Goles No Negativos** | `goles >= 0` | Rechazar registro |
| **Fechas Coherentes** | `fecha BETWEEN 2008-08-01 AND 2016-05-31` | Alertar |
| **FK Válidas** | `EXISTS en tabla referenciada` | Rechazar registro |
| **Cobertura Casas** | `MIN 1 casa por partido` | Alertar |
| **Probabilidades** | `SUM(1/cuotas) >= 1.0` | Advertencia (margen casa) |

---

### 9. Seguridad y Gobernanza

**Niveles de Acceso:**

| Rol | Permisos | Alcance |
|-----|----------|---------|
| **Analista BI** | SELECT en todas las tablas | Lectura completa |
| **Usuario Negocio** | SELECT en vistas agregadas | Solo indicadores clave |
| **Administrador DW** | ALL | Gestión completa |
| **Proceso ETL** | INSERT, UPDATE en FACT/DIM | Solo carga de datos |

---

### 10. Monitoreo y Mantenimiento

**KPIs del Data Warehouse:**

- **Frescura de Datos:** Última carga exitosa
- **Completitud:** % de partidos con cuotas completas
- **Calidad:** % de registros rechazados en ETL
- **Performance:** Tiempo promedio de queries top 10
- **Uso:** Queries ejecutadas por día/semana
- **Almacenamiento:** Crecimiento del DW por mes

---

## 📚 FUENTES DE DATOS IDENTIFICADAS

### Tablas Fuente (Database.sqlite)

| Tabla | Tipo | Descripción | Registros | Uso en DW |
|-------|------|-------------|-----------|-----------|
| **Match** | Hecho Principal | Partidos, resultados, cuotas | 25,979 | Tabla de hechos base |
| **Player** | Dimensión | Información de jugadores | 11,060 | Dimensión (opcional) |
| **Player_Attributes** | SCD | Atributos de jugadores en el tiempo | Variable | SCD Tipo 2 (opcional) |
| **Team** | Dimensión | Equipos | ~300 | Dimensión Equipo |
| **Team_Attributes** | SCD | Atributos de equipos en el tiempo | Variable | SCD Tipo 2 (opcional) |
| **League** | Dimensión | Ligas | 11 | Dimensión Liga |
| **Country** | Dimensión | Países | 11 | Jerarquía en Dim Liga |

---

## 🎓 GLOSARIO DE TÉRMINOS

| Término | Definición |
|---------|------------|
| **Arbitraje Deportivo** | Estrategia de apuestas que garantiza ganancia independiente del resultado |
| **Cuota (Odds)** | Multiplicador que determina ganancia potencial de una apuesta |
| **Favorito** | Resultado con menor cuota (mayor probabilidad según casa de apuestas) |
| **Underdog** | Resultado con mayor cuota (menor probabilidad según casa de apuestas) |
| **Probabilidad Implícita** | 1/cuota - representa la probabilidad según la casa de apuestas |
| **Margen de Casa** | Diferencia entre 100% y suma de probabilidades implícitas (ganancia casa) |
| **ROI** | Return on Investment - retorno de inversión porcentual |
| **Sure Bet** | Apuesta garantizada sin riesgo mediante arbitraje |
| **Value Bet** | Apuesta donde la probabilidad real supera la implícita en la cuota |
| **Kelly Criterion** | Fórmula matemática para optimizar tamaño de apuestas |

---

## 📞 CONTACTO Y PRÓXIMOS PASOS

**Estado Actual:** ✅ PASO 1 COMPLETADO

**Próxima Acción:** Iniciar **Paso 2 - Análisis de Fuentes OLTP**

**Contenido del Paso 2:**
- Análisis detallado de calidad de datos en tablas fuente
- Mapeo campo a campo desde origen a destino
- Identificación de transformaciones necesarias
- Definición de reglas de limpieza y validación
- Documentación de dependencias entre tablas

---

## 📄 LICENCIA

Este análisis se realiza sobre datos públicos de partidos de fútbol europeo con fines educativos y de investigación en Business Intelligence.

---

## 🔖 VERSIÓN

- **Versión:** 1.0
- **Fecha:** 2025-10-22
- **Metodología:** HEFESTO
- **Fase Completada:** Paso 1 - Análisis de Requerimientos
- **Autor:** Análisis de Business Intelligence

---

**Generado mediante metodología HEFESTO para diseño de Data Warehouse**
