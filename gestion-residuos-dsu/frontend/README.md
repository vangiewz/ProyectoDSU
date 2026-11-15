# Gestión de Residuos DSU-UAGRM — Frontend

Interfaz web del sistema de gestión de residuos sólidos de la Dirección de Servicios Universitarios (DSU) de la Universidad Autónoma Gabriel René Moreno: captura en campo desde el celular, jornadas de recolección, incidencias, tablero de indicadores, mapa de calor, predicción con Random Forest y alertas logísticas. Taller de Grado I — Grupo 8 y Software 2 — PUDS.

La API (Django) está en la carpeta hermana del mismo repositorio ProyectoDSU. Clonar la raíz una sola vez:

```
ProyectoDSU/gestion-residuos-dsu/
  backend/    ← API, reglas de negocio y despliegue
  frontend/   ← SPA React
```

## Stack

React 19 · Vite · TypeScript · Tailwind CSS v4 · React Router · Leaflet/OpenStreetMap (+ leaflet.heat) · lucide-react · oxlint.

## Desarrollo

```bash
npm ci
npm run dev          # http://localhost:5173
```

Vite redirige `/api` a `http://127.0.0.1:8000`, así que el backend debe estar corriendo (`python manage.py runserver` en `../backend`). Con los datos de demostración del backend se puede entrar como `supervisor`, `operario1`, `administrativo` (rol Administrador) o `directivo`.

## Calidad y build

```bash
npx tsc -b && npm run lint
npm run build        # genera dist/ para el hosting del frontend
```

## Producción

Se despliega por separado del backend, seleccionando `gestion-residuos-dsu/frontend` como raíz en Vercel; `vercel.json` ya tiene el rewrite del SPA. Variable de entorno del build: `VITE_API_URL` = URL del backend, sin barra final. En el backend, `CORS_ALLOWED_ORIGINS` debe incluir la URL del frontend.

## Estructura

```
src/
  components/   Shell (riel DSU), Crud genérico, ui, Sello, EjeJornada, Mapa, Graficos, FiltrosAnalisis, Estimado
  pages/        una página por módulo; Campo.tsx es la captura móvil del operario
  lib/          cliente API con JWT, sesión y permisos, formatos es-BO
```

## Manual de usuario

[docs/MANUAL_USUARIO.md](docs/MANUAL_USUARIO.md): uso del sistema por rol.

## Diseño

Mundo visual "Planilla de control sellada": papel de formulario, rojo DSU en el riel y en los sellos de estado, azul bolígrafo para lo que registran las personas y trazo a lápiz con margen de error para lo que estima el modelo. Contexto de producto y diseño en [PRODUCT.md](PRODUCT.md) y `.impeccable/`.
