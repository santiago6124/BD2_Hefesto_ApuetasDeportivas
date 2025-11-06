# 💰 DASHBOARD 2: ROI DE ESTRATEGIAS
## Guía Detallada con Campos Reales de Power BI

**Objetivo**: Analizar la rentabilidad (ROI) de diferentes estrategias de apuesta.

**Tiempo Estimado**: 35-45 minutos

---

## 🎨 DISEÑO DEL DASHBOARD

### Layout Recomendado

```
┌─────────────────────────────────────────────────────────────────┐
│  💰 Rentabilidad por Estrategia de Apuesta (ROI)                │
├──────────────────┬──────────────────┬───────────────────────────┤
│  KPI 1           │  KPI 2           │  KPI 3                    │
│  Mejor Estrat.   │  ROI Máximo      │  Beneficio Total         │
├──────────────────┴──────────────────┴───────────────────────────┤
│  TABLA: Resumen de Estrategias (4 estrategias × métricas)       │
├───────────────────────────────────┬───────────────────────────────┤
│  CASCADA: Impacto de Beneficio   │  DISPERSIÓN: ROI vs Precisión│
│  Por Estrategia                  │  Relación entre métricas     │
├───────────────────────────────────┴───────────────────────────────┤
│  MATRIZ: ROI por Liga y Estrategia                              │
├──────────────────────────────────────────────────────────────────┤
│  ÁREA APILADA: Evolución ROI por Temporada                      │
├──────────────────┬──────────────────┬───────────────────────────┤
│ FILTRO: Liga     │ FILTRO: Temp.    │ FILTRO: Casa Apuestas    │
└──────────────────┴──────────────────┴───────────────────────────┘
```

---

## 📋 PASO 1: PREPARACIÓN

### 1.1 Crear Nueva Página

1. Parte inferior → **`+`** Nueva página
2. Clic derecho → **Renombrar** → `2 - ROI por Estrategia`

---

## 📝 PASO 2: TÍTULO DEL DASHBOARD

### 2.1 Insertar y Formatear

1. **Insertar** → **Cuadro de texto**
2. Texto: `💰 Rentabilidad por Estrategia de Apuesta (ROI)`
3. Formato:
   - Fuente: Segoe UI Bold, 22pt
   - Color: `#2C3E50`
   - Alineación: Centro
   - Ancho: 100% canvas

---

## 📊 PASO 3: KPI CARDS (3 Tarjetas)

### 3.1 KPI Card 1: Mejor Estrategia

#### Crear y Configurar
1. **Visualizaciones** → **Tarjeta**
2. Posición: Superior izquierda

#### Campo
```
📊 Campos de Tarjeta
├─ Campos
   └─ Medidas > Mejor Estrategia
```

#### Formato
- **Etiqueta de categoría**: `Estrategia Más Rentable`
- **Tamaño valor**: 18pt
- **Color fondo**: `#E8F5E9` (verde claro)
- **Borde**: 1px, `#4CAF50` (verde)

---

### 3.2 KPI Card 2: ROI Máximo

#### Crear y Configurar
1. **Visualizaciones** → **Tarjeta**
2. Posición: Centro superior

#### Campo
```
📊 Campos de Tarjeta
├─ Campos
   └─ Medidas > ROI %
```

#### Filtro para Máximo
1. **Panel Filtros** → **Filtros en este visual**
2. Arrastrar: `dim_estrategia > nombre_estrategia`
3. Tipo: `Top N` → `Top 1` por `ROI %`

#### Formato
- **Etiqueta**: `ROI Máximo`
- **Formato**: Porcentaje con 2 decimales, signo `+/-`
- **Color**: Condicional según valor:
  - Verde si positivo
  - Rojo si negativo

**Aplicar color dinámico**:
1. **Formato visual** → **Etiquetas de datos**
2. **Color** → **fx Formato condicional**
3. Configurar:
   - Formato: Reglas
   - Si `ROI %` >= 0 entonces `#27AE60` (verde)
   - Si `ROI %` < 0 entonces `#E74C3C` (rojo)

