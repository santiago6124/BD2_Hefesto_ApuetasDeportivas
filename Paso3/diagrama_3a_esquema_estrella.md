# 3a) DIAGRAMA: Esquema de Estrella (Star Schema)

## Esquema de Estrella - Vista General

```mermaid
graph TB
    subgraph "⭐ ESQUEMA ESTRELLA - DATA WAREHOUSE APUESTAS DEPORTIVAS"
        direction TB

        subgraph "DIMENSIONES"
            direction LR
            DF[DIM_FECHA<br/>~2,920 registros<br/>🕐<br/>Temporada deportiva]
            DL[DIM_LIGA<br/>11 registros<br/>🏆<br/>Competiciones europeas]
            DEL[DIM_EQUIPO<br/>~400 registros<br/>⚽ ROL: Local<br/>SCD Type 2]
            DEV[DIM_EQUIPO<br/>~400 registros<br/>⚽ ROL: Visitante<br/>SCD Type 2]
            DCA[DIM_CASA_APUESTAS<br/>10 registros<br/>🏢<br/>Operadores]
            DES[DIM_ESTRATEGIA<br/>4 registros<br/>🎯<br/>Calculada]
            DRT[DIM_RESULTADO_TIPO<br/>3 registros<br/>📊<br/>H/D/A]
        end

        subgraph "TABLA DE HECHOS CENTRAL"
            FA["<b>FACT_APUESTAS</b><br/>~903,680 registros<br/><br/><b>Granularidad:</b><br/>1 apuesta × 1 casa × 1 partido × 1 estrategia<br/><br/><b>HECHOS ADITIVOS:</b><br/>• ganancia_total<br/>• perdida_total<br/>• inversion<br/>• cant_aciertos<br/>• cant_apuestas<br/><br/><b>HECHOS SEMI-ADITIVOS:</b><br/>• cuota_apostada<br/>• cuota_local, cuota_empate, cuota_visitante<br/><br/><b>CAMPOS DERIVADOS ARBITRAJE:</b><br/>• arbitraje_cuota_*_max (3)<br/>• arbitraje_casa_*_mejor (3)<br/>• arbitraje_porcentaje<br/>• arbitraje_es_oportunidad<br/>• arbitraje_beneficio"]
        end
    end

    %% Relaciones 1:N desde Dimensiones hacia Hechos
    DF -->|1:N<br/>~310 hechos/fecha| FA
    DL -->|1:N<br/>~82K hechos/liga| FA
    DEL -->|1:N<br/>~2.3K hechos/equipo| FA
    DEV -->|1:N<br/>~2.3K hechos/equipo| FA
    DCA -->|1:N<br/>~90K hechos/casa| FA
    DES -->|1:N<br/>~226K hechos/estrategia| FA
    DRT -->|1:N<br/>~301K hechos/resultado| FA

    %% Referencias adicionales para arbitraje
    DCA -.->|FK adicionales<br/>casas_mejor| FA

    style FA fill:#ff9999,stroke:#333,stroke-width:4px
    style DF fill:#ffeb99,stroke:#333,stroke-width:2px
    style DL fill:#ffeb99,stroke:#333,stroke-width:2px
    style DEL fill:#ffeb99,stroke:#333,stroke-width:2px
    style DEV fill:#ffeb99,stroke:#333,stroke-width:2px
    style DCA fill:#ccffcc,stroke:#333,stroke-width:2px
    style DES fill:#ccffcc,stroke:#333,stroke-width:2px
    style DRT fill:#ccffcc,stroke:#333,stroke-width:2px
```

## Características del Esquema de Estrella

### Ventajas del Diseño

| Aspecto | Beneficio |
|---------|-----------|
| **Simplicidad Conceptual** | Una sola tabla de hechos, fácil de entender |
| **Queries Intuitivos** | Siempre JOIN desde FACT hacia dimensiones |
| **Performance Predecible** | Optimizador DB maneja bien este patrón estándar |
| **Herramientas BI** | Compatibilidad total con herramientas visuales |
| **Mantenimiento** | Estructura simple, fácil de mantener |

### Justificación vs Constelación

```mermaid
graph LR
    subgraph "Constelación (Anterior) ❌"
        A1[2 Tablas de Hechos<br/>FACT_APUESTAS +<br/>FACT_ARBITRAJE<br/>Complejo para BI]
    end

    subgraph "Estrella (Nuevo) ✅"
        B1[1 Tabla de Hechos<br/>FACT_APUESTAS<br/>Todo consolidado<br/>Esquema estándar]
    end

    A1 -.Transformación.-> B1

    style A1 fill:#ffcccc,stroke:#333,stroke-width:2px
    style B1 fill:#ccffcc,stroke:#333,stroke-width:3px
```

