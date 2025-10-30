# 3d) DIAGRAMA: Relaciones y Cardinalidades

## Esquema Completo con Relaciones

```mermaid
erDiagram
    DIM_FECHA ||--o{ FACT_APUESTAS : "1:N (id_fecha)"
    DIM_FECHA ||--o{ FACT_ARBITRAJE : "1:N (id_fecha)"

    DIM_LIGA ||--o{ FACT_APUESTAS : "1:N (id_liga)"
    DIM_LIGA ||--o{ FACT_ARBITRAJE : "1:N (id_liga)"

    DIM_EQUIPO ||--o{ FACT_APUESTAS : "1:N (id_equipo_local)"
    DIM_EQUIPO ||--o{ FACT_APUESTAS : "1:N (id_equipo_visitante)"
    DIM_EQUIPO ||--o{ FACT_ARBITRAJE : "1:N (id_equipo_local)"
    DIM_EQUIPO ||--o{ FACT_ARBITRAJE : "1:N (id_equipo_visitante)"

    DIM_CASA_APUESTAS ||--o{ FACT_APUESTAS : "1:N (id_casa_apuestas)"
    DIM_CASA_APUESTAS ||--o{ FACT_ARBITRAJE : "1:N (casa_local_mejor)"
    DIM_CASA_APUESTAS ||--o{ FACT_ARBITRAJE : "1:N (casa_empate_mejor)"
    DIM_CASA_APUESTAS ||--o{ FACT_ARBITRAJE : "1:N (casa_visitante_mejor)"

    DIM_ESTRATEGIA ||--o{ FACT_APUESTAS : "1:N (id_estrategia)"
    DIM_RESULTADO_TIPO ||--o{ FACT_APUESTAS : "1:N (id_resultado_tipo)"

    DIM_FECHA {
        int id_fecha PK
        date fecha UK
        varchar temporada
        int año
        int mes
        int dia
        varchar dia_semana
        boolean es_fin_semana
    }

    DIM_LIGA {
        int id_liga PK
        varchar nombre_liga UK
        varchar pais
        varchar nivel
        int num_equipos
    }

    DIM_EQUIPO {
        int id_equipo PK
        varchar codigo_natural
        varchar nombre_equipo
        int liga_actual FK
        date fecha_inicio_validez
        date fecha_fin_validez
        boolean registro_actual
        int version
    }

    DIM_CASA_APUESTAS {
        int id_casa_apuestas PK
        varchar codigo_casa UK
        varchar nombre_completo
        varchar pais_origen
        boolean activo
    }

    DIM_ESTRATEGIA {
        int id_estrategia PK
        varchar codigo_estrategia UK
        varchar nombre_estrategia
        varchar tipo_estrategia
    }

    DIM_RESULTADO_TIPO {
        int id_resultado_tipo PK
        char codigo_resultado UK
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
    }

    FACT_ARBITRAJE {
        int id_fecha FK
        int id_equipo_local FK
        int id_equipo_visitante FK
        int id_liga FK
        int id_partido
        int casa_local_mejor FK
        int casa_empate_mejor FK
        int casa_visitante_mejor FK
        int cant_oportunidades
        decimal beneficio_arbitraje
        boolean es_oportunidad
    }
```

---

## Matriz Completa de Relaciones

### Relaciones FACT_APUESTAS

| # | Dimensión | FK en Fact | Cardinalidad | Tipo | Integridad |
|---|-----------|------------|--------------|------|------------|
| **R1** | DIM_FECHA | id_fecha | 1:N | Obligatoria | CASCADE |
| **R2** | DIM_LIGA | id_liga | 1:N | Obligatoria | CASCADE |
| **R3** | DIM_EQUIPO (local) | id_equipo_local | 1:N | Obligatoria | CASCADE |
| **R4** | DIM_EQUIPO (visitante) | id_equipo_visitante | 1:N | Obligatoria | CASCADE |
| **R5** | DIM_CASA_APUESTAS | id_casa_apuestas | 1:N | Obligatoria | CASCADE |
| **R6** | DIM_ESTRATEGIA | id_estrategia | 1:N | Obligatoria | CASCADE |
| **R7** | DIM_RESULTADO_TIPO | id_resultado_tipo | 1:N | Obligatoria | CASCADE |

