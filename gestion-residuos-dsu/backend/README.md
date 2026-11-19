# Gestión de Residuos DSU-UAGRM — Backend

API del sistema web de gestión de residuos sólidos de la Dirección de Servicios Universitarios (DSU) de la Universidad Autónoma Gabriel René Moreno: registro en campo de vaciados, jornadas de recolección, incidencias, analítica, predicción con Random Forest Regressor y alertas logísticas. Software 2 — PUDS.

El frontend (React) está en la carpeta hermana del mismo repositorio ProyectoDSU. Clonar la raíz una sola vez; Vite hace proxy de `/api` a `:8000`:

```
ProyectoDSU/gestion-residuos-dsu/
  backend/    ← API y despliegue
  frontend/   ← SPA React
```

Estado, decisiones y trazabilidad de requisitos (RF1–RF27): [docs/ESTADO.md](docs/ESTADO.md).

## Stack

| Capa | Tecnología |
|---|---|
| Servicios | Django REST Framework, JWT (simplejwt) con rotación y lista negra |
| Lógica de negocio | Django 5.2 LTS (Python 3.12) |
| Analítica y modelo | Pandas, NumPy, scikit-learn (Random Forest Regressor) |
| Datos | PostgreSQL (Neon) |
| Reportes | openpyxl (Excel), fpdf2 (PDF); vistas SQL `bi_*` para Power BI |
| Presentación | React 19 + Vite + TypeScript (carpeta `frontend`) |

## Arquitectura (MVC)

Todo está centralizado en el backend: configuración, `.env`, base de datos, permisos y bitácora. En producción esta carpeta despliega solo la API; el frontend se despliega por separado.

- **Modelo** — `apps/<módulo>/models/`: una entidad por archivo.
- **Vista** — `apps/<módulo>/serializers/` (representación JSON) y el SPA de la carpeta `frontend`.
- **Controlador** — `apps/<módulo>/views/` (ViewSets) y `apps/accounts/permissions/` (control de acceso por rol).
- `services/` — reglas de negocio con más de un paso; `filters/` — filtros de consulta reutilizables.

```
config/            settings (django-environ), urls, paginación
apps/
  accounts/        RF1–RF3   usuarios, roles (grupos), login/logout JWT
  audit/           RF26      bitácora inalterable (trigger PostgreSQL) y base de controladores auditados
  catalogs/        RF6, RF25 tipos de residuo, unidades, periodos académicos, parámetros del sistema
  campus/          RF4,5,7   sectores, puntos georreferenciados, contenedores
  operations/      RF8–14    vehículos, jornadas, ruta, registro de vaciados, incidencias
  analytics/       RF15–21, RF27  ETL (Pandas), indicadores, comparación, mapa, reportes
  prediction/      RF22–24   Random Forest: versiones del modelo, predicciones, alertas y recomendaciones
```

## Puesta en marcha (desarrollo)

```bash
python -m venv .venv
.venv/Scripts/activate            # Windows  (Linux/macOS: source .venv/bin/activate)
pip install -r requirements-dev.txt
# Crear .env desde .env.example y obtener los valores del titular; no se versiona.
# No ejecutar seed ni migrate como parte del primer arranque.
python manage.py runserver        # http://localhost:8000/api/
```

El frontend se levanta desde `../frontend` con `npm run dev` (proxy de `/api` a `:8000`).

**Solo para preparar una base demo nueva y separada, no al clonar este repositorio:** `seed` carga unidades y tipos de residuo base. `--demo` agrega usuarios de ejemplo (`supervisor`, `operario1`, `operario2`, `directivo`, contraseña `Residuos.2026`) y sectores/puntos con **coordenadas aproximadas no oficiales**. `--historico` agrega un año de jornadas y vaciados **sintéticos** (patrón semanal, vacaciones, crecimiento) para entrenar el modelo en demostración; después correr `python manage.py etl` y `python manage.py entrenar`. **No usar `--demo` ni `--historico` en producción.**

## Pruebas y calidad

```bash
pytest                            # BD de test en el mismo servidor (reutilizada con --reuse-db)
ruff check . && ruff format --check .
```

## Procesamiento analítico (ETL)

El ETL depura los registros de campo, estandariza unidades, deriva día/semana/mes/periodo académico y marca atípicos en el plano analítico (`HechoResiduo`), sin tocar los datos transaccionales. Se ejecuta:

- **A pedido:** botón *Ejecutar ahora* en *Administración → Procesamiento ETL* (corre en segundo plano).
- **Programado:** cron del servidor cada hora; el comando respeta la periodicidad configurada en *Parámetros*:

```cron
0 * * * *  cd /ruta/dsu/backend && docker compose exec -T app python manage.py etl --programado
```

## Modelo predictivo (Random Forest)

