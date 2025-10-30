# 3c) DIAGRAMAS: Tablas de Hechos

## Vista General de Tablas de Hechos

```mermaid
graph TB
    subgraph "FACT_APUESTAS - Detalle de Apuestas"
        FA[FACT_APUESTAS<br/>~903,680 registros<br/><br/>Granularidad:<br/>1 partido × 1 casa × 1 estrategia × 1 resultado<br/><br/>Métricas:<br/>- ganancia_total<br/>- perdida_total<br/>- inversion<br/>- cant_aciertos<br/>- cant_apuestas]
    end

    subgraph "FACT_ARBITRAJE - Análisis Agregado"
        FAR[FACT_ARBITRAJE<br/>~22,592 registros<br/><br/>Granularidad:<br/>1 partido completo<br/>(análisis cross-casa)<br/><br/>Métricas:<br/>- cant_oportunidades<br/>- beneficio_arbitraje<br/>- porcentaje_arbitraje<br/>- es_oportunidad]
    end

    FA -.->|Agregación| FAR

    style FA fill:#ff9999,stroke:#333,stroke-width:3px
    style FAR fill:#99ccff,stroke:#333,stroke-width:3px
```

### Comparación de Tablas

| Aspecto | FACT_APUESTAS | FACT_ARBITRAJE |
|---------|---------------|----------------|
| **Registros** | ~903,680 | ~22,592 |
| **Granularidad** | Apuesta individual | Partido completo |
| **Dimensiones FK** | 7 dimensiones | 4 dimensiones + 3 casas |
| **Métricas** | 12 campos | 9 campos |
| **Propósito** | Análisis detallado apuestas | Detección oportunidades |
| **Performance** | Consultas específicas | 40x más rápido |

---

## 1. FACT_APUESTAS - Tabla de Hechos de Apuestas Detalladas

### Estructura Completa

```mermaid
erDiagram
    FACT_APUESTAS {
        INTEGER id_fecha FK "→ DIM_FECHA"
        INTEGER id_equipo_local FK "→ DIM_EQUIPO (local)"
        INTEGER id_equipo_visitante FK "→ DIM_EQUIPO (visit)"
        INTEGER id_liga FK "→ DIM_LIGA"
        INTEGER id_casa_apuestas FK "→ DIM_CASA_APUESTAS"
        INTEGER id_estrategia FK "→ DIM_ESTRATEGIA"
        INTEGER id_resultado_tipo FK "→ DIM_RESULTADO_TIPO"
        INTEGER id_partido "Identificador partido OLTP"
        DECIMAL ganancia_total "Métrica aditiva"
        DECIMAL perdida_total "Métrica aditiva"
        DECIMAL inversion "Métrica aditiva"
        TINYINT cant_aciertos "Métrica aditiva"
        TINYINT cant_apuestas "Métrica aditiva"
        DECIMAL cuota_apostada "Métrica no-aditiva"
        CHAR resultado_real "H, D, A"
        BOOLEAN apuesta_acertada "TRUE/FALSE"
        DECIMAL roi_porcentaje "Métrica calculada"
        DECIMAL precision_porcentaje "Métrica calculada"
    }
```

### Clave Primaria Compuesta

```mermaid
graph LR
    PK[Clave Primaria<br/>6 columnas] --> F[id_fecha]
    PK --> EL[id_equipo_local]
    PK --> EV[id_equipo_visitante]
    PK --> CA[id_casa_apuestas]
    PK --> ES[id_estrategia]
    PK --> RT[id_resultado_tipo]

    F & EL & EV & CA & ES & RT --> UN[Combinación ÚNICA<br/>identifica 1 apuesta específica]

    style PK fill:#ff9999,stroke:#333,stroke-width:3px
    style UN fill:#ccffcc,stroke:#333,stroke-width:2px
```

### Clasificación de Métricas