### Relaciones FACT_ARBITRAJE

| # | Dimensión | FK en Fact | Cardinalidad | Tipo | Integridad |
|---|-----------|------------|--------------|------|------------|
| **R8** | DIM_FECHA | id_fecha | 1:N | Obligatoria | CASCADE |
| **R9** | DIM_LIGA | id_liga | 1:N | Obligatoria | CASCADE |
| **R10** | DIM_EQUIPO (local) | id_equipo_local | 1:N | Obligatoria | CASCADE |
| **R11** | DIM_EQUIPO (visitante) | id_equipo_visitante | 1:N | Obligatoria | CASCADE |
| **R12** | DIM_CASA_APUESTAS (mejor local) | casa_local_mejor | 1:N | Obligatoria | CASCADE |
| **R13** | DIM_CASA_APUESTAS (mejor empate) | casa_empate_mejor | 1:N | Obligatoria | CASCADE |
| **R14** | DIM_CASA_APUESTAS (mejor visitante) | casa_visitante_mejor | 1:N | Obligatoria | CASCADE |

---

## Vista Detallada por Dimensión

### DIM_FECHA - Relaciones Temporales

```mermaid
graph TB
    DF[DIM_FECHA<br/>~2,920 registros<br/>2008-2016]

    DF -->|R1: 1:N| FA_F[FACT_APUESTAS<br/>~903,680 registros<br/>≈ 310 hechos/fecha]

    DF -->|R8: 1:N| FAR_F[FACT_ARBITRAJE<br/>~22,592 registros<br/>≈ 8 hechos/fecha]

    FA_F --> E1[Ejemplo:<br/>2008-08-15 → 310 apuestas<br/>10 casas × 31 partidos]

    FAR_F --> E2[Ejemplo:<br/>2008-08-15 → 8 partidos<br/>con análisis arbitraje]

    style DF fill:#ffeb99,stroke:#333,stroke-width:3px
    style FA_F fill:#ff9999,stroke:#333,stroke-width:2px
    style FAR_F fill:#99ccff,stroke:#333,stroke-width:2px
```

**Características de Relación:**
- **Tipo**: 1 a Muchos (1:N)
- **Obligatoriedad**: Obligatoria (NOT NULL)
- **Integridad Referencial**: ON DELETE CASCADE
- **Índice**: Índice clustered en id_fecha para ambas fact tables
- **Cardinalidad Promedio**: 310 hechos/fecha en FACT_APUESTAS, 8 en FACT_ARBITRAJE

---

### DIM_LIGA - Relaciones Geográficas

```mermaid
graph TB
    DL[DIM_LIGA<br/>11 ligas]

    DL -->|R2: 1:N| FA_L[FACT_APUESTAS<br/>~82,153 hechos/liga promedio]

    DL -->|R9: 1:N| FAR_L[FACT_ARBITRAJE<br/>~2,054 hechos/liga promedio]

    FA_L --> D1[Distribución:<br/>Premier League E0: ~140K<br/>Championship E1: ~95K<br/>La Liga SP1: ~75K]

    FAR_L --> D2[Distribución:<br/>Premier League E0: ~3,500<br/>Championship E1: ~2,375<br/>La Liga SP1: ~1,875]

    style DL fill:#ffeb99,stroke:#333,stroke-width:3px
    style FA_L fill:#ff9999,stroke:#333,stroke-width:2px
    style FAR_L fill:#99ccff,stroke:#333,stroke-width:2px
```

**Características de Relación:**
- **Tipo**: 1 a Muchos (1:N)
- **Obligatoriedad**: Obligatoria (NOT NULL)
- **Integridad Referencial**: ON DELETE CASCADE
- **Índice**: Índice no-clustered en id_liga
- **Distribución**: No uniforme - ligas grandes tienen más registros

---

