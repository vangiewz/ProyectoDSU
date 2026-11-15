# Revisión del documento vigente con los criterios del 26 de octubre

Fecha: 28/10/2026. Documento: `Documento_Taller_de_Grado_I_Grupo_8.docx`.

**Resultado: estructura completa, pero requiere correcciones antes de considerarlo listo.** Actualizar los contextos no corrigió el documento. Se detectaron discrepancias de contenido, trazabilidad y presentación; también quedan aspectos institucionales que requieren evidencia del grupo.

## Alcance y evidencia de esta revisión

- DOCX original preservado. SHA-256: `52a78642ee71bdf6b0505f5cb19e4567494374891650504e6bab5b0996c23477`.
- Extracción de párrafos, tablas, títulos y 199 imágenes (escudo más 198 figuras). Comprobaciones estructurales sobre el DOCX completo.
- Exportación con Microsoft Word, en apertura de solo lectura, a un PDF de **356 páginas**. El renderer de la habilidad no pudo ejecutarse por ausencia de LibreOffice; se usó Word y luego PDFium para la revisión visual.
- Inspección panorámica de las 356 páginas en planchas y ampliación de páginas/figuras críticas. Esto permite localizar defectos evidentes, pero **no equivale a verificar cada texto pequeño, flecha o campo al 100 % de todas las páginas**.
- Revisión dirigida del contenido de cap. 1–7 frente a la guía y a la nueva clase, y contraste puntual con generadores, modelos, controladores y SQL. No se ejecutó una prueba funcional completa del sistema ni se verificaron servicios desplegados.
- El texto del cuerpo y de las tablas, desde Introducción, coincide con la versión `2026-10-19_1632_cap1-7.docx`. Se detectaron diferencias en índices respecto de esa versión. Esto no prueba igualdad de formato, imágenes o todos los metadatos.
- Evidencia interna y scripts reproducibles: `auditoria-2026-10-28/`. Las páginas citadas abajo son las de la exportación del vigente; coinciden con la numeración visible en las páginas examinadas.

## Hallazgos que deben corregirse

### A01 — Power BI no está demostrado por la captura presentada — prioridad alta

**Dónde:** p. 335, figura 177; sección 7.5.22. También RD8 (p. 135) y despliegue (pp. 241–243).

El título dice “Informe de Power BI insertado en el tablero”, pero la imagen muestra **“El informe de Power BI aún no está publicado”**. La propia captura contradice el título y no acredita la interfaz del informe. `backend/docs/ESTADO.md` también registra publicación/configuración entre los pendientes, aunque ese estado es anterior y no basta por sí solo para describir la situación actual.

**Corrección:** si ya se completó, sustituir por una captura real del informe funcionando. Si no, completar el diseño del informe o identificar expresamente el estado pendiente/prototipo y no describirlo como publicado. RD8 sigue requiriendo cobertura; cambiar únicamente el rótulo no resuelve esa parte funcional. Verificar que arquitectura, CU22, interfaces y evidencia coincidan.

### A02 — La eliminación descrita en el diseño de datos contradice el código y el SQL — prioridad alta

**Dónde:** p. 254, 7.3.1.1; p. 260, figura 133, relación lote–predicción.

El texto define las composiciones como relaciones cuyos registros “se eliminan junto con su tabla principal”. La figura 133 muestra composición de `prediction_loteprediccion` con `prediction_prediccion`. Sin embargo, `backend/apps/prediction/models/prediccion.py` declara `lote` con `on_delete=models.PROTECT`; la FK correspondiente de `generador/fase2/script.sql` no declara `ON DELETE CASCADE`.

**Corrección:** definir la política real de conservación/borrado y reflejarla coherentemente en explicación, diagrama y código. No cambiar el código a borrado en cascada solo para hacer coincidir el dibujo: debe preservarse el histórico que requieren los requisitos. Si la composición se usa como pertenencia conceptual, explicar su sentido sin atribuirle una eliminación física que no ocurre. Revisar las demás composiciones con el mismo criterio. Relacionado con R26-09 y R26-16.

