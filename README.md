# Proyecto DSU — Taller de Grado y Software 2

Sistema web de gestión de residuos sólidos de la Dirección de Servicios Universitarios de la UAGRM, con analítica y predicción mediante Random Forest Regressor. El equipo desarrolla **un mismo sistema para las dos materias**, con entregables académicos propios de cada una. Para Software 2 se eligió **PUDS**.

Este es el repositorio compartido: [vangiewz/ProyectoDSU](https://github.com/vangiewz/ProyectoDSU). Backend y frontend están incluidos como carpetas normales; no es necesario clonar los repositorios anteriores.

## Organización

| Ruta | Contenido |
|---|---|
| [AGENTS.md](AGENTS.md) | Contexto y decisiones para cualquier agente |
| [CLAUDE.md](CLAUDE.md) | Guía del material de Taller y cuidados de generación |
| [gestion-residuos-dsu/backend](gestion-residuos-dsu/backend/README.md) | API Django, ETL, Random Forest, Power BI y despliegue |
| [gestion-residuos-dsu/frontend](gestion-residuos-dsu/frontend/README.md) | Aplicación React y Vite |
| [docs](docs/) | Documento vigente de Taller, auditorías y versiones |
| [DocumentoSoftware2](DocumentoSoftware2/CONTEXTO.md) | Contexto de Software 2 y ejemplos de referencia; entregables pendientes |
| [generador](generador/) y [modelo_uml](modelo_uml/) | Fuentes del documento, figuras y modelo de Enterprise Architect |
| [clases](clases/), [cap8-10](cap8-10/) y PDF de la raíz | Material docente y referencias |

## Inicio rápido en Windows

Requisitos: Git, Python 3.12, Node.js compatible con el Vite instalado (22.12 o superior dentro de la rama 22, o 24 LTS) y acceso a Internet para Neon y la instalación de dependencias. Word y Enterprise Architect solo se necesitan para el flujo de generación de documentos y diagramas, no para ejecutar el sistema.

```powershell
git clone https://github.com/vangiewz/ProyectoDSU.git
cd ProyectoDSU
cd gestion-residuos-dsu/backend
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe manage.py runserver
```

En otra terminal, desde la raíz del clon:

```powershell
cd gestion-residuos-dsu/frontend
npm ci
npm run dev
```

Abrir `http://localhost:5173`. Vite dirige `/api` al backend en `http://127.0.0.1:8000`. En Linux/macOS, usar `.venv/bin/python` en lugar de `.venv\Scripts\python.exe`.

## Base compartida y datos cargados

**Se mantiene PostgreSQL en Neon.** El `.env` del backend está incluido por decisión del equipo mientras el repositorio sea privado. No reemplazarlo por `.env.example` al clonar. Ambos integrantes acceden a la misma base demo: no necesitan instalar PostgreSQL, restaurar un dump, generar histórico ni entrenar de nuevo para comenzar.

El estado documentado incluye usuarios de demostración, sectores y puntos, histórico sintético, datos analíticos y modelos entrenados. Usuarios demo: `supervisor`, `operario1`, `operario2`, `administrativo` (rol Administrador) y `directivo`; contraseña demo: `Residuos.2026`. El usuario `admin` tiene una contraseña distinta, no documentada aquí.

Los registros de campo dependen de jornadas asignadas a la fecha actual y las predicciones de historia reciente: los datos antiguos pueden dejar algunas pantallas sin resultados. Coordinar con el equipo las jornadas de prueba y cualquier actualización de la demo. Las métricas sobre datos sintéticos no son resultados reales de la DSU.

**Las escrituras son compartidas.** No ejecutar `seed`, limpiezas, restauraciones o cargas masivas como parte de la instalación. Si se agregan migraciones, revisar `manage.py showmigrations --plan` y coordinar quién ejecuta `manage.py migrate`. Las pruebas deben usar la base de test, nunca restaurar ni vaciar la base compartida.

## Trabajo en equipo y despliegue

Trabajar con ramas y pull requests en este repositorio, coordinando cambios en el Word y el modelo `.eapx`, que no se fusionan como texto. El documento fuente y las precauciones de generación están en [CLAUDE.md](CLAUDE.md); el estado del sistema está en [ESTADO.md](gestion-residuos-dsu/backend/docs/ESTADO.md).

Backend y frontend siguen desplegándose por separado: configurar la raíz del backend como `gestion-residuos-dsu/backend` (Docker) y la del frontend como `gestion-residuos-dsu/frontend` (Vercel). Se mantienen Neon, CORS y `VITE_API_URL`; consultar las guías de cada componente. El `.env` de demostración no sustituye la configuración de producción.

## Antes de hacer público el repositorio

El `.env` versionado contiene credenciales. **Rotarlas/revocarlas, retirar el archivo del seguimiento, volver a excluirlo y limpiar el historial Git antes de cambiar la visibilidad.** Revisar ramas, etiquetas y otros archivos; coordinar nuevos clones tras la limpieza. Borrar el archivo o esta nota no elimina las credenciales de los commits anteriores. No copiar valores del `.env` en documentación, incidencias ni registros.
