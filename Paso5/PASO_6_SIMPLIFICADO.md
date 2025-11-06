# 📊 PASO 6 SIMPLIFICADO: Crear Medidas DAX

## ⏱️ Tiempo: 15 minutos | Elementos a crear: 21 (1 columna + 20 medidas)

---

## 🎯 PARTE 1: Crear Columna ID_Partido (1 elemento)

### ¿Qué es?
Una columna nueva que se agrega a la tabla `apuestas_dw fact_apuestas`.

### ¿Para qué sirve?
Para identificar partidos únicos (combinando fecha + equipo local + equipo visitante).

### ¿Cómo crearla?

1. En el panel derecho (Datos), buscar tabla: **`apuestas_dw fact_apuestas`**

2. **Clic derecho** en esa tabla

3. Seleccionar: **"Nueva columna"**

4. Copiar y pegar este código completo:
```dax
ID_Partido = 'apuestas_dw fact_apuestas'[id_fecha] & "-" & 'apuestas_dw fact_apuestas'[id_equipo_local] & "-" & 'apuestas_dw fact_apuestas'[id_equipo_visitante]
```

5. Presionar **Enter**

6. Power BI calculará la columna (puede tomar 10-20 segundos)

### ✅ Verificación:
Deberías ver una nueva columna `ID_Partido` dentro de la tabla `apuestas_dw fact_apuestas`.

---

## 🎯 PARTE 2: Crear Tabla "Medidas" (contenedor vacío)

### ¿Qué es?
Una tabla especial vacía que solo sirve para organizar medidas.

### ¿Cómo crearla?

1. En el panel derecho (Datos), **clic derecho en espacio vacío** (no sobre ninguna tabla)

2. Seleccionar: **"Nueva tabla"**

3. En la barra de fórmulas (arriba), escribir:
```dax
Medidas = {0}
```

4. Presionar **Enter**

5. Verás una nueva tabla llamada `Medidas` con una columna "Valor"

6. **Clic derecho** en columna "Valor" → **"Ocultar"**

### ✅ Verificación:
Deberías ver tabla `Medidas` en el panel de Datos (vacía, sin datos reales).

---

## 🎯 PARTE 3: Crear 20 Medidas (dentro de tabla "Medidas")

### ¿Qué son?
Cálculos que se ejecutan dinámicamente según los filtros aplicados.

### ¿Cómo crear CADA medida?

**Proceso repetir 20 veces:**

1. **Clic derecho** en tabla **"Medidas"**

2. Seleccionar: **"Nueva medida"**

3. Copiar código de la medida desde `MEDIDAS_DAX_CORREGIDAS.txt`

4. Pegar en la barra de fórmulas

5. Presionar **Enter**

6. Repetir para siguiente medida

---

## 📋 LISTA DE LAS 20 MEDIDAS

### Bloque 1: Medidas Básicas (crear primero)

```dax
Total Aciertos = SUM('apuestas_dw fact_apuestas'[cant_aciertos])
```

```dax
Total Apuestas = SUM('apuestas_dw fact_apuestas'[cant_apuestas])
```

```dax
Ganancia Total = SUM('apuestas_dw fact_apuestas'[ganancia_total])
```

```dax
Pérdida Total = SUM('apuestas_dw fact_apuestas'[perdida_total])
```

```dax
Inversión Total = SUM('apuestas_dw fact_apuestas'[inversion])
```

```dax
Total Partidos = DISTINCTCOUNT('apuestas_dw fact_apuestas'[ID_Partido])
```

---

### Bloque 2: Medidas Calculadas (después del Bloque 1)

```dax
Precisión % = DIVIDE([Total Aciertos], [Total Apuestas], 0) * 100
```

```dax
Beneficio Neto = [Ganancia Total] - [Pérdida Total]
```

```dax
ROI % = DIVIDE([Beneficio Neto], [Inversión Total], 0) * 100
```

```dax
Partidos con Arbitraje = CALCULATE(DISTINCTCOUNT('apuestas_dw fact_apuestas'[ID_Partido]), 'apuestas_dw fact_apuestas'[arbitraje_es_oportunidad] = TRUE())
```

```dax
% Partidos Arbitraje = DIVIDE([Partidos con Arbitraje], [Total Partidos], 0) * 100
```

```dax
Beneficio Arbitraje Promedio = CALCULATE(AVERAGE('apuestas_dw fact_apuestas'[arbitraje_beneficio]), 'apuestas_dw fact_apuestas'[arbitraje_es_oportunidad] = TRUE())
```

---

