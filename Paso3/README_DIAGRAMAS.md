# DIAGRAMAS DEL PASO 3 - MODELO LÓGICO (ESQUEMA ESTRELLA)

**Fecha de Generación**: 2025-11-06
**Esquema**: Estrella (Star Schema)
**Total de Diagramas**: 45 PNG

---

Este directorio contiene los diagramas visuales completos del Paso 3 de la metodología HEFESTO para el Data Warehouse de Apuestas Deportivas, utilizando **esquema de estrella** con una tabla de hechos consolidada.

## 📋 Contenido

| Archivo | Descripción | Diagramas |
|---------|-------------|-----------|
| **diagrama_3a_esquema_estrella.md** | Esquema de Estrella (una tabla de hechos) | 7 diagramas |
| **diagrama_3b_dimensiones.md** | Diseño de las 6 tablas de dimensiones | 17 diagramas |
| **diagrama_3c_tabla_hechos.md** | Diseño de FACT_APUESTAS única | 9 diagramas |
| **diagrama_3d_relaciones.md** | Relaciones y cardinalidades completas | 12 diagramas |

**Total**: 4 archivos con 45 diagramas PNG generados

---

## 🎨 Cómo Ver los Diagramas

### Opción 1: GitHub (Recomendado)

GitHub renderiza automáticamente los diagramas Mermaid. Simplemente:

1. Sube los archivos `.md` a un repositorio de GitHub
2. Navega a cada archivo en la interfaz web
3. Los diagramas se visualizarán automáticamente

**Ventajas**: Sin instalación, interactivo, colores correctos

### Opción 2: Visual Studio Code

Usa la extensión Markdown Preview Mermaid Support:

```bash
# Instalar extensión
code --install-extension bierner.markdown-mermaid

# Abrir archivo y previsualizar
code diagrama_3a_esquema_constelacion.md
# Presiona Ctrl+Shift+V para ver preview
```

**Ventajas**: Local, editable, vista previa en tiempo real

### Opción 3: Mermaid Live Editor

Para editar y visualizar online:

1. Visita: https://mermaid.live/
2. Copia el contenido de los bloques ```mermaid```
3. Pega en el editor
4. Visualiza y edita interactivamente
5. Exporta como PNG/SVG si necesario

**Ventajas**: No requiere instalación, exportación a imágenes

### Opción 4: Obsidian

Si usas Obsidian para tomar notas:

1. Copia los archivos `.md` a tu vault de Obsidian
2. Los diagramas Mermaid se renderizan automáticamente
3. Navega entre archivos con enlaces internos

**Ventajas**: Integración con notas, navegación fluida

### Opción 5: Exportar a PNG/SVG

Usando Mermaid CLI:

```bash
# Instalar Mermaid CLI
npm install -g @mermaid-js/mermaid-cli

# Extraer y convertir diagramas a PNG
mmdc -i diagrama_3a_esquema_constelacion.md -o diagramas_3a/

# O usar puppeteer para mejor calidad
mmdc -i diagrama_3a_esquema_constelacion.md -o output.png -w 2000 -H 1500
```

**Ventajas**: Imágenes para documentos, presentaciones

---

## 📚 Estructura de los Diagramas

### 3a) Esquema de Estrella

**Archivo**: `diagrama_3a_esquema_estrella.md`

**Diagramas incluidos** (7 PNG):
1. Esquema de Estrella - Vista General
2. Justificación vs Constelación
3. Diagrama Entidad-Relación Detallado
4. Flujo de consultas - Pregunta 1 (Casa más precisa)
5. Flujo de consultas - Pregunta 2 (ROI por estrategia)
6. Flujo de consultas - Pregunta 3 (Arbitraje con índice filtrado)
7. Cardinalidades del esquema

**Métricas clave**:
- 1 tabla de hechos (FACT_APUESTAS consolidada)
- 6 dimensiones
- 903,680 registros
- 8 campos derivados de arbitraje pre-calculados
- Índice filtrado para queries de arbitraje

---

