# CLAUDE.md — Backend del Sistema de Gestión de Residuos DSU-UAGRM

API Django del sistema web real (irá a producción) de la Dirección de Servicios Universitarios de la UAGRM: registro en campo de vaciados, jornadas de recolección, incidencias, analítica, predicción con Random Forest y alertas logísticas. Entrega de Software 2 (PUDS). Leer [AGENTS.md](../../AGENTS.md).

## Repositorio unificado

Backend y frontend son carpetas hermanas del repositorio raíz ProyectoDSU (el proxy de Vite apunta al backend en `:8000`):

```
ProyectoDSU/gestion-residuos-dsu/
  backend/    ← este componente: API, reglas de negocio, ETL, modelo, despliegue (Dockerfile, docker-compose.yml)
  frontend/   ← SPA React; despliegue aparte
```

El backend no sabe nada del frontend: el `Dockerfile` y el compose solo empaquetan esta carpeta. Si trabajas en el frontend, su contexto está en `../frontend/CLAUDE.md`.

- **Requisitos (fuente de verdad):** entrega canónica de Software 2 y trazabilidad de RF1–RF27, RNF, RI, RBD y RD. Los antecedentes originales se conservan localmente; no cambiar los requisitos por retirar esos archivos de GitHub. No hay historias de usuario; se trabaja por RF.
- **Estado, decisiones, trazabilidad RF y próximos pasos (de todo el sistema):** [docs/ESTADO.md](docs/ESTADO.md). Leerlo al empezar una sesión y actualizarlo al terminar trabajo relevante, también si el cambio fue en el frontend.
- **Puesta en marcha y despliegue:** [README.md](README.md).

## Stack (fijado por el documento, no cambiar sin pedido explícito)

Django 5.2 LTS + Django REST Framework + JWT (simplejwt) · Python 3.12 · PostgreSQL en **Neon** · Pandas/NumPy · scikit-learn (Random Forest Regressor; **sin LLM** dentro del sistema, decisión del usuario) · openpyxl y fpdf2 para reportes · Power BI vía vistas SQL `bi_*`. Frontend: React 19 + Vite + TypeScript + Tailwind v4 + Leaflet (carpeta hermana).

## Arquitectura: MVC, todo centralizado en el backend

- `.env` concentra toda la configuración (SECRET_KEY, DATABASE_URL de Neon, JWT, CAMPUS_BBOX, MODELOS_DIR). La configuración es privada y local; la antigua excepción de versionarla fue revocada. No copiar sus valores a otros archivos, a `.env.example`, ni imprimirlos (p. ej. `docker compose config` los muestra).
- Django solo sirve la API (`/api/`) y los estáticos del admin/DRF; ya no sirve el SPA. En desarrollo Vite hace proxy de `/api` a `:8000`. El frontend va aparte (Vercel): el backend lee `CORS_ALLOWED_ORIGINS` del `.env` (django-cors-headers) y el frontend `VITE_API_URL`.
- **Cada app de `apps/` usa paquetes por entidad** (preferencia explícita del usuario): `models/`, `serializers/`, `views/`, y cuando aplica `services/`, `filters/`, `permissions/`, `management/commands/`, `tests/`. Un archivo por entidad y un `__init__.py` que reexporta con `__all__`. Nunca crear `models.py` o `views.py` planos.
  - Modelo = `models/` · Vista = `serializers/` + SPA React · Controlador = `views/` (ViewSets) + `accounts/permissions/`.
  - `services/` solo para lógica de negocio con varios pasos (jornadas, visitas, ETL, indicadores, reportes, bitácora, entrenamiento, predicción, recomendaciones).

| App | RF | Contenido |
|---|---|---|
| `accounts` | RF1–RF3 | `User` (AbstractUser), roles = grupos de Django, login/refresh/logout JWT, `RolePermission`, alcance por sector |
| `audit` | RF26 | `AuditLog` inalterable (trigger PostgreSQL), `services.registrar()`, `AuditedViewSet` y `DeactivatableViewSet` |
| `catalogs` | RF6, RF25 | tipos de residuo, unidades (factor a kg/L), periodos académicos, `ParametrosSistema` (registro único) |
| `campus` | RF4, RF5, RF7 | sectores, puntos georreferenciados, contenedores |
| `operations` | RF8–RF14 | vehículos, jornadas y su ruta (`JornadaPunto`), registro de vaciados, incidencias, comando `seed` |
| `analytics` | RF15–RF21, RF27 | ETL (Pandas) → `HechoResiduo`, `EjecucionETL`, `RegistroDescartado`, indicadores, comparación, mapa, reportes, vistas `bi_*` |
| `prediction` | RF22–RF24, RF20 proyectado | `ModeloEntrenado` (versiones, métricas, artefacto), `LotePrediccion`/`Prediccion` (con margen), `Recomendacion`; servicios `datos`, `entrenamiento`, `prediccion`, `recomendaciones`; comando `entrenar` |

## Reglas que el código ya aplica (respetarlas al extender)