## Diagrama Detallado de Relaciones

```mermaid
erDiagram
    DIM_FECHA ||--o{ FACT_APUESTAS : "1:N fecha"
    DIM_LIGA ||--o{ FACT_APUESTAS : "1:N liga"
    DIM_EQUIPO ||--o{ FACT_APUESTAS : "1:N local"
    DIM_EQUIPO ||--o{ FACT_APUESTAS : "1:N visitante"
    DIM_CASA_APUESTAS ||--o{ FACT_APUESTAS : "1:N casa"
    DIM_CASA_APUESTAS ||--o{ FACT_APUESTAS : "1:N casa_mejor_local"
    DIM_CASA_APUESTAS ||--o{ FACT_APUESTAS : "1:N casa_mejor_empate"
    DIM_CASA_APUESTAS ||--o{ FACT_APUESTAS : "1:N casa_mejor_visitante"
    DIM_ESTRATEGIA ||--o{ FACT_APUESTAS : "1:N estrategia"
    DIM_RESULTADO_TIPO ||--o{ FACT_APUESTAS : "1:N resultado"

    DIM_FECHA {
        int id_fecha PK
        date fecha
        varchar temporada
        int anio
        int mes
    }

    DIM_LIGA {
        int id_liga PK
        varchar nombre_liga
        varchar pais
    }

    DIM_EQUIPO {
        int id_equipo PK
        varchar nombre_equipo
        int liga_actual
        date fecha_inicio_vigencia
        date fecha_fin_vigencia
        boolean registro_actual
    }

    DIM_CASA_APUESTAS {
        int id_casa_apuestas PK
        varchar nombre_completo
        varchar codigo_casa
    }

    DIM_ESTRATEGIA {
        int id_estrategia PK
        varchar nombre_estrategia
        varchar tipo_riesgo
    }

    DIM_RESULTADO_TIPO {
        int id_resultado_tipo PK
        char codigo_resultado
        varchar descripcion
    }

    FACT_APUESTAS {
        int id_fecha FK
        int id_equipo_local FK
        int id_equipo_visitante FK
        int id_liga FK
        int id_casa_apuestas FK
        int id_estrategia FK
        int id_resultado_tipo FK
        int id_partido
        decimal ganancia_total
        decimal perdida_total
        decimal inversion
        int cant_aciertos
        int cant_apuestas
        decimal cuota_apostada
        decimal arbitraje_porcentaje
        boolean arbitraje_es_oportunidad
        decimal arbitraje_beneficio
    }
```

## Flujo de Consultas por Indicador

### Indicador 1: Precisión por Casa (FACT_APUESTAS)
```mermaid
graph LR
    Q1[🔍 Pregunta:<br/>Casa más precisa<br/>por liga] --> FA[📊 FACT_APUESTAS<br/>903K registros<br/>+JOIN]
    FA --> DCA[🏢 DIM_CASA]
    FA --> DL[🏆 DIM_LIGA]
    FA --> DF[🕐 DIM_FECHA]
    FA --> R1[✅ Resultado:<br/>Precisión %<br/>por casa y liga<br/><2 seg]

    style Q1 fill:#e1f5ff,stroke:#333,stroke-width:2px
    style FA fill:#ff9999,stroke:#333,stroke-width:3px
    style R1 fill:#ccffcc,stroke:#333,stroke-width:2px
```

### Indicador 2: ROI por Estrategia (FACT_APUESTAS)
```mermaid
graph LR
    Q2[🔍 Pregunta:<br/>ROI de<br/>estrategias] --> FA[📊 FACT_APUESTAS<br/>903K registros<br/>+JOIN]
    FA --> DES[🎯 DIM_ESTRATEGIA]
    FA --> DL[🏆 DIM_LIGA]
    FA --> DCA[🏢 DIM_CASA]
    FA --> R2[✅ Resultado:<br/>ROI %<br/>por estrategia<br/><3 seg]

    style Q2 fill:#e1f5ff,stroke:#333,stroke-width:2px
    style FA fill:#ff9999,stroke:#333,stroke-width:3px
    style R2 fill:#ccffcc,stroke:#333,stroke-width:2px
```

