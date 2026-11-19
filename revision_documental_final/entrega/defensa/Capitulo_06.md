# CAPÍTULO 6: Infraestructura para la producción de software

Objetivo: explicar y justificar Infraestructura para la producción de software.

Contenido para recorrer: 6.1. Topología y entornos; 6.2. Herramientas y utilización real; 6.3. Accesos, respaldo y control de cambios.

Pregunta: ¿qué parte se ejecutó y qué parte es propuesta? Respuesta: señalar los resultados fechados y sus archivos; una plantilla, estimación o trámite preparado no demuestra ejecución, ventas, aceptación institucional ni formalización.

Pregunta: ¿qué exige el docente? Respuesta: trece puntos en un PDF, carátula por punto, anexos con QR a material existente y cuatro modalidades de pruebas en el capítulo 9.

Evidencia: localizar el capítulo y sus referencias en el índice actualizado del Word/PDF; contrastar las afirmaciones técnicas con gestión-residuos-dsu y los resultados en auditoria_gui y auditoria_cierre.

Límite para la defensa: no convertir métricas sintéticas en resultados reales ni evidencias históricas en mediciones nuevas.


## Desarrollo específico

El navegador obtiene archivos de Vercel y llama directamente a la API por HTTPS. Caddy y Gunicorn sirven Django en Azure VM; el ORM accede a Neon por PostgreSQL/TLS. La QA usa PostgreSQL propio en loopback. Compilar y probar no equivale a desplegar; el titular publicará los cambios.

Infraestructura

**Evidencia:** backend/deploy/compose.azure.yml; config/settings.py.

**Pregunta probable:** ¿Dónde están los datos?
**Respuesta defendible:** PostgreSQL permanece en Neon. La API se despliega en Azure y React en Vercel. PostgreSQL local se usa solo para QA aislado.

**Antes de exponer:** abrir el artefacto citado, identificar su fecha y entorno y señalar qué se ejecutó, qué se estimó y qué queda pendiente.



**Trabajo del grupo:** se conserva y corrige el capítulo del documento vigente; las actividades ejecutadas son las identificadas mediante fuentes, pruebas y archivos. Las previsiones no se convierten en actas históricas.

**Referencia de lectura:** localizar el capítulo en el índice final y en la matriz de revisión, que registra sus páginas. Las rutas del repositorio requieren su copia privada; los archivos de esta entrega se consultan directamente en sus carpetas.