### DIM_EQUIPO - Relaciones Role-Playing

```mermaid
graph TB
    DE[DIM_EQUIPO<br/>~400 registros<br/>con versiones SCD-2]

    DE -->|R3: 1:N<br/>Rol LOCAL| FA_L[FACT_APUESTAS<br/>id_equipo_local<br/>~2,260 hechos/equipo]

    DE -->|R4: 1:N<br/>Rol VISITANTE| FA_V[FACT_APUESTAS<br/>id_equipo_visitante<br/>~2,260 hechos/equipo]

    DE -->|R10: 1:N<br/>Rol LOCAL| FAR_L[FACT_ARBITRAJE<br/>id_equipo_local<br/>~56 hechos/equipo]

    DE -->|R11: 1:N<br/>Rol VISITANTE| FAR_V[FACT_ARBITRAJE<br/>id_equipo_visitante<br/>~56 hechos/equipo]

    FA_L & FA_V --> SUM1[Por partido:<br/>2 equipos × 10 casas × 4 estrategias<br/>= 80 registros FACT_APUESTAS]

    FAR_L & FAR_V --> SUM2[Por partido:<br/>2 equipos × 1 análisis<br/>= 1 registro FACT_ARBITRAJE]

    style DE fill:#ffeb99,stroke:#333,stroke-width:3px
    style FA_L fill:#ff9999,stroke:#333,stroke-width:2px
    style FA_V fill:#ff9999,stroke:#333,stroke-width:2px
    style FAR_L fill:#99ccff,stroke:#333,stroke-width:2px
    style FAR_V fill:#99ccff,stroke:#333,stroke-width:2px
```

**Características Especiales:**
- **Role-Playing**: Misma dimensión, dos roles diferentes (local/visitante)
- **Tipo**: 1 a Muchos (1:N) para cada rol
- **Obligatoriedad**: Ambos FK son obligatorios (NOT NULL)
- **Restricción**: id_equipo_local ≠ id_equipo_visitante (CHECK constraint)
- **SCD Tipo 2**: Join temporal usando fecha_inicio_validez y fecha_fin_validez
- **Índices**: Índice compuesto en (id_equipo_local, id_equipo_visitante)

**Ejemplo de Validación Temporal:**
```sql
-- Join temporal correcto para FACT_APUESTAS
SELECT * FROM FACT_APUESTAS fa
JOIN DIM_EQUIPO de_local ON fa.id_equipo_local = de_local.id_equipo
  AND fa.id_fecha BETWEEN de_local.fecha_inicio_validez AND de_local.fecha_fin_validez
JOIN DIM_EQUIPO de_visit ON fa.id_equipo_visitante = de_visit.id_equipo
  AND fa.id_fecha BETWEEN de_visit.fecha_inicio_validez AND de_visit.fecha_fin_validez
```

---

### DIM_CASA_APUESTAS - Relaciones Múltiples

```mermaid
graph TB
    DCA[DIM_CASA_APUESTAS<br/>10 casas]

    DCA -->|R5: 1:N<br/>Casa de apuesta| FA[FACT_APUESTAS<br/>id_casa_apuestas<br/>~90,368 hechos/casa]

    DCA -->|R12: 1:N<br/>Mejor cuota LOCAL| FAR_H[FACT_ARBITRAJE<br/>casa_local_mejor<br/>~2,259 veces/casa]

    DCA -->|R13: 1:N<br/>Mejor cuota EMPATE| FAR_D[FACT_ARBITRAJE<br/>casa_empate_mejor<br/>~2,259 veces/casa]

    DCA -->|R14: 1:N<br/>Mejor cuota VISITANTE| FAR_A[FACT_ARBITRAJE<br/>casa_visitante_mejor<br/>~2,259 veces/casa]

    FA --> C1[Ejemplo B365:<br/>~90,368 apuestas registradas<br/>en FACT_APUESTAS]

    FAR_H & FAR_D & FAR_A --> C2[Ejemplo B365:<br/>~6,777 veces mejor cuota<br/>distribuido H/D/A]

    style DCA fill:#ccffcc,stroke:#333,stroke-width:3px
    style FA fill:#ff9999,stroke:#333,stroke-width:2px
    style FAR_H fill:#99ccff,stroke:#333,stroke-width:2px
    style FAR_D fill:#99ccff,stroke:#333,stroke-width:2px
    style FAR_A fill:#99ccff,stroke:#333,stroke-width:2px
```

