---
name: Sistema de gestión de residuos DSU-UAGRM
description: Planilla de control sellada para registrar, analizar y predecir la generación de residuos del campus.
colors:
  dsu: "#c4122f"
  dsu-hondo: "#9a0e25"
  boligrafo: "#1f3fa8"
  lapiz: "#55606c"
  sello-ok: "#1e7a46"
  sello-omit: "#9a5b00"
  papel: "#f4f6f8"
  hoja: "#ffffff"
  grafito: "#1e2328"
  grafito-2: "#4a5560"
  filete: "#c9ced6"
  filete-suave: "#e3e7ec"
  calor-1: "#f6d5da"
  calor-2: "#ec9aa6"
  calor-3: "#d9485f"
  calor-4: "#c4122f"
  calor-5: "#7a0a1c"
typography:
  cifra-grande:
    fontFamily: "Archivo Variable, Archivo, system-ui, sans-serif"
    fontSize: "3.25rem"
    fontWeight: 800
    lineHeight: 1
    letterSpacing: "-0.025em"
  display:
    fontFamily: "Archivo Variable, Archivo, system-ui, sans-serif"
    fontSize: "2.5rem"
    fontWeight: 800
    lineHeight: 1
    letterSpacing: "-0.025em"
    fontVariation: "'wdth' 75"
  headline:
    fontFamily: "Archivo Variable, Archivo, system-ui, sans-serif"
    fontSize: "1.75rem"
    fontWeight: 700
    lineHeight: 1.2
    letterSpacing: "-0.025em"
    fontVariation: "'wdth' 88"
  title:
    fontFamily: "Archivo Variable, Archivo, system-ui, sans-serif"
    fontSize: "1.125rem"
    fontWeight: 700
    lineHeight: 1.4
    fontVariation: "'wdth' 90"
  cifra:
    fontFamily: "Archivo Variable, Archivo, system-ui, sans-serif"
    fontSize: "1.75rem"
    fontWeight: 700
    lineHeight: 1
    fontFeature: "'tnum' 1"
  body:
    fontFamily: "Archivo Variable, Archivo, system-ui, sans-serif"
    fontSize: "0.875rem"
    fontWeight: 400
    lineHeight: 1.43
    fontFeature: "'tnum' 1"
  label:
    fontFamily: "Archivo Variable, Archivo, system-ui, sans-serif"
    fontSize: "0.72rem"
    fontWeight: 650
    letterSpacing: "0.06em"
    fontVariation: "'wdth' 80"
  sello:
    fontFamily: "Archivo Variable, Archivo, system-ui, sans-serif"
    fontSize: "0.78rem"
    fontWeight: 800
    lineHeight: 1.25
    letterSpacing: "0.08em"
    fontVariation: "'wdth' 70"
rounded:
  sello: "3px"
  hoja: "4px"
spacing:
  celda-y: "10px"
  celda-x: "12px"
  hoja: "20px"
  seccion: "24px"
  pagina-movil: "16px"
  pagina: "32px"
