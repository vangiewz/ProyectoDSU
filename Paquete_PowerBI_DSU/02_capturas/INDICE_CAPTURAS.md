# Índice de capturas — 16/11/2026

## Capturas nuevas de la conexión comprobada

Todas proceden de Power BI Desktop y muestran datos de la demo sintética. No acreditan publicación ni despliegue web. Las seis tablas se contrastaron con SELECT en Neon; los recuentos coinciden.

| Archivo | Evidencia |
|---|---|
| [12_powerbi_conectado_informe.png](12_powerbi_conectado_informe.png) | Gráfico cargado antes de ampliar su presentación. |
| [13_modelo_relaciones_completo.png](13_modelo_relaciones_completo.png) | Modelo completo antes de ordenar; referencia anterior a la alineación. |
| [13_modelo_relaciones_ordenado.png](13_modelo_relaciones_ordenado.png) | Modelo con siete tablas alineadas. Se preservaron las siete relaciones y 16 medidas. |
| [14_calendario_importado.png](14_calendario_importado.png) | Calendario: 1.374 filas calculadas. |
| [15_hechos_15430_filas.png](15_hechos_15430_filas.png) | Hechos: 15.430 filas. |
| [16_incidencias_1_fila.png](16_incidencias_1_fila.png) | Incidencias: 1 fila. |
| [17_jornadas_1046_filas.png](17_jornadas_1046_filas.png) | Jornadas: 1.046 filas. |
| [18_predicciones_0_filas.png](18_predicciones_0_filas.png) | Predicciones: cero filas. No hay proyecciones vigentes en esta vista a la fecha de captura. |
| [19_puntos_12_filas.png](19_puntos_12_filas.png) | Puntos: 12 filas. Coordenadas aproximadas de demo. |
| [20_recomendaciones_8_filas.png](20_recomendaciones_8_filas.png) | Recomendaciones: 8 filas, con estados visibles. |
| [21_informe_ampliado_con_datos.png](21_informe_ampliado_con_datos.png) | Gráfico existente ampliado, reabierto y renderizado con los datos cargados. |
| [22_powerbi_tablero_completo.png](22_powerbi_tablero_completo.png) | Tablero completo oficial en Desktop con datos refrescados: 4 tarjetas KPI (Total kg, Cobertura, Incidencias, Recomendaciones), segmentadores de fecha y sector, barras por sector, barras por tipo, barras por punto, evolución mensual y matriz por periodos. |
| [22_tablero_completo_desktop.png](22_tablero_completo_desktop.png) | Página Tablero completa (16/11/2026, tarde): cuatro tarjetas, segmentadores y gráficos por sector, tipo, punto, mes y periodo. Total 119,25 mil kg, igual al SQL de `05_auditoria/powerbi_medidas.json`. Es la figura de CU21 del documento. |

## Antecedentes históricos

- `01_...`: estado inicial de Desktop sin datos visibles. Quedó superado por `12_...` y `21_...`.
- `02_...`: captura aportada por el usuario del diálogo con host de ejemplo; quedó superada por la configuración real.
- `03_...`: Figura 169, pestaña web antes de publicar; no muestra un informe integrado.
- `04_...` a `11_...`: capturas existentes de la aplicación web y del documento con datos demo; no son ejecuciones nuevas.

## Qué falta

Completar las visualizaciones requeridas, comprobar medidas y filtros en cada página, decidir la seguridad/RLS y publicar por solicitud del usuario. El único gráfico actual es evidencia de conexión, no el informe final. Para reproducir los accesos se necesita el .env privado del titular; no se adjuntan claves ni caché. No alterar la base para producir capturas.


Actualización 16/11/2026 (tarde): las medidas se auditaron contra SQL y los visuales se completaron con `powerbi/tablero.py`. Siguen pendientes RLS y publicación.