**Características de Relación:**
- **FACT_APUESTAS**: 1 FK simple (id_casa_apuestas)
- **FACT_ARBITRAJE**: 3 FK role-playing (casa_mejor por resultado)
- **Tipo**: 1 a Muchos (1:N) para cada relación
- **Obligatoriedad**: Todos FK son obligatorios (NOT NULL)
- **Uso Analítico**: Permite identificar casas con mejores cuotas por tipo resultado

---

### DIM_ESTRATEGIA - Relación Exclusiva

```mermaid
graph TB
    DES[DIM_ESTRATEGIA<br/>4 estrategias]

    DES -->|R6: 1:N| FA[FACT_APUESTAS<br/>id_estrategia<br/>~225,920 hechos/estrategia]

    DES -.->|NO relacionada| FAR[FACT_ARBITRAJE<br/>No usa estrategias]

    FA --> E1[Distribución uniforme:<br/>ALWAYS_H: 225,920<br/>ALWAYS_A: 225,920<br/>FOLLOW_FAV: 225,920<br/>UNDERDOG: 225,920]

    style DES fill:#ccffcc,stroke:#333,stroke-width:3px
    style FA fill:#ff9999,stroke:#333,stroke-width:2px
    style FAR fill:#99ccff,stroke:#333,stroke-width:2px,stroke-dasharray: 5 5
```

**Características de Relación:**
- **Tipo**: 1 a Muchos (1:N)
- **Obligatoriedad**: Obligatoria en FACT_APUESTAS (NOT NULL)
- **Exclusividad**: Solo relacionada con FACT_APUESTAS
- **Distribución**: Exactamente uniforme (cada estrategia tiene misma cantidad)
- **Generación**: Multiplicador 4x en ETL

---

### DIM_RESULTADO_TIPO - Relación Exclusiva

```mermaid
graph TB
    DRT[DIM_RESULTADO_TIPO<br/>3 resultados: H, D, A]

    DRT -->|R7: 1:N| FA[FACT_APUESTAS<br/>id_resultado_tipo<br/>~301,227 hechos/resultado]

    DRT -.->|NO relacionada| FAR[FACT_ARBITRAJE<br/>No usa tipo resultado]

    FA --> D1[Distribución:<br/>H Home: ~301,227 33.3%<br/>D Draw: ~301,227 33.3%<br/>A Away: ~301,227 33.3%]

    style DRT fill:#ccffcc,stroke:#333,stroke-width:3px
    style FA fill:#ff9999,stroke:#333,stroke-width:2px
    style FAR fill:#99ccff,stroke:#333,stroke-width:2px,stroke-dasharray: 5 5
```

**Características de Relación:**
- **Tipo**: 1 a Muchos (1:N)
- **Obligatoriedad**: Obligatoria en FACT_APUESTAS (NOT NULL)
- **Exclusividad**: Solo relacionada con FACT_APUESTAS
- **Distribución**: Exactamente uniforme (cada resultado tiene misma cantidad)
- **Valores Fijos**: Solo 3 valores posibles (H, D, A)

---

## Cardinalidades Detalladas

### Tabla de Cardinalidades por Dimensión

