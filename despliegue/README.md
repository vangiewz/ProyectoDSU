# Publicación desde GitHub

Los proyectos existentes de Vercel están vinculados a vangiewz/ProyectoDSU. La rama de producción es main; las otras ramas generan previews. vercel_proyectos.json registra la configuración esperada, sin tokens ni secretos.

- dsu-uagrm: raíz gestion-residuos-dsu/frontend, Vite, Node 22.x, instalación npm ci, build npm run build y salida dist. VITE_API_URL contiene el dominio público de Azure en producción y preview.
- residata: raíz sitio-residata, preset Other, Node 22.x, build python3 preparar_publicacion.py --solo-publico, salida dist, sin instalación npm. Ese comando copia solo HTML, CSS, JS, fuentes, imágenes, marketing y pitch públicos.
- Azure: backend/deploy/compose.azure.yml, configuración .env solo en la VM. El job CD exige secrets y espera los checks de backend, frontend y sitio. No se cambia Neon ni se siembran datos al publicar.

Comprobar en cada cierre: Actions en verde, checks Vercel sin error, app y sitio 200, API 401 sin sesión, recursos del frontend disponibles y pitch con las cifras de la entrega. Un check de compilación no sustituye todos los flujos autenticados ni mide disponibilidad mensual.

El repositorio excluye .env y sus valores históricos. Conservar el respaldo privado del titular y usar clones nuevos después de la reescritura. La eliminación del historial no revoca credenciales antiguas; el repositorio permanece privado hasta completar su rotación.
