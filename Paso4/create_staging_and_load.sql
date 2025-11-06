-- ==========================================================
-- SCRIPT: create_staging_FIXED.sql
-- Proyecto: Data Warehouse Apuestas Deportivas (HEFESTO)
-- Autor: Facundo Ortega
-- Descripción: Crea staging area y carga CSVs (VERSIÓN CORREGIDA)
-- ==========================================================

-- ==========================================================
-- 🔹 0. CREAR BASE DE DATOS
-- ==========================================================
DROP DATABASE IF EXISTS apuestas_dw;
CREATE DATABASE apuestas_dw
  CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;

USE apuestas_dw;

-- ==========================================================
-- 🔹 1. TABLAS STAGING (Área temporal para CSVs)
-- ==========================================================

-- 🔸 STG_COUNTRY
DROP TABLE IF EXISTS stg_country;
CREATE TABLE stg_country (
  id INT PRIMARY KEY,
  name VARCHAR(100)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- IMPORTANTE: Ajusta la ruta según tu sistema
-- Linux/Mac: '/ruta/absoluta/export_csv/Country.csv'
-- Windows:   'C:/ruta/absoluta/export_csv/Country.csv'

LOAD DATA LOCAL INFILE '/home/facundo/Documents/4to/basedatos2/repo/BD2_Hefesto_ApuetasDeportivas/Paso4/export_csv/Country.csv'
INTO TABLE stg_country
FIELDS TERMINATED BY ',' 
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(id, name);

-- 🔸 STG_LEAGUE
DROP TABLE IF EXISTS stg_league;
CREATE TABLE stg_league (
  id INT PRIMARY KEY,
  country_id INT,
  name VARCHAR(100)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

LOAD DATA LOCAL INFILE '/home/facundo/Documents/4to/basedatos2/repo/BD2_Hefesto_ApuetasDeportivas/Paso4/export_csv/League.csv'
INTO TABLE stg_league
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(id, country_id, name);

-- 🔸 STG_TEAM
DROP TABLE IF EXISTS stg_team;
CREATE TABLE stg_team (
  id INT PRIMARY KEY,
  team_api_id INT,
  team_fifa_api_id INT,
  team_long_name VARCHAR(100),
  team_short_name VARCHAR(20)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

LOAD DATA LOCAL INFILE '/home/facundo/Documents/4to/basedatos2/repo/BD2_Hefesto_ApuetasDeportivas/Paso4/export_csv/Team.csv'
INTO TABLE stg_team
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(id, team_api_id, @fifa_id, team_long_name, team_short_name)
SET team_fifa_api_id = NULLIF(@fifa_id, '');

-- 🔸 STG_MATCH (tabla más compleja)
DROP TABLE IF EXISTS stg_match;
CREATE TABLE stg_match (
  id INT PRIMARY KEY,
  country_id INT,
  league_id INT,
  season VARCHAR(20),
  stage INT,
  date DATETIME,
  match_api_id INT,
  home_team_api_id INT,
  away_team_api_id INT,
  home_team_goal INT,
  away_team_goal INT,
  B365H DECIMAL(6,2),
  B365D DECIMAL(6,2),
  B365A DECIMAL(6,2),
  BWH DECIMAL(6,2),
  BWD DECIMAL(6,2),
  BWA DECIMAL(6,2),
  IWH DECIMAL(6,2),
  IWD DECIMAL(6,2),
  IWA DECIMAL(6,2),
  PSH DECIMAL(6,2),
  PSD DECIMAL(6,2),
  PSA DECIMAL(6,2)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

LOAD DATA LOCAL INFILE '/home/facundo/Documents/4to/basedatos2/repo/BD2_Hefesto_ApuetasDeportivas/Paso4/export_csv/Match.csv'
INTO TABLE stg_match
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(id, country_id, league_id, season, stage, @date, match_api_id,
 home_team_api_id, away_team_api_id, home_team_goal, away_team_goal,
 B365H, B365D, B365A, BWH, BWD, BWA, IWH, IWD, IWA, PSH, PSD, PSA)
SET date = STR_TO_DATE(@date, '%Y-%m-%d %H:%i:%s');

-- ==========================================================
-- 🔹 2. VALIDACIÓN DE CARGA STAGING
-- ==========================================================
SELECT '🔍 VALIDACIÓN DE STAGING' AS '━━━━━━━━━━━━━━━━━━━━';

SELECT 
  'Country' AS tabla,
  COUNT(*) AS registros,
  COUNT(DISTINCT id) AS ids_unicos
FROM stg_country
UNION ALL
SELECT 
  'League',
  COUNT(*),
  COUNT(DISTINCT id)
FROM stg_league
UNION ALL
SELECT 
  'Team',
  COUNT(*),
  COUNT(DISTINCT id)
FROM stg_team
UNION ALL
SELECT 
  'Match',
  COUNT(*),
  COUNT(DISTINCT id)
FROM stg_match;

-- Verificar integridad de cuotas
SELECT 
  '✅ Registros con cuotas completas' AS verificacion,
  COUNT(*) AS cantidad
FROM stg_match
WHERE B365H IS NOT NULL AND B365D IS NOT NULL AND B365A IS NOT NULL;

-- ==========================================================
-- 🔹 3. DIMENSIONES DEL DATA WAREHOUSE
-- ==========================================================

-- 📅 DIM_FECHA (generada automáticamente)
DROP TABLE IF EXISTS dim_fecha;
CREATE TABLE dim_fecha (
  id_fecha INT PRIMARY KEY,
  fecha DATE NOT NULL,
  anio SMALLINT NOT NULL,
  mes TINYINT NOT NULL,
  nombre_mes VARCHAR(20),
  temporada VARCHAR(10)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Procedimiento para poblar fechas
DELIMITER $$
DROP PROCEDURE IF EXISTS poblar_dim_fecha$$
CREATE PROCEDURE poblar_dim_fecha()
BEGIN
  DECLARE d DATE DEFAULT '2008-01-01';
  DECLARE temp VARCHAR(10);
  
  WHILE d <= '2016-12-31' DO
    -- Calcular temporada (Agosto=inicio)
    IF MONTH(d) >= 8 THEN
      SET temp = CONCAT(YEAR(d), '/', RIGHT(YEAR(d)+1, 2));
    ELSE
      SET temp = CONCAT(YEAR(d)-1, '/', RIGHT(YEAR(d), 2));
    END IF;
    
    INSERT IGNORE INTO dim_fecha 
    VALUES (
      YEAR(d)*10000 + MONTH(d)*100 + DAY(d),
      d,
      YEAR(d),
      MONTH(d),
      MONTHNAME(d),
      temp
    );
    SET d = DATE_ADD(d, INTERVAL 1 DAY);
  END WHILE;
END$$
DELIMITER ;

CALL poblar_dim_fecha();

-- 🏠 DIM_CASA_APUESTAS
DROP TABLE IF EXISTS dim_casa_apuestas;
CREATE TABLE dim_casa_apuestas (
  id_casa TINYINT PRIMARY KEY AUTO_INCREMENT,
  nombre VARCHAR(50) NOT NULL,
  codigo VARCHAR(10) NOT NULL UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO dim_casa_apuestas (nombre, codigo) VALUES
('Bet365', 'B365'),
('Bet&Win', 'BW'),
('Interwetten', 'IW'),
('Pinnacle Sports', 'PS');

-- 🌍 DIM_COUNTRY
DROP TABLE IF EXISTS dim_country;
CREATE TABLE dim_country (
  id_country INT PRIMARY KEY,
  name VARCHAR(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO dim_country (id_country, name)
SELECT id, name FROM stg_country;

-- 🏆 DIM_LEAGUE
DROP TABLE IF EXISTS dim_league;
CREATE TABLE dim_league (
  id_league INT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  id_country INT NOT NULL,
  FOREIGN KEY (id_country) REFERENCES dim_country(id_country)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO dim_league (id_league, name, id_country)
SELECT id, name, country_id FROM stg_league;

-- ⚽ DIM_TEAM
DROP TABLE IF EXISTS dim_team;
CREATE TABLE dim_team (
  id_team INT PRIMARY KEY,
  team_long_name VARCHAR(100) NOT NULL,
  team_short_name VARCHAR(20)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO dim_team (id_team, team_long_name, team_short_name)
SELECT team_api_id, team_long_name, team_short_name 
FROM stg_team;

-- ==========================================================
-- 🔹 4. TABLA DE HECHOS (estructura básica)
-- ==========================================================
DROP TABLE IF EXISTS fact_apuestas;
CREATE TABLE fact_apuestas (
  id_fact INT AUTO_INCREMENT PRIMARY KEY,
  id_fecha INT NOT NULL,
  id_casa TINYINT NOT NULL,
  id_league INT NOT NULL,
  id_home_team INT NOT NULL,
  id_away_team INT NOT NULL,
  home_team_goal TINYINT,
  away_team_goal TINYINT,
  resultado CHAR(1),
  cuota_local DECIMAL(6,2),
  cuota_empate DECIMAL(6,2),
  cuota_visitante DECIMAL(6,2),
  
  FOREIGN KEY (id_fecha) REFERENCES dim_fecha(id_fecha),
  FOREIGN KEY (id_casa) REFERENCES dim_casa_apuestas(id_casa),
  FOREIGN KEY (id_league) REFERENCES dim_league(id_league),
  FOREIGN KEY (id_home_team) REFERENCES dim_team(id_team),
  FOREIGN KEY (id_away_team) REFERENCES dim_team(id_team),
  
  INDEX idx_fecha (id_fecha),
  INDEX idx_casa (id_casa),
  INDEX idx_league (id_league)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ==========================================================
-- 🔹 5. RESUMEN FINAL
-- ==========================================================
SELECT '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━' AS '';
SELECT '✅ DATA WAREHOUSE CREADO EXITOSAMENTE' AS estado;
SELECT '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━' AS '';

SELECT 
  'dim_fecha' AS dimension,
  COUNT(*) AS registros
FROM dim_fecha
UNION ALL
SELECT 'dim_casa_apuestas', COUNT(*) FROM dim_casa_apuestas
UNION ALL
SELECT 'dim_country', COUNT(*) FROM dim_country
UNION ALL
SELECT 'dim_league', COUNT(*) FROM dim_league
UNION ALL
SELECT 'dim_team', COUNT(*) FROM dim_team;

SELECT '📊 Listo para ejecutar etl_apuestas.py' AS siguiente_paso;