---

### 3.3 KPI Card 3: Beneficio Total

#### Crear y Configurar
1. **Visualizaciones** → **Tarjeta**
2. Posición: Derecha superior

#### Campo
```
📊 Campos de Tarjeta
├─ Campos
   └─ Medidas > Beneficio Neto
```

#### Formato
- **Etiqueta**: `Beneficio Total`
- **Formato número**: Moneda con 0 decimales
- **Color**: Según signo (igual que KPI 2)

---

## 📋 PASO 4: TABLA RESUMEN DE ESTRATEGIAS

### 4.1 Crear Visual

1. **Visualizaciones** → **Tabla**
2. Posición: Debajo de KPIs
3. Ancho: 100%

### 4.2 Configurar Campos

```
📊 Campos de Tabla
├─ Columnas
   ├─ [1] apuestas_dw dim_estrategia > nombre_estrategia
   ├─ [2] Medidas > ROI %
   ├─ [3] Medidas > Beneficio Neto
   ├─ [4] Medidas > Inversión Total
   └─ [5] Medidas > Total Apuestas
```

### 4.3 Renombrar Columnas

- `nombre_estrategia` → `Estrategia`
- `ROI %` → `Rentabilidad (%)`
- `Beneficio Neto` → `Beneficio`
- `Inversión Total` → `Inversión`
- `Total Apuestas` → `Apuestas`

### 4.4 Formato Condicional - ROI %

**Método 1: Barras de Datos**
1. Clic derecho en columna **Rentabilidad (%)** → **Formato condicional** → **Barras de datos**
2. Configurar:
```
Barras de Datos
├─ Mínimo: Menor
├─ Máximo: Mayor
├─ Dirección: De izquierda a derecha
├─ Colores
│  ├─ Barra positiva: #27AE60 (verde)
│  ├─ Barra negativa: #E74C3C (rojo)
│  └─ Eje: #95A5A6 (gris)
└─ Solo barra: OFF (mostrar número + barra)
```

**Método 2: Escalas de Color (adicional)**
1. También aplicar **Escalas de color** al fondo:
```
Escalas de Color (Fondo)
├─ Mínimo: -10 → #FFEBEE (rojo claro)
├─ Centro: 0 → #FFFDE7 (amarillo claro)
└─ Máximo: 10 → #E8F5E9 (verde claro)
```

### 4.5 Formato Condicional - Beneficio Neto

1. Clic derecho en **Beneficio** → **Formato condicional** → **Escalas de color**
2. Configurar:
```
Escalas de Color
├─ Mínimo: Menor → #FFCDD2 (rojo claro)
├─ Centro: 0 → #FFFFFF (blanco)
└─ Máximo: Mayor → #C8E6C9 (verde claro)
```

### 4.6 Formato General

- **Valores numéricos**: Separador de miles
- **ROI %**: Formato `+0.00;-0.00` (mostrar signo)
- **Ordenar**: Por `Rentabilidad (%)` descendente

---

## 📊 PASO 5: GRÁFICO DE CASCADA (WATERFALL)

### 5.1 Crear Visual

1. **Visualizaciones** → **Gráfico de cascada**
2. Posición: Lado izquierdo, debajo de tabla
3. Tamaño: ~40% del ancho

### 5.2 Configurar Campos

```
📊 Campos de Cascada
├─ Categoría
│  └─ apuestas_dw dim_estrategia > nombre_estrategia
├─ Eje Y
│  └─ Medidas > Beneficio Neto
└─ Desglose
   └─ (vacío)
```

### 5.3 Formato Visual

**Panel Formato visual**:

1. **Título**:
   - Texto: `Impacto de Cada Estrategia en Beneficio`
   - Tamaño: 14pt

2. **Colores de cascada**:
   - **Aumentar**: `#27AE60` (verde)
   - **Disminuir**: `#E74C3C` (rojo)
   - **Total**: `#3498DB` (azul)

