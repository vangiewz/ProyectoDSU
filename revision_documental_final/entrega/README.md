# Entrega final académica DSU / Residata · 19/11/2026

**Imprimir y presentar:** Documento_Software_2_DSU_Entrega.pdf. **Editable:** Documento_Software_2_DSU_Entrega.docx.

El documento con sufijo Final es anterior y quedó abierto en Word durante la revisión; la versión canónica lleva sufijo Entrega. Son 377 páginas, trece capítulos y sus carátulas, cuatro índices automáticos, 239 figuras, 93 tablas, bibliografía y anexos. Se incluyen dos portadas generales juntas y carátulas separadas en caratulas/.

Consultar Informe_validacion_final.md, Informe_legibilidad.md y Matriz_revision_13_puntos.md antes de exponer. Las guías separadas están en defensa/; sus folios reales se encuentran en defensa/Paginas_capitulos.json.

## Contenido

- modelos/: copia nativa EA implementada, antecedentes, metadatos ORM y fuentes PNG/SVG.
- matriz_fuentes_diagramas.json: fuentes originales y vigentes con numeración final.
- pruebas/: JUnit, matemática, finanzas, listas, QA histórico y controles de entrega.
- evidencias/: informe GUI y paquete audiovisual dividido sin pérdida para GitHub.
- material_complementario/: marketing y pitch local con cifras corregidas.
- finanzas/: modelo financiero ejecutable con sus recursos.
- reproducir/: scripts del cierre; los generadores de documento requieren la estructura del repositorio privado y el Word original, no solo esta carpeta.

## Reproducción segura

Desde la raíz del repositorio, usar Python 3.13 y las dependencias python-docx/Pillow/PyMuPDF para los scripts documentales. Ejecutar completar.py y luego exportar_word.py (Python 3.8 con pywin32 y Microsoft Word instalado); actualizar campos antes de exportar. Renderizar con renderizar.py. La introspección extraer_modelos.py usa el entorno del backend y un destino local ficticio sin abrir conexión a la BD. No ejecutar seed ni escrituras en Neon para reproducir estas comprobaciones.

Los scripts de dibujo se ejecutan por dependencia: dibujar_actividades.py, dibujar_casos_paquetes.py, dibujar_hojas_finales.py y pulido_assets.py; después ampliar_secuencias.py si faltan sus archivos. Cada importación del dibujante base puede regenerar sus vistas; conservar la secuencia y la copia del manifiesto. crear_EA_implementado.py se diseñó para una copia nueva y se detiene si ya existe; usar verificar_EA.py para leer la copia entregada.

Para las evidencias audiovisuales descargadas de GitHub, entrar a evidencias/Evidencias_GUI_DSU_Residata.zip.partes y ejecutar python reconstruir.py. Se verifica SHA-256; el ZIP original local se conserva. Todas las partes son necesarias.

Las pruebas de software completas se reproducen con el runner aislado del repositorio, no lanzando los tests incluidos contra el entorno compartido. Las credenciales no forman parte de esta entrega. La publicación de app/sitio y los accesos privados corresponden al titular.
