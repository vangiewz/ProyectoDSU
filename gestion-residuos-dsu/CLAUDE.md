# CLAUDE.md — Código del proyecto DSU

El Sistema de Gestión de Residuos DSU-UAGRM forma parte del repositorio único **ProyectoDSU**, cuya raíz está un nivel arriba. Backend y frontend son carpetas hermanas, no repositorios independientes ni submódulos. Leer [AGENTS.md](../AGENTS.md) para las decisiones compartidas de Taller y Software 2. Se mantiene Neon; el despliegue Docker sigue siendo solo del backend.

| Carpeta | Componente | Contexto |
|---|---|---|
| `backend/` | API Django, ETL, Random Forest, despliegue (`Dockerfile`, `docker-compose.yml`) | [backend/CLAUDE.md](backend/CLAUDE.md) |
| `frontend/` | SPA React, contexto de diseño de impeccable (`PRODUCT.md`, `.impeccable/`) | [frontend/CLAUDE.md](frontend/CLAUDE.md) |

- **Estado, decisiones y trazabilidad RF1–RF27 de todo el sistema:** [backend/docs/ESTADO.md](backend/docs/ESTADO.md). Leerlo al empezar una sesión y actualizarlo al terminar trabajo relevante.
- Al trabajar en una parte, leer el `CLAUDE.md` de ese componente; si el cambio cruza la API (forma de respuestas, permisos, parámetros), revisar los dos.
- `graphify-out/` (aquí, en esta carpeta) es el grafo de código de **backend y frontend juntos**; no se versiona. Comandos desde esta carpeta, nunca desde `backend/` o `frontend/`: `graphify update .`, `graphify query "<pregunta>" --budget 1500`, `graphify affected "X"`. El hook SessionStart de Claude es una configuración local no versionada; no asumir que exista en otros clones.
- Responder en español. Commitear solo cuando el usuario lo pida, en el repositorio raíz.
