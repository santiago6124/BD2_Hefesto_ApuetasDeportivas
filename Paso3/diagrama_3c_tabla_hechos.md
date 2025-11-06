# 3c) DIAGRAMA: Tabla de Hechos Única (Esquema Estrella)

## FACT_APUESTAS - Tabla de Hechos Consolidada

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
        DECIMAL ganancia_total "Hecho aditivo"
        DECIMAL perdida_total "Hecho aditivo"
        DECIMAL inversion "Hecho aditivo"
        TINYINT cant_aciertos "Hecho aditivo"
        TINYINT cant_apuestas "Hecho aditivo"
        DECIMAL cuota_apostada "Hecho semi-aditivo"
        DECIMAL cuota_local "Hecho semi-aditivo"
        DECIMAL cuota_empate "Hecho semi-aditivo"
        DECIMAL cuota_visitante "Hecho semi-aditivo"
        CHAR resultado_real "H, D, A"
        BOOLEAN acierto "TRUE/FALSE"
        DECIMAL arbitraje_cuota_local_max "Derivado"
        DECIMAL arbitraje_cuota_empate_max "Derivado"
        DECIMAL arbitraje_cuota_visitante_max "Derivado"
        INTEGER arbitraje_casa_local_mejor FK "→ DIM_CASA"
        INTEGER arbitraje_casa_empate_mejor FK "→ DIM_CASA"
        INTEGER arbitraje_casa_visitante_mejor FK "→ DIM_CASA"
        DECIMAL arbitraje_porcentaje "Derivado"
        BOOLEAN arbitraje_es_oportunidad "Derivado"
        DECIMAL arbitraje_beneficio "Derivado"
    }
```

### Clave Primaria Compuesta

```mermaid
graph TB
    PK["<b>Clave Primaria Compuesta</b><br/>7 columnas"] --> F[id_fecha]
    PK --> EL[id_equipo_local]
    PK --> EV[id_equipo_visitante]
    PK --> CA[id_casa_apuestas]
    PK --> ES[id_estrategia]
    PK --> RT[id_resultado_tipo]
    PK --> LI[id_liga]

    F & EL & EV & CA & ES & RT & LI --> UN["✅ Combinación ÚNICA<br/>identifica 1 apuesta específica<br/>de 1 casa en 1 partido<br/>con 1 estrategia"]

    style PK fill:#ff9999,stroke:#333,stroke-width:3px
    style UN fill:#ccffcc,stroke:#333,stroke-width:2px
```

### Clasificación de Campos

```mermaid
graph TB
    subgraph "HECHOS ADITIVOS ✅ (SUM válido)"
        A1[ganancia_total<br/>Suma de ganancias]
        A2[perdida_total<br/>Suma de pérdidas]
        A3[inversion<br/>Suma de inversiones]
        A4[cant_aciertos<br/>Suma de aciertos]
        A5[cant_apuestas<br/>Suma de apuestas]
    end

    subgraph "HECHOS SEMI-ADITIVOS ⚠️ (AVG/MAX/MIN)"
        SA1[cuota_apostada<br/>Requiere AVG]
        SA2[cuota_local<br/>Requiere AVG]
        SA3[cuota_empate<br/>Requiere AVG]
        SA4[cuota_visitante<br/>Requiere AVG]
    end

    subgraph "CAMPOS DERIVADOS 📊 (Pre-calculados en ETL)"
        D1[arbitraje_cuota_*_max<br/>Mejor cuota del mercado]
        D2[arbitraje_casa_*_mejor<br/>Casa con mejor cuota]
        D3[arbitraje_porcentaje<br/>1/max_H + 1/max_D + 1/max_A]
        D4[arbitraje_es_oportunidad<br/>TRUE si porcentaje < 1.0]
        D5[arbitraje_beneficio<br/>% ganancia garantizada]
    end

    subgraph "METADATOS 📝"
        M1[resultado_real<br/>H, D, A]
        M2[acierto<br/>TRUE/FALSE]
        M3[id_partido<br/>Surrogate key OLTP]
    end

    style A1 fill:#ccffcc,stroke:#333,stroke-width:2px
    style A2 fill:#ccffcc,stroke:#333,stroke-width:2px
    style A3 fill:#ccffcc,stroke:#333,stroke-width:2px
    style A4 fill:#ccffcc,stroke:#333,stroke-width:2px
    style A5 fill:#ccffcc,stroke:#333,stroke-width:2px
    style SA1 fill:#ffeb99,stroke:#333,stroke-width:2px
    style SA2 fill:#ffeb99,stroke:#333,stroke-width:2px
    style SA3 fill:#ffeb99,stroke:#333,stroke-width:2px
    style SA4 fill:#ffeb99,stroke:#333,stroke-width:2px
    style D1 fill:#e1f5ff,stroke:#333,stroke-width:2px
    style D2 fill:#e1f5ff,stroke:#333,stroke-width:2px
    style D3 fill:#e1f5ff,stroke:#333,stroke-width:2px
    style D4 fill:#e1f5ff,stroke:#333,stroke-width:2px
    style D5 fill:#e1f5ff,stroke:#333,stroke-width:2px