```mermaid
graph TB
    subgraph "MÉTRICAS ADITIVAS ✅"
        A1[ganancia_total<br/>SUM() válido en todas dimensiones]
        A2[perdida_total<br/>SUM() válido en todas dimensiones]
        A3[inversion<br/>SUM() válido en todas dimensiones]
        A4[cant_aciertos<br/>SUM() válido en todas dimensiones]
        A5[cant_apuestas<br/>SUM() válido en todas dimensiones]
    end

    subgraph "MÉTRICAS NO-ADITIVAS ⚠️"
        NA1[cuota_apostada<br/>Requiere AVG() o ponderación]
        NA2[roi_porcentaje<br/>Requiere cálculo derivado]
        NA3[precision_porcentaje<br/>Requiere cálculo derivado]
    end

    A1 & A2 & A3 & A4 & A5 --> SUM[Se pueden sumar<br/>directamente]
    NA1 & NA2 & NA3 --> CALC[Requieren<br/>cálculo especial]

    style A1 fill:#ccffcc,stroke:#333,stroke-width:2px
    style A2 fill:#ccffcc,stroke:#333,stroke-width:2px
    style A3 fill:#ccffcc,stroke:#333,stroke-width:2px
    style A4 fill:#ccffcc,stroke:#333,stroke-width:2px
    style A5 fill:#ccffcc,stroke:#333,stroke-width:2px
    style NA1 fill:#ffeb99,stroke:#333,stroke-width:2px
    style NA2 fill:#ffeb99,stroke:#333,stroke-width:2px
    style NA3 fill:#ffeb99,stroke:#333,stroke-width:2px
```

### Granularidad y Cardinalidad

```mermaid
graph TB
    P[22,592 Partidos OLTP] -->|× 10 casas| C[225,920 combinaciones]
    C -->|× 4 estrategias| E[903,680 registros base]

    E --> D1[Dimensión FECHA<br/>~2,920 valores<br/>= 309 registros/día promedio]
    E --> D2[Dimensión LIGA<br/>11 valores<br/>= 82,153 registros/liga promedio]
    E --> D3[Dimensión CASA<br/>10 valores<br/>= 90,368 registros/casa]
    E --> D4[Dimensión ESTRATEGIA<br/>4 valores<br/>= 225,920 registros/estrategia]

    style P fill:#ffcccc,stroke:#333,stroke-width:2px
    style E fill:#ff9999,stroke:#333,stroke-width:3px
```

### Relaciones con Dimensiones

```mermaid
graph TB
    FA[FACT_APUESTAS<br/>903,680 registros]

    DF[DIM_FECHA<br/>~2,920 registros]
    DL[DIM_LIGA<br/>11 registros]
    DEL[DIM_EQUIPO<br/>~400 registros<br/>Rol: LOCAL]
    DEV[DIM_EQUIPO<br/>~400 registros<br/>Rol: VISITANTE]
    DCA[DIM_CASA_APUESTAS<br/>10 registros]
    DES[DIM_ESTRATEGIA<br/>4 registros]
    DRT[DIM_RESULTADO_TIPO<br/>3 registros]

    DF -->|1:N<br/>~310 hechos/fecha| FA
    DL -->|1:N<br/>~82K hechos/liga| FA
    DEL -->|1:N<br/>~2.3K hechos/equipo| FA
    DEV -->|1:N<br/>~2.3K hechos/equipo| FA
    DCA -->|1:N<br/>~90K hechos/casa| FA
    DES -->|1:N<br/>~226K hechos/estrategia| FA
    DRT -->|1:N<br/>~301K hechos/resultado| FA

    style FA fill:#ff9999,stroke:#333,stroke-width:3px
    style DF fill:#ffeb99,stroke:#333,stroke-width:2px
    style DL fill:#ffeb99,stroke:#333,stroke-width:2px
    style DEL fill:#ffeb99,stroke:#333,stroke-width:2px
    style DEV fill:#ffeb99,stroke:#333,stroke-width:2px
    style DCA fill:#ccffcc,stroke:#333,stroke-width:2px
    style DES fill:#ccffcc,stroke:#333,stroke-width:2px
    style DRT fill:#ccffcc,stroke:#333,stroke-width:2px
```

### Ejemplo de Registros

| id_fecha | id_equipo_local | id_equipo_visitante | id_casa | id_estrategia | id_resultado | ganancia | perdida | inversion | acertada |
|----------|-----------------|---------------------|---------|---------------|--------------|----------|---------|-----------|----------|
| 20080815 | 112 (Man Utd) | 87 (Newcastle) | 1 (B365) | 1 (ALWAYS_H) | 1 (H) | 1.75 | 0.00 | 1.00 | TRUE |
| 20080815 | 112 (Man Utd) | 87 (Newcastle) | 1 (B365) | 2 (ALWAYS_A) | 3 (A) | 0.00 | 1.00 | 1.00 | FALSE |
| 20080815 | 112 (Man Utd) | 87 (Newcastle) | 2 (BW) | 3 (FOLLOW_FAV) | 1 (H) | 1.80 | 0.00 | 1.00 | TRUE |