### 3b) Dimensiones

**Archivo**: `diagrama_3b_dimensiones.md`

**Dimensiones documentadas**:

1. **DIM_CASA_APUESTAS** (10 registros)
   - Diagrama ER
   - Mapeo desde OLTP (UNPIVOT)
   - Ejemplo de datos

2. **DIM_LIGA** (11 registros)
   - Diagrama ER
   - Distribución geográfica por país
   - Jerarquía país → liga

3. **DIM_FECHA** (~2,920 registros)
   - Diagrama ER con atributos temporales
   - Jerarquía temporal (temporada → año → trimestre → mes → día)
   - Distribución por temporada

4. **DIM_RESULTADO_TIPO** (3 registros)
   - Diagrama ER
   - Tipos de resultado (H, D, A)
   - Probabilidades por cuota

5. **DIM_EQUIPO** (~400 registros con SCD Tipo 2)
   - Diagrama ER con versionado
   - Versionado temporal (SCD Type 2)
   - Role-playing (local y visitante)
   - Ejemplo de versiones por ascensos/descensos

6. **DIM_ESTRATEGIA** (4 registros)
   - Diagrama ER
   - Las 4 estrategias (ALWAYS_H, ALWAYS_A, FOLLOW_FAV, UNDERDOG)
   - Multiplicación en ETL (4x por partido)

**Comparación final**:
- Tabla comparativa de todas las dimensiones
- Clasificación por tipo (temporal, geográfica, descriptiva, etc.)

---

### 3c) Tabla de Hechos Única

**Archivo**: `diagrama_3c_tabla_hechos.md`

**Tabla documentada** (9 PNG):

**FACT_APUESTAS** (~903,680 registros) - Tabla consolidada
   - Estructura completa ER con todos los campos
   - Clave primaria compuesta (7 columnas)
   - Clasificación de campos:
     - **Hechos Aditivos**: ganancia_total, perdida_total, inversion, cant_aciertos, cant_apuestas
     - **Hechos Semi-Aditivos**: cuotas (apostada, local, empate, visitante)
     - **Campos Derivados de Arbitraje** (8): Pre-calculados en ETL
       - arbitraje_cuota_*_max (3 campos)
       - arbitraje_casa_*_mejor (3 campos)
       - arbitraje_porcentaje, arbitraje_es_oportunidad, arbitraje_beneficio
   - Granularidad: 1 apuesta individual
   - Relaciones con 6 dimensiones + 3 FK adicionales
   - Índices (6): 5 estándar + 1 filtrado para arbitraje
   - Uso en TODOS los indicadores

**Diagramas incluidos**:
1. Estructura completa (ER)
2. Clave primaria compuesta
3. Clasificación de campos
4. Granularidad y cardinalidad
5. (Error de parsing)
6. Relaciones con dimensiones
7. Cálculo campos derivados arbitraje
8. Índices definidos
9. Uso en indicadores
10. Performance por tipo consulta

---

### 3d) Relaciones y Cardinalidades

**Archivo**: `diagrama_3d_relaciones.md`

**Contenido**:

1. **Esquema ER Completo**
   - Todas las tablas con sus campos
   - Todas las relaciones FK
   - Notación ER con cardinalidades

2. **Matriz Completa de Relaciones**
   - 14 relaciones FK documentadas
   - 7 para FACT_APUESTAS
   - 7 para FACT_ARBITRAJE

3. **Vista Detallada por Dimensión**:
   - DIM_FECHA: Relaciones temporales
   - DIM_LIGA: Relaciones geográficas
   - DIM_EQUIPO: Role-playing (local/visitante)
   - DIM_CASA_APUESTAS: Relaciones múltiples
   - DIM_ESTRATEGIA: Relación exclusiva
   - DIM_RESULTADO_TIPO: Relación exclusiva

4. **Cardinalidades Detalladas**:
   - Tabla numérica con promedios
   - Diagramas de distribución

5. **Dimensiones Conformadas vs Exclusivas**:
   - Qué permite drill-across
   - Dimensiones compartidas