components:
  button-primario:
    backgroundColor: "{colors.grafito}"
    textColor: "{colors.hoja}"
    rounded: "{rounded.hoja}"
    padding: "0 16px"
    height: "40px"
  button-primario-hover:
    backgroundColor: "#000000"
  button-primario-grande:
    backgroundColor: "{colors.grafito}"
    textColor: "{colors.hoja}"
    rounded: "{rounded.hoja}"
    padding: "0 24px"
    height: "56px"
  button-secundario:
    backgroundColor: "{colors.hoja}"
    textColor: "{colors.grafito}"
    rounded: "{rounded.hoja}"
    padding: "0 16px"
    height: "40px"
  button-peligro:
    backgroundColor: "{colors.hoja}"
    textColor: "{colors.dsu}"
    rounded: "{rounded.hoja}"
    padding: "0 16px"
    height: "40px"
  button-peligro-hover:
    backgroundColor: "{colors.dsu}"
    textColor: "{colors.hoja}"
  button-fantasma:
    textColor: "{colors.grafito-2}"
    rounded: "{rounded.hoja}"
    padding: "0 16px"
    height: "40px"
  input:
    backgroundColor: "{colors.hoja}"
    textColor: "{colors.boligrafo}"
    rounded: "{rounded.hoja}"
    padding: "0 12px"
    height: "40px"
  input-cantidad-campo:
    backgroundColor: "{colors.hoja}"
    textColor: "{colors.boligrafo}"
    typography: "{typography.display}"
    rounded: "{rounded.hoja}"
    height: "64px"
  opcion-campo-elegida:
    backgroundColor: "{colors.boligrafo}"
    textColor: "{colors.hoja}"
    rounded: "{rounded.hoja}"
    padding: "0 12px"
    height: "56px"
  hoja:
    backgroundColor: "{colors.hoja}"
    rounded: "{rounded.hoja}"
    padding: "{spacing.hoja}"
  sello:
    typography: "{typography.sello}"
    rounded: "{rounded.sello}"
    padding: "0.15em 0.55em"
  riel:
    backgroundColor: "{colors.dsu}"
    textColor: "{colors.hoja}"
    width: "248px"
  riel-item-activo:
    backgroundColor: "{colors.papel}"
    textColor: "{colors.grafito}"
    rounded: "4px 0 0 4px"
    height: "40px"
---

# Design System: Sistema de gestión de residuos DSU-UAGRM

## Overview

**Creative North Star: "La planilla de control sellada"**

El sistema es el papel que la DSU ya usa, convertido en herramienta: un formulario impreso sobre papel frío, con filetes finos, rótulos condensados en mayúsculas, lo que una persona capturó escrito en bolígrafo azul, lo que estima el modelo escrito a lápiz, y cada estado asentado con un sello de goma. El modo es **Operate**: densidad de tabla real, sin decoración que no cargue un dato, y un riel institucional rojo DSU que enmarca todo.

La jerarquía nace de la tinta, no de cajas ni sombras. Tres tintas distinguen la procedencia de cada cifra (bolígrafo, lápiz, sello) y el lector sabe, sin leer una leyenda, si un número fue medido en campo, estimado por el Random Forest o si es un estado. En el celular del operario la misma planilla se reduce a una sola parada grande, con objetivos táctiles de 56–64px y la cantidad escrita en bolígrafo a tamaño de display.

Interfaz en español (Bolivia). La terminología del dominio (punto de recolección, sector, jornada, vaciado, incidencia, ruta, cuadrilla) aparece tal cual en rótulos y sellos.

**Key Characteristics:**
- Papel frío (`papel`) con hojas blancas planas delimitadas por filetes de 1px; sin sombras en reposo.
- Riel lateral rojo DSU con el monograma blanco; el rojo vive en el riel, en errores y en sellos de alarma, no en los botones.
- Tres tintas de procedencia: bolígrafo = capturado por personas, lápiz = estimado por el modelo, sello = estado.
- Una sola familia (Archivo variable) que recorre toda la escala usando el eje de ancho; cifras tabulares por defecto.
- Movimiento en dos pasos cortos, sin easing decorativo.

## Colors

Paleta de oficina pública: grises fríos de formulario, un rojo institucional y tintas de escritura con significado fijo.

### Primary
- **Rojo DSU** (`dsu`): color institucional. Fondo del riel lateral y de la barra móvil, color del monograma sobre blanco, tinta de los sellos CERRADA, FALLIDO y URGENCIA ALTA, texto de error de campo y borde/tinte del botón de peligro. Nunca es el fondo del botón primario.
- **Rojo DSU hondo** (`dsu-hondo`): texto de los avisos de error sobre tinte rojo al 5%, donde el rojo pleno no alcanza contraste.

