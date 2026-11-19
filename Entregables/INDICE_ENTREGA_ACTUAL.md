# Entrega vigente DSU y Residata

Fecha: 19/11/2026. Rama: cierre-software2-20261118.

- **Documento para imprimir:** [PDF canónico](../revision_documental_final/entrega/Documento_Software_2_DSU_Entrega.pdf). Editable Word del mismo nombre. No se modificó el contenido académico para añadir Flutter.
- **Manual de usuario web:** [PDF independiente](Material_Drive/04_Manual_de_Usuario.pdf), [fuente por rol](../gestion-residuos-dsu/frontend/docs/MANUAL_USUARIO.md) y capítulo 12 del documento.
- **Estándares de codificación:** sección 3.9.3 y anexo I del documento canónico.
- **Android:** [APK de demostración ARM64](Material_Drive/09_Android/DSU_Campo_Android_Demo.apk) y [guía](../gestion-residuos-dsu/movil/README.md). Usa GPS y dictado para localizar un punto permitido y reportar una incidencia.
- **Folleto:** [PDF de Residata](Material_Drive/10_Marketing/Folleto_Residata.pdf); fuente ejecutable en generador/materiales/folleto.py.
- **Marketing y pitch:** sitio-residata/marketing, sitio-residata/pitch y piezas marketing-*.png de DocumentoSoftware2/recursos/sitio. Cifras del cierre: VAN Bs 117027, TIR operativa 41,8 %, capital propuesto Bs 200000; escenarios, no resultados comerciales.
- **Videos de pruebas:** [ZIP dividido y verificado](../revision_documental_final/entrega/evidencias/Evidencias_GUI_DSU_Residata.zip.partes/README.md), con 66 grabaciones. No es un video publicitario narrado.
- **Diagramas, modelos EA, pruebas y defensa:** revision_documental_final/entrega, según su README.
- **Limpieza:** Entregables/versiones/INDICE_COPIAS_IDENTICAS.json y restaurar_copias.py permiten reconstruir 980 copias idénticas retiradas. Se conserva todo contenido distinto y el historial Git.

## Drive

Carpeta de destino del QR: https://drive.google.com/drive/folders/1GtrE_rtlimZ3zcj4aZsuvZf6RaErTHqg

Preparar con `python generador/materiales/preparar_drive.py`. Genera Entregables/Drive_Actualizado_20261119 con documento, manual, folleto, APK, guía, ZIP completo e inventario SHA-256. Excluye configuraciones .env, historial Git y configuraciones personales. El ZIP incluye el paquete audiovisual reconstruido; el índice comprueba CRC e integridad del original.

El paquete reconstruible para Drive no se duplica en Git. El APK, las fuentes y los materiales nuevos sí se conservan en el repositorio privado. Las versiones anteriores de Drive se conservan mientras se identifica la entrega nueva.
