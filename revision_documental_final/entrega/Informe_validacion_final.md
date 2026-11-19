# Validación de la entrega DSU / Residata

Revisión documental del 19/11/2026. Documento canónico: **Documento_Software_2_DSU_Entrega.docx / .pdf**. La copia con sufijo Final es una exportación anterior que estaba abierta durante el cierre; no es la versión para imprimir.

## Conservación y correcciones

Se partió del Word vigente, con copia de seguridad y sin ejecutar el ensamblador antiguo. Se conservaron la portada general, las trece carátulas institucionales, los integrantes, sus registros, el docente, el grupo y la identidad del proyecto. El documento de otro grupo sirvió como referencia de estructura, sin copiar sus datos.

Se corrigieron la numeración heredada de PUDS, las referencias del SQAP, títulos y fuentes de figuras, rótulos SEQ de figuras/tablas, cuatro índices automáticos, páginas vacías de sección, rótulos separados de sus figuras, cabeceras repetidas y cortes de cifras. Los títulos se mantienen en negro. Se agregó bibliografía oficial para las correcciones legales y se retiró una cifra poblacional sin respaldo.

## Modelado

Se revisaron las 190 fuentes originales y se estableció su correspondencia con la numeración final. Hay 141 sustituciones o vistas de lectura ampliadas, 15 continuaciones adicionales de actividades, nueve láminas de mensajes ampliados y un atlas de 23 entidades del ORM. Las responsabilidades de análisis/diseño se etiquetan como conceptuales; sus nombres no se anuncian como clases Python.

La introspección del esquema, sin consultar la base compartida, identifica 21 modelos propios y dos de Django auth. La copia DSU-ModeloImplementado-20261119.eapx contiene 23 modelos, 225 atributos y 51 relaciones, con lectura de retorno sin discrepancias respecto del JSON. Las cinco tablas intermedias automáticas están inventariadas por separado. Los otros EAPX conservan antecedentes de modelado, no reemplazan el atlas implementado.

Las vistas de clases completas incluyen campos y multiplicidades; los componentes señalan archivos reales. La topología muestra que el navegador descarga React desde Vercel y llama directamente a la API de Azure, que usa PostgreSQL en Neon. Los flujos de actividades conservan sus identificadores y referencias entre partes. La lectura ampliada confirmó CU14 → CU15 include: no existe un include inverso desde CU15.

## Pruebas y alcance de la evidencia

El capítulo 9 desarrolla PUDS aplicado a pruebas, listas adaptadas, herramientas QA y caja blanca. Los anexos L/M/N amplían 14 áreas de comprobación, trazabilidad de 27 RF y fichas de herramientas con fecha/configuración/límites.

Los tres grafos tienen (N,E,P,V): CU9 (11,17,1,8), CU15 (11,17,1,8), CU28 (14,21,1,9). Se verificaron matrices y rango de 25 caminos independientes. El vínculo de cada camino con un test JUnit se conserva; no equivale a instrumentación automática de todas las aristas.

La regresión del cierre GUI registra **74 pruebas aprobadas en 236,50 s**, en PostgreSQL 18 local y aislado. Hay 34 CU recorridos: **28 flujos principales aprobados y seis parciales**; 240/242 recorridos consolidados, 33 recorridos corporativos, 71/75 combinaciones CU/rol con evidencia y 66 videos. Las nueve parejas PDF/XLSX coincidieron con sus tablas (169 filas iniciales y 12 por cada reporte proyectado). Se describen once correcciones funcionales. Las dos diferencias de autorización y los límites de excepciones no se ocultan.

Se conservan Lighthouse, W3C, Observatory, SSL Labs y ZAP con sus fechas originales. No se presentan como nuevos escaneos de esta edición. ZAP fue baseline pasivo en HTTP local y terminó con advertencias; no acredita pentest completo. Un 200 de un sitio no acredita recepción de correo, aceptación institucional ni disponibilidad mensual.

## Cálculos y coherencia comercial

Se distinguieron archivos lógicos de puntos de función y tablas ORM; se comprobaron las operaciones de PAPS/PERT/COCOMO en su alcance de estimación. Se recalculó la carga patronal de planificación: 17,21 % (salud 10 % + SIP 7,21 %). Las siete comprobaciones financieras pasaron. Word, JSON, gráficos, HTML y PDF local del pitch usan el mismo modelo:

- VAN al 15 %: Bs 117027; TIR operativa: 41,8 %.
- Déficit acumulado máximo: Bs 164540; solicitud propuesta: Bs 200000.
- Equilibrio: 14,5 clientes Campus equivalentes; egresos antes de IUE y flujos después de IUE simplificado.
- Ejemplo de inversor: 15 % de participación, valoración post-money Bs 1333333 y retorno anual ilustrativo 5,0 %.

Son escenarios, no ventas, capacidad de nube medida ni inversión conseguida. La publicación pública aún puede conservar cifras anteriores.

## Fuentes oficiales consultadas para correcciones

- [Gestora: aporte patronal SIP](https://www.gestora.bo/archivos/bajar?id=5408).
- [ASUSS: reglamento de seguros delegados, salud](https://www.asuss.gob.bo/wp-content/uploads/2024/03/REGLAMENTO-DE-SEGUROS-DELEGADOS_CON-FIRMAS.pdf).
- [SENAPI: signos distintivos](https://www.senapi.gob.bo/signos-distintivos), [tasas](https://www.senapi.gob.bo/tasas-de-propiedad-intelectual), [procedimiento de registro de marca](https://www.gob.bo/tramites/embed/registro-de-signo-distintivo) y [registro de software](https://www.gob.bo/tramites/registro-de-programas-de-ordenador-o-software).
- [Wiley: The Art of Software Testing](https://onlinelibrary.wiley.com/doi/book/10.1002/9781119202486), como referencia de inspección; las catorce listas son una adaptación DSU, no una transcripción del libro.

## Revisión visual y límites externos

Se renderizó el PDF completo. Se inspeccionaron las 377 páginas en 48 planchas y se revisaron los cambios de la ronda final mediante comparación del cuerpo de las páginas, excluyendo únicamente el área de folio. Se ampliaron páginas críticas. El registro de legibilidad separa este examen del control automático de geometría. No se detectaron páginas vacías ni errores de campos.

Los cinco destinos QR se decodifican desde las imágenes del PDF. El repositorio devuelve 404 sin autenticación porque es privado; Drive solicita acceso. App, sitio y pitch públicos responden, pero eso no demuestra que contengan esta revisión. Se conservan los archivos complementarios sin publicar secretos para resolver los accesos.

Pendientes externos: acceso del docente al material privado, publicación por el titular, impresión y escaneo físico de QR, aceptación de la DSU, formalización empresarial/jurídica, Power BI publicado y recepción real de correo. Los permisos no observados y la cobertura exhaustiva de excepciones no se declaran aprobados.

El archivo conserva las secciones Carta del original. Para papel A4, usar ajustar al área imprimible sin recortar y revisar la vista previa, especialmente las hojas horizontales. No se realizó una impresión física ni se promete una nota de 100/100.
