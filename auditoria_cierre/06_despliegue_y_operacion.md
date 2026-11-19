# Operación y entrega para publicación por el titular

Estado PARCIAL: app y API respondieron en auditoría; el sitio corporativo devolvió inicialmente 404 y posteriormente 200, con la oferta anterior aún publicada. Las correcciones de esta rama son locales, no están desplegadas. El usuario eligió realizar la publicación personalmente.

## Sitio

1. Ejecutar `py -3.13 sitio-residata/preparar_publicacion.py` desde la raíz.
2. Ejecutar `node sitio-residata/probar_salud.cjs` y `python auditoria_cierre/probar_sitio.py` (este Python requiere Playwright y Chrome).
3. Iniciar sesión Vercel con la cuenta propietaria o colaboradora. Confirmar los proyectos existentes; no crear uno por error.
4. Vincular/publicar exclusivamente `sitio-residata/dist` al proyecto Residata correcto. Revisar la URL de producción antes de cambiar alias.
5. Verificar raíz, planes, contacto, soporte, privacidad, términos, marketing, pitch, PDF y RSS. No enviar correos de prueba sin autorización.
6. Conservar el identificador de despliegue anterior para revertir desde Vercel si falla.

## Backend y frontend

Leer backend/deploy/README.md. La configuración privada de la VM se conserva. El .env local no es apto para copiar a producción. El Dockerfile ejecuta migraciones normales: coordinar el despliegue y respaldar datos antes. No se aplicaron migraciones ni pruebas con escritura en Neon en el cierre.

CI ahora espera backend, frontend y sitio; verifica los dos secretos y reintenta el healthcheck. No se hizo push y no se acredita una ejecución nueva de GitHub Actions ni del CD.

## Continuidad

El ensayo restauracion.json usa PostgreSQL local y datos sintéticos; no acredita RTO productivo. La copia independiente de la VM y la restauración de un dump productivo siguen sin demostración nueva. No se promete SLA por una muestra de minutos. ETL y entrenamiento bajo demanda aún dependen de hilos web: riesgo interno declarado, no oculto como pendiente de un tercero.