- **Sin borrado físico** de históricos ni maestros: bajas lógicas con `is_active` y acciones `desactivar/activar`; FKs con `on_delete=PROTECT`; los ViewSets heredan de `AuditedViewSet` (sin DELETE).
- **Toda escritura queda en la bitácora**: usar `AuditedViewSet` o llamar a `apps.audit.services.registrar(...)` en acciones propias. La tabla `audit_auditlog` rechaza UPDATE/DELETE por trigger.
- **Permisos**: `RolePermission` es el permiso por defecto; GET exige `view_<modelo>`. Las acciones propias declaran `action_perms = {"accion": ["app.codename"]}`. Permisos nuevos se asignan a los roles con una **migración de datos** (ver `operations/0002_roles`, `analytics/0002_permisos_roles`, `prediction/0002_permisos_roles`). Si se agrega un permiso que el frontend consulta, avisar: el SPA filtra navegación y rutas por esos nombres.
- **Alcance territorial**: usar `filtrar_por_sector(qs, user, "<ruta_al_sector>", filtro_operativo)` en `get_queryset`; el supervisor ve sus sectores y el operativo solo lo de sus jornadas. `exigir_sector()` valida escrituras.
- **Roles** (nombres de grupo, `accounts.models.Rol`): Administrador, Supervisor, Operativo, Directivo (el rol Administrativo se integró al Administrador, migración `operations/0003`).
- **Precisión**: cantidades en `DecimalField`, coordenadas `max_digits=9, decimal_places=6`. Nunca float para cantidades persistidas (las métricas del modelo sí son `FloatField`: son estadísticos, no cantidades).
- **Validaciones de negocio** en `services/` o serializers, con `ValidationError`/`PermissionDenied` de DRF y mensajes en español claros (RNF9).
- **Umbrales configurables** viven en `ParametrosSistema.actual()`, no en settings ni constantes (RNF21). Un parámetro nuevo también se agrega a la lista `CAMPOS` de `frontend/src/pages/Sistema.tsx`.
- **Plano analítico separado** (RNF20): indicadores, mapa, reportes y el modelo leen `HechoResiduo`, que solo llena el ETL. El ETL es incremental y nunca modifica datos transaccionales.
- **Predicciones (RNF13)**: siempre con margen de error y versión del modelo; nunca como valor exacto. Las recomendaciones son de apoyo: el supervisor las acepta o descarta con motivo.

## Contrato con el frontend

- Todo bajo `/api/`, JSON, paginación `{count, next, previous, results}` (`page`, `page_size`), errores DRF (`detail` o `{campo: [mensajes]}`) en español.
- `GET /api/auth/me/` devuelve `roles` y `permisos` (`app.codename`); el SPA muestra solo lo permitido y el backend vuelve a validar siempre.
- Al cambiar la forma de una respuesta, actualizar los tipos del frontend (`src/lib/tipos.ts` o el tipo local de la página).

## Comandos

```bash
# Desde esta carpeta, con .venv activo
python manage.py runserver
python manage.py migrate
python manage.py seed --admin-password "<clave>" [--demo] [--historico]   # --historico: año sintético para entrenar (solo demo)
python manage.py etl [--programado]
python manage.py entrenar [--n-estimators N --max-depth D --min-samples-leaf L]
python manage.py medir_rendimiento   # RTR/RCM con 500 puntos y ~100k observaciones; deshace todo al final
python scripts/carga.py --usuario <u> --clave <c>   # 12 usuarios simultáneos contra un servidor en marcha (RNF4)
python powerbi/generar.py           # NO ejecutar sobre el proyecto actual: sobrescribe cambios manuales; ver powerbi/README.md
pytest                      # configuración histórica usa Neon; para QA aislado usar el runner de fase_final indicado abajo
ruff check . && ruff format .
docker compose up -d --build   # producción (app + respaldo diario), solo backend

# Grafo de código (no versionado): vive en la carpeta padre (../graphify-out/) y cubre backend + frontend.
# Correr desde ../ (no desde este repo): graphify update . / graphify query "<pregunta>" --budget 1500
# El hook SessionStart de Claude es local y no se distribuye en otros clones.
```

Para la auditoría sin afectar la demo compartida: desde la raíz del proyecto, `python herramientas/pruebas/pruebas_aisladas.py` crea su propio PostgreSQL desechable; `pruebas_linux.py` repite la suite sobre la imagen Linux preparada. No ejecutar pytest, migraciones, ETL ni entrenamiento contra Neon por preparar otro clon. Configuración productiva propuesta: `deploy/README.md`; su existencia no acredita despliegue remoto.

## Cuidado con

- **Tests contra Neon**: no usar `--create-db`; el pooler deja sesiones abiertas y no se puede borrar `test_neondb`. Con `--reuse-db` (por defecto) las migraciones nuevas se aplican solas. La suite tarda ~4 min por la latencia a Neon.
- **Pooler de Neon (PgBouncer)**: `DISABLE_SERVER_SIDE_CURSORS=True` ya está en settings; no quitarlo.
- **La base de Neon tiene datos de demostración**: usuarios demo con contraseña publicada en el README, sectores con coordenadas aproximadas y un año de histórico **sintético** (`seed --historico`) con el que se entrenó el modelo. Sus métricas no son resultados reales. Limpiar o usar otra rama de Neon antes de producción.
- **Memoria de la máquina**: los servidores en segundo plano (runserver/vite) pueden ser detenidos por falta de memoria; si pasa, avisar y pedir permiso antes de relanzarlos.
- **Vistas `bi_*`**: si se cambia una vista, actualizar `VISTAS` en `powerbi/generar.py` y regenerar; las columnas deben coincidir exactamente o Power BI falla al actualizar.
- **Respaldo (RNF12)**: servicio `respaldo` de `docker-compose.yml` con `scripts/respaldo.sh`; la imagen de `pg_dump` debe ser de la versión mayor de Neon (hoy PostgreSQL 18) o más nueva.
- **Commits**: solo cuando el usuario lo pida.

## Convenciones

- Responder y documentar en español; nombres de código, rutas y comandos en inglés o español según el código existente (el dominio está en español: `Jornada`, `PuntoRecoleccion`, `registrar_visita`).
- Mínimo código que resuelva lo pedido; lo que el documento exige (patrón, capas, tests, Pandas) es requisito, no sobreingeniería.
- Lógica no trivial nueva deja al menos un test en `apps/<app>/tests/`. Fixtures compartidas en `conftest.py` (`usuarios`, `campus`, `cliente`, `hoy`).
