# 📊 DASHBOARD 1: PRECISIÓN DE CASAS DE APUESTAS
## Guía Detallada con Campos Reales de Power BI

**Objetivo**: Analizar qué casas de apuestas tienen las cuotas más precisas.

**Tiempo Estimado**: 30-40 minutos

---

## 🎨 DISEÑO DEL DASHBOARD

### Layout Recomendado (Pantalla Completa)

```
┌─────────────────────────────────────────────────────────────────┐
│  📊 Precisión de Casas de Apuestas                              │
├──────────────────┬──────────────────┬───────────────────────────┤
│  KPI 1           │  KPI 2           │  KPI 3                    │
│  Casa + Precisa  │  Precisión Max   │  Total Aciertos          │
├──────────────────┴──────────────────┴───────────────────────────┤
│  TABLA: Ranking de Precisión                                    │
│  (10 casas con métricas)                                        │
├──────────────────────────────┬───────────────────────────────────┤
│  BARRAS HORIZONTALES         │  LÍNEAS: Evolución Temporal      │
│  Comparación Precisión       │  Por Temporada                   │
├──────────────────────────────┴───────────────────────────────────┤
│  MATRIZ: Precisión por Liga y Casa                              │
├──────────────────┬──────────────────┬───────────────────────────┤
│ FILTRO: Liga     │ FILTRO: Temp.    │ FILTRO: Tipo Resultado   │
└──────────────────┴──────────────────┴───────────────────────────┘
```

---

## 📋 PASO 1: PREPARACIÓN

### 1.1 Crear Nueva Página

1. En la parte inferior de Power BI, clic en **`+`** (Nueva página)
2. **Clic derecho** en pestaña → **Renombrar página**
3. Escribir: `1 - Precisión por Casa`
4. Enter

---

## 📝 PASO 2: TÍTULO DEL DASHBOARD

### 2.1 Insertar Cuadro de Texto

1. Barra superior → **Insertar** → **Cuadro de texto**
2. Clic en el canvas para crear cuadro
3. Escribir: `📊 Precisión de Casas de Apuestas`

### 2.2 Formatear Título

1. Seleccionar el texto
2. En barra de formato superior:
   - **Fuente**: Segoe UI
   - **Estilo**: Negrita
   - **Tamaño**: 24
   - **Color**: `#2C3E50` (gris oscuro)
   - **Alineación**: Centro

3. Ajustar tamaño del cuadro:
   - **Ancho**: 100% del canvas (borde a borde)
   - **Alto**: ~60 px
   - **Posición**: Superior del canvas

---

## 📊 PASO 3: KPI CARDS (3 Tarjetas)

### 3.1 KPI Card 1: Casa Más Precisa

#### Crear Visual
1. Panel **Visualizaciones** → Seleccionar **Tarjeta** (ícono con "123")
2. Arrastrar visual a la esquina superior izquierda

#### Configurar Campos
**Panel "Datos" (lado derecho)**:
```
📊 Campos de Tarjeta
├─ Campos
   └─ [Arrastrar aquí] → Medidas > Casa Más Precisa
```

**Resultado**: La tarjeta muestra el nombre de una casa (ej: "Bet365")

#### Formato
1. Seleccionar tarjeta → Panel **Formato visual** (ícono de rodillo de pintura)

2. **Etiqueta de categoría**:
   - Activar: `ON`
   - Texto: `Casa Más Precisa`
   - Fuente: Segoe UI Semibold, 12pt
   - Color: `#7F8C8D` (gris medio)

3. **Etiquetas de datos**:
   - Tamaño de texto: 20pt
   - Color: `#2C3E50` (gris oscuro)
   - Fuente: Segoe UI Bold

4. **Fondo** (Efectos):
   - Color: `#ECF0F1` (gris claro)
   - Transparencia: 0%

5. **Borde**:
   - Activar: `ON`
   - Color: `#BDC3C7`
   - Radio: 5px
   - Ancho: 1px

#### Tamaño y Posición
- **Ancho**: 250px
- **Alto**: 120px
- **Posición**: Superior izquierda (debajo del título)

---

### 3.2 KPI Card 2: Precisión Máxima

#### Crear Visual
1. Panel **Visualizaciones** → **Tarjeta**
2. Colocar a la derecha de KPI 1

#### Configurar Campos
```
📊 Campos de Tarjeta
├─ Campos
   └─ Medidas > Precisión %
```

**IMPORTANTE**: Necesitamos filtrar para mostrar solo el máximo.

