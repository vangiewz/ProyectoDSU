# Matriz final de los trece requisitos

La hoja con notas pertenece a otro grupo; no se asignan sus resultados a DSU. Estado del alcance académico/local al cierre; no implica certificación ni aceptación institucional.

|N|Requisito|Estado|Ruta exacta relativa a la raíz|Criterio verificado|Pendiente o límite|
|---|---|---|---|---|---|
|1|PAPS|CUMPLE|DocumentoSoftware2/paps.md; Entregables/Material_Drive/02_PAPS.pdf|Alcance, métricas, presupuesto y cronograma; costos distinguidos de gastos reales.|Estimaciones y responsabilidades no son horas ni actuaciones acreditadas.|
|2|Proceso PUDS|CUMPLE|DocumentoSoftware2/capitulos.md, capítulo 2; generador/fase2/datos.py; modelo_uml/|Fases, 34 CU y artefactos del mismo sistema.|No atribuir fechas de iteración ni autoría sin registros.|
|3|Manual de calidad|CUMPLE|DocumentoSoftware2/capitulos.md, capítulo 3; 03_SQAP.pdf|Plan, roles, controles, métricas, defectos y resultados reales.|No es certificación ISO ni nivel CMMI; actas vacías son formatos.|
|4|Herramientas CASE|CUMPLE|modelo_uml/*.eapx; enterprise_architect_todos.json; capítulos 2/4|Los tres modelos abrieron por API nativa; exportaciones y generadores localizables.|Lectura estructural, no inspección visual exhaustiva de cada objeto.|
|5|Aspectos legales|PARCIAL|capítulo 5; auditoria_cierre/legal/|Nombre unificado, propuesta de licencia y matriz de trámites; 174 componentes inventariados.|Registro, NIT, SENAPI, firmas y revisión final de obligaciones no acreditados. PENDIENTE EXTERNO cuando corresponda.|
|6|Infraestructura|CUMPLE|backend/deploy/compose.azure.yml; deploy/README.md; .github/workflows/ci.yml|Topología, configuración, pruebas aisladas y procedimiento de reversión concretos.|Cambios de esta rama no desplegados; CI nuevo no ejecutado en GitHub.|
|7|Sitio corporativo publicado|PARCIAL|sitio-residata/dist/; sitio/resultados.json; estado_publico_final.json|Versión local corregida, 16 recorridos y materiales preparados.|Reverificación: once rutas/recursos HTTP 200, pero con oferta y cifras anteriores. La actualización la publicará el titular; no se atribuye la recuperación a esta sesión.|
|8|Mercado y valorización|PARCIAL|capítulo 8; finanzas.py; recursos/finanzas.json|Competidores, hipótesis, TAM/SAM, precios, escenarios y sensibilidad.|No hay entrevistas, ventas ni disposición a pagar acreditadas; capacidad por cliente es supuesto.|
|9|Pruebas|CUMPLE|capítulo 9; 05_ejecuciones_pruebas/; matriz_trazabilidad.json|Regresión nueva, fallos antes/después, conexiones concurrentes, UI/API, carga, restauración y tres matrices de caja blanca.|Cumple como evidencia académica; no acredita pentest completo, aceptación de todos los RNF ni rendimiento productivo.|
|10|Marketing|CUMPLE|sitio-residata/marketing/; recursos/sitio/marketing-*.png; capítulo 10|Material digital revisado y responsive, con propuesta comercial diferenciada.|No se acreditan campañas, conversiones ni ventas; publicación dependiente del punto 7.|
|11|Puesta en marcha|PARCIAL|capítulo 11; 06_despliegue_y_operacion.md; restauracion.json|Runbook Azure, rollback, salud, demo y restauración aislada comprobados.|Publicación de correcciones, copia externa y recuperación productiva no demostradas; hilos web conservan riesgo de interrupción.|
|12|Software como producto|PARCIAL|backend/ y frontend/; demo_ui/resultados.json; regresion_final.xml|Piloto técnico funcional: jornada, vaciado, ETL, reportes y predicción con persistencia.|No es SaaS comercial terminado ni producción institucional aceptada; Power BI publicado y validación real pendientes.|
|13|Financiamiento|CUMPLE|capítulo 13; recursos/finanzas.json; pitch/Residata_pitch.pdf|Propuesta reproducible de Bs 200.000, escenarios, uso de fondos y retorno ilustrativo separado.|No es capital obtenido ni garantía de rentabilidad; ofertas y elegibilidad de terceros por confirmar.|

Resultado: 8 CUMPLE, 5 PARCIAL y 0 NO CUMPLE. CUMPLE se refiere al alcance indicado en su fila, no a una operación comercial/institucional al 100 %.