### Secondary
- **Azul bolígrafo** (`boligrafo`): exclusivamente valores capturados por personas: el texto dentro de todo campo de entrada (y el caret), cifras medidas (`.tinta`), barras y columnas de cantidades medidas, la opción elegida en la captura de campo y el anillo de foco. También tiñe los sellos CONFIRMADA, APROBADO y EN CURSO.
- **Lápiz** (`lapiz`): exclusivamente estimaciones del modelo, siempre escritas como "≈ valor ± margen unidad" con subrayado punteado (RNF13). Es la tinta de los gráficos de predicción.

### Tertiary
- **Tinta de sello verde** (`sello-ok`): ATENDIDO, SIN RESIDUOS, ATENDIDA, VIGENTE, ACEPTADA; avisos de éxito; punto de "Activo".
- **Tinta de sello ámbar** (`sello-omit`): OMITIDO, PENDIENTE, EN EJECUCIÓN, RECHAZADO, URGENCIA MEDIA; puntos observados en el mapa.

### Neutral
- **Papel de formulario** (`papel`): fondo de la aplicación, fila en hover, ítem activo del riel, campos deshabilitados.
- **Hoja** (`hoja`): toda superficie de trabajo (tablas, gráficos, tarjetas de parada, avisos informativos).
- **Grafito** (`grafito`): texto principal y rótulos impresos; fondo del botón primario.
- **Grafito medio** (`grafito-2`): texto secundario, rótulos de campo, ejes de gráficos, sellos neutros (PLANIFICADA, DESCARTADA, REEMPLAZADA, URGENCIA BAJA).
- **Filete** (`filete`): bordes de hojas, controles y tablas.
- **Filete suave** (`filete-suave`): separadores entre filas, líneas de grilla de los gráficos, fondo del lienzo del mapa.

### Escala de calor
- **Calor 1–5** (`calor-1` a `calor-5`): escala secuencial de un solo tono, rojo DSU de claro a oscuro, para la intensidad de generación en el mapa de calor, el relleno de los marcadores por peso y la leyenda en degradé. En la capa proyectada los marcadores llevan además contorno discontinuo.

### Named Rules
**The Tres Tintas Rule.** Bolígrafo es lo que escribió una persona; lápiz es lo que estimó el modelo; nada estimado se escribe jamás en bolígrafo, y ninguna estimación aparece sin "≈" y sin su "± margen".

**The Riel Rojo Rule.** El rojo DSU es el marco institucional (riel, monograma) y la tinta de alarma; las acciones van en grafito. Si un botón rojo aparece fuera de una acción destructiva, está mal.

## Typography

**Display Font:** Archivo Variable (con Archivo, system-ui, sans-serif)
**Body Font:** Archivo Variable
**Label/Mono Font:** Archivo Variable, comprimida por el eje de ancho

**Character:** Una sola grotesca carga toda la escala, de la cifra de 52px al rótulo de 11.5px. La voz cambia con el ancho (`font-stretch` 70%–100%), no con otra familia: condensada y en mayúsculas suena a formulario impreso y a sello de goma; a ancho normal es texto de lectura.

### Hierarchy
- **Cifra grande** (800, 3.25rem, 1): el total del tablero, en bolígrafo; única excepción con numerales proporcionales porque está sola.
- **Display** (800, 2.5rem, 1, ancho 75%): el código del punto en la parada actual de la captura móvil.
- **Headline** (700, 1.5rem → 1.75rem desde 640px, ancho 88%): título de página en el encabezado con filete inferior.
- **Title** (700, 1.125rem / 1rem, ancho 90%): títulos de hoja y de figura.
- **Cifra** (700, 1.75rem, 1): consolidados de jornada, en bolígrafo, con la unidad en 1rem.
- **Body** (400, 0.875rem): tablas, avisos y detalle; controles a 0.95rem.
- **Label** (650, 0.72rem, 0.06em, mayúsculas, ancho 80%): rótulos de campo, encabezados de tabla, términos de listas de datos.
- **Sello** (800, 0.78rem, 0.08em, mayúsculas, ancho 70%): solo dentro del sello.