#### Aplicar Filtro Visual
1. Seleccionar la tarjeta
2. Panel **Filtros** (lado derecho) → **Filtros en este visual**
3. Arrastrar: `dim_casa_apuestas > nombre_completo`
4. **Tipo de filtro**: Cambiar a `Top N`
5. Configurar:
   - **Mostrar elementos**: `Top 1`
   - **Por valor**: Arrastrar `Precisión %`
6. **Aplicar filtro**

**Resultado**: Muestra el valor máximo de precisión (ej: "52.34%")

#### Formato
Igual que KPI 1, pero:
- **Etiqueta de categoría**: `Mejor Precisión`
- **Color fondo**: `#D5F4E6` (verde claro)
- **Formato número**: Porcentaje con 2 decimales

---

### 3.3 KPI Card 3: Total Aciertos

#### Crear Visual
1. Panel **Visualizaciones** → **Tarjeta**
2. Colocar a la derecha de KPI 2

#### Configurar Campos
```
📊 Campos de Tarjeta
├─ Campos
   └─ Medidas > Total Aciertos
```

#### Formato
Igual que KPI 1, pero:
- **Etiqueta de categoría**: `Total Aciertos`
- **Formato número**: Número con separador de miles (ej: "123,456")

---

## 📋 PASO 4: TABLA RANKING DE PRECISIÓN

### 4.1 Crear Visual

1. Panel **Visualizaciones** → **Tabla** (ícono de tabla)
2. Arrastrar debajo de las 3 KPI cards
3. Ajustar tamaño para que ocupe ancho completo

### 4.2 Configurar Campos

**Panel "Datos" - Agregar en este orden**:
```
📊 Campos de Tabla
├─ Columnas
   ├─ [1] apuestas_dw dim_casa_apuestas > nombre_completo
   ├─ [2] Medidas > Precisión %
   ├─ [3] Medidas > Total Aciertos
   └─ [4] Medidas > Total Apuestas
```

**Cómo agregar**:
- Arrastrar cada campo desde panel "Datos" al área "Columnas"
- O marcar checkbox de cada campo (se añade automáticamente)

### 4.3 Formato de Columnas

#### Columna 1: nombre_completo
1. Clic derecho en encabezado → **Cambiar nombre**
2. Escribir: `Casa de Apuestas`
3. Panel Formato → **Encabezados de columna**:
   - Tamaño texto: 12pt
   - Negrita: ON
   - Color fondo: `#34495E` (azul oscuro)
   - Color texto: `#FFFFFF` (blanco)

#### Columna 2: Precisión %
1. Clic derecho en encabezado → **Cambiar nombre** → `Precisión`
2. Clic derecho en columna → **Formato condicional** → **Escalas de color**

**Configurar escalas**:
```
Escala de Color (Precisión)
├─ Mínimo
│  ├─ Tipo: Número
│  ├─ Valor: 45
│  └─ Color: #FF6B6B (rojo)
├─ Centro
│  ├─ Tipo: Número
│  ├─ Valor: 50
│  └─ Color: #FFD700 (amarillo)
└─ Máximo
   ├─ Tipo: Número
   ├─ Valor: 55
   └─ Color: #00A36C (verde)
```

3. **Aplicar**

#### Columna 3: Total Aciertos
1. Cambiar nombre → `Aciertos`
2. Clic derecho → **Formato** → **Separador de miles**: ON

#### Columna 4: Total Apuestas
1. Cambiar nombre → `Apuestas`
2. Formato: Separador de miles ON

### 4.4 Ordenar Tabla

1. Clic en **`...`** (esquina superior derecha de la tabla)
2. **Ordenar por** → `Precisión`
3. **Orden descendente** (mayor a menor)

### 4.5 Formato Visual General

**Panel Formato visual**:

1. **Cuadrícula**:
   - Líneas horizontales: ON
   - Color: `#E0E0E0` (gris claro)
   - Grosor: 1px

2. **Valores** (filas de datos):
   - Tamaño texto: 11pt
   - Alineación: Izquierda (texto), Derecha (números)

3. **Estilo**:
   - Estilo de encabezado: Predeterminado
   - Alternar colores de fila: ON
   - Color 1: Blanco
   - Color 2: `#F8F9FA` (gris muy claro)

---

## 📊 PASO 5: GRÁFICO DE BARRAS HORIZONTALES

### 5.1 Crear Visual

