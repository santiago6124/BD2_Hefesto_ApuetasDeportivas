# 📊 GUÍA COMPLETA: DASHBOARDS POWER BI
## Data Warehouse Apuestas Deportivas

**Versión**: 2.0 - Ultra Detallada
**Fecha**: Noviembre 2025
**Tiempo Total Estimado**: 2-3 horas

---

## 📑 ÍNDICE DE DOCUMENTOS

Has recibido 4 documentos detallados:

1. **DASHBOARD_1_PRECISION_DETALLADO.md**
   - 8 visuales con configuración exacta
   - Análisis de precisión de casas de apuestas
   - Tiempo: 30-40 minutos

2. **DASHBOARD_2_ROI_DETALLADO.md**
   - 8 visuales con formato avanzado
   - Análisis de rentabilidad por estrategia
   - Tiempo: 35-45 minutos

3. **DASHBOARD_3_ARBITRAJE_DETALLADO.md**
   - 9 visuales + 1 columna calculada
   - Detección de oportunidades de arbitraje
   - Tiempo: 40-50 minutos

4. **GUIA_COMPLETA_DASHBOARDS.md** ← Este documento
   - Tips generales y troubleshooting

---

## 🎯 ORDEN RECOMENDADO DE CREACIÓN

### Opción 1: Secuencial (Recomendado para principiantes)
```
Dashboard 1 → Verificar → Dashboard 2 → Verificar → Dashboard 3
```
**Ventaja**: Aprendes progresivamente, menos errores

### Opción 2: Paralelo (Para usuarios avanzados)
```
Crear estructura de los 3 → Configurar campos → Aplicar formatos
```
**Ventaja**: Más rápido, pero requiere experiencia

### Opción 3: Iterativo (Más flexible)
```
KPIs de todos → Tablas de todos → Gráficos de todos → Formatos
```
**Ventaja**: Ve resultados rápido, ajusta sobre la marcha

---

## 🛠️ CONCEPTOS CLAVE DE POWER BI

### Tipos de Campos

#### 1. Dimensiones (🔵 Ícono Azul)
- Campos de texto o categóricos
- Ejemplos: `nombre_liga`, `nombre_estrategia`
- Uso: Filas, Columnas, Ejes, Leyendas

#### 2. Medidas (📊 Ícono Calculadora)
- Cálculos dinámicos
- Ejemplos: `Precisión %`, `ROI %`
- Uso: Valores, métricas en visuales

#### 3. Columnas Calculadas (📋 Ícono Tabla)
- Calculadas por fila en la tabla
- Ejemplos: `ID_Partido`, `Rango Beneficio Arbitraje`
- Uso: Como dimensiones en visuales

### Áreas de Campos en Visuales

Cada visual tiene áreas específicas donde arrastrar campos:

**Tabla**:
```
├─ Columnas: Campos a mostrar (dimensiones + medidas)
```

**Gráfico de Barras**:
```
├─ Eje Y: Categorías (dimensión)
├─ Eje X: Valores (medida)
├─ Leyenda: Subgrupos (dimensión)
└─ Información sobre herramientas: Campos extra en hover
```

**Matriz**:
```
├─ Filas: Dimensión vertical
├─ Columnas: Dimensión horizontal
├─ Valores: Medidas en celdas
└─ Obtención de detalles: Drill-down adicional
```

**Tarjeta (KPI)**:
```
├─ Campos: Una o más medidas
```

**Gráfico de Líneas**:
```
├─ Eje X: Dimensión temporal o categórica
├─ Eje Y: Medida principal
├─ Leyenda: Múltiples series
└─ Valores secundarios: Segundo eje Y
```

---

## 🎨 GUÍA DE COLORES CONSISTENTE

### Paleta del Proyecto

```
COLORES PRINCIPALES:
├─ Títulos: #2C3E50 (gris oscuro)
├─ Subtítulos: #7F8C8D (gris medio)
├─ Fondos claros: #ECF0F1 (gris muy claro)
└─ Bordes: #BDC3C7 (gris claro)

COLORES SEMÁNTICOS:
├─ Positivo/Éxito: #27AE60 (verde)
├─ Negativo/Error: #E74C3C (rojo)
├─ Advertencia: #F39C12 (naranja)
├─ Información: #3498DB (azul)
└─ Neutral: #95A5A6 (gris)

DEGRADADOS:
├─ Precisión/ROI: Rojo → Amarillo → Verde
├─ Arbitraje: Blanco → Verde
└─ Temporal: Azul claro → Azul oscuro
```

