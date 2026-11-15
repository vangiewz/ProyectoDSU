---
version: 1
slug: "src-app-tsx"
primary_target: "src/App.tsx"
related_targets: []
---

# Superficie: aplicación web DSU (panel + captura en campo)

Modo: Operate. Ruta code-led (sin generación de imágenes).

Audiencia y tarea: personal operativo registra vaciados en el punto (celular, exteriores, ≤4 interacciones); supervisor planifica, asigna, ejecuta y cierra jornadas; administrativo y directivo consultan histórico, incidencias y bitácora; administrador gestiona usuarios, roles y catálogos.

Restricciones: español; rojo DSU y monograma DSU como marca; contraste AA mínimo; objetivos táctiles ≥48px en campo; Leaflet/OSM para mapas; navegación y controles estándar web.

## Direction contract

THESIS: La planilla de control en papel que la DSU usa hoy se vuelve el sistema: cada cambio de estado se estampa como un sello y cada dato capturado en campo se ve en tinta de bolígrafo. Rechaza el panel gris con tarjetas de métricas y acento azul.

OWN-WORLD: Papel de formulario frío (#F4F6F8) con hojas blancas, grafito (#1E2328) para rótulos, azul bolígrafo (#1F3FA8) solo para valores capturados por personas, rojo DSU (#C4122F) como riel lateral y tinta de sello. Sellos rectangulares de doble filete, rotados, en tintas por estado (ATENDIDO verde, OMITIDO ámbar, CERRADA rojo DSU). Archivo como única familia: ancho condensado para sellos y rótulos, normal para texto, cifras tabulares siempre. Filetes de 1px, esquinas de 2–4px.

STORY: El usuario entra y ve de inmediato qué le toca hoy y en qué estado está cada punto; registra o planifica sin pensar en la herramienta; confía en que todo queda asentado y es rastreable.

FIRST VIEWPORT: Escritorio: riel rojo DSU de 240px a la izquierda con el monograma DSU en blanco arriba y la navegación por rol; la pestaña activa sale del riel como hoja blanca. Área de trabajo: encabezado con título y acción primaria a la derecha; debajo, la jornada del día con su eje 08:00–15:00 y los sellos de cada parada en su hora real, y la tabla de paradas. Celular (operativo): barra roja superior, la parada actual expandida a pantalla con código grande, tipos de residuo como botones grandes, cantidad numérica y el botón Registrar fijo al pulgar; paradas previas comprimidas con su sello.

FORM: Planilla de control sellada, posición 3 de mi lista ordenada; seed key 2f3f2645. Gesto distintivo: el sello que cae en dos pasos (120ms, steps(2)) al confirmar un estado. Raises: cifras tabulares alineadas (Ikeda); una sola familia a toda escala (Emigre); eje horario real de la jornada (Labanotation); parada actual expandida, previas comprimidas (streaming); cambios de estado en pasos cortos sin easing (acetato).

FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance
