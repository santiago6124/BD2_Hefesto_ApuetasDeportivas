-- ==========================================================
-- SCRIPT: create_dw_WINDOWS.sql (ADAPTADO PARA WINDOWS)
-- Proyecto: Data Warehouse Apuestas Deportivas (HEFESTO)
-- Base: Esquema ESTRELLA con campos derivados de arbitraje
-- Fecha: Noviembre 2025
-- ==========================================================

-- ==========================================================
-- 0. CREAR BASE DE DATOS
-- ==========================================================
DROP DATABASE IF EXISTS apuestas_dw;
CREATE DATABASE apuestas_dw
  CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;

USE apuestas_dw;

-- ==========================================================
-- 1. DIMENSIONES
-- ==========================================================

-- DIM_FECHA (Dimensión Temporal)
DROP TABLE IF EXISTS DIM_FECHA;
CREATE TABLE DIM_FECHA (
    id_fecha INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
    fecha DATE NOT NULL UNIQUE,
    dia TINYINT NOT NULL,
    mes TINYINT NOT NULL,
    anio SMALLINT NOT NULL,
    trimestre TINYINT NOT NULL,
    nombre_mes VARCHAR(20) NOT NULL,
    nombre_dia_semana VARCHAR(20) NOT NULL,
    temporada VARCHAR(10) NOT NULL,
    es_fin_semana BOOLEAN NOT NULL,

    INDEX idx_fecha_fecha (fecha),
    INDEX idx_fecha_temporada (temporada),
    INDEX idx_fecha_anio_mes (anio, mes)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Dimensión temporal con jerarquías';

-- DIM_LIGA (Dimensión Geográfica)
DROP TABLE IF EXISTS DIM_LIGA;
CREATE TABLE DIM_LIGA (
    id_liga INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
    codigo_liga VARCHAR(50) UNIQUE,
    nombre_liga VARCHAR(100) NOT NULL,
    pais VARCHAR(100) NOT NULL,
    nivel_competicion TINYINT DEFAULT 1,

    INDEX idx_liga_pais (pais),
    INDEX idx_liga_nombre (nombre_liga)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Ligas de fútbol europeo';

-- DIM_EQUIPO (Dimensión con SCD Tipo 2)
DROP TABLE IF EXISTS DIM_EQUIPO;
CREATE TABLE DIM_EQUIPO (
    id_equipo INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
    codigo_equipo INTEGER NOT NULL,
    nombre_equipo VARCHAR(100) NOT NULL,
    nombre_corto VARCHAR(50),
    id_liga INTEGER NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE,
    registro_actual BOOLEAN NOT NULL DEFAULT TRUE,

    INDEX idx_equipo_codigo (codigo_equipo),
    INDEX idx_equipo_actual (registro_actual),
    INDEX idx_equipo_liga (id_liga),
    FOREIGN KEY (id_liga) REFERENCES DIM_LIGA(id_liga)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Equipos con versionado temporal (SCD-2)';

-- DIM_CASA_APUESTAS (Dimensión Descriptiva)
DROP TABLE IF EXISTS DIM_CASA_APUESTAS;
CREATE TABLE DIM_CASA_APUESTAS (
    id_casa_apuestas INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
    codigo_casa VARCHAR(10) NOT NULL UNIQUE,
    nombre_completo VARCHAR(100) NOT NULL,
    pais_origen VARCHAR(50),

    INDEX idx_casa_codigo (codigo_casa)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Casas de apuestas (10 casas)';

-- DIM_ESTRATEGIA (Dimensión de Análisis)
DROP TABLE IF EXISTS DIM_ESTRATEGIA;
CREATE TABLE DIM_ESTRATEGIA (
    id_estrategia INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
    codigo_estrategia VARCHAR(20) NOT NULL UNIQUE,
    nombre_estrategia VARCHAR(100) NOT NULL,
    descripcion TEXT,

    INDEX idx_estrategia_codigo (codigo_estrategia)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Estrategias de apuesta (4 estrategias)';

-- DIM_RESULTADO_TIPO (Dimensión Pequeña)
DROP TABLE IF EXISTS DIM_RESULTADO_TIPO;
CREATE TABLE DIM_RESULTADO_TIPO (
    id_resultado_tipo INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
    codigo_resultado CHAR(1) NOT NULL UNIQUE,
    tipo_resultado VARCHAR(50) NOT NULL,
    descripcion VARCHAR(100),

    INDEX idx_resultado_codigo (codigo_resultado)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Tipos de resultado (H/D/A)';

-- ==========================================================
-- 2. TABLA DE HECHOS CONSOLIDADA (ESQUEMA ESTRELLA)
-- ==========================================================

DROP TABLE IF EXISTS FACT_APUESTAS;
CREATE TABLE FACT_APUESTAS (
    -- CLAVE PRIMARIA COMPUESTA
    id_fecha INTEGER NOT NULL,
    id_equipo_local INTEGER NOT NULL,
    id_equipo_visitante INTEGER NOT NULL,
    id_liga INTEGER NOT NULL,
    id_casa_apuestas INTEGER NOT NULL,
    id_estrategia INTEGER NOT NULL,
    id_resultado_tipo INTEGER NOT NULL,

    -- CONTEXTO ADICIONAL
    id_partido INTEGER NOT NULL,
    goles_local TINYINT NOT NULL,
    goles_visitante TINYINT NOT NULL,
    resultado_real CHAR(1) NOT NULL,

    -- CUOTAS ORIGINALES (Semi-Aditivas)
    cuota_apostada DECIMAL(6,3) NOT NULL,
    cuota_local DECIMAL(6,3) NOT NULL,
    cuota_empate DECIMAL(6,3) NOT NULL,
    cuota_visitante DECIMAL(6,3) NOT NULL,

    -- MÉTRICAS DE APUESTAS (Aditivas)
    ganancia_total DECIMAL(10,2) NOT NULL DEFAULT 0,
    perdida_total DECIMAL(10,2) NOT NULL DEFAULT 0,
    inversion DECIMAL(10,2) NOT NULL DEFAULT 1,
    cant_aciertos TINYINT NOT NULL DEFAULT 0,
    cant_apuestas TINYINT NOT NULL DEFAULT 1,

    -- CAMPOS DERIVADOS DE ARBITRAJE (Pre-calculados en ETL)
    arbitraje_cuota_local_max DECIMAL(6,3),
    arbitraje_cuota_empate_max DECIMAL(6,3),
    arbitraje_cuota_visitante_max DECIMAL(6,3),
    arbitraje_casa_local_mejor INTEGER,
    arbitraje_casa_empate_mejor INTEGER,
    arbitraje_casa_visitante_mejor INTEGER,
    arbitraje_porcentaje DECIMAL(8,6),
    arbitraje_es_oportunidad BOOLEAN DEFAULT FALSE,
    arbitraje_beneficio DECIMAL(8,4) DEFAULT 0,

    -- CONSTRAINTS
    PRIMARY KEY (id_fecha, id_equipo_local, id_equipo_visitante,
                 id_casa_apuestas, id_estrategia, id_resultado_tipo),

    -- FOREIGN KEYS
    FOREIGN KEY (id_fecha) REFERENCES DIM_FECHA(id_fecha) ON DELETE CASCADE,
    FOREIGN KEY (id_liga) REFERENCES DIM_LIGA(id_liga) ON DELETE CASCADE,
    FOREIGN KEY (id_equipo_local) REFERENCES DIM_EQUIPO(id_equipo) ON DELETE CASCADE,
    FOREIGN KEY (id_equipo_visitante) REFERENCES DIM_EQUIPO(id_equipo) ON DELETE CASCADE,
    FOREIGN KEY (id_casa_apuestas) REFERENCES DIM_CASA_APUESTAS(id_casa_apuestas) ON DELETE CASCADE,
    FOREIGN KEY (id_estrategia) REFERENCES DIM_ESTRATEGIA(id_estrategia) ON DELETE CASCADE,
    FOREIGN KEY (id_resultado_tipo) REFERENCES DIM_RESULTADO_TIPO(id_resultado_tipo) ON DELETE CASCADE,

    -- ÍNDICES ESTÁNDAR
    INDEX idx_fact_fecha (id_fecha),
    INDEX idx_fact_liga (id_liga),
    INDEX idx_fact_casa (id_casa_apuestas),
    INDEX idx_fact_estrategia (id_estrategia),
    INDEX idx_fact_partido (id_partido),

    -- ÍNDICE FILTRADO PARA ARBITRAJE (Solo oportunidades reales)
    INDEX idx_fact_arbitraje (id_fecha, id_liga, arbitraje_beneficio, arbitraje_es_oportunidad),

    -- CHECKS
    CHECK (goles_local >= 0),
    CHECK (goles_visitante >= 0),
    CHECK (cuota_apostada > 0),
    CHECK (inversion > 0),
    CHECK (cant_apuestas > 0),
    CHECK (resultado_real IN ('H', 'D', 'A'))

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Tabla de hechos consolidada - Esquema ESTRELLA';

-- ==========================================================
-- 3. POBLAR DIMENSIONES CON DATOS INICIALES
-- ==========================================================

-- Poblar DIM_CASA_APUESTAS (10 casas)
INSERT INTO DIM_CASA_APUESTAS (codigo_casa, nombre_completo, pais_origen) VALUES
('B365', 'Bet365', 'Inglaterra'),
('BW', 'Bet&Win (bwin)', 'Austria'),
('IW', 'Interwetten', 'Austria'),
('LB', 'Ladbrokes', 'Inglaterra'),
('PS', 'Pinnacle Sports', 'Curazao'),
('WH', 'William Hill', 'Inglaterra'),
('SJ', 'Stan James', 'Inglaterra'),
('VC', 'Victor Chandler (BetVictor)', 'Gibraltar'),
('GB', 'Gamebookers', 'Inglaterra'),
('BS', 'Blue Square (Betfred)', 'Inglaterra');

-- Poblar DIM_ESTRATEGIA (4 estrategias)
INSERT INTO DIM_ESTRATEGIA (codigo_estrategia, nombre_estrategia, descripcion) VALUES
('ALWAYS_H', 'Siempre Local', 'Apostar siempre al equipo local'),
('ALWAYS_A', 'Siempre Visitante', 'Apostar siempre al equipo visitante'),
('FOLLOW_FAV', 'Seguir Favorito', 'Apostar al resultado con menor cuota (favorito)'),
('UNDERDOG', 'Apostar Underdog', 'Apostar al resultado con mayor cuota (menos favorito)');

-- Poblar DIM_RESULTADO_TIPO (3 tipos)
INSERT INTO DIM_RESULTADO_TIPO (codigo_resultado, tipo_resultado, descripcion) VALUES
('H', 'Local (Home)', 'Victoria del equipo local'),
('D', 'Empate (Draw)', 'Empate entre ambos equipos'),
('A', 'Visitante (Away)', 'Victoria del equipo visitante');

-- ==========================================================
-- 4. ESTADÍSTICAS Y VERIFICACIÓN
-- ==========================================================

SELECT 'Base de datos creada exitosamente' as Mensaje;

SELECT 'Tablas creadas:' as Info, COUNT(*) as Total
FROM information_schema.tables
WHERE table_schema = 'apuestas_dw';

SELECT table_name as Tabla, table_rows as Filas_Aproximadas
FROM information_schema.tables
WHERE table_schema = 'apuestas_dw'
ORDER BY table_name;

-- ==========================================================
-- LISTO PARA CARGA DE DATOS
-- ==========================================================
-- Siguiente paso: Ejecutar script Python etl_apuestas.py
-- para poblar DIM_FECHA, DIM_LIGA, DIM_EQUIPO y FACT_APUESTAS
-- desde los archivos CSV exportados de SQLite
-- ==========================================================