```mermaid
graph TB
    subgraph "CARDINALIDADES FACT_APUESTAS"
        FA[903,680 registros totales]

        FA -->|÷ 2,920 fechas| CF1[≈ 310 registros/fecha]
        FA -->|÷ 11 ligas| CF2[≈ 82,153 registros/liga]
        FA -->|÷ 400 equipos| CF3[≈ 2,260 registros/equipo]
        FA -->|÷ 10 casas| CF4[≈ 90,368 registros/casa]
        FA -->|÷ 4 estrategias| CF5[≈ 225,920 registros/estrategia]
        FA -->|÷ 3 resultados| CF6[≈ 301,227 registros/resultado]
    end

    subgraph "CARDINALIDADES FACT_ARBITRAJE"
        FAR[22,592 registros totales]

        FAR -->|÷ 2,920 fechas| CAR1[≈ 8 registros/fecha]
        FAR -->|÷ 11 ligas| CAR2[≈ 2,054 registros/liga]
        FAR -->|÷ 400 equipos| CAR3[≈ 56 registros/equipo]
        FAR -->|÷ 10 casas| CAR4[≈ 2,259 veces mejor/casa]
    end

    style FA fill:#ff9999,stroke:#333,stroke-width:2px
    style FAR fill:#99ccff,stroke:#333,stroke-width:2px
```

### Matriz Numérica de Cardinalidades

| Dimensión | Registros Dim | FACT_APUESTAS (N) | Promedio | FACT_ARBITRAJE (N) | Promedio |
|-----------|---------------|-------------------|----------|---------------------|----------|
| **DIM_FECHA** | 2,920 | 903,680 | 310 | 22,592 | 8 |
| **DIM_LIGA** | 11 | 903,680 | 82,153 | 22,592 | 2,054 |
| **DIM_EQUIPO (local)** | ~400 | 903,680 | 2,260 | 22,592 | 56 |
| **DIM_EQUIPO (visit)** | ~400 | 903,680 | 2,260 | 22,592 | 56 |
| **DIM_CASA_APUESTAS** | 10 | 903,680 | 90,368 | - | - |
| **DIM_CASA (mejores)** | 10 | - | - | 67,776 | 6,778 |
| **DIM_ESTRATEGIA** | 4 | 903,680 | 225,920 | - | - |
| **DIM_RESULTADO_TIPO** | 3 | 903,680 | 301,227 | - | - |

---

## Dimensiones Conformadas vs Exclusivas

```mermaid
graph TB
    subgraph "DIMENSIONES CONFORMADAS (Compartidas)"
        DC1[DIM_FECHA<br/>Usada por ambas facts]
        DC2[DIM_LIGA<br/>Usada por ambas facts]
        DC3[DIM_EQUIPO<br/>Usada por ambas facts<br/>Role-playing: local + visitante]
    end

    subgraph "DIMENSIONES EXCLUSIVAS FACT_APUESTAS"
        DE1[DIM_CASA_APUESTAS<br/>Solo id_casa_apuestas directo]
        DE2[DIM_ESTRATEGIA<br/>Solo en FACT_APUESTAS]
        DE3[DIM_RESULTADO_TIPO<br/>Solo en FACT_APUESTAS]
    end

    subgraph "DIMENSIONES EXCLUSIVAS FACT_ARBITRAJE"
        DE4[DIM_CASA_APUESTAS<br/>Solo FK mejores cuotas:<br/>casa_local_mejor<br/>casa_empate_mejor<br/>casa_visitante_mejor]
    end

    DC1 & DC2 & DC3 --> DRILL[Permiten<br/>DRILL-ACROSS<br/>entre tablas de hechos]

    style DC1 fill:#ffeb99,stroke:#333,stroke-width:3px
    style DC2 fill:#ffeb99,stroke:#333,stroke-width:3px
    style DC3 fill:#ffeb99,stroke:#333,stroke-width:3px
    style DE1 fill:#ffcccc,stroke:#333,stroke-width:2px
    style DE2 fill:#ffcccc,stroke:#333,stroke-width:2px
    style DE3 fill:#ffcccc,stroke:#333,stroke-width:2px
    style DE4 fill:#99ccff,stroke:#333,stroke-width:2px
    style DRILL fill:#ccffcc,stroke:#333,stroke-width:3px
```

---

## Integridad Referencial

### Políticas de Borrado y Actualización