1. Panel **Visualizaciones** → **Gráfico de barras agrupadas** (barras horizontales)
2. Posicionar debajo de la tabla (lado izquierdo)

### 5.2 Configurar Campos

```
📊 Campos de Gráfico de Barras
├─ Eje Y
│  └─ apuestas_dw dim_casa_apuestas > nombre_completo
├─ Eje X
│  └─ Medidas > Precisión %
├─ Leyenda
│  └─ (vacío)
└─ Información sobre herramientas
   └─ (vacío por ahora)
```

### 5.3 Formato Visual

**Panel Formato visual**:

1. **Título**:
   - Activar: ON
   - Texto: `Comparación de Precisión`
   - Alineación: Centro
   - Tamaño: 14pt
   - Color: `#2C3E50`

2. **Eje X**:
   - Título: OFF (no necesario)
   - Mínimo: 40
   - Máximo: 60
   - Gridlines: ON

3. **Eje Y**:
   - Título: OFF
   - Tamaño texto: 10pt

4. **Barras de datos**:
   - **Colores**:
     - Expandir **Colores**
     - Activar: `Aplicar formato de degradado`
     - Mínimo: `#FF6B6B` (rojo)
     - Centro: `#FFD700` (amarillo)
     - Máximo: `#00A36C` (verde)

5. **Etiquetas de datos**:
   - Activar: ON
   - Posición: Fuera del extremo
   - Formato: `0.0%` (un decimal)
   - Color: `#2C3E50`
   - Tamaño: 10pt

---

## 📈 PASO 6: GRÁFICO DE LÍNEAS - EVOLUCIÓN TEMPORAL

### 6.1 Crear Visual

1. Panel **Visualizaciones** → **Gráfico de líneas**
2. Posicionar al lado derecho del gráfico de barras

### 6.2 Configurar Campos

```
📊 Campos de Gráfico de Líneas
├─ Eje X
│  └─ apuestas_dw dim_fecha > temporada
├─ Eje Y
│  └─ Medidas > Precisión %
├─ Leyenda
│  └─ apuestas_dw dim_casa_apuestas > nombre_completo
└─ Valores secundarios
   └─ (vacío)
```

**IMPORTANTE**: Este gráfico puede tener muchas líneas (10 casas). Si es confuso, limitar a Top 5.

### 6.3 Filtrar a Top 5 Casas (Opcional)

1. Panel **Filtros** → **Filtros en este visual**
2. Arrastrar: `dim_casa_apuestas > nombre_completo`
3. Tipo: `Top N`
4. Configurar:
   - Mostrar: `Top 5`
   - Por valor: `Total Apuestas` (para mostrar las 5 más activas)
5. Aplicar

### 6.4 Formato Visual

**Panel Formato visual**:

1. **Título**:
   - Texto: `Evolución de Precisión por Temporada`
   - Alineación: Centro

2. **Eje X**:
   - Tipo: Categórico
   - Gridlines: OFF

3. **Eje Y**:
   - Mínimo: 40
   - Máximo: 60
   - Gridlines: ON

4. **Líneas**:
   - Grosor: 2px
   - Estilo: Sólido

5. **Marcadores**:
   - Activar: ON
   - Forma: Círculo
   - Tamaño: 4

6. **Leyenda**:
   - Posición: Derecha
   - Tamaño texto: 9pt

---

## 🔢 PASO 7: MATRIZ - PRECISIÓN POR LIGA Y CASA

### 7.1 Crear Visual

1. Panel **Visualizaciones** → **Matriz**
2. Posicionar debajo de gráficos anteriores

### 7.2 Configurar Campos

```
📊 Campos de Matriz
├─ Filas
│  └─ apuestas_dw dim_liga > nombre_liga
├─ Columnas
│  └─ apuestas_dw dim_casa_apuestas > nombre_completo
├─ Valores
│  └─ Medidas > Precisión %
└─ Obtención de detalles
   └─ (vacío)
```

### 7.3 Formato Condicional

1. Seleccionar la matriz
2. Panel **Formato visual** → **Valores de celda**
3. Expandir **Precisión %**
4. **Fondo** → Activar → **Formato condicional** (fx)

**Configurar**:
```
Escalas de Color (Fondo)
├─ Formato de estilo: Degradado
├─ ¿En qué campo se debería basar?
│  └─ Precisión %
├─ Resumir por: Promedio
├─ Mínimo
│  ├─ Número: 45
│  └─ Color: #FFCDD2 (rojo claro)
├─ Centro
│  ├─ Número: 50
│  └─ Color: #FFF9C4 (amarillo claro)
└─ Máximo
   ├─ Número: 55
   └─ Color: #C8E6C9 (verde claro)
```

