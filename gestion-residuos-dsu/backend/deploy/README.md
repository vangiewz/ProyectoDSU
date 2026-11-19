# Operación del piloto en Azure VM

Arquitectura de producción de Taller: Azure VM Linux/Docker en Mexico Central, Neon conservado, frontend independiente en Vercel. La API y la aplicación están desplegadas como piloto técnico; esto no equivale a aceptación institucional. El cierre local no publica cambios ni modifica Neon.

## Preparación

1. Usar una instancia Linux x86_64 con Docker Engine y Compose. Dimensionar CPU/memoria con las mediciones del modelo y concurrencia; no prometer que un tamaño concreto cumple antes de medirlo.
2. Apuntar el DNS del dominio de la API a la instancia. Permitir TCP 443 y 80 para HTTPS y emisión/redirección del certificado; limitar SSH al equipo administrador. No publicar 8000 ni 5432.
3. Conservar `backend/.env` sin imprimirlo. Configurar `DEBUG=False`, `ALLOWED_HOSTS` con el dominio real, `CORS_ALLOWED_ORIGINS` con el origen exacto de Vercel, `DATABASE_URL` con Neon/TLS y `RESPALDO_DATABASE_URL` con conexión directa. Usar una clave Django propia del despliegue. No copiar credenciales a este README.
4. Definir `DSU_API_DOMAIN` en el entorno del operador o en la configuración privada de despliegue. Desde esta carpeta ejecutar `docker compose --env-file ../.env -f compose.azure.yml up -d --build`. Este comando aplica migraciones: revisar y coordinar los cambios antes de usarlo con la base compartida.
5. Configurar en Vercel la raíz `gestion-residuos-dsu/frontend` y `VITE_API_URL` con el origen HTTPS de la API. La configuración `vercel.json` añade cabeceras y fallback de rutas.

El proxy Caddy administra TLS y reenvía las peticiones al contenedor de aplicación por la red interna. La aplicación se conecta a Neon; no se instala PostgreSQL institucional en Azure VM. El servicio de respaldo guarda dumps diarios en el disco de la VM. Falta configurar y comprobar una copia externa; la carpeta del servidor no es un respaldo independiente de este.

## ETL y controles

Programar una entrada de cron del usuario administrador cada hora, usando la ruta absoluta de este directorio:

```cron
0 * * * * cd /ruta/ProyectoDSU/gestion-residuos-dsu/backend/deploy && docker compose --env-file ../.env -f compose.azure.yml exec -T app python manage.py etl --programado
```

Comprobar certificado, redirección HTTP→HTTPS, cabeceras, CORS de Vercel, login y permisos, CRUD autorizado, mapas, reportes, publicación/inferencia, actualización de Power BI, ETL programado y restauración en un destino aislado. Repetir rendimiento (incluido RTR11) y carga desde la región del servidor. Guardar evidencias antes de declarar operativo el despliegue.

La CSP del cliente permite conexiones HTTPS para admitir el origen real de API antes de disponer de su dominio. Restringir `connect-src` al dominio confirmado al cerrar la verificación productiva. No añadir COEP restrictivo sin comprobar la inserción de Power BI y los recursos cartográficos.

No eliminar los datos demo ni modificar credenciales compartidas sin coordinarlo. La retirada de datos sintéticos corresponde a una puesta en producción institucional acordada, no a preparar una defensa con la demo existente.


## Verificación y reversión del cierre

El titular realizará la publicación. Antes de desplegar debe conservar el paquete y la imagen anteriores, guardar un respaldo comprobado y revisar las migraciones: el Dockerfile aplica migrate al arrancar. No copiar a producción el .env local con DEBUG=True. No imprimir variables sensibles.

Rollback: recuperar el paquete anterior sin sobrescribir el .env privado y arrancar esa versión con Compose. Las migraciones de datos no se revierten automáticamente: requieren análisis y autorización. No borrar volúmenes ni aplicar prune como rutina.

Pruebas Windows: backend/.venv/Scripts/python.exe auditoria_cierre/ejecutar_aislado.py desde la raíz. Crea su propio PostgreSQL 18 en loopback y fuerza DATABASE_URL local; no usa el servicio instalado ni Neon. DSU_EXTENDED=1 añade demo, restauración sintética y navegador efímeros. El Node recomendado es >=22.22; el equipo tiene 22.16 aunque compiló correctamente. Docker y CI mantienen Python 3.12; el cierre local usa 3.13 y lo declara.

ETL y entrenamiento bajo demanda conservan hilos del proceso web. El bloqueo de arranque evita trabajos simultáneos, pero no los vuelve durables: un reinicio puede interrumpirlos. Ejecutar comandos supervisados, no redesplegar durante trabajos activos y revisar estados abandonados hasta evaluar una cola persistente.

Las 50 muestras históricas de disponibilidad son 19 de API, 15 de app y 16 de sitio; no acreditan SLA mensual. La restauración local compara todas las tablas y claves foráneas; no acredita recuperación productiva ni un RTO institucional. Mantener copia de respaldo fuera de la VM requiere configuración y comprobación aparte.