```mermaid
graph TB
    subgraph "POLÍTICAS ON DELETE CASCADE"
        P1[Si se borra 1 fecha<br/>→ Se borran todos sus hechos]
        P2[Si se borra 1 liga<br/>→ Se borran todos sus hechos]
        P3[Si se borra 1 equipo<br/>→ Se borran todos sus hechos]
        P4[Si se borra 1 casa<br/>→ Se borran todos sus hechos]
    end

    subgraph "POLÍTICAS ON UPDATE CASCADE"
        U1[Si cambia PK de dimensión<br/>→ Se actualiza FK en hechos<br/>automáticamente]
    end

    subgraph "RESTRICCIONES CHECK"
        C1[id_equipo_local ≠ id_equipo_visitante<br/>Un equipo no juega vs sí mismo]
        C2[fecha BETWEEN inicio AND fin<br/>Validación temporal SCD-2]
        C3[cuota > 1.0<br/>Las cuotas son mayores a 1]
    end

    style P1 fill:#ffcccc,stroke:#333,stroke-width:2px
    style P2 fill:#ffcccc,stroke:#333,stroke-width:2px
    style P3 fill:#ffcccc,stroke:#333,stroke-width:2px
    style P4 fill:#ffcccc,stroke:#333,stroke-width:2px
    style U1 fill:#ffffcc,stroke:#333,stroke-width:2px
    style C1 fill:#ccffcc,stroke:#333,stroke-width:2px
    style C2 fill:#ccffcc,stroke:#333,stroke-width:2px
    style C3 fill:#ccffcc,stroke:#333,stroke-width:2px
```

### Definición DDL de Constraints