- **Entrenar (RF22):** *Administración → Modelo predictivo* (en segundo plano) o `python manage.py entrenar [--n-estimators 100 --max-depth 12 --min-samples-leaf 5]`. Partición cronológica 80/20; se calculan MAE, MSE, RMSE y R² y la importancia de cada variable. La versión se publica solo si R² ≥ el umbral de *Parámetros*; cualquier versión aprobada puede volver a publicarse (reversión).
- **Predecir (RF23):** *Análisis → Predicción*, con horizonte (hasta el máximo configurado) y alcance por sector o punto. Cada estimación se guarda con la versión del modelo y su margen de error (el RMSE de prueba; al sumar, raíz de la suma de cuadrados).
- **Alertas y recomendaciones (RF24):** se emiten al generar cada predicción, con su evidencia. Al aceptar una alerta de desborde, el punto pasa al primer lugar de la siguiente jornada planificada de su sector.
- El modelo serializado vive en la BD (`ModeloEntrenado.artefacto`) y se copia a `MODELOS_DIR` (por defecto `modelos/`, no versionado) para no descargarlo en cada predicción.

## Power BI

Las migraciones `analytics/0003_vistas_bi` y `prediction/0003_vistas_bi` crean vistas depuradas y sin datos personales: `bi_hechos_residuos`, `bi_jornadas`, `bi_incidencias`, `bi_puntos`, `bi_predicciones` (vigentes, con margen) y `bi_recomendaciones`. La carpeta [`powerbi/`](powerbi/README.md) trae el proyecto de Power BI Desktop (`DSU-Residuos.pbip`) ya conectado a ellas, con relaciones y medidas, y los pasos para crear el usuario de solo lectura, publicarlo y mostrarlo en *Tablero → Power BI*.

## Respaldos (RNF12)

- **Automático diario:** el servicio `respaldo` de `docker-compose.yml` ejecuta `pg_dump` una vez al día y guarda `respaldos/dsu-AAAAMMDD-HHMM.dump` en el servidor, conservando los últimos 14 días (`RESPALDO_DIAS`). Para el respaldo conviene la conexión directa de Neon: definir `RESPALDO_DATABASE_URL` (el mismo URL sin `-pooler`) en `.env`. Copiar la carpeta `respaldos/` a otro equipo o a la nube periódicamente.
- **Restaurar:** `pg_restore --clean --if-exists --no-owner -d "<url-destino>" respaldos/dsu-AAAAMMDD-HHMM.dump`.
- Además, Neon conserva el historial de la base y permite restaurarla a cualquier momento dentro de su ventana de retención.

## Rendimiento y carga

- `python manage.py medir_rendimiento`: crea 500 puntos y ~100 000 observaciones dentro de una transacción, mide RTR1–RTR12 y RCM3/5/7 por la API y **deshace todo** al final. Resultados en [docs/RENDIMIENTO.md](docs/RENDIMIENTO.md).
- `python scripts/carga.py --url <servidor> --usuario <u> --clave <c>`: 12 usuarios simultáneos durante 60 s (RNF4/RCM1). Con `--jornada <id> --operario <u> --clave-operario <c>` también registra vaciados y verifica que no se pierda ninguno (RCM2); usar con una **rama de prueba de Neon**, porque esos vaciados quedan guardados.

## Producción

```bash
git clone https://github.com/vangiewz/ProyectoDSU.git
cd ProyectoDSU/gestion-residuos-dsu/backend
cp .env.example .env              # DEBUG=False, ALLOWED_HOSTS, SECRET_KEY nueva, DATABASE_URL, RESPALDO_DATABASE_URL
docker compose up -d --build      # migra y arranca gunicorn en :8000 (+ respaldo diario)
```

El contexto de build es esta carpeta del repositorio unificado. `RESPALDO_DATABASE_URL` debe ser la conexión **directa** de Neon (sin `-pooler`): `pg_dump` fija `search_path` en su sesión y, por el pooler, ese ajuste se filtra a la app y rompe las consultas. Poner un proxy con TLS (nginx/Caddy) delante. Con `DEBUG=False` se activan HSTS, redirección HTTPS y cabeceras seguras.

## Roles

| Rol | Puede |
|---|---|
| Administrador | Usuarios, roles, catálogos, campus, consultas, bitácora, ETL, reportes, parámetros, entrenar y publicar el modelo; sin acciones de campo (absorbió al antiguo rol Administrativo) |
| Supervisor | Sus sectores: puntos, contenedores, jornadas (planificar, asignar, abrir, cerrar), incidencias, predicciones, resolver recomendaciones |
| Operativo | Sus jornadas del día: abrir, registrar vaciados, omitir con motivo, reportar incidencias |
| Directivo | Consulta general, predicciones y recomendaciones |

## Estado

Implementado: RF1–RF27. Pendientes no funcionales y de puesta en producción en [docs/ESTADO.md](docs/ESTADO.md).
