# Auditoría de la fase final

Documento 1–10 integrado y revisión editorial digital completada; validación final del proyecto pendiente

Documento: `docs\Documento_Taller_de_Grado_I_Grupo_8.docx`. La matriz registra comprobaciones ejecutadas y dependencias; no certifica producción ni aceptación institucional.

| ID | Control | Estado | Evidencia o acción |
|---|---|---|---|
| P01 | Copia íntegra del vigente anterior | Verificado | inventario.json |
| P05 | 186 imágenes anteriores conservadas; vista general, despliegue y Power BI actualizados | Verificado | Comparación SHA-256 de imágenes en orden; vista general con nombres completos en posición 58, despliegue en 111, informe de Power BI Desktop en 170; nuevas: 9 componentes, 2 grafos, 27 evidencias CP y 3 de ZAP |
| P02 | Diez capítulos presentes | Verificado | DOCX: títulos de capítulo |
| P03 | Cuatro actores y 34 CU | Verificado | datos.py |
| P04 | RF1–RF27 trazados a CU | Verificado | datos.py |
| DOC-5.4. | Cobertura de apartados 5.4. | Verificado | 34 de 34 |
| DOC-6.2. | Cobertura de apartados 6.2. | Verificado | 34 de 34 |
| DOC-7.5. | Cobertura de apartados 7.5. | Verificado | 34 de 34 |
| DOC-8.2. | Cobertura de apartados 8.2. | Verificado | 8 de 8 |
| C8-01 | Nueve diagramas de componentes disponibles | Verificado | Exportación de Enterprise Architect |
| C8-02 | Seis apartados de herramientas | Verificado | DOCX: títulos 8.3.1–8.3.6 |
| CP-01 | Plantilla de siete campos | Verificado | Tabla de caja negra del DOCX |
| CP-02 | Plantilla de siete campos | Verificado | Tabla de caja negra del DOCX |
| CP-03 | Plantilla de siete campos | Verificado | Tabla de caja negra del DOCX |
| CP-04 | Plantilla de siete campos | Verificado | Tabla de caja negra del DOCX |
| CP-05 | Plantilla de siete campos | Verificado | Tabla de caja negra del DOCX |
| CP-06 | Plantilla de siete campos | Verificado | Tabla de caja negra del DOCX |
| CP-07 | Plantilla de siete campos | Verificado | Tabla de caja negra del DOCX |
| CP-08 | Plantilla de siete campos | Verificado | Tabla de caja negra del DOCX |
| CP-09 | Plantilla de siete campos | Verificado | Tabla de caja negra del DOCX |
| CP-10 | Plantilla de siete campos | Verificado | Tabla de caja negra del DOCX |
| CP-11 | Plantilla de siete campos | Verificado | Tabla de caja negra del DOCX |
| CP-12 | Plantilla de siete campos | Verificado | Tabla de caja negra del DOCX |
| CP-13 | Plantilla de siete campos | Verificado | Tabla de caja negra del DOCX |
| CP-14 | Plantilla de siete campos | Verificado | Tabla de caja negra del DOCX |
| CP-15 | Plantilla de siete campos | Verificado | Tabla de caja negra del DOCX |
| CP-16 | Plantilla de siete campos | Verificado | Tabla de caja negra del DOCX |
| CP-17 | Plantilla de siete campos | Verificado | Tabla de caja negra del DOCX |
| CP-18 | Plantilla de siete campos | Verificado | Tabla de caja negra del DOCX |
| CP-19 | Plantilla de siete campos | Verificado | Tabla de caja negra del DOCX |
| CP-20 | Plantilla de siete campos | Verificado | Tabla de caja negra del DOCX |
| CP-21 | Plantilla de siete campos | Verificado | Tabla de caja negra del DOCX |
| CP-22 | Plantilla de siete campos | Verificado | Tabla de caja negra del DOCX |
| CP-23 | Plantilla de siete campos | Verificado | Tabla de caja negra del DOCX |
| CP-24 | Plantilla de siete campos | Verificado | Tabla de caja negra del DOCX |
| CP-25 | Plantilla de siete campos | Verificado | Tabla de caja negra del DOCX |
| CP-26 | Plantilla de siete campos | Verificado | Tabla de caja negra del DOCX |
| CP-27 | Plantilla de siete campos | Verificado | Tabla de caja negra del DOCX |
| C9-01 | Veintisiete escenarios funcionales documentados | Verificado | 27 |
| TEST-pruebas | 42 pruebas ejecutadas sin fallos ni omisiones | Verificado | 42 pruebas; pruebas/pytest.xml |
| TEST-pruebas_linux | 42 pruebas ejecutadas sin fallos ni omisiones | Verificado | 42 pruebas; pruebas_linux/pytest.xml |
| CB-asignar | Caminos y base factible contrastados | Verificado | V estructural 7; rango factible/ejecutado 7 |
| CB-generar | Caminos y base factible contrastados | Verificado | V estructural 9; rango factible/ejecutado 7 |
| ZAP-api | Reporte posterior de seguridad disponible | Verificado | docs\auditoria-fase-final\seguridad\verificado\api.json |
| ZAP-frontend | Reporte posterior de seguridad disponible | Verificado | docs\auditoria-fase-final\seguridad\verificado\frontend.json |
| DOC-ERROR | Sin marcadores de error de campos o imágenes | Verificado | Inspección del texto DOCX; PDF tiene control independiente |
| DOC-TOKEN | Sin JWT de prueba en el documento | Verificado | Búsqueda de estructura JWT; no se imprimen credenciales |
| UI-01 | Carga de 25 combinaciones de rol/ruta en dos resoluciones | Verificado | ui/resultados.json y ui/auditoria.json; no sustituye flujos completos |
| BIB-01 | Edición española de Jacobson unificada y contrastada | Verificado | bibliografia_verificada.json y página legal conservada |
| PAG-01 | Tablas nuevas y notas en la misma página | Verificado | paginacion_tablas.json: rangos de página calculados por Word |
| PDF-01 | PDF actualizado sin errores de campos ni páginas vacías | Verificado | pdf_indice.json; inspección visual complementaria en revision_visual.json |
| IND-01 | 742 entradas de índice contrastadas con el PDF vigente | Verificado | verificacion_indices.json: 229 figuras y 205 tablas; título presente en la página indicada |
| PAG-02 | Caracteres dentro del papel en todas las páginas | Verificado | geometria_pdf.json; no sustituye revisión de rótulos dentro de imágenes |
| VIS-01 | Revisión digital global y correcciones posteriores contrastadas | Verificado | revision_visual.json y continuidad_maquetacion.json; alcance digital, sin prueba de impresión física |
| SEG-01 | RNF15 distingue hash de cifrado reversible | Verificado | RNF15; algoritmo de desarrollo contrastado en contraseñas_verificacion.json |
| COST-01 | Presupuesto del perfil conciliado con capítulo 10 | Verificado | Tablas 6 y 191; costos_calculados.json |
| DOC-TABLAS | Tablas añadidas completas y notas en la misma página | Verificado | paginacion_tablas.json; comprobación nativa Word |
| R2-01 | Secciones finales en el orden de la presentación de la materia | Verificado | DOCX: títulos de nivel 1; finales.py |
| R2-02 | 8.2 por nodos reales con archivos, tablas y vistas existentes | Verificado | componentes.validar(): archivos, tablas de esquema.json, vistas bi_* y dependencias por imports |
| R2-03 | Diagrama general de CU con nombres completos y todas las relaciones | Verificado | c5_general_nombres.json: {'extend': 7, 'include': 2, 'Association': 75}; 85 cruces y 20 líneas sobre elipses |
| R2-04 | Evidencia de caja negra por la interfaz para los 27 CP | Verificado | evidencia_cp/evidencias.json: estado HTTP y texto del oráculo; 27 figuras en 9.3.1 |
| R2-05 | Código de caja blanca con marcas de nodo y sin cortes dentro de identificadores | Verificado | 148 líneas de código; máximo 81 caracteres |
| R2-06 | Figuras de la prueba de vulnerabilidad | Verificado | c9_zap_consola, c9_zap_inicial y c9_zap_verificado |
| R2-07 | Medidas de Power BI contrastadas con SQL | Verificado | powerbi_medidas.json: 14 medidas con su consulta SQL equivalente; 2 limitaciones declaradas |
| V02 | Power BI completo y publicado | Pendiente del titular | Medidas auditadas contra SQL y visuales escritos en el PBIR con powerbi/tablero.py. Falta abrir en Desktop, actualizar, revisar filtros, capturar, definir RLS y publicar. |
| V03 | Despliegue AWS/Vercel verificado | Pendiente | Compose y Caddy preparados; construcción y regresión Linux no sustituyen el despliegue remoto. |
| V04 | Rendimiento y concurrencia en la región del servidor | Pendiente | Repetir RTR11, carga y fluidez del mapa en entorno representativo y aislado. |
| V05 | Seguridad productiva y residual de frontend | Pendiente | CSP mantiene connect-src HTTPS amplio y estilos inline por compatibilidad. Ajustar dominio final, comprobar Power BI/mapas y revisar advertencias residuales. |
| V06 | Validación predictiva con histórico institucional | Dependencia externa | Las métricas actuales de demo/prueba utilizan datos sintéticos; no prueban precisión DSU. |
| V07 | Prueba de impresión y entrega física | Pendiente | Revisión digital realizada. La página A3 del diagrama general requiere impresión y plegado. Confirmar acabado/entrega indicados por el docente. |
| V11 | Letra impresa de los diagramas EA de los capítulos 5–7 | Pendiente decisión | Medición por figura: la mayoría entre 3 y 5 pt impresos (letra por defecto de EA reducida al ancho de página). Corregido en 5.5, 8.1–8.2 y 9.3.2; el resto requiere regenerar las figuras con letra mayor. |
| V08 | Cotizaciones y línea base económica institucional | Proyección condicionada | Referencia CITI de la lámina 2021 y supuestos declarados; no son tarifas certificadas vigentes, compras ni ahorros medidos. |
| V09 | Respaldo externo y restauración del despliegue | Pendiente | No afirmar copia S3 o restauración productiva ejecutada por incluir su provisión en el presupuesto. |
| V10 | Caracterización institucional del capítulo 3 | Dependencia externa | Misión, visión, organigrama, datos de contacto, ubicación y dimensionamiento delimitados como propuestas o referencias pendientes. Falta fuente institucional aprobada o validación DSU; las imágenes disponibles no acreditan por sí solas la ubicación de sus oficinas. |

Los cálculos económicos se reproducen con `generador/fase_final/costos.py`. Las pruebas se ejecutan en bases desechables; Neon solo se consultó en modo lectura para confirmar su versión. No se realizaron commits ni publicaciones.