```

### Granularidad y Cardinalidad

```mermaid
graph TB
    P[22,592 Partidos OLTP<br/>con cuotas completas] -->|× 10 casas| C[225,920 combinaciones<br/>partido × casa]
    C -->|× 4 estrategias| E[903,680 registros base<br/>FACT_APUESTAS]

    E --> D1["<b>Por FECHA:</b><br/>~2,920 fechas<br/>= 309 registros/día promedio"]
    E --> D2["<b>Por LIGA:</b><br/>11 ligas<br/>= 82,153 registros/liga promedio"]
    E --> D3["<b>Por CASA:</b><br/>10 casas<br/>= 90,368 registros/casa"]
    E --> D4["<b>Por ESTRATEGIA:</b><br/>4 estrategias<br/>= 225,920 registros/estrategia"]
    E --> D5["<b>Por PARTIDO:</b><br/>22,592 partidos<br/>= 40 registros/partido<br/>(10 casas × 4 estrategias)"]

    style P fill:#ffcccc,stroke:#333,stroke-width:2px
    style E fill:#ff9999,stroke:#333,stroke-width:4px
    style D5 fill:#ffffcc,stroke:#333,stroke-width:3px
```

### Relaciones con Dimensiones

```mermaid
graph TB
    FA["<b>FACT_APUESTAS</b><br/>903,680 registros<br/><br/>Granularidad:<br/>1 apuesta individual"]

    DF[DIM_FECHA<br/>~2,920 registros<br/>🕐]
    DL[DIM_LIGA<br/>11 registros<br/>🏆]
    DEL[DIM_EQUIPO<br/>~400 registros<br/>⚽ Rol: LOCAL]
    DEV[DIM_EQUIPO<br/>~400 registros<br/>⚽ Rol: VISITANTE]
    DCA[DIM_CASA_APUESTAS<br/>10 registros<br/>🏢]
    DES[DIM_ESTRATEGIA<br/>4 registros<br/>🎯]
    DRT[DIM_RESULTADO_TIPO<br/>3 registros<br/>📊]

    DF -->|1:N<br/>~310 hechos/fecha| FA
    DL -->|1:N<br/>~82K hechos/liga| FA
    DEL -->|1:N<br/>~2.3K hechos/equipo| FA
    DEV -->|1:N<br/>~2.3K hechos/equipo| FA
    DCA -->|1:N<br/>~90K hechos/casa| FA
    DES -->|1:N<br/>~226K hechos/estrategia| FA
    DRT -->|1:N<br/>~301K hechos/resultado| FA

    DCA -.->|FKs adicionales<br/>casas_mejor (arbitraje)| FA

    style FA fill:#ff9999,stroke:#333,stroke-width:4px
    style DF fill:#ffeb99,stroke:#333,stroke-width:2px
    style DL fill:#ffeb99,stroke:#333,stroke-width:2px
    style DEL fill:#ffeb99,stroke:#333,stroke-width:2px
    style DEV fill:#ffeb99,stroke:#333,stroke-width:2px
    style DCA fill:#ccffcc,stroke:#333,stroke-width:2px
    style DES fill:#ccffcc,stroke:#333,stroke-width:2px
    style DRT fill:#ccffcc,stroke:#333,stroke-width:2px
```

### Campos Derivados de Arbitraje - Explicación

```mermaid
graph TB
    subgraph "CÁLCULO ETL - Una vez por partido"
        P1[Partido: Real Madrid vs Barcelona<br/>2015-11-21]

        P1 --> C1[Analizar cuotas de 10 casas:<br/>B365, BW, IW, LB, PS, WH,<br/>SJ, VC, GB, BS]

        C1 --> M1[MAX cuota_local = 2.50 Bet365]
        C1 --> M2[MAX cuota_empate = 3.75 Pinnacle]
        C1 --> M3[MAX cuota_visitante = 3.00 William Hill]

        M1 & M2 & M3 --> CALC["Fórmula arbitraje:<br/>porcentaje = 1/2.50 + 1/3.75 + 1/3.00<br/>= 0.4 + 0.267 + 0.333<br/>= 1.000"]

        CALC --> D1{porcentaje < 1.0?}

        D1 -->|SÍ| OPP["es_oportunidad = TRUE<br/>beneficio = 1/porcentaje - 1"]
        D1 -->|NO| NOPP["es_oportunidad = FALSE<br/>beneficio = 0"]
    end

    subgraph "DUPLICACIÓN - 40 registros del mismo partido"
        REP["Los 40 registros<br/>(10 casas × 4 estrategias)<br/>comparten MISMOS valores:<br/><br/>arbitraje_cuota_local_max = 2.50<br/>arbitraje_cuota_empate_max = 3.75<br/>arbitraje_cuota_visitante_max = 3.00<br/>arbitraje_casa_local_mejor = 1 (Bet365)<br/>arbitraje_casa_empate_mejor = 5 (Pinnacle)<br/>arbitraje_casa_visitante_mejor = 6 (WH)<br/>arbitraje_porcentaje = 1.000<br/>arbitraje_es_oportunidad = FALSE<br/>arbitraje_beneficio = 0"]
    end

    OPP --> REP
    NOPP --> REP

    style P1 fill:#ffcccc,stroke:#333,stroke-width:2px
    style CALC fill:#ffffcc,stroke:#333,stroke-width:2px
    style OPP fill:#ccffcc,stroke:#333,stroke-width:2px
    style NOPP fill:#ffcccc,stroke:#333,stroke-width:2px
    style REP fill:#e1f5ff,stroke:#333,stroke-width:3px
