# CAPÍTULO 11: Puesta en marcha y operación

Objetivo: explicar y justificar Puesta en marcha y operación.

Contenido para recorrer: 11.1. Arquitectura comprobada y comparación económica; 11.2. Instalación, despliegue y reversión; 11.3. Disponibilidad y monitoreo; 11.4. Continuidad, respaldo y restauración; 11.5. Licencia y propuesta de condiciones.

Pregunta: ¿qué parte se ejecutó y qué parte es propuesta? Respuesta: señalar los resultados fechados y sus archivos; una plantilla, estimación o trámite preparado no demuestra ejecución, ventas, aceptación institucional ni formalización.

Pregunta: ¿qué exige el docente? Respuesta: trece puntos en un PDF, carátula por punto, anexos con QR a material existente y cuatro modalidades de pruebas en el capítulo 9.

Evidencia: localizar el capítulo y sus referencias en el índice actualizado del Word/PDF; contrastar las afirmaciones técnicas con gestión-residuos-dsu y los resultados en auditoria_gui y auditoria_cierre.

Límite para la defensa: no convertir métricas sintéticas en resultados reales ni evidencias históricas en mediciones nuevas.


## Desarrollo específico

La muestra histórica de disponibilidad tiene 19 sondeos de API, 15 de aplicación y 16 de sitio: 50 en total, no 50 de API ni disponibilidad mensual. RPO/RTO son objetivos. La restauración de QA no restaura Neon. Una copia en la misma VM no protege de pérdida del servidor.

Puesta en marcha

**Evidencia:** backend/deploy; auditoria_cierre/05_ejecuciones_pruebas/restauracion.json.

**Pregunta probable:** ¿Se probó recuperación productiva?
**Respuesta defendible:** Se verificó restauración sintética local con recuentos y claves; no es simulación de pérdida de la VM ni prueba de RTO productivo.

**Antes de exponer:** abrir el artefacto citado, identificar su fecha y entorno y señalar qué se ejecutó, qué se estimó y qué queda pendiente.



**Trabajo del grupo:** se conserva y corrige el capítulo del documento vigente; las actividades ejecutadas son las identificadas mediante fuentes, pruebas y archivos. Las previsiones no se convierten en actas históricas.

**Referencia de lectura:** localizar el capítulo en el índice final y en la matriz de revisión, que registra sus páginas. Las rutas del repositorio requieren su copia privada; los archivos de esta entrega se consultan directamente en sus carpetas.