3. **Etiquetas de datos**:
   - Activar: ON
   - Posición: Fuera del extremo
   - Color: Automático (según barra)
   - Formato: Número con separador de miles

4. **Eje Y**:
   - Título: `Beneficio (€)`
   - Gridlines: ON
   - Color gridlines: `#E0E0E0`

5. **Sentinela**:
   - Mostrar total: ON
   - Etiqueta total: `Beneficio Total`

**IMPORTANTE**: El gráfico de cascada muestra cómo cada estrategia contribuye al beneficio total. Las barras verdes suman, las rojas restan.

---

## 📊 PASO 6: GRÁFICO DE DISPERSIÓN - ROI vs PRECISIÓN

### 6.1 Crear Visual

1. **Visualizaciones** → **Gráfico de dispersión**
2. Posición: Lado derecho de cascada
3. Tamaño: ~60% del ancho restante

### 6.2 Configurar Campos

```
📊 Campos de Dispersión
├─ Eje X
│  └─ Medidas > Precisión %
├─ Eje Y
│  └─ Medidas > ROI %
├─ Leyenda
│  └─ apuestas_dw dim_estrategia > nombre_estrategia
├─ Tamaño
│  └─ Medidas > Inversión Total
└─ Reproducir eje
   └─ (vacío)
```

**Resultado**: Cada estrategia aparece como una burbuja. El tamaño representa inversión.

### 6.3 Formato Visual

**Panel Formato visual**:

1. **Título**:
   - Texto: `Relación Precisión vs Rentabilidad`
   - Subtítulo: `Tamaño = Inversión Total`

2. **Eje X (Precisión)**:
   - Título: `Precisión (%)`
   - Mínimo: 45
   - Máximo: 55
   - Gridlines: ON

3. **Eje Y (ROI)**:
   - Título: `ROI (%)`
   - Mínimo: Automático
   - Máximo: Automático
   - Gridlines: ON

4. **Marcadores**:
   - Forma: Círculo
   - Tamaño mínimo: 20
   - Tamaño máximo: 100
   - Transparencia: 60%

5. **Líneas de promedio**:
   - **Línea constante X (Promedio Precisión)**:
     - Activar: ON
     - Valor: Medida `Precisión %`
     - Color: `#95A5A6` (gris)
     - Estilo: Punteado
     - Etiqueta: `Promedio Precisión`

   - **Línea constante Y (Promedio ROI)**:
     - Activar: ON
     - Valor: Medida `ROI %`
     - Color: `#95A5A6` (gris)
     - Estilo: Punteado
     - Etiqueta: `Promedio ROI`

6. **Leyenda**:
   - Posición: Derecha
   - Título: `Estrategia`

7. **Etiquetas de datos**:
   - Activar: ON (opcional)
   - Campo: `nombre_estrategia`
   - Tamaño: 9pt

**Interpretación**: Este gráfico muestra si hay correlación entre precisión y rentabilidad. Las burbujas grandes indican estrategias con mayor volumen de inversión.

---

## 🔢 PASO 7: MATRIZ - ROI POR LIGA Y ESTRATEGIA

### 7.1 Crear Visual

1. **Visualizaciones** → **Matriz**
2. Posición: Debajo de gráficos anteriores
3. Ancho: 100%

### 7.2 Configurar Campos

```
📊 Campos de Matriz
├─ Filas
│  └─ apuestas_dw dim_liga > nombre_liga
├─ Columnas
│  └─ apuestas_dw dim_estrategia > nombre_estrategia
├─ Valores
│  └─ Medidas > ROI %
└─ Obtención de detalles
   └─ (vacío - o agregar dimensiones para drill-down)
```

### 7.3 Formato Condicional

**Escalas de Color en Valores**:
1. Seleccionar matriz → **Formato visual** → **Valores de celda**
2. Expandir **ROI %** → **Fondo** → **fx Formato condicional**