### Indicador 3: Oportunidades Arbitraje (FACT_APUESTAS con índice filtrado)
```mermaid
graph LR
    Q3[🔍 Pregunta:<br/>Oportunidades<br/>de arbitraje] --> FA[📊 FACT_APUESTAS<br/>Campos derivados<br/>+ Índice filtrado<br/>⚡ Solo ~20K registros]
    FA --> DL[🏆 DIM_LIGA]
    FA --> DF[🕐 DIM_FECHA]
    FA --> DCA[🏢 DIM_CASA<br/>casas mejores]
    FA --> R3[✅ Resultado:<br/>Arbitrajes<br/>por liga/temporada<br/><1 seg ⚡]

    style Q3 fill:#e1f5ff,stroke:#333,stroke-width:2px
    style FA fill:#ff9999,stroke:#333,stroke-width:3px
    style R3 fill:#ccffcc,stroke:#333,stroke-width:3px
```

**Nota**: El índice filtrado `idx_fact_arbitraje` solo indexa registros con `arbitraje_es_oportunidad = TRUE`, optimizando drásticamente las consultas de arbitraje.

## Comparación con Esquema Anterior

### Métricas Comparativas

| Métrica | Constelación (Anterior) | Estrella (Nuevo) |
|---------|------------------------|------------------|
| **Tablas de Hechos** | 2 | 1 ✅ |
| **Registros Totales** | 903K + 23K = 926K | 903K |
| **Complejidad Queries** | Media (UNION/múltiples FACTs) | Baja ✅ |
| **Mantenimiento** | Medio (2 tablas) | Bajo ✅ |
| **Performance Arbitraje** | 40ms (tabla dedicada) | <100ms (índice filtrado) |
| **Performance Apuestas** | Óptima | Óptima ✅ |
| **Redundancia** | Cero | 8 campos × 23K = 184K valores (~3%) |
| **Compatibilidad BI** | Buena | Excelente ✅ |

### Trade-offs Aceptados

| Aspecto | Trade-off | Mitigación |
|---------|-----------|------------|
| **Redundancia** | Campos arbitraje duplicados por partido | Solo 3% overhead, aceptable |
| **Performance Arbitraje** | 2.5x más lento que tabla dedicada | Índice filtrado recupera 80% performance |
| **Tamaño Tabla** | Ligeramente mayor por campos extra | Compresión columnar en DB moderna |

## Cardinalidades del Esquema

```mermaid
graph TB
    P[📊 22,592 Partidos OLTP] -->|× 10 casas| C[225,920 combinaciones]
    C -->|× 4 estrategias| E[903,680 registros FACT]

    E --> D1[🕐 DIM_FECHA<br/>~2,920 registros<br/>= 309 hechos/fecha]
    E --> D2[🏆 DIM_LIGA<br/>11 registros<br/>= 82K hechos/liga]
    E --> D3[🏢 DIM_CASA<br/>10 registros<br/>= 90K hechos/casa]
    E --> D4[🎯 DIM_ESTRATEGIA<br/>4 registros<br/>= 226K hechos/estrategia]

    style P fill:#ffcccc,stroke:#333,stroke-width:2px
    style E fill:#ff9999,stroke:#333,stroke-width:4px
    style D1 fill:#ffeb99,stroke:#333,stroke-width:2px
    style D2 fill:#ffeb99,stroke:#333,stroke-width:2px
    style D3 fill:#ccffcc,stroke:#333,stroke-width:2px
    style D4 fill:#ccffcc,stroke:#333,stroke-width:2px
```

## Resumen de Decisiones

### ✅ Decisión: Esquema de Estrella Consolidado

**Razones**:
1. **Simplicidad**: Una tabla de hechos, estructura estándar
2. **Mantenibilidad**: Fácil de entender y mantener
3. **Compatibilidad**: Herramientas BI optimizadas para este patrón
4. **Performance**: Aceptable con índices apropiados
5. **Flexibilidad**: Permite todos los análisis requeridos

### 📊 Métricas del Esquema Estrella

| Métrica | Valor |
|---------|-------|
| **Tabla de Hechos** | 1 (FACT_APUESTAS) |
| **Dimensiones** | 6 |
| **Registros** | ~903,680 |
| **Hechos Aditivos** | 5 |
| **Hechos Semi-Aditivos** | 4 |
| **Campos Derivados** | 8 (arbitraje) |
| **Índices** | 6 (5 estándar + 1 filtrado) |

---

**Diagrama 3a - Esquema de Estrella Completo** ✅