### Uso en Indicadores

```mermaid
graph LR
    FA[FACT_APUESTAS]

    FA --> I1[Indicador 1:<br/>% Precisión<br/>= cant_aciertos / cant_apuestas]

    FA --> I2[Indicador 2:<br/>ROI %<br/>= ganancia-perdida / inversion × 100]

    FA --> I3[Indicador 3:<br/>Precisión por Casa<br/>GROUP BY casa]

    FA --> I4[Indicador 4:<br/>ROI por Estrategia<br/>GROUP BY estrategia]

    FA --> I5[Indicador 5:<br/>Mejor Estrategia Liga<br/>GROUP BY liga, estrategia]

    style FA fill:#ff9999,stroke:#333,stroke-width:3px
    style I1 fill:#e1f5ff,stroke:#333,stroke-width:2px
    style I2 fill:#e1f5ff,stroke:#333,stroke-width:2px
    style I3 fill:#e1f5ff,stroke:#333,stroke-width:2px
    style I4 fill:#e1f5ff,stroke:#333,stroke-width:2px
    style I5 fill:#e1f5ff,stroke:#333,stroke-width:2px
```

---

## 2. FACT_ARBITRAJE - Tabla de Hechos de Oportunidades de Arbitraje

### Estructura Completa

```mermaid
erDiagram
    FACT_ARBITRAJE {
        INTEGER id_fecha FK "→ DIM_FECHA"
        INTEGER id_equipo_local FK "→ DIM_EQUIPO (local)"
        INTEGER id_equipo_visitante FK "→ DIM_EQUIPO (visit)"
        INTEGER id_liga FK "→ DIM_LIGA"
        INTEGER id_partido "Identificador partido OLTP"
        INTEGER casa_local_mejor FK "→ DIM_CASA mejor cuota H"
        INTEGER casa_empate_mejor FK "→ DIM_CASA mejor cuota D"
        INTEGER casa_visitante_mejor FK "→ DIM_CASA mejor cuota A"
        DECIMAL cuota_local_max "Mejor cuota H"
        DECIMAL cuota_empate_max "Mejor cuota D"
        DECIMAL cuota_visitante_max "Mejor cuota A"
        INTEGER cant_oportunidades "Métrica aditiva"
        DECIMAL beneficio_arbitraje "Ganancia potencial"
        DECIMAL porcentaje_arbitraje "% de beneficio"
        BOOLEAN es_oportunidad "TRUE si arbitraje posible"
    }
```

### Clave Primaria Compuesta

```mermaid
graph LR
    PK[Clave Primaria<br/>4 columnas] --> F[id_fecha]
    PK --> EL[id_equipo_local]
    PK --> EV[id_equipo_visitante]
    PK --> L[id_liga]

    F & EL & EV & L --> UN[Combinación ÚNICA<br/>identifica 1 partido específico]

    style PK fill:#99ccff,stroke:#333,stroke-width:3px
    style UN fill:#ccffcc,stroke:#333,stroke-width:2px
```

### Lógica de Arbitraje

```mermaid
graph TB
    P[Partido con 10 casas] --> E1[Encontrar MAX cuota_local<br/>entre todas las casas]
    P --> E2[Encontrar MAX cuota_empate<br/>entre todas las casas]
    P --> E3[Encontrar MAX cuota_visitante<br/>entre todas las casas]

    E1 & E2 & E3 --> C[Calcular suma inversa:<br/>S = 1/cuota_local + 1/cuota_empate + 1/cuota_visitante]

    C --> D{S < 1.0?}

    D -->|SÍ| O1[es_oportunidad = TRUE<br/>Arbitraje posible<br/>beneficio = 1/S - 1]
    D -->|NO| O2[es_oportunidad = FALSE<br/>No hay arbitraje<br/>beneficio = 0]

    style P fill:#ffcccc,stroke:#333,stroke-width:2px
    style C fill:#ffffcc,stroke:#333,stroke-width:2px
    style O1 fill:#ccffcc,stroke:#333,stroke-width:3px
    style O2 fill:#ffcccc,stroke:#333,stroke-width:2px
```

### Cardinalidad Reducida