```
Escalas de Color (Fondo)
├─ Formato: Degradado
├─ Campo: ROI %
├─ Resumir: Promedio
├─ Mínimo
│  ├─ Número: -10
│  └─ Color: #FFCDD2 (rojo claro)
├─ Centro
│  ├─ Número: 0
│  └─ Color: #FFF9C4 (amarillo claro)
└─ Máximo
   ├─ Número: 10
   └─ Color: #C8E6C9 (verde claro)
```

3. **Aplicar**

### 7.4 Formato de Valores

1. **Valores de celda** → **ROI %**
2. **Formato de valores**:
   - Mostrar como: Porcentaje
   - Decimales: 1
   - Prefijo personalizado: `+` para positivos, `-` para negativos

### 7.5 Totales y Subtotales

1. **Valores de celda** → **Totales**
2. Configurar:
   - **Totales de fila**: ON
   - **Totales de columna**: ON
   - **Aplicar a etiquetas**: ON
   - **Etiqueta totales fila**: `Promedio`
   - **Etiqueta totales columna**: `Promedio`

3. **Formato totales**:
   - Negrita: ON
   - Color fondo: `#ECF0F1` (gris claro)

---

## 📈 PASO 8: GRÁFICO DE ÁREA - EVOLUCIÓN TEMPORAL

### 8.1 Crear Visual

1. **Visualizaciones** → **Gráfico de áreas apiladas**
2. Posición: Debajo de matriz
3. Ancho: 100%
4. Alto: ~250px

### 8.2 Configurar Campos

```
📊 Campos de Área Apilada
├─ Eje X
│  └─ apuestas_dw dim_fecha > temporada
├─ Eje Y
│  └─ Medidas > ROI %
└─ Leyenda
   └─ apuestas_dw dim_estrategia > nombre_estrategia
```

### 8.3 Formato Visual

**Panel Formato visual**:

1. **Título**:
   - Texto: `Evolución del ROI por Temporada y Estrategia`
   - Tamaño: 14pt

2. **Eje X**:
   - Título: OFF
   - Tipo: Categórico
   - Etiquetas: 45° inclinadas (si muchas temporadas)

3. **Eje Y**:
   - Título: `ROI (%)`
   - Mínimo: Automático
   - Máximo: Automático
   - Gridlines: ON

4. **Áreas**:
   - Transparencia: 70% (para ver superposición)
   - Líneas de borde: 1px

5. **Leyenda**:
   - Posición: Derecha
   - Título: `Estrategia`
   - Tamaño: 10pt

6. **Información sobre herramientas**:
   - Agregar campos adicionales:
     - `Beneficio Neto`
     - `Inversión Total`
     - `Total Apuestas`

**IMPORTANTE**: Si el gráfico es confuso con áreas apiladas, cambiar a **Gráfico de líneas** para ver tendencias individuales más claras.

**Alternativa - Gráfico de Líneas**:
- Mismo visual pero cambiar tipo de gráfico
- Líneas en lugar de áreas
- Sin apilar

---

## 🎚️ PASO 9: SEGMENTACIONES (FILTROS)

### 9.1 Segmentación 1: Liga

#### Crear y Configurar
1. **Visualizaciones** → **Segmentación**
2. Posición: Inferior izquierda

```
📊 Campo
└─ Campo
   └─ apuestas_dw dim_liga > nombre_liga
```

#### Formato
- **Estilo**: Lista
- **Selección múltiple**: ON
- **Título**: `Filtrar por Liga`
- **Tamaño**: 250px ancho × 180px alto

---

### 9.2 Segmentación 2: Temporada

#### Crear y Configurar
1. **Visualizaciones** → **Segmentación**
2. Posición: Inferior centro

```
📊 Campo
└─ Campo
   └─ apuestas_dw dim_fecha > temporada
```

#### Formato
- **Estilo**: Desplegable
- **Título**: `Temporada`

---

### 9.3 Segmentación 3: Casa de Apuestas

#### Crear y Configurar
1. **Visualizaciones** → **Segmentación**
2. Posición: Inferior derecha

```
📊 Campo
└─ Campo
   └─ apuestas_dw dim_casa_apuestas > nombre_completo
```

