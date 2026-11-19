# Demostración DSU (8–10 minutos)

Usar un entorno aislado o los videos conservados. Identificar expresamente el entorno y fecha. Las credenciales se proporcionan fuera de esta guía.

1. Explicar navegador, app Vercel, API Azure y datos Neon.
2. Operario: jornada, punto, validación y registro; recargar para comprobar persistencia en QA.
3. Supervisor: planificación, asignación, omisión justificada y cierre con control de pendientes.
4. Analítica: distinguir registro, ETL, hecho normalizado y filtros temporales.
5. Predicción: horizonte, modelo vigente, cantidades y margen; explicar decisión humana sobre recomendaciones.
6. Reportes: contrastar tabla y descarga PDF/Excel conservando filtros.
7. Administración: mostrar roles y auditoría con datos de QA, sin claves ni tokens.
8. Pruebas: elegir una guarda de CU9, seguir secuencia, grafo, matriz y testcase aprobado.
9. Exponer límites: seis CU parciales, aceptación y servicios externos pendientes, publicación a cargo del titular.

Evidencia: evidencias/Evidencias_GUI_DSU_Residata.zip y pruebas/regresion_74_pruebas.xml. Reproducción desde el repositorio: `gestion-residuos-dsu/backend/.venv/Scripts/python.exe auditoria_cierre/ejecutar_aislado.py`. Ese runner crea PostgreSQL propio; no sustituirlo por una ejecución directa contra Neon.