```sql
-- FACT_APUESTAS Constraints
ALTER TABLE FACT_APUESTAS
    ADD CONSTRAINT FK_APUESTAS_FECHA
        FOREIGN KEY (id_fecha)
        REFERENCES DIM_FECHA(id_fecha)
        ON DELETE CASCADE
        ON UPDATE CASCADE;

ALTER TABLE FACT_APUESTAS
    ADD CONSTRAINT FK_APUESTAS_LIGA
        FOREIGN KEY (id_liga)
        REFERENCES DIM_LIGA(id_liga)
        ON DELETE CASCADE
        ON UPDATE CASCADE;

ALTER TABLE FACT_APUESTAS
    ADD CONSTRAINT FK_APUESTAS_EQUIPO_LOCAL
        FOREIGN KEY (id_equipo_local)
        REFERENCES DIM_EQUIPO(id_equipo)
        ON DELETE CASCADE
        ON UPDATE CASCADE;

ALTER TABLE FACT_APUESTAS
    ADD CONSTRAINT FK_APUESTAS_EQUIPO_VISITANTE
        FOREIGN KEY (id_equipo_visitante)
        REFERENCES DIM_EQUIPO(id_equipo)
        ON DELETE CASCADE
        ON UPDATE CASCADE;

ALTER TABLE FACT_APUESTAS
    ADD CONSTRAINT FK_APUESTAS_CASA
        FOREIGN KEY (id_casa_apuestas)
        REFERENCES DIM_CASA_APUESTAS(id_casa_apuestas)
        ON DELETE CASCADE
        ON UPDATE CASCADE;

ALTER TABLE FACT_APUESTAS
    ADD CONSTRAINT FK_APUESTAS_ESTRATEGIA
        FOREIGN KEY (id_estrategia)
        REFERENCES DIM_ESTRATEGIA(id_estrategia)
        ON DELETE CASCADE
        ON UPDATE CASCADE;

ALTER TABLE FACT_APUESTAS
    ADD CONSTRAINT FK_APUESTAS_RESULTADO
        FOREIGN KEY (id_resultado_tipo)
        REFERENCES DIM_RESULTADO_TIPO(id_resultado_tipo)
        ON DELETE CASCADE
        ON UPDATE CASCADE;

-- CHECK Constraints FACT_APUESTAS
ALTER TABLE FACT_APUESTAS
    ADD CONSTRAINT CHK_EQUIPOS_DIFERENTES
        CHECK (id_equipo_local != id_equipo_visitante);

ALTER TABLE FACT_APUESTAS
    ADD CONSTRAINT CHK_CUOTA_VALIDA
        CHECK (cuota_apostada >= 1.0);

-- FACT_ARBITRAJE Constraints
ALTER TABLE FACT_ARBITRAJE
    ADD CONSTRAINT FK_ARBITRAJE_FECHA
        FOREIGN KEY (id_fecha)
        REFERENCES DIM_FECHA(id_fecha)
        ON DELETE CASCADE
        ON UPDATE CASCADE;

ALTER TABLE FACT_ARBITRAJE
    ADD CONSTRAINT FK_ARBITRAJE_LIGA
        FOREIGN KEY (id_liga)
        REFERENCES DIM_LIGA(id_liga)
        ON DELETE CASCADE
        ON UPDATE CASCADE;

ALTER TABLE FACT_ARBITRAJE
    ADD CONSTRAINT FK_ARBITRAJE_EQUIPO_LOCAL
        FOREIGN KEY (id_equipo_local)
        REFERENCES DIM_EQUIPO(id_equipo)
        ON DELETE CASCADE
        ON UPDATE CASCADE;

ALTER TABLE FACT_ARBITRAJE
    ADD CONSTRAINT FK_ARBITRAJE_EQUIPO_VISITANTE
        FOREIGN KEY (id_equipo_visitante)
        REFERENCES DIM_EQUIPO(id_equipo)
        ON DELETE CASCADE
        ON UPDATE CASCADE;

ALTER TABLE FACT_ARBITRAJE
    ADD CONSTRAINT FK_ARBITRAJE_CASA_LOCAL
        FOREIGN KEY (casa_local_mejor)
        REFERENCES DIM_CASA_APUESTAS(id_casa_apuestas)
        ON DELETE CASCADE
        ON UPDATE CASCADE;

ALTER TABLE FACT_ARBITRAJE
    ADD CONSTRAINT FK_ARBITRAJE_CASA_EMPATE
        FOREIGN KEY (casa_empate_mejor)
        REFERENCES DIM_CASA_APUESTAS(id_casa_apuestas)
        ON DELETE CASCADE
        ON UPDATE CASCADE;

ALTER TABLE FACT_ARBITRAJE
    ADD CONSTRAINT FK_ARBITRAJE_CASA_VISITANTE
        FOREIGN KEY (casa_visitante_mejor)
        REFERENCES DIM_CASA_APUESTAS(id_casa_apuestas)
        ON DELETE CASCADE
        ON UPDATE CASCADE;

-- CHECK Constraints FACT_ARBITRAJE
ALTER TABLE FACT_ARBITRAJE
    ADD CONSTRAINT CHK_ARB_EQUIPOS_DIFERENTES
        CHECK (id_equipo_local != id_equipo_visitante);

ALTER TABLE FACT_ARBITRAJE
    ADD CONSTRAINT CHK_ARB_CUOTAS_VALIDAS
        CHECK (cuota_local_max >= 1.0
           AND cuota_empate_max >= 1.0
           AND cuota_visitante_max >= 1.0);
```

---

## Índices para Optimización de Joins

```mermaid
graph TB
    subgraph "ÍNDICES FACT_APUESTAS"
        I1[PK Clustered:<br/>6 columnas compuestas<br/>fecha + equipos + casa + estrategia + resultado]

        I2[Non-Clustered:<br/>id_fecha covering<br/>Para queries temporales]

        I3[Non-Clustered:<br/>id_liga covering<br/>Para queries por liga]

        I4[Non-Clustered:<br/>id_casa_apuestas covering<br/>Para análisis por casa]

        I5[Non-Clustered:<br/>id_estrategia covering<br/>Para análisis por estrategia]
    end

    subgraph "ÍNDICES FACT_ARBITRAJE"
        I6[PK Clustered:<br/>4 columnas compuestas<br/>fecha + equipos + liga]

        I7[Non-Clustered:<br/>es_oportunidad covering<br/>Para filtrar oportunidades]

        I8[Non-Clustered:<br/>id_fecha + id_liga<br/>Para queries drill-across]
    end

    style I1 fill:#ff9999,stroke:#333,stroke-width:3px
    style I6 fill:#99ccff,stroke:#333,stroke-width:3px
```