### Bloque 3: Medidas de Formato

```dax
Precisión Texto = FORMAT([Precisión %], "0.00") & "%"
```

```dax
ROI Texto = FORMAT([ROI %], "+0.00;-0.00") & "%"
```

```dax
KPI Precisión = SWITCH(TRUE(), [Precisión %] >= 55, "🟢 Alta", [Precisión %] >= 50, "🟡 Media", "🔴 Baja")
```

```dax
Color ROI = SWITCH(TRUE(), [ROI %] > 5, "#00A36C", [ROI %] > 0, "#90EE90", [ROI %] > -5, "#FFD700", "#FF6B6B")
```

---

### Bloque 4: Medidas Avanzadas

```dax
Casa Más Precisa =
VAR MaxPrecision = CALCULATE(MAX([Precisión %]), ALLSELECTED('apuestas_dw dim_casa_apuestas'))
RETURN CALCULATE(SELECTEDVALUE('apuestas_dw dim_casa_apuestas'[nombre_completo]), FILTER(ALLSELECTED('apuestas_dw dim_casa_apuestas'), [Precisión %] = MaxPrecision))
```

```dax
Mejor Estrategia =
VAR MaxROI = CALCULATE(MAX([ROI %]), ALLSELECTED('apuestas_dw dim_estrategia'))
RETURN CALCULATE(SELECTEDVALUE('apuestas_dw dim_estrategia'[nombre_estrategia]), FILTER(ALLSELECTED('apuestas_dw dim_estrategia'), [ROI %] = MaxROI))
```

```dax
Oportunidades Arbitraje = [Partidos con Arbitraje]
```

```dax
Partidos Analizados = DISTINCTCOUNT('apuestas_dw fact_apuestas'[ID_Partido])
```

---

## ✅ VERIFICACIÓN FINAL

### En el Panel de Datos deberías ver:

```
📦 apuestas_dw fact_apuestas
  └─ 📋 ID_Partido ← Nueva columna

📦 Medidas
  ├─ 📊 Total Aciertos
  ├─ 📊 Total Apuestas
  ├─ 📊 Precisión %
  ├─ 📊 Ganancia Total
  ├─ 📊 Pérdida Total
  ├─ 📊 Inversión Total
  ├─ 📊 Beneficio Neto
  ├─ 📊 ROI %
  ├─ 📊 Total Partidos
  ├─ 📊 Partidos con Arbitraje
  ├─ 📊 % Partidos Arbitraje
  ├─ 📊 Beneficio Arbitraje Promedio
  ├─ 📊 Precisión Texto
  ├─ 📊 ROI Texto
  ├─ 📊 KPI Precisión
  ├─ 📊 Color ROI
  ├─ 📊 Casa Más Precisa
  ├─ 📊 Mejor Estrategia
  ├─ 📊 Oportunidades Arbitraje
  └─ 📊 Partidos Analizados
```

**Total: 20 medidas en tabla "Medidas" + 1 columna en "fact_apuestas"**

---

## 🧪 PRUEBA RÁPIDA

Para verificar que funciona:

1. En Power BI, ir a vista "Informe" (ícono de gráfico en barra izquierda)

2. Seleccionar visual **"Tarjeta"** (ícono de número grande)

3. Arrastrar medida **"Total Partidos"** al campo "Campos"

4. Deberías ver: **22,502** (aproximadamente)

### Si ves ese número: ✅ ¡Todo funciona!

---

## 🆘 SOLUCIÓN DE PROBLEMAS

### Error: "No se encuentra el nombre"
**Causa**: Nombre de tabla incorrecto
**Solución**: Usar comillas simples: `'apuestas_dw fact_apuestas'`

### Error: "No se puede calcular"
**Causa**: Columna ID_Partido no existe
**Solución**: Crear primero la columna ID_Partido (Parte 1)

### Error: "La medida X no está definida"
**Causa**: Intentas usar una medida que no has creado
**Solución**: Crear primero las medidas básicas (Bloque 1)

### Número incorrecto en "Total Partidos"
**Causa**: Columna ID_Partido mal creada
**Solución**: Verificar que la columna ID_Partido existe en fact_apuestas

---

## 🎯 SIGUIENTE PASO

Una vez completadas las 21 elementos (1 columna + 20 medidas):

**PASO 7: Crear Dashboard 1 - Precisión de Casas de Apuestas**

Avísame cuando termines y te guío en la creación de visualizaciones.

---

📅 Generado: Noviembre 2025
📊 Proyecto: BD2_Hefesto_ApuestasDeportivas
