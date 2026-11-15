# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

- **Personal operativo de limpieza** (10 personas, 3 cuadrillas fijas, una por sector). Registra en el propio punto de recolección cada vaciado (tipo, cantidad, observaciones) y las incidencias, desde su celular, durante la jornada 08:00–15:00 de lunes a sábado. No tiene formación técnica en informática; la interfaz debe entenderse sin capacitación extensa.
- **Supervisor de recolección** (1). Planifica jornadas y rutas, asigna personal y vehículos, sigue la ejecución, cierra jornadas y atiende incidencias de sus sectores. Se reúne con las cuadrillas al inicio y cierre de cada jornada en el Pabellón 150.
- **Cuerpo directivo de la DSU** (director). Consume indicadores, mapas y predicciones para decidir; solo consulta.
- **Administrador del sistema**. Gestiona usuarios, roles, permisos, catálogos y parámetros; ejecuta el ETL, entrena el modelo, revisa la bitácora y elabora reportes (absorbió al antiguo rol administrativo). No registra la operación de campo.

## Product Purpose

Sistema web de gestión de residuos sólidos para la Dirección de Servicios Universitarios (DSU) de la Universidad Autónoma Gabriel René Moreno (Santa Cruz de la Sierra, Bolivia). Sustituye la inspección visual y las planillas en papel por un registro digital en el punto de recolección, para saber con métricas exactas cuánto residuo genera cada sector y punto, y planificar la recolección con evidencia. Éxito: cada vaciado queda registrado en campo y el supervisor planifica rutas con datos en lugar de costumbre.

## Positioning

Es la primera plataforma informática de la DSU (no reemplaza ningún sistema). Su diferencia es el ciclo completo propio del campus: captura en campo por punto georreferenciado → histórico depurado → predicción de generación por punto con Random Forest Regressor → alertas y recomendaciones que el supervisor acepta o descarta. Las predicciones son siempre de apoyo y se muestran con su margen de error, nunca como valores exactos.

## Operating Context

- Campus central UAGRM: 45 puntos de recolección (contenedores y basureros en accesos, pasillos, patios y áreas verdes), 3 sectores, 2 vehículos (camioneta y camión), 6 carros recolectores manuales, área de acopio temporal junto al Pabellón 150.
- Flujo: jornada planificada → asignación de cuadrilla → apertura → recorrido punto por punto (vaciado o motivo de omisión) → cierre con resumen.
- Captura con celular en exteriores del campus; condiciones del dispositivo (sol, guantes, gama) no confirmadas: diseñar para el peor caso razonable.
- Conectividad: red institucional o datos móviles; las interrupciones deben informarse al usuario.

## Capabilities and Constraints

- Implementado RF1–RF27: usuarios, roles y permisos, autenticación, sectores, puntos georreferenciados, tipos de residuo y unidades, contenedores, registro de vaciado, histórico, incidencias, jornadas, bitácora; ETL, indicadores, tablero (y vistas para Power BI), mapa de calor observado y proyectado, comparación de periodos, reportes Excel/PDF; modelo Random Forest (versiones, métricas), predicción con margen de error, alertas y recomendaciones que el supervisor acepta o descarta.
- Las estimaciones del modelo se muestran "a lápiz" (gris grafito, subrayado punteado, "≈ valor ± margen"), nunca en el azul de bolígrafo reservado a lo capturado por personas.
- Requisitos de interfaz del documento: registro de un vaciado en ≤4 interacciones (RNF8); captura optimizada para pantalla pequeña y una sola mano (RI3); búsqueda de puntos por código, nombre o sector (RI4); mensajes claros de error, validación y confirmación (RI5); pantalla cartográfica Leaflet/OpenStreetMap (RI6).
- Ningún registro histórico se elimina; las bajas son lógicas. La bitácora es inalterable.
- Terminología: punto de recolección, sector, jornada, vaciado, incidencia, ruta, cuadrilla.

## Brand Commitments

- Identidad de la Dirección de Servicios Universitarios: emblema tipográfico con la sigla **DSU** en blanco sobre bloque **rojo**, color institucional de la dirección, acompañado de la denominación completa y la referencia a la UAGRM. El sistema adopta el rojo DSU como color de marca y el monograma DSU como logo.
- Idioma: español (Bolivia).

## Evidence on Hand

- Documento de requisitos: `../Documento_Taller_de_Grado_I_Grupo_8.docx` (cap. 4, IEEE 830).
- No hay logotipo en archivo vectorial, fotos del campus ni coordenadas oficiales de los puntos; los datos del comando `seed --demo` son de ejemplo y no deben presentarse como reales.

## Product Principles

1. El registro en campo manda: si capturar es lento o confuso, todo lo demás (indicadores, mapas, predicción) pierde valor.
2. Cada pantalla muestra solo lo que el rol puede hacer; el control de acceso se ve, no solo se aplica.
3. Las predicciones y recomendaciones apoyan la decisión; nunca la reemplazan ni se muestran como exactas.
4. Trazabilidad visible: quién registró qué y cuándo siempre es consultable.

## Accessibility & Inclusion

- Usuarios operativos sin formación técnica: lenguaje llano, objetivos táctiles amplios, sin depender de gestos finos.
- Uso en exteriores probable: contraste alto en la pantalla de captura (WCAG 2.2 AA como mínimo).