```

**Justificación**: Calcular 1 vez en ETL y duplicar es más eficiente que agregar en cada query.

### Índices Definidos

```mermaid
graph TB
    subgraph "ÍNDICES ESTÁNDAR"
        I1[idx_fact_casa_fecha<br/>id_casa_apuestas, id_fecha<br/>📊 Para análisis por casa]
        I2[idx_fact_liga_estrategia<br/>id_liga, id_estrategia<br/>🎯 Para análisis por estrategia]
        I3[idx_fact_temporada<br/>id_fecha<br/>📅 Para análisis temporal]
        I4[idx_fact_equipo_local<br/>id_equipo_local<br/>⚽ Para análisis por equipo]
        I5[idx_fact_equipo_visitante<br/>id_equipo_visitante<br/>⚽ Para análisis por equipo]
    end

    subgraph "ÍNDICE FILTRADO ⚡ CLAVE"
        IF["<b>idx_fact_arbitraje</b><br/>id_fecha, id_liga, arbitraje_beneficio<br/>WHERE arbitraje_es_oportunidad = TRUE<br/><br/>🎯 Solo indexa ~2-5% de registros<br/>⚡ 10-15x más rápido para queries arbitraje"]
    end

    style IF fill:#ccffcc,stroke:#333,stroke-width:4px
    style I1 fill:#ffeb99,stroke:#333,stroke-width:2px
    style I2 fill:#ffeb99,stroke:#333,stroke-width:2px
    style I3 fill:#ffeb99,stroke:#333,stroke-width:2px
    style I4 fill:#ffeb99,stroke:#333,stroke-width:2px
    style I5 fill:#ffeb99,stroke:#333,stroke-width:2px
```

### Ejemplo de Registros

| id_fecha | equipo_local | equipo_visitante | casa | estrategia | resultado | ganancia | perdida | inv | acierto | arb_oport |
|----------|--------------|------------------|------|------------|-----------|----------|---------|-----|---------|-----------|
| 20150810 | 112 (Man Utd) | 87 (Newcastle) | 1 (B365) | 1 (Favorito) | 1 (H) | 1.75 | 0.00 | 1.00 | TRUE | FALSE |
| 20150810 | 112 (Man Utd) | 87 (Newcastle) | 1 (B365) | 2 (Underdog) | 3 (A) | 0.00 | 1.00 | 1.00 | FALSE | FALSE |
| 20150810 | 112 (Man Utd) | 87 (Newcastle) | 2 (BW) | 1 (Favorito) | 1 (H) | 1.80 | 0.00 | 1.00 | TRUE | FALSE |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |

**Nota**: Los 40 registros del mismo partido comparten valores idénticos en campos `arb_*`.

### Uso en Indicadores

```mermaid
graph TB
    FA[FACT_APUESTAS<br/>903,680 registros]

    FA --> I1["<b>Indicador 1:</b><br/>% Precisión por Casa<br/>= SUM(cant_aciertos) / SUM(cant_apuestas) × 100<br/>GROUP BY casa, liga, temporada"]

    FA --> I2["<b>Indicador 2:</b><br/>ROI % por Estrategia<br/>= SUM(ganancia - perdida) / SUM(inversion) × 100<br/>GROUP BY estrategia, liga, temporada"]

    FA --> I3["<b>Indicador 3:</b><br/>Oportunidades Arbitraje<br/>= COUNT(DISTINCT id_partido)<br/>WHERE arbitraje_es_oportunidad = TRUE<br/>GROUP BY liga, temporada<br/>⚡ USA ÍNDICE FILTRADO"]

    FA --> I4["<b>Indicador 4:</b><br/>Beneficio Arbitraje Promedio<br/>= AVG(arbitraje_beneficio)<br/>WHERE arbitraje_es_oportunidad = TRUE"]

    FA --> I5["<b>Indicador 5:</b><br/>Casa con Mejores Cuotas<br/>= COUNT(arbitraje_casa_*_mejor)<br/>GROUP BY casa"]

    style FA fill:#ff9999,stroke:#333,stroke-width:3px
    style I1 fill:#e1f5ff,stroke:#333,stroke-width:2px
    style I2 fill:#e1f5ff,stroke:#333,stroke-width:2px
    style I3 fill:#ccffcc,stroke:#333,stroke-width:3px
    style I4 fill:#e1f5ff,stroke:#333,stroke-width:2px
    style I5 fill:#e1f5ff,stroke:#333,stroke-width:2px
```

### Performance por Tipo de Consulta

```mermaid
graph LR
    subgraph "Consultas de Apuestas Individuales"
        Q1["Precisión por Casa<br/>📊 Escanea ~900K registros<br/>⏱️ ~2 segundos<br/>Índice: casa+fecha"]
        Q2["ROI por Estrategia<br/>🎯 Escanea ~900K registros<br/>⏱️ ~3 segundos<br/>Índice: liga+estrategia"]
    end

    subgraph "Consultas de Arbitraje"
        Q3["Oportunidades Arbitraje<br/>⚡ Escanea ~20-40K registros<br/>⏱️ <1 segundo<br/>Índice: FILTRADO<br/><br/>✅ 10-15x más rápido<br/>vs full scan"]
    end

    style Q1 fill:#ffeb99,stroke:#333,stroke-width:2px
    style Q2 fill:#ffeb99,stroke:#333,stroke-width:2px
    style Q3 fill:#ccffcc,stroke:#333,stroke-width:3px
```

### Comparación con Esquema Anterior

| Aspecto | Constelación (2 Tablas) | Estrella (1 Tabla) |
|---------|--------------------------|---------------------|
| **Tablas de Hechos** | FACT_APUESTAS + FACT_ARBITRAJE | FACT_APUESTAS (única) ✅ |
| **Registros Totales** | 903K + 23K = 926K | 903K |
| **Complejidad Queries** | Media (UNION, múltiples FACTs) | Baja ✅ |
| **Performance Arbitraje** | 40ms (tabla dedicada) | <100ms (índice filtrado) |
| **Redundancia** | Cero | 8 campos × 23K = 184K (~3%) |
| **Mantenimiento** | 2 tablas independientes | 1 tabla simple ✅ |
| **Compatibilidad BI** | Buena | Excelente ✅ |

---

## Resumen de la Tabla de Hechos

### Componentes

| Componente | Cantidad | Descripción |
|------------|----------|-------------|
| **Dimensiones FK** | 7 | Fecha, Liga, 2×Equipo, Casa, Estrategia, Resultado |
| **Hechos Aditivos** | 5 | Ganancia, Pérdida, Inversión, Aciertos, Apuestas |
| **Hechos Semi-Aditivos** | 4 | Cuotas (apostada, local, empate, visitante) |
| **Campos Derivados** | 8 | Campos de arbitraje pre-calculados |
| **FKs Adicionales** | 3 | Casas con mejores cuotas (arbitraje) |
| **Metadatos** | 3 | id_partido, resultado_real, acierto |
| **Total Columnas** | 27 | Estructura completa y eficiente |

### Métricas de Diseño

```mermaid
graph TB
    subgraph "Cardinalidad"
        C1[903,680 registros totales]
        C2[~790K registros reales<br/>87% cobertura]
        C3[40 registros por partido<br/>10 casas × 4 estrategias]
    end

    subgraph "Performance"
        P1[Índices: 6 total]
        P2[Índice filtrado arbitraje: ⚡]
        P3[Queries < 3 segundos]
    end

    subgraph "Almacenamiento"
        S1[~180 MB estimado]
        S2[Redundancia: 3%]
        S3[Optimizable con compresión]
    end

    style C1 fill:#ffeb99,stroke:#333,stroke-width:2px
    style C2 fill:#ffeb99,stroke:#333,stroke-width:2px
    style C3 fill:#ffeb99,stroke:#333,stroke-width:2px
    style P1 fill:#e1f5ff,stroke:#333,stroke-width:2px
    style P2 fill:#ccffcc,stroke:#333,stroke-width:3px
    style P3 fill:#e1f5ff,stroke:#333,stroke-width:2px
    style S1 fill:#ffffcc,stroke:#333,stroke-width:2px
    style S2 fill:#ffffcc,stroke:#333,stroke-width:2px
    style S3 fill:#ffffcc,stroke:#333,stroke-width:2px
```

---

**Diagrama 3c - Tabla de Hechos Única (Esquema Estrella) Completo** ✅
