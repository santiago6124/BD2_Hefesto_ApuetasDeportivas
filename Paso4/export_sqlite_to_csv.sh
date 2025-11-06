#!/bin/bash
# ============================================================
# Script: export_sqlite_to_csv_FIXED.sh
# Proyecto: Data Warehouse Apuestas Deportivas (HEFESTO)
# Autor: Facundo Ortega
# Descripción: Exporta tablas de database.sqlite a CSV (CORREGIDO)
# ============================================================

# ⚙️ CONFIGURACIÓN (ajusta según tu estructura)
DB_FILE="./database.sqlite"  # Si ejecutas desde Paso4/
EXPORT_DIR="./export_csv"     # Carpeta destino

# Crear carpeta si no existe
mkdir -p "$EXPORT_DIR"

# ✅ Verificar existencia de la base
if [ ! -f "$DB_FILE" ]; then
    echo "❌ ERROR: No se encontró $DB_FILE"
    echo "📁 Revisa que la ruta sea correcta desde donde ejecutas el script"
    exit 1
fi

echo "✅ Base de datos encontrada: $DB_FILE"
echo "📂 Exportando a: $EXPORT_DIR"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 🔹 Exportar COUNTRY
sqlite3 "$DB_FILE" <<EOF
.headers on
.mode csv
.output $EXPORT_DIR/Country.csv
SELECT * FROM Country;
.quit
EOF
echo "✓ Country.csv exportado"

# 🔹 Exportar LEAGUE
sqlite3 "$DB_FILE" <<EOF
.headers on
.mode csv
.output $EXPORT_DIR/League.csv
SELECT * FROM League;
.quit
EOF
echo "✓ League.csv exportado"

# 🔹 Exportar TEAM
sqlite3 "$DB_FILE" <<EOF
.headers on
.mode csv
.output $EXPORT_DIR/Team.csv
SELECT * FROM Team;
.quit
EOF
echo "✓ Team.csv exportado"

# 🔹 Exportar MATCH (solo columnas necesarias)
sqlite3 "$DB_FILE" <<EOF
.headers on
.mode csv
.output $EXPORT_DIR/Match.csv
SELECT
    id,
    country_id,
    league_id,
    season,
    stage,
    date,
    match_api_id,
    home_team_api_id,
    away_team_api_id,
    home_team_goal,
    away_team_goal,
    B365H, B365D, B365A,
    BWH, BWD, BWA,
    IWH, IWD, IWA,
    PSH, PSD, PSA
FROM Match
WHERE B365H IS NOT NULL 
  AND B365D IS NOT NULL 
  AND B365A IS NOT NULL;
.quit
EOF
echo "✓ Match.csv exportado (solo registros completos)"

# 🔧 Normalizar saltos de línea a formato UNIX
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔧 Normalizando formato de archivos..."

for file in "$EXPORT_DIR"/*.csv; do
    if [ -f "$file" ]; then
        # Convertir Windows (CRLF) a Unix (LF)
        sed -i 's/\r$//' "$file" 2>/dev/null || sed -i '' 's/\r$//' "$file"
        echo "   ✓ $(basename "$file")"
    fi
done

# 📊 Resumen
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ EXPORTACIÓN COMPLETADA"
echo "📂 Archivos generados:"
ls -lh "$EXPORT_DIR"/*.csv
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🔍 Verificación rápida de registros:"
for file in "$EXPORT_DIR"/*.csv; do
    lines=$(wc -l < "$file")
    echo "   $(basename "$file"): $((lines - 1)) registros"
done