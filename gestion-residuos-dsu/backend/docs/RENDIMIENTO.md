# Rendimiento y capacidad (RTR1–RTR12, RCM3–RCM8)

Medición del 05/10/2026 con `python manage.py medir_rendimiento`: 512 puntos activos y ~100 000 vaciados sintéticos (112 171 observaciones de entrenamiento), creados dentro de una transacción que se deshace al final. Cada operación se mide por la API en el mismo proceso (mediana de 3).

**Entorno de la medición:** PC de desarrollo en Bolivia contra Neon en São Paulo (AWS `sa-east-1`), con **~160 ms de latencia por consulta** y poco ancho de banda. En producción el servidor debe ubicarse en la misma región que Neon; con eso la latencia por consulta baja a pocos milisegundos y estos tiempos mejoran.

| Requisito | Operación | Límite | Medido | Cumple |
|---|---|---|---|---|
| RCM5 | ETL sobre el histórico nuevo (100000 registros) | — | 117.24 s | — |
| RTR1 | Autenticación | ≤ 2 s | 1.41 s | ✅ |
| RTR2 | Datos de la interfaz principal (sesión + jornadas) | ≤ 3 s | 1.77 s | ✅ |
| RTR3 | Búsqueda de un punto | ≤ 2 s | 0.26 s | ✅ |
| RTR3 | Búsqueda de un sector | ≤ 2 s | 0.25 s | ✅ |
| RTR4 | Registro de un vaciado | ≤ 3 s | 2.29 s | ✅ |
| RTR5 | Registro de una incidencia | ≤ 3 s | 0.89 s | ✅ |
| RTR6 | Histórico con filtros (12 meses, un sector) | ≤ 4 s | 0.58 s | ✅ |
| RTR7 | Mapa con los 500+ puntos activos (30 días) | ≤ 4 s | 1.47 s | ✅ |
| RTR8 | Capa de calor de 12 meses | ≤ 6 s | 1.93 s | ✅ |
| RTR9 | Indicadores del periodo (30 días) | ≤ 5 s | 3.30 s | ✅ |
| RTR9 | Indicadores del periodo (12 meses) | ≤ 5 s | 3.39 s | ✅ |
| RTR10 | Reporte exportable PDF (12 meses) | ≤ 8 s | 0.56 s | ✅ |
| RTR10 | Reporte exportable Excel (12 meses) | ≤ 8 s | 2.60 s | ✅ |
| RTR12 / RCM7 | Entrenamiento completo (112171 observaciones, R² 0.906, aprobado) | ≤ 600 s | 78.92 s | ✅ |
| RTR11 / RCM8 | Predicción a 30 días de todos los puntos (512 puntos) | ≤ 15 s | 40.00 s | ❌ |

## Correcciones hechas a partir de la medición

| Problema | Antes | Después | Corrección |
|---|---|---|---|
| Predicción descargaba el modelo serializado (MB) desde la BD en cada uso | 294 s | 30–40 s | `ModeloEntrenado` difiere el artefacto por defecto; se lee de la copia en disco |
| Recomendaciones releían todas las predicciones recién guardadas | — | — | Se pasan en memoria |
| Listado de jornadas traía usuarios completos y puntos completos de cada ruta | 5,3 s | 1,8 s | `Prefetch` con solo los campos usados |
| Reporte de jornadas traía todas las columnas | 8,9 s | 2,6 s | `.only()` con los campos del reporte |
| Búsqueda de puntos | 2,7 s | 0,3 s | (efecto de lo anterior sobre la conexión compartida) |

## Pendiente

- **RTR11 (predicción de 500 puntos a 30 días): 30–40 s, no cumple ≤ 15 s en este entorno.** El tiempo restante es transferencia: insertar ~24 000 predicciones y leer el historial reciente de 512 puntos por una conexión de ~160 ms. Con el volumen real de la DSU (45 puntos) tarda unos 5 s. Repetir la medición desde el servidor de producción en `sa-east-1`; si aún no cumple, guardar las predicciones con `COPY` o agregadas por punto y día.
- **RNF4 / RCM1 / RCM2 (concurrencia):** `scripts/carga.py` está listo; correrlo contra el servidor de producción o una rama de prueba de Neon (el modo con escrituras registra vaciados reales).
- **RCM4 (fluidez del mapa con todos los puntos):** se mide en el navegador.