5. **Aplicar**

### 7.4 Formato General

1. **Cuadrícula**:
   - Líneas verticales: ON
   - Líneas horizontales: ON
   - Color: `#E0E0E0`

2. **Totales**:
   - Totales de fila: ON (Promedio)
   - Totales de columna: ON (Promedio)
   - Etiqueta: "Promedio"

3. **Valores**:
   - Formato: `0.0%`
   - Tamaño texto: 10pt

---

## 🎚️ PASO 8: SEGMENTACIONES (FILTROS)

### 8.1 Segmentación 1: Liga

#### Crear
1. Panel **Visualizaciones** → **Segmentación de datos**
2. Posicionar en parte inferior izquierda

#### Configurar Campo
```
📊 Campo de Segmentación
└─ Campo
   └─ apuestas_dw dim_liga > nombre_liga
```

#### Formato
**Panel Formato visual**:

1. **Configuración de segmentación**:
   - Estilo: `Lista`
   - Orientación: Vertical
   - Selección múltiple: ON (Ctrl+clic para múltiple)

2. **Encabezado de segmentación**:
   - Texto: `Seleccionar Liga`
   - Tamaño: 12pt
   - Color fondo: `#34495E`
   - Color texto: Blanco

3. **Valores**:
   - Tamaño: 10pt
   - Espaciado: 5px

4. **General**:
   - Ancho: 250px
   - Alto: 200px

---

### 8.2 Segmentación 2: Temporada

#### Crear
1. Panel **Visualizaciones** → **Segmentación de datos**
2. Posicionar al centro inferior

#### Configurar Campo
```
📊 Campo de Segmentación
└─ Campo
   └─ apuestas_dw dim_fecha > temporada
```

#### Formato
**Configuración de segmentación**:
- Estilo: `Desplegable`
- Título: `Temporada`

---

### 8.3 Segmentación 3: Tipo de Resultado

#### Crear
1. Panel **Visualizaciones** → **Segmentación de datos**
2. Posicionar a la derecha inferior

#### Configurar Campo
```
📊 Campo de Segmentación
└─ Campo
   └─ apuestas_dw dim_resultado_tipo > tipo_resultado
```

#### Formato
**Configuración de segmentación**:
- Estilo: `Botón`
- Orientación: Horizontal
- Selección múltiple: ON

**Valores esperados**: H (Local), D (Empate), A (Visitante)

---

## ✅ VERIFICACIÓN FINAL

### Checklist Dashboard 1

- [ ] Título visible y centrado
- [ ] 3 KPI cards funcionando:
  - [ ] Casa Más Precisa muestra nombre
  - [ ] Precisión Máxima muestra ~50-55%
  - [ ] Total Aciertos muestra número grande
- [ ] Tabla con 10 casas ordenadas por precisión
- [ ] Colores condicionales funcionando en tabla
- [ ] Gráfico de barras muestra todas las casas
- [ ] Gráfico de líneas muestra evolución temporal
- [ ] Matriz muestra cruce Liga × Casa
- [ ] 3 segmentaciones funcionan y filtran todos los visuales

### Valores Esperados

**Precisión típica**: 48% - 53%
**Total Aciertos**: ~380,000 - 400,000
**Casas más precisas**: Típicamente Pinnacle, Bet365

---

## 🆘 SOLUCIÓN DE PROBLEMAS

### Problema: "No puedo arrastrar campos"
**Solución**: Asegúrate de tener el visual seleccionado (borde azul alrededor)

### Problema: "Los filtros no afectan a todos los visuales"
**Solución**:
1. Seleccionar la segmentación
2. Panel **Formato visual** → **Editar interacciones**
3. Verificar que todos los visuales tienen ícono de filtro (no "Ninguno")

### Problema: "Colores condicionales no se ven"
**Solución**: Los valores pueden estar fuera del rango. Ajustar mínimo/máximo según datos reales.

### Problema: "Matriz muy grande"
**Solución**: Activar scroll horizontal/vertical en Formato → Cuadrícula

---

📅 **Creado**: Noviembre 2025
📊 **Proyecto**: BD2_Hefesto_ApuestasDeportivas
📄 **Siguiente**: DASHBOARD_2_ROI_DETALLADO.md