6. **Integridad Referencial**:
   - Políticas ON DELETE CASCADE
   - Políticas ON UPDATE CASCADE
   - Restricciones CHECK
   - DDL completo de constraints

7. **Índices para Optimización**:
   - Índices clustered
   - Índices non-clustered
   - Índices covering

8. **Drill-Across**:
   - Ejemplo SQL completo
   - Diagrama de flujo de query

---

## 🔍 Navegación por Tema

### Si buscas información sobre...

| Tema | Archivo | Sección |
|------|---------|---------|
| **Esquema general del DW** | 3a | Vista General Estrella |
| **Por qué Estrella** | 3a | Justificación vs Constelación |
| **Cómo responder preguntas** | 3a | Flujo de Consultas |
| **Diseño de fecha/tiempo** | 3b | DIM_FECHA |
| **Equipos y cambios de liga** | 3b | DIM_EQUIPO (SCD-2) |
| **Estrategias de apuesta** | 3b | DIM_ESTRATEGIA |
| **Casas de apuestas** | 3b | DIM_CASA_APUESTAS |
| **Tabla de hechos única** | 3c | FACT_APUESTAS |
| **Detección de arbitraje** | 3c | Campos Derivados |
| **Índice filtrado** | 3c | Índices Definidos |
| **Todas las FK** | 3d | Matriz de Relaciones |
| **Integridad referencial** | 3d | Constraints |
| **Performance optimización** | 3c, 3d | Índices |

---

## 🎯 Diagramas Destacados

### Top 5 Diagramas Más Importantes

1. **Esquema de Estrella Completo** (3a_01)
   - Vista general de todo el DW
   - Una tabla de hechos central
   - 6 dimensiones conectadas

2. **DIM_EQUIPO con SCD Tipo 2** (3b_10-13)
   - Ejemplo de versionado temporal
   - Manejo de ascensos/descensos
   - Validación temporal en queries

3. **FACT_APUESTAS Estructura Completa** (3c_01)
   - Tabla de hechos única consolidada
   - Granularidad detallada
   - Campos derivados de arbitraje

4. **Cálculo Campos Derivados Arbitraje** (3c_07)
   - Pre-cálculo en ETL
   - Duplicación por partido
   - Optimización de performance

5. **Esquema ER Completo con Relaciones** (3d_01)
   - Todas las tablas y relaciones
   - Cardinalidades visuales
   - Base para implementación SQL

---

## 💡 Consejos de Visualización

### Para Presentaciones

**Recomendación**: Exporta a PNG de alta resolución

```bash
mmdc -i diagrama_3a_esquema_constelacion.md -o presentacion_esquema.png -w 3000 -H 2000 -b white
```

**Mejor para**:
- PowerPoint
- Google Slides
- Documentos PDF

### Para Documentación Técnica

**Recomendación**: Mantén en Markdown con Mermaid

**Mejor para**:
- GitHub/GitLab wikis
- Confluence
- Notion
- Documentación viva (editable)

### Para Estudio/Aprendizaje

**Recomendación**: Usa Visual Studio Code con preview

**Ventajas**:
- Navegación rápida
- Búsqueda en todos los archivos
- Vista previa lado a lado con código SQL

---

## 📊 Estadísticas de Diagramas

| Tipo de Diagrama | Cantidad | Archivos |
|------------------|----------|----------|
| **ER Diagrams** | 10 | 3a, 3b, 3c, 3d |
| **Flowcharts** | 12 | 3a, 3c |
| **Graph TB/LR** | 15 | 3a, 3b, 3c, 3d |
| **Comparisons** | 5 | 3a, 3c |
| **Índices/Performance** | 3 | 3c, 3d |

**Total generado**: 45 diagramas PNG (95.7% éxito de 47 intentos)

---

## 🛠️ Herramientas Recomendadas

### Desarrollo y Edición