```mermaid
graph TB
    P[22,592 Partidos OLTP] -->|Agregación<br/>Cross-Casa| ARB[22,592 registros<br/>FACT_ARBITRAJE]

    ARB --> COMP[Comparación con FACT_APUESTAS:<br/>903,680 registros<br/>÷ 22,592 registros<br/>= 40x menos registros]

    COMP --> PERF[Performance:<br/>Consultas arbitraje 40x más rápidas<br/>Índices más pequeños<br/>Mejor cache hit ratio]

    style P fill:#ffcccc,stroke:#333,stroke-width:2px
    style ARB fill:#99ccff,stroke:#333,stroke-width:3px
    style PERF fill:#ccffcc,stroke:#333,stroke-width:2px
```

### Relaciones con Dimensiones

```mermaid
graph TB
    FAR[FACT_ARBITRAJE<br/>22,592 registros]

    DF[DIM_FECHA<br/>~2,920 registros]
    DL[DIM_LIGA<br/>11 registros]
    DEL[DIM_EQUIPO<br/>~400 registros<br/>Rol: LOCAL]
    DEV[DIM_EQUIPO<br/>~400 registros<br/>Rol: VISITANTE]
    DCA[DIM_CASA_APUESTAS<br/>10 registros]

    DF -->|1:N<br/>~8 hechos/fecha| FAR
    DL -->|1:N<br/>~2,054 hechos/liga| FAR
    DEL -->|1:N<br/>~57 hechos/equipo| FAR
    DEV -->|1:N<br/>~57 hechos/equipo| FAR
    DCA -.->|FK adicionales<br/>3 casas mejores| FAR

    style FAR fill:#99ccff,stroke:#333,stroke-width:3px
    style DF fill:#ffeb99,stroke:#333,stroke-width:2px
    style DL fill:#ffeb99,stroke:#333,stroke-width:2px
    style DEL fill:#ffeb99,stroke:#333,stroke-width:2px
    style DEV fill:#ffeb99,stroke:#333,stroke-width:2px
    style DCA fill:#ccffcc,stroke:#333,stroke-width:2px
```

### Ejemplo de Registros

| id_fecha | id_equipo_local | id_equipo_visitante | casa_H_mejor | casa_D_mejor | casa_A_mejor | cuota_H | cuota_D | cuota_A | es_oportunidad | beneficio |
|----------|-----------------|---------------------|--------------|--------------|--------------|---------|---------|---------|----------------|-----------|
| 20080815 | 112 (Man Utd) | 87 (Newcastle) | 4 (PS) | 2 (BW) | 1 (B365) | 1.85 | 3.75 | 5.50 | FALSE | 0.00 |
| 20081025 | 45 (Arsenal) | 78 (Tottenham) | 1 (B365) | 3 (IW) | 4 (PS) | 2.10 | 3.40 | 4.20 | TRUE | 2.35% |

### Uso en Indicadores

```mermaid
graph LR
    FAR[FACT_ARBITRAJE]

    FAR --> I6[Indicador 6:<br/>Oportunidades Arbitraje<br/>COUNT WHERE es_oportunidad]

    FAR --> I7[Indicador 7:<br/>Beneficio Promedio<br/>AVG beneficio_arbitraje]

    FAR --> I8[Indicador 8:<br/>Casa con Mejores Cuotas<br/>COUNT casa_mejor]

    FAR --> I9[Indicador 9:<br/>Frecuencia por Liga<br/>GROUP BY liga]

    style FAR fill:#99ccff,stroke:#333,stroke-width:3px
    style I6 fill:#e1f5ff,stroke:#333,stroke-width:2px
    style I7 fill:#e1f5ff,stroke:#333,stroke-width:2px
    style I8 fill:#e1f5ff,stroke:#333,stroke-width:2px
    style I9 fill:#e1f5ff,stroke:#333,stroke-width:2px
```

---

## Comparación Detallada de Tablas de Hechos

### Dimensiones Relacionadas

