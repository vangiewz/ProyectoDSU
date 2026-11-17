# Encargo para el siguiente agente

Completa y audita el informe de Power BI del sistema DSU-UAGRM. La conexión real ya se comprobó en SQL y Desktop; no vuelvas a crear el rol ni a renovar contraseñas para comenzar. Lee `00_LEER_PRIMERO.md`, el índice de capturas, `05_auditoria/`, el README del PBIP y el capítulo 4 del documento vigente, 2.6, CU21/CU22 y 7.5.21. El proyecto es único para Taller y Software 2.

## Continuación

1. Abrir `01_proyecto_powerbi/DSU-Residuos.pbip`. Conserva BIM y PBIR; no ejecutar `powerbi/generar.py` ni sustituir archivos por una versión anterior. El original operativo está en `gestion-residuos-dsu/backend/powerbi/` del repositorio.
2. Revisar siete tablas, 16 medidas, relaciones y propagación de filtros. Auditar las diferentes granularidades, en particular jornadas frente a hechos/puntos; no asumir que un filtro de punto filtra correctamente las jornadas. Contrastar totales con SELECT o fixtures aisladas, y dejar filtros, entorno y resultados reproducibles.
3. Completar gráficos según los requisitos: indicadores kg y L separados, generación por sector y tipo, evolución, comparación de periodos, cobertura/incidencias/recomendaciones y filtros pertinentes. Revisar nulos, ceros, porcentajes y selecciones sin datos. Identidad DSU: rojo #C4122F, grafito #1E2328, azul observado #1F3FA8 y gris estimado #55606C.
4. Proyecciones: la vista está vacía actualmente. Mostrar una explicación si no hay datos. Cuando existan, incluir margen, versión y carácter estimado. No entrenar ni alterar la demo para llenar la visualización.
5. Capturar cada página final, filtros y comprobaciones relevantes. Auditar visualmente y corregir antes de entregar. Una captura de Desktop se identifica como Desktop; no reemplaza evidencia de integración web.
6. Publicar solo con solicitud del usuario y destino definido. El titular usa su cuenta Microsoft. No publicar anónimamente; revisar RLS y quién puede consultar cada sector antes de compartir. Los permisos de Django no se heredan automáticamente.
7. Si se actualiza la Figura 169, preservar el nombre oficial del Word, los campos SEQ y los índices. Renderizar y revisar páginas afectadas. No ejecutar `generador/build.py` ni `fase2/insertar.py`.

## Restricciones

Mantener Neon, Vercel y AWS EC2 Linux/Docker. No ejecutar seed, ETL, entrenamiento, limpieza, restauraciones, migraciones ni cambios de esquema/datos compartidos por preparar el informe. Los SQL adjuntos son referencia existente. No copiar secretos del `.env` a este paquete, al modelo, a capturas ni a documentación. La credencial local está en `POWERBI_PASSWORD` del `.env` privado; una máquina diferente puede necesitar que el titular la introduzca.

No inventar pruebas, datos institucionales, publicación ni ahorros. Los ejemplos docentes no crean requisitos adicionales. No hacer commits ni publicaciones sin solicitud del usuario.

## Entrega

PBIP completo, cambios justificados, cálculos y filtros contrastados, capturas reales rotuladas, estado de publicación exacto y pendientes. Validar cada producto antes de declararlo terminado.