### Named Rules
**The Una Familia Rule.** Archivo variable es la única familia. La jerarquía se construye con peso y ancho, nunca con una segunda tipografía.

**The Cifra Tabular Rule.** Todo el documento usa `tabular-nums`; las cantidades en columnas se alinean a la derecha.

## Layout

Rejilla de dos columnas desde 1024px: riel fijo de 248px a la izquierda y contenido con ancho máximo de 72rem centrado (padding 32px horizontal, 32px vertical). Debajo de 1024px el riel se convierte en una barra roja de 56px con el monograma y un menú que abre el riel como cajón (máx. 300px u 85vw). Padding de página móvil 16px.

Ritmo sobre la base de 4px de Tailwind: hojas con 20px de padding (16px en la captura móvil), celdas de tabla 10px × 12px, 24px entre el encabezado y el contenido, 8–12px entre controles. La captura en campo es una sola columna: tarjeta de la parada, opciones de residuo en dos columnas, cantidad, y el recorrido comprimido debajo. El eje de la jornada dibuja 08:00–15:00 en horizontal y coloca cada parada en su hora real.

## Elevation & Depth

Plano por defecto: la profundidad la dan el papel frente a la hoja blanca y los filetes de 1px. Las sombras solo aparecen en elementos que flotan sobre otro contenido.

### Shadow Vocabulary
- **Etiqueta flotante** (`box-shadow: 0 2px 8px rgb(0 0 0 / 0.08)`): tooltip de los gráficos y leyenda del mapa (0.1 de opacidad).
- **Cajón** (`box-shadow: 4px 0 24px rgb(0 0 0 / 0.25)`): riel móvil abierto sobre un velo de grafito al 40%.

### Named Rules
**The Hoja Plana Rule.** Una hoja en reposo no tiene sombra; si necesita separarse, gana un filete, no una sombra.

## Shapes

Esquinas casi rectas de papel cortado: 4px en hojas, controles y botones; 3px en sellos y en el bloque del monograma; las barras horizontales solo redondean la punta (4px a la derecha) y las columnas solo la parte superior. Los bordes son filetes de 1px; la selección táctil de campo usa 2px. El estado vacío usa filete discontinuo. Las únicas formas circulares son los marcadores del mapa y el punto de "Activo".

## Components

### Buttons
Sobrios y tipográficos: la acción se distingue por peso, no por color de marca.
- **Shape:** esquina de hoja (4px); 40px de alto, 56px y texto 1.125rem en la variante grande de campo.
- **Primario:** grafito con texto blanco, semibold; hover a negro.
- **Secundario:** hoja blanca con filete; hover oscurece el filete a grafito medio.
- **Peligro:** hoja blanca, texto rojo DSU y filete rojo al 50%; hover se llena de rojo DSU con texto blanco.
- **Fantasma:** texto grafito medio; hover a grafito sobre filete suave.
- **Estados:** transición de color de 100ms; deshabilitado al 60% de opacidad; cargando muestra un spinner a la izquierda y bloquea el botón.

### Inputs / Fields
- **Style:** hoja blanca, filete de 1px, 4px, 40px de alto; el texto escrito es bolígrafo. Rótulo encima en estilo Label.
- **Focus:** el borde pasa a bolígrafo; el foco por teclado global es un contorno de 2px en bolígrafo con 2px de separación.
- **Error / Disabled:** mensaje en 0.75rem rojo DSU bajo el campo; deshabilitado sobre papel con texto grafito medio.
- **Campo móvil:** la cantidad se escribe en un campo de 64px con cifra de 2rem; los tipos de residuo son botones de 56px con filete de 2px que se llenan de bolígrafo al elegirse.

### Cards / Containers
- **Corner Style:** 4px.
- **Background:** hoja blanca sobre papel.
- **Shadow Strategy:** ninguna (ver Elevation & Depth).
- **Border:** filete de 1px.
- **Internal Padding:** 20px.