| Herramienta | Propósito | Link |
|-------------|-----------|------|
| **VS Code** | Editor con preview | https://code.visualstudio.com/ |
| **Mermaid Extension** | Renderizado en VS Code | https://marketplace.visualstudio.com/items?itemName=bierner.markdown-mermaid |
| **Mermaid Live** | Editor online | https://mermaid.live/ |
| **Obsidian** | Notas con Mermaid | https://obsidian.md/ |

### Exportación

| Herramienta | Propósito | Link |
|-------------|-----------|------|
| **mermaid-cli** | Conversión a PNG/SVG | https://github.com/mermaid-js/mermaid-cli |
| **Pandoc** | Conversión Markdown→PDF | https://pandoc.org/ |

### Visualización

| Plataforma | Soporte Mermaid | Requiere |
|------------|-----------------|----------|
| **GitHub** | ✅ Nativo | Nada |
| **GitLab** | ✅ Nativo | Nada |
| **Bitbucket** | ❌ | Plugin |
| **Confluence** | ✅ | Macro Mermaid |
| **Notion** | ❌ | Embed de Mermaid Live |

---

## 📖 Referencias

### Metodología HEFESTO

- **Paso 3**: Modelo Lógico del Data Warehouse
- **Fuente**: hefesto-v2-97-128[1].pdf (páginas 97-128)
- **Secciones**:
  - 3a) Tipo de Esquema
  - 3b) Tablas de Dimensiones
  - 3c) Tablas de Hechos
  - 3d) Relaciones

### Documentación Relacionada

- **Paso 1**: `../Paso1/README.md` - Requerimientos y análisis de negocio
- **Paso 2**: `../Paso2/paso2_analisis_oltp.md` - Análisis OLTP y mapeos
- **Paso 3 Completo**: `paso3_modelo_logico.md` - Documento maestro (76 páginas)

### Sintaxis Mermaid

- **Documentación Oficial**: https://mermaid.js.org/
- **Ejemplos**: https://mermaid.js.org/syntax/examples.html
- **Live Editor**: https://mermaid.live/

---

## ✅ Checklist de Visualización

Verifica que puedas ver:

- [ ] Colores diferenciados en las tablas
- [ ] Flechas de relaciones con etiquetas
- [ ] Cardinalidades (1:N) en las relaciones
- [ ] Símbolos especiales (🏠, ⚽, 📊, etc.)
- [ ] Tablas con campos y tipos de datos
- [ ] Subgrafos con fondos de colores
- [ ] Líneas punteadas vs sólidas
- [ ] Pie charts con porcentajes

Si alguno falla, intenta con otra herramienta de visualización.

---

## 🚀 Siguientes Pasos

Una vez visualizados los diagramas:

1. **Revisar** el modelo lógico completo
2. **Validar** que responde a las 3 preguntas de negocio
3. **Implementar** el DDL en la base de datos
4. **Continuar** con Paso 4 (ETL e integración)

---

## 📞 Soporte

**Problemas con visualización**:
- Verifica que tu herramienta soporte Mermaid
- Prueba con Mermaid Live Editor primero
- Revisa la sintaxis en la documentación oficial

**Problemas con contenido**:
- Consulta `paso3_modelo_logico.md` para más detalles
- Revisa los archivos de Paso 1 y Paso 2 para contexto

---

## 📋 Resumen Final

**Documentación generada**: Paso 3 - Modelo Lógico del DW (Esquema Estrella)
**Proyecto**: BD2_Hefesto_ApuetasDeportivas
**Fecha Actualización**: 2025-11-06
**Formato**: Mermaid Diagrams → PNG (transparente)

✅ **4 archivos • 45 diagramas PNG • Esquema Estrella completo**

### Cambios v2.0

- ✅ Transformación completa de Constelación → Estrella
- ✅ 1 tabla de hechos consolidada (FACT_APUESTAS)
- ✅ Campos derivados de arbitraje pre-calculados
- ✅ 45 diagramas PNG generados con Mermaid CLI
- ✅ Índice filtrado para optimización
- ❌ Eliminados todos los archivos de constelación
