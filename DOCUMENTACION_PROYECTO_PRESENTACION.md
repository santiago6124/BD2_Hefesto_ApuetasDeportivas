# 📊 DATA WAREHOUSE PARA ANÁLISIS DE APUESTAS DEPORTIVAS
## Documentación General del Proyecto | Metodología HEFESTO

**Proyecto**: Sistema de Inteligencia de Negocios para Análisis de Mercado de Apuestas Deportivas
**Metodología**: HEFESTO v2.0 (Pasos 1-3 Completados)
**Fecha**: Octubre 2025
**Estado**: Modelo Lógico Completado - Listo para Implementación

---

## 📋 TABLA DE CONTENIDOS

1. [Resumen Ejecutivo](#1-resumen-ejecutivo)
2. [¿Qué es este Proyecto?](#2-qué-es-este-proyecto)
3. [¿Por qué este Proyecto?](#3-por-qué-este-proyecto)
4. [Datos del Proyecto](#4-datos-del-proyecto)
5. [Metodología HEFESTO Explicada](#5-metodología-hefesto-explicada)
6. [Paso 1: Análisis de Requerimientos](#6-paso-1-análisis-de-requerimientos)
7. [Paso 2: Análisis OLTP](#7-paso-2-análisis-oltp)
8. [Paso 3: Modelo Lógico](#8-paso-3-modelo-lógico)
9. [Arquitectura del Data Warehouse](#9-arquitectura-del-data-warehouse)
10. [Conceptos Clave Explicados](#10-conceptos-clave-explicados)
11. [Resultados Esperados](#11-resultados-esperados)
12. [Próximos Pasos](#12-próximos-pasos)

---

## 1. RESUMEN EJECUTIVO

### ¿Qué es?
Un **Data Warehouse (Almacén de Datos)** diseñado para analizar el mercado de apuestas deportivas de fútbol europeo, permitiendo tomar decisiones basadas en datos históricos de 8 años (2008-2016) con información de 10 casas de apuestas y 22,592 partidos.

### Objetivo Principal
Responder 3 preguntas clave de negocio:
1. **¿Qué casa de apuestas predice mejor los resultados?**
2. **¿Qué estrategias de apuesta son rentables?**
3. **¿Dónde hay oportunidades de arbitraje (ganancia garantizada)?**

### Estado Actual
✅ **PASO 1 COMPLETADO**: Requerimientos identificados
✅ **PASO 2 COMPLETADO**: Datos fuente analizados y mapeados
✅ **PASO 3 COMPLETADO**: Modelo lógico diseñado
🔄 **SIGUIENTE**: Implementación física del Data Warehouse

### Métricas Clave del Proyecto
- **22,592 partidos** con datos completos
- **10 casas de apuestas** analizadas
- **11 ligas europeas** (Premier League, La Liga, etc.)
- **903,680 registros** en la tabla principal de hechos
- **40x más rápido** para consultas de arbitraje gracias al diseño optimizado

---

## 2. ¿QUÉ ES ESTE PROYECTO?

### Definición Simple
Imagina que tienes miles de partidos de fútbol con las cuotas (probabilidades) que ofrecieron 10 casas de apuestas diferentes, y conoces el resultado real de cada partido. Este proyecto construye un sistema que te permite:

- **Analizar** qué casa acierta más
- **Evaluar** si apostar sistemáticamente es rentable
- **Detectar** oportunidades donde puedes ganar sin importar el resultado

### Analogía
Es como tener una máquina del tiempo para las apuestas: sabes lo que pasó y puedes ver qué hubiera funcionado mejor. No es para predecir el futuro, sino para entender patrones del pasado y tomar mejores decisiones.

### ¿Qué NO es?
❌ No es un sistema de predicción de resultados
❌ No es una plataforma de apuestas en tiempo real
❌ No es un bot automático de apuestas
✅ Es un sistema de **análisis histórico** para **toma de decisiones informadas**

---

## 3. ¿POR QUÉ ESTE PROYECTO?

### Problema de Negocio
Las casas de apuestas ofrecen diferentes cuotas para el mismo partido. Analistas y apostadores profesionales necesitan:
- Identificar qué información es más confiable
- Evaluar si estrategias sistemáticas funcionan
- Detectar ineficiencias en el mercado

### Valor del Proyecto

#### Para Analistas de Datos
- Modelo de negocio complejo con múltiples dimensiones de análisis
- Desafíos técnicos: transformación UNPIVOT, SCD Tipo 2, esquema constelación
- Métricas aditivas y no-aditivas

#### Para Decisores de Negocio
- **ROI Cuantificable**: Identificar estrategias rentables históricamente
- **Reducción de Riesgo**: Detectar oportunidades de arbitraje sin riesgo
- **Ventaja Competitiva**: Entender qué fuentes de información son mejores

#### Para Estudiantes/Profesionales
- Aplicación práctica de metodología HEFESTO
- Data Warehouse real con datos complejos
- Ejemplo completo desde requerimientos hasta modelo lógico

---

## 4. DATOS DEL PROYECTO

### Fuente de Datos
**Base de Datos SQLite**: `database.sqlite`

### Estadísticas del Dataset

| Métrica | Valor | Detalle |
|---------|-------|---------|
| **Partidos Totales** | 25,979 | Fútbol europeo 2008-2016 |
| **Partidos Útiles** | 22,592 | 87% con datos completos de cuotas |
| **Casas de Apuestas** | 10 | Bet365, Betway, Pinnacle, etc. |
| **Ligas** | 11 | Premier League, La Liga, Bundesliga, etc. |
| **Equipos** | ~300 | Equipos de primera y segunda división |
| **Temporadas** | 8 | Desde 2008/09 hasta 2015/16 |
| **Período** | 8 años | Datos históricos completos |

### Ligas Incluidas
🏴󠁧󠁢󠁥󠁮󠁧󠁿 **Inglaterra** - Premier League (3,040 partidos)
🇪🇸 **España** - La Liga (3,039 partidos)
🇫🇷 **Francia** - Ligue 1 (3,036 partidos)
🇮🇹 **Italia** - Serie A (3,011 partidos)
🇩🇪 **Alemania** - Bundesliga (2,447 partidos)
🇳🇱 **Países Bajos** - Eredivisie (2,445 partidos)
🇵🇹 **Portugal** - Primeira Liga (2,044 partidos)
🏴󠁧󠁢󠁳󠁣󠁴󠁿 **Escocia** - Premiership (1,824 partidos)
... y 3 más

### Casas de Apuestas
1. **Bet365** - 87% cobertura
2. **Betway** - 87% cobertura
3. **Interwetten** - 87% cobertura
4. **Ladbrokes** - 87% cobertura
5. **William Hill** - 87% cobertura
6. **Pinnacle** - 43% cobertura
7. **Stan James** - 66% cobertura
8. Y 3 más...

---

## 5. METODOLOGÍA HEFESTO EXPLICADA

### ¿Qué es HEFESTO?
**HEFESTO** es una metodología específica para diseñar Data Warehouses (almacenes de datos). Es como una receta paso a paso para construir sistemas de análisis de datos complejos.

### ¿Por qué HEFESTO y no solo "hacer una base de datos"?
Los Data Warehouses NO son bases de datos normales:

| Base de Datos Transaccional (OLTP) | Data Warehouse (OLAP) |
|-------------------------------------|----------------------|
| Para operaciones diarias | Para análisis histórico |
| Muchas escrituras | Pocas escrituras, muchas lecturas |
| Normalizado (evita redundancia) | Desnormalizado (optimizado para consultas) |
| Respuesta rápida a operaciones | Respuesta rápida a análisis complejos |
| **Ejemplo**: Registrar una apuesta | **Ejemplo**: "¿Cuál casa acierta más?" |

### Los 4 Pasos de HEFESTO

```
┌─────────────────────────────────────────────────────────────┐
│                     METODOLOGÍA HEFESTO                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  PASO 1: ANÁLISIS DE REQUERIMIENTOS ✅ COMPLETADO          │
│  ├─ Identificar preguntas de negocio                        │
│  ├─ Definir indicadores (métricas)                          │
│  └─ Identificar perspectivas (dimensiones)                  │
│                                                              │
│  PASO 2: ANÁLISIS DE LOS OLTP ✅ COMPLETADO                │
│  ├─ Conformar indicadores (mapear fórmulas)                 │
│  ├─ Establecer correspondencias (mapear dimensiones)        │
│  └─ Nivel de granularidad (campos específicos)              │
│                                                              │
│  PASO 3: MODELO LÓGICO DEL DW ✅ COMPLETADO                │
│  ├─ Seleccionar tipo de esquema                             │
│  ├─ Diseñar tablas de dimensiones                           │
│  ├─ Diseñar tablas de hechos                                │
│  └─ Definir relaciones y cardinalidades                     │
│                                                              │
│  PASO 4: INTEGRACIÓN DE DATOS 🔄 PENDIENTE                 │
│  ├─ Diseño ETL (Extract, Transform, Load)                   │
│  ├─ Carga inicial                                            │
│  └─ Actualización periódica                                 │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 6. PASO 1: ANÁLISIS DE REQUERIMIENTOS

### Objetivo
Entender **QUÉ** se quiere analizar antes de pensar en **CÓMO** construirlo.

### 6.1. Preguntas de Negocio (¿Qué queremos responder?)

#### PREGUNTA 1: Precisión de las Casas de Apuestas
**Pregunta**: ¿Cuál casa de apuestas predice mejor los resultados?

**¿Cómo se mide?**
Las cuotas más bajas indican el favorito según la casa. Si Bet365 pone cuota 1.50 al equipo local, está diciendo "tiene alta probabilidad de ganar". Contamos cuántas veces acertaron.

**Análisis por**:
- Por liga (¿En qué liga aciertan más?)
- Por temporada (¿Mejoran con el tiempo?)
- Por tipo de resultado (¿Predicen mejor locales, empates o visitantes?)

**Ejemplo de Insight**:
> "Pinnacle tiene 56% de precisión en Premier League pero solo 48% en Ligue 1"

---

#### PREGUNTA 2: ROI de Estrategias de Apuesta
**Pregunta**: ¿Qué estrategias sistemáticas son rentables?

**Estrategias a evaluar**:
1. **Siempre Favorito**: Apostar siempre al resultado con menor cuota
2. **Siempre Underdog**: Apostar siempre al resultado con mayor cuota
3. **Siempre Empate**: Apostar siempre al empate
4. **Value Betting**: Apostar cuando la cuota es mayor que la probabilidad estimada

**¿Cómo se mide?**
ROI (Return on Investment) = (Ganancia - Inversión) / Inversión × 100

**Ejemplo de Insight**:
> "Apostar siempre al favorito en Bundesliga da -5% ROI (pierdes), pero en Championship da +8% ROI (ganas)"

---

#### PREGUNTA 3: Oportunidades de Arbitraje
**Pregunta**: ¿Dónde hay ganancia garantizada sin importar el resultado?

**¿Qué es Arbitraje Deportivo?**
Cuando las cuotas de diferentes casas permiten cubrir todos los resultados con ganancia garantizada.

**Ejemplo Simplificado**:
```
Partido: Real Madrid vs Barcelona

Casa A ofrece:  Real Madrid gana: 2.10
Casa B ofrece:  Empate: 4.00
Casa C ofrece:  Barcelona gana: 4.50

Si apostamos correctamente en las 3 casas:
- Invertimos: 100€ total
- Ganamos: 103€ sin importar el resultado
- Beneficio: 3% garantizado
```

**Fórmula Técnica**:
```
Arbitraje existe cuando: (1/cuota_local + 1/cuota_empate + 1/cuota_visitante) < 1.0
```

**Ejemplo de Insight**:
> "248 oportunidades de arbitraje en Premier League 2015/16, beneficio promedio 2.3%"

---

### 6.2. Indicadores (¿Qué métricas calculamos?)

| Indicador | Qué Mide | Tipo | Ejemplo |
|-----------|----------|------|---------|
| **% Precisión** | Porcentaje de aciertos | No Aditivo | "Bet365: 54%" |
| **ROI %** | Rentabilidad porcentual | No Aditivo | "Estrategia X: +12%" |
| **Ganancia Total** | Dinero ganado | Aditivo | "€15,430" |
| **Pérdida Total** | Dinero perdido | Aditivo | "€8,200" |
| **% Arbitraje** | Frecuencia de oportunidades | No Aditivo | "1.2% de partidos" |
| **Cant. Aciertos** | Número de predicciones correctas | Aditivo | "12,340 aciertos" |
| **Cant. Apuestas** | Total de apuestas | Aditivo | "22,592 apuestas" |

**¿Qué significa "Aditivo" vs "No Aditivo"?**
- **Aditivo**: Se puede sumar directamente (ganancias de enero + ganancias de febrero = ganancias del bimestre)
- **No Aditivo**: Requiere recalcular (precisión de enero + precisión de febrero ≠ precisión del bimestre)

---

### 6.3. Perspectivas (¿Desde qué ángulos analizamos?)

Las perspectivas son las "dimensiones" del análisis. Son como diferentes formas de "rebanar" los datos:

1. **Casa de Apuestas** - ¿Qué casa? (Bet365, Betway, etc.)
2. **Liga** - ¿En qué liga? (Premier League, La Liga, etc.)
3. **Tiempo** - ¿Cuándo? (Temporada, mes, fecha)
4. **Tipo de Resultado** - ¿Qué resultado? (Local, Empate, Visitante)
5. **Equipo** - ¿Qué equipo? (Real Madrid, Barcelona, etc.)
6. **Estrategia** - ¿Qué estrategia? (Favorito, Underdog, etc.)

**Ejemplo de Análisis Multidimensional**:
> "ROI de la estrategia 'Siempre Favorito' en Bet365, para partidos de Premier League, en la temporada 2015/16, cuando juega de local el Manchester United"

---

## 7. PASO 2: ANÁLISIS OLTP

### Objetivo
Entender **CÓMO ESTÁN** los datos actualmente y **CÓMO MAPEARLOS** al Data Warehouse.

### 7.1. ¿Qué es OLTP?
**OLTP** = Online Transaction Processing = La base de datos original donde se registran operaciones diarias.

En nuestro caso: SQLite con tabla `Match` que tiene:
- Información del partido (equipos, goles, fecha)
- 30 columnas de cuotas (10 casas × 3 resultados)

### 7.2. Desafío Principal: Transformación UNPIVOT

**Problema**: Los datos están "acostados" (en columnas)

**Estructura Original**:
```
match_id | B365H | B365D | B365A | BWH | BWD | BWA | ... (30 columnas!)
---------|-------|-------|-------|-----|-----|-----|
   1     | 1.85  | 3.40  | 4.20  | 1.90| 3.30| 4.10| ...
```

**Estructura Necesaria** (en Data Warehouse):
```
match_id | casa      | cuota_local | cuota_empate | cuota_visitante
---------|-----------|-------------|--------------|----------------
   1     | Bet365    | 1.85        | 3.40         | 4.20
   1     | Betway    | 1.90        | 3.30         | 4.10
   1     | Pinnacle  | 1.88        | 3.35         | 4.15
   ...   | ...       | ...         | ...          | ...
```

**Resultado**: 1 partido → 10 filas (una por casa)

### 7.3. Mapeo de Dimensiones

#### Mapeo DIRECTO (fácil)
- **Liga**: Existe tabla `League` → Mapeo directo
- **Equipo**: Existe tabla `Team` → Mapeo directo

#### Mapeo DERIVADO (requiere cálculo)
- **Tiempo**: Se extrae de `Match.date`
- **Tipo Resultado**: Se calcula comparando goles
- **Casa Apuestas**: Se deriva haciendo UNPIVOT

#### Mapeo CALCULADO (lógica de negocio)
- **Estrategia**: No existe en OLTP, se calcula según reglas:
  - Favorito = MIN(cuotas)
  - Underdog = MAX(cuotas)
  - etc.

### 7.4. Cardinalidad de Transformación

| Concepto OLTP | Registros OLTP | Registros DW | Factor |
|---------------|----------------|--------------|--------|
| **Match** | 25,979 | 903,680 | **40x** |
| Liga | 11 | 11 | 1x |
| Equipo | 300 | 600 | 2x |
| Casa Apuestas | - | 10 | N/A |

**¿Por qué 40x?**
- 22,592 partidos útiles
- × 10 casas
- × 4 estrategias
= 903,680 registros en tabla de hechos

---

## 8. PASO 3: MODELO LÓGICO

### Objetivo
Diseñar la **ESTRUCTURA** del Data Warehouse: tablas, campos, relaciones.

### 8.1. Decisión de Esquema: CONSTELACIÓN

**¿Por qué NO Estrella Simple?**
Porque tenemos **2 granularidades diferentes**:
- Análisis detallado de apuestas (Preguntas 1 y 2)
- Análisis agregado de arbitraje (Pregunta 3)

**Solución**: 2 Tablas de Hechos que comparten dimensiones

```
        DIM_FECHA          DIM_LIGA
           │                 │
           │                 │
      ┌────┴────┐       ┌────┴────┐
      │         │       │         │
   FACT_      FACT_  DIM_      DIM_
 APUESTAS  ARBITRAJE EQUIPO   CASA
      │         │
      │         │
  DIM_ESTRATEGIA
     DIM_RESULTADO
```

### 8.2. Tablas de Dimensiones (6)

#### DIM_CASA_APUESTAS
**Cardinalidad**: 10 registros
**Campos Clave**: id_casa, nombre_completo, código_casa
**Ejemplo**: `1, 'Bet365', 'B365'`

#### DIM_LIGA
**Cardinalidad**: 11 registros
**Jerarquía**: País → Liga → Temporada
**Ejemplo**: `1, 'Premier League', 'England'`

#### DIM_FECHA
**Cardinalidad**: ~2,920 registros (fechas únicas)
**Jerarquía**: Año → Trimestre → Mes → Día
**Ejemplo**: `20150815, '2015-08-15', 'Agosto', 2015, '2015/16'`

#### DIM_EQUIPO (con SCD Tipo 2)
**Cardinalidad**: ~400 registros (con versiones)
**Particularidad**: Captura ascensos/descensos
**Ejemplo**:
```
Leicester City - versión 1: Championship (2008-2014)
Leicester City - versión 2: Premier League (2014-2016)
```

#### DIM_RESULTADO_TIPO
**Cardinalidad**: 3 registros
**Valores**: Local (H), Empate (D), Visitante (A)

#### DIM_ESTRATEGIA
**Cardinalidad**: 4 registros
**Valores**: ALWAYS_H, ALWAYS_A, FOLLOW_FAV, UNDERDOG

---

### 8.3. Tablas de Hechos (2)

#### FACT_APUESTAS (Principal)
**Granularidad**: 1 fila = 1 apuesta de 1 casa en 1 partido con 1 estrategia
**Registros**: ~903,680
**Métricas Almacenadas**:
- ganancia_total (aditivo)
- perdida_total (aditivo)
- inversion (aditivo)
- cant_aciertos (aditivo)
- cant_apuestas (aditivo)

**Métricas Calculadas**:
- % Precisión = cant_aciertos / cant_apuestas × 100
- ROI % = (ganancia - perdida) / inversion × 100

**Clave Primaria**: (id_fecha, id_equipo_local, id_equipo_visitante, id_casa, id_estrategia, id_resultado)

---

#### FACT_ARBITRAJE (Secundaria)
**Granularidad**: 1 fila = 1 partido completo (análisis cross-casa)
**Registros**: ~22,592
**Métricas Almacenadas**:
- cant_oportunidades
- beneficio_arbitraje
- porcentaje_arbitraje
- es_oportunidad (booleano)

**Ventaja**: Consultas de arbitraje **40x más rápidas** (no necesitan escanear 903K registros)

**Clave Primaria**: (id_fecha, id_equipo_local, id_equipo_visitante, id_liga)

---

### 8.4. Relaciones y Cardinalidades

**Dimensiones Conformadas** (compartidas por ambas tablas de hechos):
- DIM_FECHA
- DIM_LIGA
- DIM_EQUIPO

**Dimensiones Exclusivas**:
- DIM_ESTRATEGIA → solo FACT_APUESTAS
- DIM_RESULTADO_TIPO → solo FACT_APUESTAS
- DIM_CASA_APUESTAS → ambas (pero diferente uso)

**Cardinalidades**: Todas son 1:N (una dimensión, muchos hechos)

**Role-Playing**: DIM_EQUIPO se usa 2 veces (equipo local y equipo visitante)

---

## 9. ARQUITECTURA DEL DATA WAREHOUSE

### 9.1. Esquema Visual Completo

```
┌─────────────────────────────────────────────────────────────────┐
│                    DATA WAREHOUSE ARCHITECTURE                   │
│                 Análisis de Apuestas Deportivas                  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                      DIMENSIONES CONFORMADAS                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  📅 DIM_FECHA        ⚽ DIM_LIGA        👥 DIM_EQUIPO          │
│   (~2,920)             (11)               (~400 con SCD-2)      │
│                                                                  │
│  Temporalidad        Geografía          Entidades              │
│  Jerarquías         Jerarquías         Role-Playing            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────┐ ┌───────────────────────┐
│   DIMENSIONES EXCLUSIVAS APUESTAS    │ │ DIM. EXCLUSIVAS ARB.  │
├──────────────────────────────────────┤ ├───────────────────────┤
│ 🏢 DIM_CASA_APUESTAS (10)            │ │ (Usa DIM_CASA_APUESTAS│
│ 🎲 DIM_ESTRATEGIA (4)                │ │  de forma diferente)  │
│ 🎯 DIM_RESULTADO_TIPO (3)            │ │                       │
└──────────────────────────────────────┘ └───────────────────────┘
                │                                    │
                │                                    │
                ▼                                    ▼
┌──────────────────────────────┐  ┌─────────────────────────────┐
│    FACT_APUESTAS             │  │   FACT_ARBITRAJE           │
│    (~903,680 registros)      │  │   (~22,592 registros)      │
├──────────────────────────────┤  ├─────────────────────────────┤
│ Granularidad:                │  │ Granularidad:              │
│ 1 apuesta individual         │  │ 1 partido completo         │
│                              │  │                            │
│ Métricas:                    │  │ Métricas:                  │
│ • ganancia_total             │  │ • cant_oportunidades       │
│ • perdida_total              │  │ • beneficio_arbitraje      │
│ • inversion                  │  │ • porcentaje_arbitraje     │
│ • cant_aciertos              │  │ • es_oportunidad           │
│ • cant_apuestas              │  │                            │
│                              │  │ Ventaja:                   │
│ Responde:                    │  │ 40x más rápido            │
│ ✓ Pregunta 1 (Precisión)    │  │                            │
│ ✓ Pregunta 2 (ROI)          │  │ Responde:                  │
│                              │  │ ✓ Pregunta 3 (Arbitraje)  │
└──────────────────────────────┘  └─────────────────────────────┘
```

### 9.2. Flujo de Datos

```
┌─────────────────────────────────────────────────────────────────┐
│                        FLUJO ETL                                 │
└─────────────────────────────────────────────────────────────────┘

1. EXTRACT (Extracción)
   ├─ database.sqlite
   │  ├─ Match (25,979 partidos)
   │  ├─ League (11 ligas)
   │  ├─ Team (300 equipos)
   │  └─ Country (11 países)
   │
2. TRANSFORM (Transformación)
   ├─ Filtrar partidos con datos completos → 22,592
   ├─ UNPIVOT 30 columnas cuotas → 10 filas por partido
   ├─ Calcular 4 estrategias por combinación
   ├─ Derivar dimensiones tiempo, resultado
   ├─ Aplicar SCD Tipo 2 en equipos
   │
3. LOAD (Carga)
   ├─ Poblar 6 tablas de dimensiones
   ├─ Generar claves subrogadas
   ├─ Cargar FACT_APUESTAS (903,680 registros)
   └─ Cargar FACT_ARBITRAJE (22,592 registros)
```

---

## 10. CONCEPTOS CLAVE EXPLICADOS

### 10.1. Data Warehouse vs Base de Datos

**Base de Datos Transaccional**:
- Registra operaciones en tiempo real
- Optimizada para escrituras rápidas
- Datos normalizados (sin redundancia)
- Ejemplo: Sistema de ventas de una tienda

**Data Warehouse**:
- Almacena historia para análisis
- Optimizada para consultas complejas
- Datos desnormalizados (con redundancia intencional)
- Ejemplo: "¿Qué productos se vendieron más en navidad los últimos 5 años?"

### 10.2. Esquema Estrella vs Constelación

**Esquema Estrella**:
```
        DIM1
         │
    DIM2─FACT─DIM3
         │
        DIM4
```
- 1 tabla de hechos central
- Múltiples dimensiones alrededor
- Más simple, pero menos flexible

**Esquema Constelación** (Nuestro Proyecto):
```
      DIM1    DIM2
        │      │
    ┌───┴──┬───┴───┐
    │      │       │
  FACT1  FACT2  DIM3
```
- 2+ tablas de hechos
- Dimensiones compartidas
- Más complejo, pero más eficiente

### 10.3. SCD Tipo 2 (Slowly Changing Dimensions)

**Problema**: ¿Qué pasa cuando un equipo cambia de liga?

**Solución SCD Tipo 2**: Crear nueva versión del registro

```
Ejemplo: Leicester City

Versión 1:
id_equipo: 245
nombre: Leicester City
liga: Championship
fecha_inicio: 2008-08-01
fecha_fin: 2014-05-31
registro_actual: FALSE

Versión 2:
id_equipo: 246
nombre: Leicester City
liga: Premier League
fecha_inicio: 2014-06-01
fecha_fin: NULL
registro_actual: TRUE
```

**Beneficio**: Mantiene historia correcta. Podemos analizar "Leicester cuando estaba en Championship" vs "Leicester en Premier League"

### 10.4. Métricas Aditivas vs No-Aditivas

**Aditivo**: Se puede sumar directamente
- Ganancia enero: €1,000
- Ganancia febrero: €2,000
- **Ganancia bimestre: €3,000 ✓** (suma correcta)

**No-Aditivo**: Requiere recalcular
- Precisión enero: 60% (60 de 100 aciertos)
- Precisión febrero: 50% (50 de 100 aciertos)
- **Precisión bimestre: ¿55%? ✗ INCORRECTO**
- **Precisión bimestre: 110/200 = 55% ✓** (recalcular desde cantidades)

### 10.5. UNPIVOT

**Antes** (columnas):
```
Partido | B365_Local | B365_Empate | BW_Local | BW_Empate | ...
--------|-----------|-------------|----------|-----------|----
   1    |   1.85    |    3.40     |   1.90   |   3.30    | ...
```

**Después** (filas):
```
Partido | Casa   | Cuota_Local | Cuota_Empate
--------|--------|-------------|-------------
   1    | Bet365 |    1.85     |    3.40
   1    | Betway |    1.90     |    3.30
```

**Por qué**: Facilita consultas tipo "comparar todas las casas"

### 10.6. Granularidad

**Definición**: Nivel de detalle de cada registro

**Nuestro caso FACT_APUESTAS**:
```
1 fila = 1 apuesta de 1 casa en 1 partido con 1 estrategia
```

**Ejemplo**:
- Partido: Real Madrid vs Barcelona
- Casa: Bet365
- Estrategia: Apostar al favorito
- Resultado: Local

→ 1 registro en FACT_APUESTAS

**Granularidad FACT_ARBITRAJE**:
```
1 fila = 1 partido completo (todas las casas analizadas)
```

---

## 11. RESULTADOS ESPERADOS

### 11.1. Consultas que se Pueden Responder

#### Consulta 1: Casa Más Precisa por Liga
```sql
SELECT
    c.nombre_completo,
    l.nombre_liga,
    SUM(f.cant_aciertos) * 100.0 / SUM(f.cant_apuestas) as precision_pct
FROM FACT_APUESTAS f
JOIN DIM_CASA_APUESTAS c ON f.id_casa_apuestas = c.id_casa_apuestas
JOIN DIM_LIGA l ON f.id_liga = l.id_liga
GROUP BY c.nombre_completo, l.nombre_liga
ORDER BY precision_pct DESC;
```

**Resultado Esperado**:
```
Casa             | Liga              | Precisión
-----------------|-------------------|----------
Pinnacle         | Premier League    | 56.3%
Bet365           | La Liga           | 54.8%
Betway           | Bundesliga        | 53.2%
...
```

---

#### Consulta 2: ROI por Estrategia y Temporada
```sql
SELECT
    e.nombre_estrategia,
    t.temporada,
    (SUM(f.ganancia_total) - SUM(f.perdida_total)) * 100.0 /
     SUM(f.inversion) as roi_pct
FROM FACT_APUESTAS f
JOIN DIM_ESTRATEGIA e ON f.id_estrategia = e.id_estrategia
JOIN DIM_FECHA t ON f.id_fecha = t.id_fecha
GROUP BY e.nombre_estrategia, t.temporada
HAVING SUM(f.inversion) > 0
ORDER BY roi_pct DESC;
```

**Resultado Esperado**:
```
Estrategia         | Temporada | ROI%
-------------------|-----------|------
FOLLOW_FAV         | 2015/16   | +12.3%
ALWAYS_H           | 2014/15   | +8.7%
UNDERDOG           | 2013/14   | -15.2%
...
```

---

#### Consulta 3: Oportunidades de Arbitraje
```sql
SELECT
    l.nombre_liga,
    t.temporada,
    SUM(f.cant_oportunidades) as total_oportunidades,
    AVG(f.porcentaje_arbitraje) as beneficio_promedio
FROM FACT_ARBITRAJE f
JOIN DIM_LIGA l ON f.id_liga = l.id_liga
JOIN DIM_FECHA t ON f.id_fecha = t.id_fecha
WHERE f.es_oportunidad = TRUE
GROUP BY l.nombre_liga, t.temporada
ORDER BY total_oportunidades DESC;
```

**Resultado Esperado**:
```
Liga              | Temporada | Oportunidades | Beneficio Promedio
------------------|-----------|---------------|-------------------
Premier League    | 2015/16   | 248           | 2.34%
La Liga           | 2015/16   | 186           | 1.87%
Bundesliga        | 2014/15   | 142           | 2.01%
...
```

---

### 11.2. Dashboards y Visualizaciones

#### Dashboard 1: Análisis de Casas de Apuestas
- **Gráfico de Barras**: Precisión por casa
- **Mapa de Calor**: Precisión por casa × liga
- **Línea de Tiempo**: Evolución de precisión por temporada

#### Dashboard 2: Análisis de Estrategias
- **Gráfico de Líneas**: ROI por estrategia a lo largo del tiempo
- **Gráfico de Dispersión**: Rentabilidad vs Riesgo
- **Tabla Ranking**: Top estrategias por liga

#### Dashboard 3: Análisis de Arbitraje
- **Gráfico de Barras**: Oportunidades por liga
- **Histograma**: Distribución de beneficios
- **Timeline**: Frecuencia temporal de oportunidades

---

## 12. PRÓXIMOS PASOS

### Paso 4: Integración de Datos (ETL)

En esta etapa se realizó la integración de los datos del dataset “European Soccer Database” (Kaggle), siguiendo la metodología HEFESTO.
El objetivo fue centralizar la información en un repositorio unificado (Data Warehouse) para su posterior análisis en Power BI o herramientas equivalentes.

## 4.1 Fuente de datos

Archivo original: database.sqlite (formato SQLite)
Contiene tablas: Country, League, Team, Match
Total de registros procesados: 25.979 partidos (tabla Match)

## 4.2 Proceso de extracción

Se utilizaron herramientas de línea de comandos de SQLite y un script en Bash (export_sqlite_to_csv.sh) para exportar cada tabla del archivo .sqlite a archivos .csv.
Esto permitió transformar la base relacional de origen en un formato plano, apto para su importación a MySQL.

## 4.3 Proceso de carga (staging)

Se creó un entorno MySQL denominado apuestas_dw.
En él se definieron las tablas de staging:

stg_country
stg_league
stg_team
stg_match

Los archivos .csv se cargaron mediante el comando LOAD DATA LOCAL INFILE, consolidando la información cruda en el área de staging.

## 4.4 Transformación y creación de dimensiones/hechos

Se implementó un proceso ETL en Python (etl_apuestas.py) utilizando la librería pandas y el conector mysql-connector-python.
El proceso realiza las siguientes tareas:

Limpieza y validación de datos.
Creación de nuevos campos derivados (resultado, año, mes).
Inserción en las tablas dimensionales y de hechos:
dim_fecha
dim_casa_apuestas
fact_apuestas

## 4.5 Carga en el Data Warehouse

Los datos transformados se cargaron exitosamente en MySQL, cumpliendo las integridades referenciales establecidas.
El proceso se validó con 25.979 filas insertadas en fact_apuestas.

## 4.6 Conexión con herramientas de análisis

Con la base apuestas_dw disponible, el entorno quedó listo para su conexión con herramientas de BI:
En Windows, Power BI Desktop se conecta mediante el conector nativo de MySQL (localhost, usuario root, base apuestas_dw).

## 4.7 Resultado final

El entorno de datos resultante permite realizar análisis como:
Promedio de goles por liga y temporada.
Distribución de resultados (local/empate/visitante).
Evaluación de cuotas de apuestas y rendimientos esperados.

Con esto se completó el Paso 4 – Integración de Datos de la metodología HEFESTO, dejando los datos preparados para el Paso 5 – Visualización y Análisis.

#### 12.1. Diseño ETL
```
┌─────────────────────────────────────────────┐
│         PROCESO ETL PLANIFICADO              │
├─────────────────────────────────────────────┤
│                                              │
│  1. EXTRACT                                  │
│     ├─ Conexión a database.sqlite            │
│     └─ Lectura de tablas Match, League, Team│
│                                              │
│  2. TRANSFORM                                │
│     ├─ Filtrado de calidad (NULLs)          │
│     ├─ UNPIVOT de cuotas                    │
│     ├─ Cálculo de estrategias               │
│     ├─ Derivación de dimensiones            │
│     └─ Generación de claves subrogadas      │
│                                              │
│  3. LOAD                                     │
│     ├─ Carga de dimensiones (orden)         │
│     ├─ Carga FACT_APUESTAS                  │
│     └─ Carga FACT_ARBITRAJE                 │
│                                              │
│  4. VALIDATE                                 │
│     ├─ Validar conteos                      │
│     ├─ Validar integridad referencial       │
│     └─ Validar cálculos de métricas         │
│                                              │
└─────────────────────────────────────────────┘
```

#### 12.2. Herramientas Sugeridas
- **Python + Pandas**: Para transformaciones UNPIVOT
- **SQL Scripts**: Para carga de dimensiones
- **dbt (data build tool)**: Para orquestación ETL
- **Airflow**: Para automatización periódica

#### 12.3. Implementación Física
- **Motor de BD**: PostgreSQL o SQL Server
- **Índices**: En FKs y campos de filtro frecuente
- **Particionamiento**: Por temporada en tablas de hechos
- **Agregaciones**: Tablas precalculadas para consultas frecuentes

#### 12.4. BI y Visualización
- **Power BI** o **Tableau**: Para dashboards interactivos
- **Jupyter Notebooks**: Para análisis exploratorio
- **API REST**: Para integración con aplicaciones

---

## ANEXOS

### A. Glosario de Términos

| Término | Significado Simple | Ejemplo |
|---------|-------------------|---------|
| **Data Warehouse** | Almacén de datos históricos para análisis | "Base de datos de análisis" |
| **OLTP** | Base de datos operacional | "Base de datos original" |
| **OLAP** | Sistema de análisis multidimensional | "Sistema de consultas complejas" |
| **Dimensión** | Perspectiva de análisis | "¿Por qué casa? ¿En qué liga?" |
| **Tabla de Hechos** | Tabla con métricas numéricas | "Tabla con ganancias, pérdidas" |
| **Granularidad** | Nivel de detalle de cada registro | "1 fila = 1 apuesta específica" |
| **SCD** | Dimensión que cambia lentamente | "Equipos que cambian de liga" |
| **ETL** | Extracción, Transformación, Carga | "Proceso de llenar el DW" |
| **ROI** | Retorno de inversión | "¿Cuánto gané vs invertí?" |
| **Arbitraje** | Ganancia garantizada | "Ganar sin importar resultado" |
| **UNPIVOT** | Convertir columnas en filas | "30 columnas → 10 filas" |

### B. Archivos del Proyecto

```
BD2_Hefesto_ApuetasDeportivas/
│
├── database.sqlite                      # Base de datos fuente
│
├── Paso1/                               # Análisis de Requerimientos
│   ├── README.md                        # 3 preguntas, 9 indicadores, 6 perspectivas
│   └── modelo_conceptual_hefesto.md     # 7 diagramas Mermaid
│
├── Paso2/                               # Análisis OLTP
│   ├── paso2_analisis_oltp.md          # Mapeo completo OLTP→DW
│   └── modelo_conceptual_ampliado.png   # Diagrama con campos físicos
│
├── Paso3/                               # Modelo Lógico
│   ├── paso3_modelo_logico.md          # Diseño completo (76 páginas)
│   ├── diagrama_3a_*.md                # 6 diagramas esquema constelación
│   ├── diagrama_3b_*.md                # 17 diagramas dimensiones
│   ├── diagrama_3c_*.md                # 19 diagramas tablas hechos
│   ├── diagrama_3d_*.md                # 13 diagramas relaciones
│   ├── diagramas_png/                  # 55 diagramas en PNG alta calidad
│   └── README_DIAGRAMAS.md             # Guía de visualización
│
└── DOCUMENTACION_PROYECTO_PRESENTACION.md  # Este documento
```

### C. Referencias

#### Metodología HEFESTO
- **Fuente**: hefesto-v2-97-128[1].pdf
- **Autor**: Metodología para diseño de Data Warehouses
- **Pasos Implementados**: 1, 2, 3 de 4

#### Conceptos Técnicos
- **Data Warehousing**: Ralph Kimball - The Data Warehouse Toolkit
- **Dimensional Modeling**: Star Schema vs Snowflake vs Constellation
- **ETL Best Practices**: Slowly Changing Dimensions, Surrogate Keys

#### Dominio de Negocio
- **Apuestas Deportivas**: Análisis de mercado, arbitraje, estrategias
- **Métricas Financieras**: ROI, precisión predictiva, oportunidades

---

## CONCLUSIONES

### Lo que Hemos Logrado

✅ **Análisis Completo del Negocio**
- 3 preguntas estratégicas identificadas
- 9 indicadores clave definidos
- 6 perspectivas de análisis establecidas

✅ **Mapeo Detallado de Datos**
- Correspondencias OLTP→DW documentadas
- Transformaciones UNPIVOT diseñadas
- Cálculos de métricas especificados

✅ **Modelo Lógico Robusto**
- Esquema constelación con 2 tablas de hechos
- 6 dimensiones con SCD Tipo 2 en equipos
- 55 diagramas de alta calidad generados
- Optimización 40x en consultas de arbitraje

### Valor del Proyecto

💡 **Para el Negocio**
- Sistema de análisis basado en 22,592 partidos históricos
- Identificación de patrones y oportunidades de mercado
- Base para decisiones informadas en apuestas deportivas

💡 **Técnicamente**
- Implementación completa de metodología HEFESTO
- Solución elegante a desafíos complejos (UNPIVOT, SCD, constelación)
- Modelo escalable y optimizado para performance

### Lo que Falta

🔄 **Paso 4: Implementación**
- Desarrollo de procesos ETL
- Implementación física en motor de BD
- Carga inicial de 903K+ registros
- Creación de dashboards y reportes

---

## 📞 CONTACTO Y SOPORTE

**Proyecto**: Data Warehouse Apuestas Deportivas
**Metodología**: HEFESTO v2.0
**Estado**: Pasos 1-3 Completados
**Próximo Hito**: Implementación ETL (Paso 4)

---

**Documento Generado**: Octubre 2025
**Versión**: 1.0 - Presentación General
**Audiencia**: Stakeholders técnicos y de negocio

---

*Este documento proporciona una visión completa y comprensible del proyecto, desde conceptos básicos hasta detalles técnicos avanzados. Diseñado para ser leído por personas con diferentes niveles de conocimiento técnico.*