### Aplicar Colores

**En Tarjetas KPI**:
1. Formato visual → Etiquetas de datos → Color
2. Usar colores semánticos según métrica

**En Gráficos**:
1. Formato visual → Colores
2. Elegir:
   - Color sólido: Un color para todo
   - Degradado: Escala según valores
   - Por serie: Color diferente por categoría

**Formato Condicional**:
1. Clic derecho en columna/celda
2. Formato condicional → Escalas de color
3. Configurar mínimo/centro/máximo con colores de paleta

---

## ⚡ ATAJOS DE TECLADO ÚTILES

```
NAVEGACIÓN:
├─ Ctrl + Flecha: Mover entre objetos
├─ Ctrl + C / V: Copiar/Pegar visuales
├─ Ctrl + D: Duplicar visual
├─ Ctrl + Z: Deshacer
└─ Ctrl + Y: Rehacer

VISUALES:
├─ Ctrl + Click: Selección múltiple
├─ Shift + Drag: Mantener proporción al redimensionar
├─ Alt + Drag: Copiar arrastrando
└─ Delete: Eliminar visual

VISTAS:
├─ Ctrl + 1: Vista Informe
├─ Ctrl + 2: Vista Datos
├─ Ctrl + 3: Vista Modelo
└─ F5: Modo presentación
```

---

## 🔧 TROUBLESHOOTING COMÚN

### Problema: Visual No Muestra Datos

**Síntomas**: Visual vacío o "No hay datos"

**Causas y Soluciones**:

1. **Filtros activos bloqueando datos**
   - Verificar: Panel Filtros → Ver todos los niveles
   - Solución: Borrar filtros o ajustar valores

2. **Relaciones rotas**
   - Verificar: Vista Modelo → Ver conexiones entre tablas
   - Solución: Recrear relaciones necesarias

3. **Medida con error**
   - Verificar: Clic en medida → Ver mensaje error
   - Solución: Revisar fórmula DAX

4. **Nombres de campos incorrectos**
   - Verificar: Panel Datos → Expandir tabla → Ver nombres reales
   - Solución: Usar comillas simples para nombres con espacios

### Problema: Formato Condicional No Funciona

**Síntomas**: Colores no aparecen o incorrectos

**Causas y Soluciones**:

1. **Rangos mínimo/máximo incorrectos**
   - Verificar: Formato condicional → Ver valores configurados
   - Solución: Ajustar a rango real de datos (ej: 45-55 para precisión)

2. **Tipo de campo incorrecto**
   - Verificar: Campo es numérico, no texto
   - Solución: Cambiar tipo de dato en Vista Datos

3. **Aplicado a campo equivocado**
   - Verificar: Formato condicional → Ver campo base
   - Solución: Reaplicar a campo correcto

### Problema: Lentitud en Power BI

**Síntomas**: Dashboard tarda en actualizar

**Causas y Soluciones**:

1. **Demasiados visuales**
   - Límite recomendado: 15-20 visuales por página
   - Solución: Dividir en múltiples páginas

2. **Consultas complejas**
   - Verificar: Vista Rendimiento (Ver → Analizador de rendimiento)
   - Solución: Optimizar medidas DAX

3. **Datos sin agregación**
   - Problema: Mostrar 700K filas individuales
   - Solución: Usar medidas agregadas, no tablas completas

4. **Modo DirectQuery en lugar de Import**
   - Verificar: Propiedades de conexión
   - Solución: Cambiar a Import si datos son estáticos

### Problema: Medida Devuelve Error

**Errores Comunes DAX**:

```
Error: "No se encuentra el nombre 'fact_apuestas'"
Solución: Usar 'apuestas_dw fact_apuestas' con comillas

Error: "No se puede calcular la tabla X en el contexto actual"
Solución: Verificar relaciones y usar CALCULATE si necesario

Error: "La función MAX solo acepta una referencia de columna"
Solución: Usar MAXX o TOPN para medidas

Error: "Tipo de datos incompatible"
Solución: Verificar que medidas usan campos numéricos
```

### Problema: Segmentación No Filtra Visuales

**Síntomas**: Al usar filtro, visuales no cambian

**Causas y Soluciones**:

1. **Interacciones desactivadas**
   - Seleccionar segmentación
   - Barra superior: **Formato** → **Editar interacciones**
   - Verificar que visuales tienen ícono de filtro ✓ (no "Ninguno")