### A03 — Falta hacer explícita la correspondencia entre clases de diseño y componentes implementados — prioridad alta

**Dónde:** pp. 244–252, especialmente 7.2.6 y figura 127; análisis de CU1 y clases de seguridad.

El diseño presenta `AuthController`, `JornadaController`, `UserController`, etc., y afirma que cada controlador especializa `APIView`. En el código los componentes se llaman, por ejemplo, `LoginView(TokenObtainPairView)`, `LogoutView(APIView)` y `JornadaViewSet(AuditedViewSet)`. En `User` se modelan operaciones como `buscarPorUsuario`, `create`, `find`, `update` y `verificarClave` sin explicar su realización mediante ORM, servicios o autenticación. Los generadores trasladan operaciones del análisis al diseño y asignan retornos por convención.

**Corrección:** distinguir nombres conceptuales de nombres físicos y aportar una correspondencia verificable, o ajustar el diseño a las clases y operaciones reales. Revisar también servicios que en Python son módulos de funciones. No hace falta forzar el código a clases ficticias; sí evitar que un modelo conceptual se presente como descripción literal de la implementación. Relacionado con R26-09 y R26-16.

### A04 — La introducción todavía presenta un documento de cuatro capítulos — prioridad media

**Dónde:** pp. 36–37, Introducción.

Dice “corresponde a la primera fase” y “desarrolla los cuatro primeros capítulos”, y termina su recorrido en el capítulo 4. El vigente ya contiene siete capítulos.

**Corrección:** actualizar el alcance introductorio a fases 1 y 2, añadiendo captura de requisitos, análisis y diseño. Conservar el enfoque de propuesta donde todavía se describan resultados esperados. Relacionado con R26-20.

### A05 — Deben separarse diseño de producción y evidencia de demostración — prioridad alta

**Dónde:** pp. 241–243 (despliegue), p. 280 (introducción al script), pp. 341–343 (modelo y predicciones).

El despliegue ya usa servicios y protocolos adecuados para una propuesta de producción; **no debe rechazarse por utilizar Vercel, Neon o Docker**. El problema es la falta de distinción del estado: el script se presenta como obtenido de “la base de datos en producción”, mientras los contextos registran Neon como base con datos demo e histórico sintético y despliegue definitivo pendiente. Las figuras muestran métricas del modelo sin una nota que explique el origen sintético de los datos documentado en `backend/docs/ESTADO.md`.

**Corrección:** confirmar qué infraestructura está efectivamente en producción y cuál es el diseño objetivo. Identificar capturas, métricas y coordenadas de demostración; no presentar métricas sintéticas como validación con datos reales de DSU. Esto no obliga a usar servidores universitarios: se necesita un destino previsto y justificado. Relacionado con R26-13.

### A06 — La explicación de normalización contiene afirmaciones demasiado amplias — prioridad media

**Dónde:** p. 253, sección 7.3; tablas/diagramas de predicción.

Se afirma que la “única desnormalización” es `analytics_hechoresiduo` y las vistas, y que las tablas transaccionales cumplen Boyce-Codd. Sin embargo, el diseño también conserva `punto_id` y `sector_id` en predicciones y recomendaciones, mientras el punto ya referencia su sector. Puede tratarse de una decisión válida para conservar el sector histórico, pero esa excepción no se explica. Tampoco se documentan las dependencias funcionales que respaldan la afirmación general de Boyce-Codd. Decir que el ETL es el único escritor no demuestra, por sí solo, ausencia de inconsistencias tras cambios en los datos de origen.

**Corrección:** justificar dependencias y claves relevantes con ejemplos concretos; enumerar redundancias/snapshots reales y su política de actualización. Ajustar el alcance de la afirmación de normalización a lo demostrado. No modificar tablas para cumplir una explicación genérica.

### A07 — La imagen de ubicación identifica otra unidad institucional — prioridad media

**Dónde:** p. 78, figura 8, “Ubicación geográfica de la institución”.

