# 🚀 Guía Rápida: Crear Medidas DAX en Power BI

## ⏱️ Tiempo Estimado: 10-15 minutos

---

## PASO 1: Crear Tabla de Medidas

1. En Power BI, lado derecho panel **"Datos"**
2. **Clic derecho** en espacio vacío → **"Nueva tabla"**
3. En la barra de fórmulas (arriba), escribir:
   ```
   Medidas = {0}
   ```
4. Presionar **Enter**
5. Verás nueva tabla "Medidas" con columna "Valor"
6. **Clic derecho** en columna "Valor" → **"Ocultar"**

✅ **Resultado**: Tabla "Medidas" lista para recibir medidas

---

## PASO 2: Crear Columna Calculada ID_Partido

**⚠️ IMPORTANTE: Esta va en fact_apuestas, NO en Medidas**

1. **Clic derecho** en tabla **"fact_apuestas"**
2. Seleccionar **"Nueva columna"**
3. Copiar y pegar este código:
   ```dax
   ID_Partido = fact_apuestas[id_fecha] & "-" & fact_apuestas[id_equipo_local] & "-" & fact_apuestas[id_equipo_visitante]
   ```
4. Presionar **Enter**

✅ **Resultado**: Columna ID_Partido creada en fact_apuestas

---

## PASO 3: Crear las 20 Medidas DAX

### 🔄 Proceso para CADA Medida:

1. **Clic derecho** en tabla **"Medidas"**
2. Seleccionar **"Nueva medida"**
3. **Copiar** código de la medida desde `MEDIDAS_DAX_COMPLETAS.txt`
4. **Pegar** en barra de fórmulas
5. Presionar **Enter**
6. Repetir para siguiente medida

---

## 📊 ORDEN DE CREACIÓN (Recomendado)

### BLOQUE 1: Medidas Básicas (Crear Primero)
Estas son necesarias para las demás:

```dax
Total Aciertos = SUM(fact_apuestas[cant_aciertos])
```

```dax
Total Apuestas = SUM(fact_apuestas[cant_apuestas])
```

```dax
Ganancia Total = SUM(fact_apuestas[ganancia_total])
```

```dax
Pérdida Total = SUM(fact_apuestas[perdida_total])
```

```dax
Inversión Total = SUM(fact_apuestas[inversion])
```

```dax
Total Partidos = DISTINCTCOUNT(fact_apuestas[ID_Partido])
```

---

### BLOQUE 2: Medidas Calculadas (Dependen de Bloque 1)

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
Partidos con Arbitraje = CALCULATE(DISTINCTCOUNT(fact_apuestas[ID_Partido]), fact_apuestas[arbitraje_es_oportunidad] = TRUE())
```

```dax
% Partidos Arbitraje = DIVIDE([Partidos con Arbitraje], [Total Partidos], 0) * 100
```

```dax
Beneficio Arbitraje Promedio = CALCULATE(AVERAGE(fact_apuestas[arbitraje_beneficio]), fact_apuestas[arbitraje_es_oportunidad] = TRUE())
```

---

### BLOQUE 3: Medidas de Formato (Para Visualización)

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

### BLOQUE 4: Medidas Avanzadas (Análisis Complejo)

```dax
Casa Más Precisa =
VAR MaxPrecision = CALCULATE(MAX([Precisión %]), ALLSELECTED(dim_casa_apuestas))
RETURN CALCULATE(SELECTEDVALUE(dim_casa_apuestas[nombre_completo]), FILTER(ALLSELECTED(dim_casa_apuestas), [Precisión %] = MaxPrecision))
```

```dax
Mejor Estrategia =
VAR MaxROI = CALCULATE(MAX([ROI %]), ALLSELECTED(dim_estrategia))
RETURN CALCULATE(SELECTEDVALUE(dim_estrategia[nombre_estrategia]), FILTER(ALLSELECTED(dim_estrategia), [ROI %] = MaxROI))
```

```dax
Oportunidades Arbitraje = [Partidos con Arbitraje]
```

```dax
Partidos Analizados = DISTINCTCOUNT(fact_apuestas[ID_Partido])
```

---

## ✅ VERIFICACIÓN RÁPIDA

### Después de Crear Todas las Medidas:

En el panel "Datos", deberías ver en la tabla "Medidas":

- [ ] 20 medidas con ícono de calculadora (fx)
- [ ] Sin errores (sin iconos de advertencia ⚠️)

En la tabla "fact_apuestas":
- [ ] Columna "ID_Partido" (ícono de tabla)

---

## 🧪 PROBAR UNA MEDIDA

Para verificar que funciona:

1. Crear una **tarjeta** (visual simple)
2. Arrastrar medida **"Total Partidos"**
3. Debería mostrar: **~22,502** partidos

Si ves este número, ¡todo funciona! ✅

---

## 🆘 SOLUCIÓN DE PROBLEMAS

### Error: "No se puede determinar la tabla"
**Solución**: Asegúrate de escribir el nombre completo con tabla:
```dax
fact_apuestas[campo]  ✅ Correcto
[campo]                ❌ Incorrecto (a veces)
```

### Error: "La medida X no existe"
**Solución**: Crea primero las medidas básicas (Bloque 1) antes que las calculadas

### Error en medidas con TRUE()
**Solución**: Verifica que el campo sea booleano (True/False)
```dax
fact_apuestas[arbitraje_es_oportunidad] = TRUE()  ✅ Correcto
```

### Número incorrecto en "Total Partidos"
**Solución**: Verifica que creaste la columna ID_Partido en fact_apuestas

---

## 📝 CHECKLIST FINAL

Antes de continuar con dashboards:

- [ ] Tabla "Medidas" creada
- [ ] Columna "ID_Partido" en fact_apuestas
- [ ] 20 medidas creadas sin errores
- [ ] Prueba con tarjeta muestra valor correcto
- [ ] Todas las medidas visibles en panel "Datos"

---

## 🎯 SIGUIENTE PASO

Una vez completado, continuar con:
**PASO 7: Dashboard 1 - Precisión de Casas de Apuestas**

¿Necesitas ayuda con los dashboards?
Avísame cuando termines las medidas y te guío en la creación de visualizaciones.

---

📅 **Generado**: Noviembre 2025
📊 **Proyecto**: BD2_Hefesto_ApuestasDeportivas - Paso 5 (Power BI)
