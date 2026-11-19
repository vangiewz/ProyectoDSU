# Publicación desde GitHub

Los proyectos existentes de Vercel están vinculados a vangiewz/ProyectoDSU. La rama de producción es main; las otras ramas generan previews. vercel_proyectos.json registra la configuración esperada, sin tokens ni secretos.

- dsu-uagrm: raíz gestion-residuos-dsu/frontend, Vite, Node 22.x, instalación npm ci, build npm run build y salida dist. VITE_API_URL contiene el dominio público de Azure en producción y preview.
- residata: raíz sitio-residata, preset Other, Node 22.x, build python3 preparar_publicacion.py --solo-publico, salida dist, sin instalación npm. Ese comando copia solo HTML, CSS, JS, fuentes, imágenes, marketing y pitch públicos.
- Azure: backend/deploy/compose.azure.yml, configuración .env solo en la VM. El job CD exige secrets y espera los checks de backend, frontend y sitio. No se cambia Neon ni se siembran datos al publicar.

Comprobar en cada cierre: Actions en verde, checks Vercel sin error, app y sitio 200, API 401 sin sesión, recursos del frontend disponibles y pitch con las cifras de la entrega. Un check de compilación no sustituye todos los flujos autenticados ni mide disponibilidad mensual.

El repositorio excluye .env y sus valores históricos. Conservar el respaldo privado del titular y usar clones nuevos después de la reescritura. La eliminación del historial no revoca credenciales antiguas; el repositorio permanece privado hasta completar su rotación.

## Alcance de CI/CD

GitHub Actions ejecuta las comprobaciones de backend, frontend y sitio. El móvil se analiza, prueba y compila localmente con los comandos de su README; no tiene job automático ni publicación en una tienda.

Vercel publica la aplicación web y el sitio mediante su integración Git: main es producción y las otras ramas generan previews. Esa integración es independiente del resultado de GitHub Actions.

La API de Azure se despliega desde main después de aprobar backend, frontend y sitio. El entorno produccion de GitHub está limitado a main y contiene AZURE_VM_HOST, AZURE_VM_SSH_KEY, AZURE_VM_KNOWN_HOSTS, AZURE_CLIENT_ID, AZURE_TENANT_ID y AZURE_SUBSCRIPTION_ID. Sus valores no forman parte del repositorio. La clave SSH es exclusiva de GitHub Actions; la clave personal del titular se conserva fuera de GitHub.

Con los accesos disponibles, el job espera las pruebas, copia el backend sin .env por SSH, ejecuta Docker Compose para reconstruir el servicio app y comprueba la respuesta HTTP. La configuración privada permanece en la VM y Neon se conserva.

La identidad administrada dsu-github-deploy usa federación OIDC con el entorno produccion de este repositorio y tiene Network Contributor limitado al NSG dsu-apiNSG. El workflow autoriza solo la IP /32 del ejecutor en el puerto 22 y retira la regla temporal al terminar. La clave del host SSH está fijada; no se obtiene por ssh-keyscan durante el despliegue. No se almacena un secreto permanente de inicio de sesión de Azure.

La imagen incluye la etiqueta org.opencontainers.image.revision. El workflow comprueba que coincida con el commit de GitHub y luego verifica la respuesta HTTP de la API. Si faltan secrets o falla alguna comprobación, el despliegue falla explícitamente.

La credencial federada debe coincidir con el subject inmutable que emite GitHub para este repositorio: `repo:vangiewz@94424043/ProyectoDSU@1459293899:environment:produccion`. Incluye los IDs públicos del propietario y del repositorio; una credencial con el formato anterior sin IDs es rechazada por Azure antes de conectarse a la VM.