La captura de Google Maps selecciona “Dirección Universitaria de Investigación Científica e Innovación Tecnol…”, no DSU. Puede servir como referencia de proximidad, pero no identifica por sí sola las oficinas DSU que describe el texto.

**Corrección:** usar un marcador verificado de DSU o anotar expresamente el punto real y la referencia vecina, con fuente/fecha de consulta. No inferir que la dirección textual sea falsa solo por esta captura.

### A08 — Hay diagramas con letra demasiado pequeña para una lectura cómoda — prioridad alta

**Dónde:** p. 190, figura 62 (general de CU); p. 252, figura 127 (controladores). Revisar también tamaño de detalles en clases, datos y colaboraciones.

En la página renderizada las operaciones de los controladores se reducen considerablemente respecto del texto del documento, aun en página horizontal. El general de CU tiene muchos cruces y etiquetas pequeñas. Disponer del PNG grande no garantiza legibilidad en el tamaño al que se inserta en Word.

**Corrección:** conservar la vista general exigida y añadir/reorganizar detalles legibles; dividir la vista de controladores por grupos, aumentar tipografía en EA y revisar tamaño físico de impresión. Para el general de CU, reducir cruces y ordenar grupos sin quitar actores/relaciones por estética. Verificar a tamaño de lectura, no solo ampliando la imagen fuente.

### A09 — Algunas notas quedaron separadas de su figura o tabla — prioridad media

**Dónde:** p. 158 abre con “Nota. Elaboración Propia” correspondiente a una figura de p. 157. También se observan notas al inicio de pp. 311, 316, 320 y 336, separadas de contenido de la página precedente.

**Corrección:** mantener juntos rótulo, figura y nota cuando sea posible; reservar el espacio de la nota al dimensionar capturas. Revisar ajustes de párrafos y paginación sin mantener juntas tablas enteras demasiado largas. Exportar otra vez y comprobar los cortes.

### A10 — La columna Tamaño mezcla magnitudes sin explicar su unidad — prioridad media

**Dónde:** 7.3.2.1, tablas de volumen, por ejemplo tabla 134 (pp. 269–270), tabla 137 (p. 271) y tabla 151 (pp. 277–278).

Se combinan “8 bytes”, “Variable” y números sin unidad: `numeric(8,2)` aparece con tamaño `8`, `numeric(4,3)` con `4`, y `varchar(600)` con `600`. El generador `_tamano()` toma el primer parámetro entre paréntesis: describe precisión/longitud declarada, no un tamaño físico homogéneo. El lector no puede interpretar la columna de manera uniforme.

**Corrección:** separar longitud/precisión y escala de almacenamiento, o usar etiquetas explícitas (“8 dígitos, escala 2”, “máx. 600 caracteres”, “almacenamiento variable”). Si se quiere estimar volumen físico, establecer supuestos y una unidad consistente; no tratar precisión numérica como bytes.

## Aspectos que requieren respaldo, no deben darse por falsos

1. **Información institucional, pp. 72–80.** Misión, visión, historia específica de DSU, organigrama, teléfonos, correo y dimensionamiento (10 operarios, 45 puntos, tres sectores, etc.) no tienen una fuente identificable junto a esos datos. “Elaboración propia” explica la autoría de una tabla, pero no de dónde se obtuvo la información. Incorporar la fuente institucional o entrevista/levantamiento real y diferenciar una propuesta de una declaración oficial. No inventar nombres, fechas de entrevistas o cargos. R26-03.
2. **Antecedente específico, p. 40.** Se habla de experiencias documentadas en otros campus para predecir residuos, pero se cita únicamente “Breiman (2001), Random forests”. Hace falta verificar que la fuente respalde ese caso aplicado o aportar un estudio específico. En esta auditoría no se consultó íntegramente ese artículo; se registra como comprobación bibliográfica pendiente, no como falsedad comprobada.
3. **Validación externa y operativa.** No se verificó la totalidad de referencias, el despliegue activo, licencias/configuración de Power BI, requisitos de rendimiento, datos institucionales ni todos los permisos ejecutando el sistema. El estado histórico del código no certifica cumplimiento actual.

