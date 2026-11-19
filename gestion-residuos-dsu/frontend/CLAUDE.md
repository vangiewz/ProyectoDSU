# CLAUDE.md — Frontend del Sistema de Gestión de Residuos DSU-UAGRM

SPA React del sistema web real (irá a producción) de la Dirección de Servicios Universitarios de la UAGRM: captura en campo de vaciados, jornadas, incidencias, tablero, mapa, predicción y alertas. Entrega de Software 2 (PUDS). Leer [AGENTS.md](../../AGENTS.md).

## Carpetas del repositorio unificado ProyectoDSU

```
ProyectoDSU/gestion-residuos-dsu/
  backend/    ← API Django, reglas de negocio, despliegue; su contexto: ../backend/CLAUDE.md
  frontend/   ← este componente
```

- **Todo está centralizado en el backend** (MVC): reglas, permisos, validaciones, configuración y bitácora. El frontend es la Vista: muestra lo que la API devuelve y oculta lo que el rol no puede hacer, pero el backend vuelve a validar siempre. No duplicar reglas de negocio aquí.
- En desarrollo Vite hace proxy de `/api` a `http://127.0.0.1:8000` (levantar `../backend` con `python manage.py runserver`). El backend ya no sirve este build: se despliega aparte (Vercel). `VITE_API_URL` (build) apunta al backend; vacío = mismo origen/proxy de Vite. El backend necesita esa URL del frontend en `CORS_ALLOWED_ORIGINS`.
- **Estado, decisiones y trazabilidad RF de todo el sistema:** `../backend/docs/ESTADO.md`. Leerlo al empezar y actualizarlo al terminar trabajo relevante.
- **Manual de usuario por rol:** [docs/MANUAL_USUARIO.md](docs/MANUAL_USUARIO.md). Actualizarlo si cambia un flujo o el texto de un botón.
- **Requisitos:** entrega canónica de Software 2 y trazabilidad de RF1–RF27, RNF y RI. Los antecedentes originales se conservan localmente.

## Stack (fijado por el documento)

React 19 + Vite + TypeScript · Tailwind CSS v4 (`@theme` en `src/index.css`) · React Router · Leaflet/OpenStreetMap (+ leaflet.heat) · lucide-react · oxlint. Gráficos en SVG propio (`components/Graficos.tsx`), sin librería de charts.

## Estructura

- `src/components/`: `Shell` (riel lateral rojo DSU, navegación filtrada por permisos en `NAVEGACION`), `Crud` (CRUD genérico por configuración), `ui` (Boton, Campo, Tabla, Aviso, Vacio, Paginacion…), `Sello`, `EjeJornada`, `Mapa`, `Graficos`, `FiltrosAnalisis`, `Estimado` (cifra del modelo con margen).
- `src/pages/`: una página por módulo. `Campo.tsx` es la captura móvil del operario (≤4 interacciones, RNF8). Predictivo: `Modelo.tsx` (RF22), `Prediccion.tsx` (RF23), `Recomendaciones.tsx` (RF24), capa proyectada en `MapaCampus.tsx` (RF20). `Tablero.tsx`: indicadores con detalle al hacer clic (RF17), comparación de periodos y pestaña Power BI (RD8, informe insertado desde el enlace en Parámetros).
- `src/lib/`: `api.ts` (fetch + JWT con renovación; `archivo: true` para descargas), `auth.tsx` (`useAuth().puede('app.codename')`), `datos.ts` (`useCarga`, formatos es-BO, `aproximado` para estimaciones), `tipos.ts`.
- Rutas protegidas en `App.tsx` con `<Con permiso="...">`. Los nombres de permiso (`app.codename`) vienen del backend (`GET /api/auth/me/`); uno nuevo se crea allá con una migración de datos.
- API: todo bajo `/api/`, paginación `{count, next, previous, results}` con `page` y `page_size`; errores de DRF ya traducidos a texto por `mensajeDeError`.

## Diseño — usar siempre `impeccable`

- Antes de tocar cualquier UI, invocar la skill `impeccable` (regla global del usuario). Su contexto está versionado aquí: [PRODUCT.md](PRODUCT.md), `.impeccable/surfaces/src-app-tsx.md` (contrato del mundo visual, modo Operate) y `.impeccable/decision/` (dirección elegida). El sistema de diseño está documentado en [DESIGN.md](DESIGN.md) (con su sidecar `.impeccable/design.json`): sus tokens y reglas mandan; actualizarlo si se agrega o cambia un token o componente.
- Mundo **"Planilla de control sellada"**. Tokens en `src/index.css`: papel `#f4f6f8`, hoja `#ffffff`, grafito `#1e2328`, rojo DSU `#c4122f` (riel y tinta de sello), azul bolígrafo `#1f3fa8` **solo para valores capturados por personas** (`.tinta`), lápiz `#55606c` **para toda estimación del modelo, siempre "≈ valor ± margen"** (`.lapiz`, `<Estimado>`; RNF13), sellos de estado (verde ATENDIDO/ACEPTADA/VIGENTE, ámbar OMITIDO/URGENCIA MEDIA, rojo CERRADA/URGENCIA ALTA) con su caída en dos pasos al confirmar (`.sello-recien`).
- Una sola familia: Archivo variable (ancho condensado para rótulos y sellos, `.rotulo`), cifras tabulares. Filetes de 1px, esquinas de 2–4px. Sin tarjetas genéricas, sin eyebrows, sin degradados de texto.
- Gráficos: cargar la skill `dataviz`; una serie por gráfico, un tono (bolígrafo para lo medido, lápiz con bigotes de margen para lo estimado).
- Verificar en navegador a 1440 px y 390 px, y correr `impeccable detect` sobre los archivos tocados.

## Comandos

```bash
npm install
npm run dev                 # http://localhost:5173 (requiere el backend en :8000)
npx tsc -b && npm run lint && npm run build
```

## Cuidado con

- **Usuarios demo** (`supervisor`, `administrativo` —rol Administrador—, etc.) existen en la base de demostración con la contraseña del README del backend; solo para desarrollo.
- **Memoria de la máquina**: los servidores en segundo plano (runserver/vite) pueden ser detenidos por falta de memoria; si pasa, avisar y pedir permiso antes de relanzarlos.
- Los avisos de oxlint `only-export-components` son conocidos y aceptados.
- **Grafo de código**: vive en `../graphify-out/` y cubre backend + frontend; los comandos `graphify` se corren desde `../`, no desde este repo.
- **Commits**: solo cuando el usuario lo pida.

## Convenciones

- Responder y documentar en español; el dominio y los textos de la interfaz en español (Bolivia). Nombres de componentes y variables en español como el código existente (`Jornada`, `useCarga`, `puede`).
- Mínimo código que resuelva lo pedido; reutilizar `ui.tsx`, `Crud`, `Graficos` y `useCarga` antes de crear piezas nuevas.
- Textos de la interfaz: lenguaje llano para personal sin formación técnica; los errores nombran el problema y cómo seguir.