### Navigation
- **Riel:** fondo rojo DSU, monograma "DSU" en rojo sobre bloque blanco (ancho 80%, 800) con la denominación en blanco al 85%. Grupos con título en mayúsculas condensadas blanco al 65%. Ítems de 40px con icono de 18px; hover blanco al 10%; el ítem activo se convierte en una pestaña de papel (fondo papel, texto grafito, esquinas izquierdas de 4px) que se funde con el contenido.
- **Móvil:** barra roja de 56px y cajón.

### Tabla
Hoja con filete; encabezados en estilo Label; filas separadas por filete suave; hover a papel cuando la fila es seleccionable; paginación con botones secundarios. El estado vacío es una hoja con filete discontinuo y texto centrado.

### Aviso
Franja de 4px de esquina con icono de 16px: error (filete rojo 40%, tinte rojo 5%, texto rojo hondo), éxito (verde de sello), información (hoja con filete, texto grafito medio).

### Sello (componente firma)
Estado asentado sobre el registro, no adorno. Mayúsculas condensadas (ancho 70%, 800), doble filete en la tinta del estado (borde de 2px más contorno de 1px separado 2px), esquina de 3px, rotado −3° y con una máscara de ruido fractal que imita la tinta irregular de un sello de goma. Al asentarse un estado nuevo cae en dos pasos (`estampar`: 140ms `steps(2, jump-end)`, de escala 1.4 a 1), sin animación con `prefers-reduced-motion`. Admite una nota corta (por ejemplo, el motivo de omisión) a ancho 85%. En el eje de la jornada el sello se reduce a una etiqueta con el código del punto en verde o ámbar.

### Estimado
La cifra del modelo: "≈ valor" a lápiz semibold con subrayado punteado y "± margen unidad" a 0.8em, sin salto de línea; el título nativo da el intervalo completo.

### Gráficos
SVG propios. Una serie y un tono por gráfico, sin leyenda: bolígrafo para cantidades medidas, lápiz para estimaciones. Barras horizontales ordenadas con el valor en la punta; columnas con grilla de tres líneas en filete suave y ejes en 11px grafito medio; las columnas en hover atenúan el resto al 45%. Lo estimado lleva bigotes de margen (trazo grafito de 1.25px de valor − margen a valor + margen). Cada gráfico tiene un conmutador "Ver tabla" que es su vista accesible.

### Mapa
Leaflet con OpenStreetMap dentro de una hoja con filete. Marcadores circulares con borde blanco: bolígrafo (en servicio), ámbar (observado), rojo DSU (fuera de servicio), grafito medio (inactivo). La capa de calor usa la escala Calor 1–5 con leyenda en degradé sobre una etiqueta flotante.

## Do's and Don'ts

### Do:
- **Do** escribir todo valor capturado por personas en bolígrafo (`boligrafo`), incluido el texto de los campos.
- **Do** escribir toda estimación del modelo a lápiz como "≈ valor ± margen unidad", con el componente Estimado o con tinta lápiz y bigotes de margen en los gráficos.
- **Do** expresar los estados con el sello y su tinta asignada; un estado nuevo cae en dos pasos (140ms `steps(2)`).
- **Do** usar un solo tono por gráfico y ofrecer siempre la vista de tabla.
- **Do** construir la jerarquía con peso y ancho de Archivo; rótulos en mayúsculas condensadas al 80%.
- **Do** mantener objetivos táctiles de 56px o más en la captura de campo.

### Don't:
- **Don't** pintar una estimación en bolígrafo ni mostrarla sin su margen.
- **Don't** usar el sello como decoración: solo marca un estado real del registro.
- **Don't** introducir una segunda familia tipográfica.
- **Don't** usar rojo DSU como fondo de botones de acción no destructiva.
- **Don't** mezclar varias series o una paleta categórica en un mismo gráfico.
- **Don't** dar sombra a las hojas en reposo ni usar transiciones con easing decorativo.