## Lo que sí se comprobó

- Siete capítulos y subcarátulas presentes.
- El título contiene función principal, institución y Random Forest Regressor; la observación sobre títulos del otro grupo no exige cambiarlo por OCR o IA genérica.
- Los cinco roles humanos de DSU, Usuario abstracto y Temporizador se explican; no corresponde reducirlos automáticamente a los tres actores de la dirección de carrera del compañero.
- **38 CU** en identificación y catálogo vigente; 38 tablas de detalle con las nueve filas previstas, 38 apartados de análisis y 38 apartados de interfaces.
- El catálogo cubre **RF1–RF27**, y asigna cada CU a uno de ocho paquetes: 4, 4, 4, 7, 4, 3, 5 y 7 CU respectivamente. Esta comprobación no sustituye revisar semánticamente todos los enlaces de las figuras.
- Entrenar/evaluar (CU27), publicar/revertir (CU28), predecir (CU29), generar alertas/recomendaciones (CU30) y atender (CU31) están separados. La omisión de ejecutar el análisis que tenía el compañero no existe como omisión de catálogo en DSU.
- Existen `include`, `extend` y generalizaciones; arquitectura física con protocolos, explicación del despliegue y arquitectura lógica por capas.
- Hay ocho secuencias de CU principales, coherente con la selección permitida por el docente, y capturas de escritorio/móvil.
- 198 rótulos de figuras y 154 de tablas, sin huecos ni duplicados; los 352 rótulos usan campos. No se encontraron mensajes de error de referencia en los párrafos.
- Las 356 páginas tienen contenido; las páginas de poco texto son subcarátulas. La revisión panorámica no detectó páginas totalmente vacías.
- Las interfaces tienen fondo mayormente claro. No hay motivo para rehacer el producto entero por la recomendación sobre pantallas oscuras; conviene valorar el gasto de tinta de las grandes áreas rojas en portada de acceso y menús.

## Orden sugerido para corregir

1. Resolver A01–A03 y A05: evidencia Power BI, política de borrado, correspondencia diseño–código y distinción producción/demo.
2. Actualizar introducción, normalización, ubicación y unidades de tablas; incorporar las fuentes institucionales disponibles.
3. Mejorar diagramas y paginación, conservando la cobertura verificada.
4. Revisar que todo cambio se propague a tablas, figuras, generadores y contexto. Regenerar desde una base preservada y comparar con el vigente.
5. Exportar y revisar nuevamente; la nueva versión debe verificarse antes de marcar estos hallazgos resueltos.

## Contexto y archivos de instrucciones

Se retiró `AGENTS.md`, que se había creado como entrada adicional y duplicaba el mapa de lectura. `CLAUDE.md` sigue siendo la entrada de contexto junto con la guía, el progreso y la nota de clase. Se puede leer directamente sin mantener una copia de sus instrucciones en otro archivo.

La nota del 26/10 cubre el contenido identificado en la transcripción completa y distingue observaciones particulares de criterios generales. No se garantiza ausencia absoluta de errores de reconocimiento ni de matices visuales no examinados. La evidencia original y las marcas temporales permiten volver a comprobar un punto dudoso.

**No se modificó el DOCX, los diagramas EA ni el software durante esta revisión. Los hallazgos siguen abiertos.**

## Estado al 30/10/2026

Corregidos en los generadores y regenerado el vigente (`versiones/2026-10-30_1211_cap1-7.docx`, 371 páginas, 200 figuras, 155 tablas; detalle en `generador/fase2/PROGRESO.md`): A02, A03, A04, A05, A06, A09 (sin notas separadas en el PDF exportado), A10 y la vista de controladores de A08 (dividida en tres figuras).
A01 solo parcial: el rótulo ya no afirma que el informe esté publicado; falta publicarlo y recapturar.
Siguen abiertos: A07, el diagrama general de CU (A08) y los aspectos que requieren respaldo institucional/bibliográfico.