```mermaid
graph TB
    subgraph "FACT_APUESTAS"
        FA_DIM[7 Dimensiones FK:<br/>- DIM_FECHA<br/>- DIM_LIGA<br/>- DIM_EQUIPO local<br/>- DIM_EQUIPO visitante<br/>- DIM_CASA_APUESTAS<br/>- DIM_ESTRATEGIA<br/>- DIM_RESULTADO_TIPO]
    end

    subgraph "FACT_ARBITRAJE"
        FAR_DIM[4 Dimensiones FK base:<br/>- DIM_FECHA<br/>- DIM_LIGA<br/>- DIM_EQUIPO local<br/>- DIM_EQUIPO visitante<br/><br/>+ 3 FK adicionales:<br/>- casa_local_mejor<br/>- casa_empate_mejor<br/>- casa_visitante_mejor]
    end

    CONF[Dimensiones Conformadas<br/>compartidas entre ambas:<br/>DIM_FECHA, DIM_LIGA, DIM_EQUIPO]

    FA_DIM -.-> CONF
    FAR_DIM -.-> CONF

    style FA_DIM fill:#ff9999,stroke:#333,stroke-width:2px
    style FAR_DIM fill:#99ccff,stroke:#333,stroke-width:2px
    style CONF fill:#ffeb99,stroke:#333,stroke-width:3px
```

### Granularidad Comparada

```mermaid
graph TB
    subgraph "FACT_APUESTAS - Granularidad FINA"
        FA_G[Nivel: Apuesta Individual<br/><br/>1 registro =<br/>1 partido ×<br/>1 casa de apuestas ×<br/>1 estrategia ×<br/>1 tipo resultado<br/><br/>Permite análisis:<br/>- Por estrategia específica<br/>- Por casa individual<br/>- Por tipo resultado]
    end

    subgraph "FACT_ARBITRAJE - Granularidad GRUESA"
        FAR_G[Nivel: Partido Completo<br/><br/>1 registro =<br/>1 partido<br/>(análisis cross-casa)<br/><br/>Permite análisis:<br/>- Oportunidades arbitraje<br/>- Mejores cuotas mercado<br/>- Comparación casas]
    end

    style FA_G fill:#ff9999,stroke:#333,stroke-width:2px
    style FAR_G fill:#99ccff,stroke:#333,stroke-width:2px
```

### Métricas y Tipos

```mermaid
graph TB
    subgraph "FACT_APUESTAS - Métricas Financieras"
        FA_M[Aditivas:<br/>- ganancia_total<br/>- perdida_total<br/>- inversion<br/>- cant_aciertos<br/>- cant_apuestas<br/><br/>No-Aditivas:<br/>- cuota_apostada<br/>- roi_porcentaje<br/>- precision_porcentaje]
    end

    subgraph "FACT_ARBITRAJE - Métricas Analíticas"
        FAR_M[Aditivas:<br/>- cant_oportunidades<br/><br/>Semi-Aditivas:<br/>- beneficio_arbitraje<br/>- porcentaje_arbitraje<br/><br/>Booleanas:<br/>- es_oportunidad<br/><br/>Descriptivas:<br/>- cuota_local_max<br/>- cuota_empate_max<br/>- cuota_visitante_max]
    end

    style FA_M fill:#ff9999,stroke:#333,stroke-width:2px
    style FAR_M fill:#99ccff,stroke:#333,stroke-width:2px
```

### Ventaja de Performance

```mermaid
graph LR
    Q[Consulta: Oportunidades de arbitraje<br/>por liga y temporada]

    Q -->|Opción 1| FA_PATH[Usar FACT_APUESTAS:<br/>1. Leer 903,680 registros<br/>2. Agrupar por partido<br/>3. Calcular máximos<br/>4. Detectar arbitraje<br/><br/>⏱️ Tiempo: 100ms]

    Q -->|Opción 2| FAR_PATH[Usar FACT_ARBITRAJE:<br/>1. Leer 22,592 registros<br/>2. Filtrar es_oportunidad=TRUE<br/>3. Agrupar por liga<br/><br/>⏱️ Tiempo: 2.5ms]

    FA_PATH --> COMP[Comparación:<br/>40x menos registros<br/>40x más rápido<br/>Índices más pequeños<br/>Mejor cache]

    FAR_PATH --> COMP

    style FA_PATH fill:#ffcccc,stroke:#333,stroke-width:2px
    style FAR_PATH fill:#ccffcc,stroke:#333,stroke-width:3px
    style COMP fill:#e1f5ff,stroke:#333,stroke-width:2px
```

---

## Matriz de Indicadores vs Tablas de Hechos

