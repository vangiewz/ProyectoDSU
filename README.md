# DSU y Residata — Software 2

Sistema de gestión de residuos sólidos para la DSU-UAGRM, con aplicación web, API Django en Azure y predicción mediante Random Forest Regressor. Entrega académica de Software 2 con metodología PUDS y trece puntos. El complemento Flutter Android usa los mismos usuarios, permisos y API.

## Contenido vigente

| Carpeta | Contenido |
|---|---|
| gestion-residuos-dsu/backend | API, reglas de negocio, ETL, predicción, pruebas y despliegue Azure |
| gestion-residuos-dsu/frontend | Aplicación React/Vite publicada en Vercel |
| gestion-residuos-dsu/movil | Flutter Android: puntos cercanos por GPS e incidencias con dictado |
| sitio-residata | Sitio corporativo, marketing y pitch |
| revision_documental_final/entrega | Word/PDF canónicos, diagramas, modelos EA, pruebas y defensa |
| DocumentoSoftware2 | Contexto, textos de apoyo, recursos y modelo financiero |
| Entregables | Manuales y materiales distribuibles, APK y folleto |
| auditoria_gui, auditoria_movil, auditoria_cierre, docs/auditoria-fase-final | Evidencias con sus fechas, alcance y límites |
| herramientas | Preparación de materiales y pruebas aisladas; sin generadores del documento académico |
| despliegue | Configuración esperada de los proyectos Vercel y cierre del repositorio |

**Documento vigente:** [PDF para imprimir](revision_documental_final/entrega/Documento_Software_2_DSU_Entrega.pdf) y Word editable del mismo nombre. El contenido académico se conserva; Flutter no se añadió al documento. El manual está en el capítulo 12 y los estándares en 3.9.3 y el anexo I.

**Material compartido:** [carpeta del QR de Drive](https://drive.google.com/drive/folders/1GtrE_rtlimZ3zcj4aZsuvZf6RaErTHqg), organizada por tipo de material. [Índice local](Entregables/INDICE_ENTREGA_ACTUAL.md).

## Servicios

- App web: https://dsu-uagrm.vercel.app/
- API: https://dsu-uagrm-api.mexicocentral.cloudapp.azure.com/api/
- Sitio: https://residata-bolivia.vercel.app/
- Datos: PostgreSQL en Neon; no se cambia de proveedor.

## Desarrollo

Usar Python 3.12, PostgreSQL y Node.js 22 actualizado; para Android, Flutter 3.41.7 y Android SDK. Consultar los README de cada componente. Crear la configuración local desde .env.example y obtener las credenciales del titular por un canal privado. .env no forma parte del repositorio ni de Drive.

La base demo es compartida. No ejecutar seed, restauraciones, limpieza, ETL ni entrenamiento para preparar un clon. Las pruebas de backend usan PostgreSQL aislado: `python herramientas/pruebas/pruebas_aisladas.py`, o el servicio PostgreSQL definido en CI. Las pruebas de Flutter se ejecutan con `flutter analyze` y `flutter test` dentro de movil.

Las capturas y métricas de demo usan datos sintéticos y mantienen sus límites. No acreditan aceptación institucional, ventas ni cobertura exhaustiva.

## Alcance del repositorio y credenciales

Por instrucción del titular del 19/11/2026, el material de la otra materia, los ejemplos ajenos, las versiones documentales antiguas y los generadores académicos se conservan localmente, fuera del seguimiento de Git. El código de negocio sigue siendo el mismo sistema DSU.

La limpieza del historial retira .env y busca los valores sensibles de sus versiones. Esto no revoca las credenciales antiguas: deben rotarse antes de una publicación abierta. Mantener el repositorio privado y usar clones nuevos después de la reescritura; un clon anterior puede reintroducir el historial retirado.