2. **Diferentes tablas sin relación**
   - Verificar: Vista Modelo → Relaciones entre tablas
   - Solución: Crear relaciones necesarias

### Problema: No Puedo Exportar a PDF/PowerPoint

**Síntomas**: Opción deshabilitada o error

**Causas y Soluciones**:

1. **No guardado localmente**
   - Archivo → Guardar como → Guardar .pbix primero

2. **Demasiados datos**
   - Solución: Simplificar visuales o exportar por página

3. **Visual personalizado**
   - Algunos visuales custom no exportan bien
   - Solución: Usar visuales nativos de Power BI

---

## ✅ CHECKLIST FINAL

### Antes de Presentar

**Contenido**:
- [ ] Los 3 dashboards completados
- [ ] Títulos descriptivos en cada página
- [ ] Cada visual tiene título claro
- [ ] No hay errores en visuales (⚠️ ícono advertencia)

**Formato**:
- [ ] Colores consistentes (paleta del proyecto)
- [ ] Tamaños de fuente legibles (mínimo 10pt)
- [ ] Alineación correcta de visuales
- [ ] Bordes y fondos aplicados consistentemente

**Funcionalidad**:
- [ ] Segmentaciones funcionan correctamente
- [ ] Filtros afectan a todos los visuales relevantes
- [ ] Drill-down/up funciona (si aplicable)
- [ ] Tooltips muestran información adicional

**Datos**:
- [ ] Medidas calculan correctamente
- [ ] Formato de números apropiado (%, miles, decimales)
- [ ] Ordenamiento lógico en tablas y gráficos
- [ ] No hay valores NULL inesperados

**Performance**:
- [ ] Dashboards cargan en <5 segundos
- [ ] No hay lag al usar filtros
- [ ] Memoria de Power BI <2GB

### Valores de Referencia

**Dashboard 1 - Precisión**:
- Precisión típica: 48-53%
- Casa más precisa: Varía, típicamente Pinnacle o Bet365
- Total aciertos: ~380,000-400,000

**Dashboard 2 - ROI**:
- ROI típico: -5% a +5%
- La mayoría de estrategias cerca de 0% (equilibrio)
- Beneficio neto: Puede ser negativo (pérdidas)

**Dashboard 3 - Arbitraje**:
- Oportunidades: 5,000-10,000 (20-40% de partidos)
- Beneficio promedio: 0.5-2.5%
- Beneficio máximo: <5% (excepcional)

---

## 💡 TIPS PROFESIONALES

### Diseño y UX

1. **Principio F-Pattern**: Los usuarios leen en F
   - Información clave arriba-izquierda
   - Detalles abajo-derecha

2. **Jerarquía Visual**:
   - Títulos grandes (24pt)
   - Subtítulos medianos (14-16pt)
   - Valores grandes (20-32pt) en KPIs
   - Texto normal (10-12pt) en tablas

3. **Espacio en Blanco**:
   - No llenar 100% del canvas
   - Dejar ~50px de margen
   - Separar grupos de visuales con espacio

4. **Consistencia**:
   - Mismo estilo de tarjetas KPI
   - Misma familia de fuentes (Segoe UI)
   - Paleta de colores limitada (5-7 colores max)

### Performance

1. **Limitar Campos en Tooltips**:
   - Solo información esencial
   - Máximo 5 campos

2. **Usar Medidas en lugar de Columnas Calculadas**:
   - Medidas: Calculan bajo demanda
   - Columnas: Almacenadas en memoria

3. **Filtros a Nivel de Página**:
   - Mejor que filtros individuales por visual
   - Reduce consultas duplicadas

4. **Formato Condicional con Reglas, No Degradados**:
   - Reglas: Más rápido
   - Degradados: Más carga visual

### DAX

1. **Usar Variables**:
   ```dax
   // LENTO
   Medida = [Valor1] + [Valor1] * 2

   // RÁPIDO
   Medida =
   VAR V1 = [Valor1]
   RETURN V1 + V1 * 2
   ```

2. **DIVIDE en lugar de División**:
   ```dax
   // ERROR si denominador = 0
   Medida = SUM(Tabla[A]) / SUM(Tabla[B])

   // SEGURO (devuelve 0 si error)
   Medida = DIVIDE(SUM(Tabla[A]), SUM(Tabla[B]), 0)
   ```

3. **CALCULATE vs FILTER**:
   ```dax
   // ÓPTIMO
   Medida = CALCULATE(SUM(...), Tabla[Campo] = "Valor")

   // MENOS ÓPTIMO
   Medida = CALCULATE(SUM(...), FILTER(Tabla, Tabla[Campo] = "Valor"))
   ```