```mermaid
graph TB
    subgraph "INDICADORES FACT_APUESTAS"
        I1[I1: % Precisión Casa<br/>✅ Directa]
        I2[I2: ROI por Estrategia<br/>✅ Directa]
        I3[I3: Precisión Temporal<br/>✅ Directa]
        I4[I4: Ganancia/Pérdida Liga<br/>✅ Directa]
        I5[I5: Mejor Estrategia<br/>✅ Directa]
    end

    subgraph "INDICADORES FACT_ARBITRAJE"
        I6[I6: Oportunidades Arbitraje<br/>✅ Directa]
        I7[I7: Beneficio Arbitraje<br/>✅ Directa]
        I8[I8: Casa Mejores Cuotas<br/>✅ Directa]
        I9[I9: Frecuencia Arbitraje<br/>✅ Directa]
    end

    subgraph "INDICADORES DRILL-ACROSS"
        I10[Comparación:<br/>ROI vs Oportunidades<br/>🔄 Usa ambas tablas]
    end

    style I1 fill:#ff9999,stroke:#333,stroke-width:2px
    style I2 fill:#ff9999,stroke:#333,stroke-width:2px
    style I3 fill:#ff9999,stroke:#333,stroke-width:2px
    style I4 fill:#ff9999,stroke:#333,stroke-width:2px
    style I5 fill:#ff9999,stroke:#333,stroke-width:2px
    style I6 fill:#99ccff,stroke:#333,stroke-width:2px
    style I7 fill:#99ccff,stroke:#333,stroke-width:2px
    style I8 fill:#99ccff,stroke:#333,stroke-width:2px
    style I9 fill:#99ccff,stroke:#333,stroke-width:2px
    style I10 fill:#ffeb99,stroke:#333,stroke-width:3px
```

### Tabla de Uso de Indicadores

| Indicador | Tabla Principal | Métrica Usada | Complejidad Query |
|-----------|----------------|---------------|-------------------|
| I1: % Precisión Casa | FACT_APUESTAS | cant_aciertos / cant_apuestas | Baja |
| I2: ROI Estrategia | FACT_APUESTAS | (ganancia - perdida) / inversion | Baja |
| I3: Precisión Temporal | FACT_APUESTAS | cant_aciertos / cant_apuestas + DIM_FECHA | Media |
| I4: Ganancia/Pérdida Liga | FACT_APUESTAS | SUM(ganancia - perdida) + DIM_LIGA | Baja |
| I5: Mejor Estrategia | FACT_APUESTAS | MAX(ROI) GROUP BY estrategia | Media |
| I6: Oportunidades Arbitraje | FACT_ARBITRAJE | COUNT WHERE es_oportunidad | Baja |
| I7: Beneficio Arbitraje | FACT_ARBITRAJE | AVG(beneficio_arbitraje) | Baja |
| I8: Casa Mejores Cuotas | FACT_ARBITRAJE | COUNT(casa_mejor) | Baja |
| I9: Frecuencia por Liga | FACT_ARBITRAJE | COUNT + DIM_LIGA | Baja |

---

## Resumen de Diseño de Tablas de Hechos

### Decisión Arquitectónica: Dos Tablas vs Una

```mermaid
graph TB
    D[Decisión de Diseño]

    D --> O1[Opción 1: Tabla Única<br/>FACT_APUESTAS_TODO<br/><br/>❌ Desventajas:<br/>- 903K registros siempre<br/>- Campos NULL para arbitraje<br/>- Consultas lentas arbitraje<br/>- Índices grandes]

    D --> O2[Opción 2: Dos Tablas ✅<br/>FACT_APUESTAS + FACT_ARBITRAJE<br/><br/>✅ Ventajas:<br/>- Separación conceptual clara<br/>- Performance 40x mejor arbitraje<br/>- Sin campos NULL<br/>- Índices optimizados<br/>- Dimensiones conformadas]

    style O1 fill:#ffcccc,stroke:#333,stroke-width:2px
    style O2 fill:#ccffcc,stroke:#333,stroke-width:3px
```

### Métricas de Decisión

| Métrica | Tabla Única | Dos Tablas (Constelación) |
|---------|-------------|---------------------------|
| **Registros totales** | ~903,680 | 903,680 + 22,592 = 926,272 |
| **Almacenamiento** | ~180 MB | ~185 MB (+2.7%) |
| **Campos NULL** | ~25% valores NULL | 0% valores NULL |
| **Performance arbitraje** | 100 ms | 2.5 ms (40x mejor) |
| **Índices** | 7 índices grandes | 7 + 4 índices especializados |
| **Complejidad consultas** | Media-Alta | Baja |
| **Mantenibilidad** | Media | Alta |

---

**Diagrama 3c - Tablas de Hechos Completo** ✅