---

## Drill-Across con Dimensiones Conformadas

```mermaid
graph TB
    Q[Query Drill-Across:<br/>Comparar ROI vs Oportunidades<br/>por Liga y Temporada]

    Q --> Q1[Subconsulta 1:<br/>FACT_APUESTAS<br/>→ DIM_FECHA<br/>→ DIM_LIGA<br/>Calcular ROI]

    Q --> Q2[Subconsulta 2:<br/>FACT_ARBITRAJE<br/>→ DIM_FECHA<br/>→ DIM_LIGA<br/>Calcular Oportunidades]

    Q1 & Q2 --> JOIN[JOIN en dimensiones conformadas:<br/>fecha.temporada + liga.nombre]

    JOIN --> RES[Resultado combinado:<br/>Liga | Temporada | ROI | Oportunidades]

    style Q fill:#e1f5ff,stroke:#333,stroke-width:3px
    style Q1 fill:#ff9999,stroke:#333,stroke-width:2px
    style Q2 fill:#99ccff,stroke:#333,stroke-width:2px
    style JOIN fill:#ffeb99,stroke:#333,stroke-width:3px
    style RES fill:#ccffcc,stroke:#333,stroke-width:2px
```

**Ejemplo SQL Drill-Across:**
```sql
SELECT
    l.nombre_liga,
    f.temporada,
    ap.roi_promedio,
    arb.cant_oportunidades
FROM DIM_LIGA l
JOIN DIM_FECHA f ON 1=1  -- Cross join controlado
LEFT JOIN (
    -- Subconsulta FACT_APUESTAS
    SELECT
        id_liga,
        id_fecha,
        AVG(roi_porcentaje) as roi_promedio
    FROM FACT_APUESTAS
    GROUP BY id_liga, id_fecha
) ap ON ap.id_liga = l.id_liga AND ap.id_fecha = f.id_fecha
LEFT JOIN (
    -- Subconsulta FACT_ARBITRAJE
    SELECT
        id_liga,
        id_fecha,
        SUM(cant_oportunidades) as cant_oportunidades
    FROM FACT_ARBITRAJE
    WHERE es_oportunidad = TRUE
    GROUP BY id_liga, id_fecha
) arb ON arb.id_liga = l.id_liga AND arb.id_fecha = f.id_fecha
ORDER BY l.nombre_liga, f.temporada;
```

---

## Resumen Ejecutivo de Relaciones

### Totales por Tabla

| Tabla | Total FK | Dimensiones Relacionadas | Role-Playing | Tipo Relaciones |
|-------|----------|--------------------------|--------------|-----------------|
| **FACT_APUESTAS** | 7 | 6 dimensiones | 1 (DIM_EQUIPO) | 1:N todas |
| **FACT_ARBITRAJE** | 7 | 2 dimensiones base | 2 (DIM_EQUIPO + DIM_CASA) | 1:N todas |

### Clasificación de Relaciones

```mermaid
pie title "Distribución de Relaciones por Tipo"
    "Conformadas (compartidas)" : 6
    "Exclusivas FACT_APUESTAS" : 3
    "Exclusivas FACT_ARBITRAJE (mejores)" : 3
    "Role-Playing" : 2
```

### Beneficios del Diseño

| Beneficio | Descripción |
|-----------|-------------|
| **Dimensiones Conformadas** | Permite drill-across entre FACT_APUESTAS y FACT_ARBITRAJE |
| **Integridad Referencial** | Garantiza consistencia con CASCADE constraints |
| **Role-Playing** | Reutiliza DIM_EQUIPO para local y visitante eficientemente |
| **Índices Optimizados** | Joins rápidos con índices covering en FK |
| **Cardinalidad Equilibrada** | Distribución uniforme en dimensiones calculadas |

---

**Diagrama 3d - Relaciones y Cardinalidades Completo** ✅