### Colaboración

1. **Guardar Frecuentemente**:
   - Ctrl + S cada 10-15 minutos
   - Power BI no autoguarda

2. **Versionado de Archivos**:
   - Nombrar: `Dashboard_v1.0.pbix`, `Dashboard_v1.1.pbix`
   - O usar Git para .pbix

3. **Documentar Medidas Complejas**:
   - Añadir comentarios en DAX con `//`
   - Describir lógica no obvia

4. **Bookmark de Estados**:
   - Crear bookmarks para diferentes vistas
   - Facilita navegación y presentaciones

---

## 📚 RECURSOS ADICIONALES

### Documentación Oficial

- **Power BI Docs**: https://docs.microsoft.com/power-bi/
- **DAX Reference**: https://dax.guide/
- **Power BI Community**: https://community.powerbi.com/

### Tutoriales Recomendados

1. **Microsoft Learn - Power BI**:
   - Ruta de aprendizaje gratuita
   - Certificación disponible

2. **SQLBI - DAX Patterns**:
   - Patrones comunes de DAX
   - Ejemplos prácticos

3. **Guy in a Cube (YouTube)**:
   - Canal oficial de Microsoft
   - Tips semanales

### Cursos Gratuitos

- **edX**: Analyzing and Visualizing Data with Power BI
- **Coursera**: Data Visualization with Microsoft Power BI
- **YouTube**: Cursos completos en español

---

## 🎓 PRÓXIMOS PASOS

### Mejoras Opcionales

1. **Interactividad Avanzada**:
   - Drill-through pages
   - Bookmarks para navegación
   - Tooltips personalizados

2. **Análisis Avanzado**:
   - Clustering de estrategias
   - Pronósticos con AI
   - Análisis de tendencias

3. **Integración**:
   - Publicar a Power BI Service
   - Configurar actualización automática
   - Compartir con stakeholders

4. **Automatización**:
   - Refresh programado desde MySQL
   - Alertas por email en umbrales
   - API de Power BI para exports

### Extensiones del Proyecto

1. **Dashboard 4 - Análisis de Equipos**:
   - Performance por equipo
   - Home vs Away analysis
   - Racha de victorias/derrotas

2. **Dashboard 5 - Análisis Temporal**:
   - Tendencias por día de semana
   - Estacionalidad
   - Horarios óptimos

3. **Dashboard 6 - Análisis Comparativo**:
   - Benchmark entre ligas
   - Comparación año sobre año
   - Market efficiency

---

## 📞 SOPORTE

### Problemas con las Guías

Si encuentras errores o tienes dudas sobre estas guías:
1. Revisar sección Troubleshooting
2. Verificar nombres de campos en tu modelo
3. Consultar documentación oficial de Power BI

### Problemas con Datos

Si hay inconsistencias en los datos:
1. Verificar ETL se ejecutó correctamente
2. Validar conteos en MySQL
3. Revisar relaciones en Vista Modelo

---

## ✨ CONCLUSIÓN

Has recibido guías ultra detalladas para crear 3 dashboards profesionales con:

- ✅ **25+ visuales** configurados paso a paso
- ✅ **Campos exactos** de Power BI especificados
- ✅ **Formato condicional** completo
- ✅ **Troubleshooting** exhaustivo
- ✅ **Best practices** de diseño y performance

**Tiempo Total**: 2-3 horas de trabajo
**Resultado**: Dashboard profesional listo para presentación

---

## 🎯 ORDEN DE LECTURA RECOMENDADO

```
1. Leer este documento (GUIA_COMPLETA_DASHBOARDS.md)
   ↓
2. Crear Dashboard 1 (DASHBOARD_1_PRECISION_DETALLADO.md)
   ↓
3. Verificar y probar Dashboard 1
   ↓
4. Crear Dashboard 2 (DASHBOARD_2_ROI_DETALLADO.md)
   ↓
5. Verificar y probar Dashboard 2
   ↓
6. Crear Dashboard 3 (DASHBOARD_3_ARBITRAJE_DETALLADO.md)
   ↓
7. Verificación final con checklist de este documento
   ↓
8. Guardar, exportar y presentar
```

---

📅 **Versión**: 2.0 - Ultra Detallada
📊 **Proyecto**: BD2_Hefesto_ApuestasDeportivas
✅ **Estado**: Documentación Completa

**¡Éxito con tu proyecto!** 🚀