#### Formato
- **Estilo**: Lista
- **Selección múltiple**: ON
- **Título**: `Casa de Apuestas`
- **Tamaño**: 250px ancho × 180px alto

---

## ✅ VERIFICACIÓN FINAL

### Checklist Dashboard 2

- [ ] Título visible: "💰 Rentabilidad por Estrategia de Apuesta (ROI)"
- [ ] 3 KPI cards funcionando:
  - [ ] Mejor Estrategia muestra nombre
  - [ ] ROI Máximo muestra porcentaje con signo
  - [ ] Beneficio Total muestra valor
- [ ] Tabla con 4 estrategias:
  - [ ] ROI % con barras de datos
  - [ ] Colores condicionales activos
  - [ ] Ordenada por ROI descendente
- [ ] Gráfico de cascada:
  - [ ] Barras verdes (positivas) y rojas (negativas)
  - [ ] Total al final
- [ ] Gráfico de dispersión:
  - [ ] 4 burbujas (una por estrategia)
  - [ ] Tamaño proporcional a inversión
  - [ ] Líneas de promedio visibles
- [ ] Matriz Liga × Estrategia:
  - [ ] Colores condicionales funcionando
  - [ ] Totales visibles
- [ ] Gráfico de área/líneas:
  - [ ] Evolución clara por temporada
  - [ ] Leyenda correcta
- [ ] 3 segmentaciones activas y funcionales

### Valores Esperados

**ROI típico**: -5% a +5% (mayoria cercano a 0%)
**Beneficio Total**: Puede ser negativo o positivo
**Mejor estrategia**: Varía según datos reales

### Interpretación de Resultados

**ROI Positivo (>0%)**: La estrategia genera ganancias
**ROI Negativo (<0%)**: La estrategia genera pérdidas
**ROI ~0%**: La estrategia está equilibrada (típico en apuestas)

**Estrategias esperadas**:
- `ALWAYS_H`: Apostar siempre al equipo local
- `ALWAYS_A`: Apostar siempre al visitante
- `FOLLOW_FAV`: Seguir al favorito (menor cuota)
- `UNDERDOG`: Apostar al underdog (mayor cuota)

---

## 🆘 SOLUCIÓN DE PROBLEMAS

### Problema: "ROI muestra valores extraños (>100%)"
**Causa**: Fórmula incorrecta o datos atípicos
**Solución**: Verificar medida `ROI %` y validar con SQL

### Problema: "Cascada no muestra correctamente"
**Causa**: Gráfico de cascada requiere valores individuales
**Solución**: Asegurar que cada estrategia tiene un valor único de Beneficio Neto

### Problema: "Dispersión muestra solo un punto"
**Causa**: Estrategias están siendo agregadas
**Solución**: Verificar que `nombre_estrategia` está en Leyenda (no en Eje)

### Problema: "Colores no se aplican correctamente"
**Causa**: Rangos de mínimo/máximo no coinciden con datos
**Solución**: Ajustar rangos en formato condicional según valores reales

### Problema: "Gráfico de área confuso (muchas superposiciones)"
**Cambiar a**: Gráfico de líneas para ver tendencias individuales

---

## 💡 TIPS AVANZADOS

### Tip 1: Añadir Línea de Referencia "Break-even"
En gráficos de ROI, agregar línea en Y=0 para mostrar el punto de equilibrio:
1. **Formato visual** → **Líneas de referencia**
2. Agregar línea: Y = 0
3. Color: Rojo, Grosor: 2px, Estilo: Sólido
4. Etiqueta: "Break-even"

### Tip 2: Drill-down en Matriz
Agregar jerarquía en Filas:
1. Liga → País → Temporada
2. Permite hacer clic para explorar niveles

### Tip 3: Información sobre herramientas personalizada
Crear página tooltip con detalles adicionales de cada estrategia.

---

📅 **Creado**: Noviembre 2025
📊 **Proyecto**: BD2_Hefesto_ApuestasDeportivas
📄 **Siguiente**: DASHBOARD_3_ARBITRAJE_DETALLADO.md
