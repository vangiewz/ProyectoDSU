# Despliegue previsto en AWS EC2

Arquitectura de producción de Taller: EC2 Linux/Docker en São Paulo (`sa-east-1`), Neon conservado, frontend independiente en Vercel. Este directorio prepara la instalación; no acredita que se haya ejecutado.

## Preparación

1. Usar una instancia Linux x86_64 con Docker Engine y Compose. Dimensionar CPU/memoria con las mediciones del modelo y concurrencia; no prometer que un tamaño concreto cumple antes de medirlo.
2. Apuntar el DNS del dominio de la API a la instancia. Permitir TCP 443 y 80 para HTTPS y emisión/redirección del certificado; limitar SSH al equipo administrador. No publicar 8000 ni 5432.
3. Conservar `backend/.env` sin imprimirlo. Configurar `DEBUG=False`, `ALLOWED_HOSTS` con el dominio real, `CORS_ALLOWED_ORIGINS` con el origen exacto de Vercel, `DATABASE_URL` con Neon/TLS y `RESPALDO_DATABASE_URL` con conexión directa. Usar una clave Django propia del despliegue. No copiar credenciales a este README.
4. Definir `DSU_API_DOMAIN` en el entorno del operador o en la configuración privada de despliegue. Desde esta carpeta ejecutar `docker compose --env-file ../.env -f compose.aws.yml up -d --build`. Este comando aplica migraciones: revisar y coordinar los cambios antes de usarlo con la base compartida.
5. Configurar en Vercel la raíz `gestion-residuos-dsu/frontend` y `VITE_API_URL` con el origen HTTPS de la API. La configuración `vercel.json` añade cabeceras y fallback de rutas.

El proxy Caddy administra TLS y reenvía las peticiones al contenedor de aplicación por la red interna. La aplicación se conecta a Neon; no se instala PostgreSQL institucional en EC2. El servicio de respaldo guarda dumps diarios en el disco de EC2. Falta configurar y comprobar una copia externa; la carpeta del servidor no es un respaldo independiente de este.

## ETL y controles

Programar una entrada de cron del usuario administrador cada hora, usando la ruta absoluta de este directorio:

```cron
0 * * * * cd /ruta/ProyectoDSU/gestion-residuos-dsu/backend/deploy && docker compose --env-file ../.env -f compose.aws.yml exec -T app python manage.py etl --programado
```

Comprobar certificado, redirección HTTP→HTTPS, cabeceras, CORS de Vercel, login y permisos, CRUD autorizado, mapas, reportes, publicación/inferencia, actualización de Power BI, ETL programado y restauración en un destino aislado. Repetir rendimiento (incluido RTR11) y carga desde la región del servidor. Guardar evidencias antes de declarar operativo el despliegue.

La CSP del cliente permite conexiones HTTPS para admitir el origen real de API antes de disponer de su dominio. Restringir `connect-src` al dominio confirmado al cerrar la verificación productiva. No añadir COEP restrictivo sin comprobar la inserción de Power BI y los recursos cartográficos.

No eliminar los datos demo ni modificar credenciales compartidas sin coordinarlo. La retirada de datos sintéticos corresponde a una puesta en producción institucional acordada, no a preparar una defensa con la demo existente.
