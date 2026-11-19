# Proyecto DSU — Software 2

## Contexto vigente al 19/11/2026

Este repositorio presenta el sistema DSU / Residata para Software 2, con PUDS. No crear requisitos ni sistemas de negocio divergentes: se mantienen RF1–RF27 y la implementación compartida. El titular pidió retirar de GitHub el material de la otra materia y los generadores académicos; sus archivos originales se conservan localmente y en el respaldo privado, sin alterar el documento vigente.

- Entrega canónica: revision_documental_final/entrega/Documento_Software_2_DSU_Entrega.docx y .pdf. No regenerarlos desde fuentes antiguas. Word/PDF conservan su contenido; el complemento móvil está fuera del documento por decisión del usuario.
- API Azure: https://dsu-uagrm-api.mexicocentral.cloudapp.azure.com; VM dsu-api, grupo residata-dsu-rg, Mexico Central. App: https://dsu-uagrm.vercel.app. Sitio: https://residata-bolivia.vercel.app.
- Se mantiene PostgreSQL en Neon. Las escrituras son compartidas: no ejecutar seed, restauraciones, limpieza, ETL ni entrenamiento como preparación de un clon. Coordinar migraciones.
- .env es solo local y del servidor. La antigua excepción de versionarlo fue revocada por el usuario. No imprimir valores, copiarlos a documentación/ejemplos/Drive ni versionar secretos. Las credenciales incluidas anteriormente requieren rotación; retirar el historial no las revoca.
- La limpieza histórica requiere revisar todas las ramas y etiquetas y usar clones nuevos. El respaldo previo contiene configuración privada y nunca se publica.
- Antes de tocar código, leer gestion-residuos-dsu/CLAUDE.md, el CLAUDE del componente y backend/docs/ESTADO.md. Actualizar el estado al cerrar trabajo relevante.
- Vercel: frontend raíz gestion-residuos-dsu/frontend; sitio raíz sitio-residata. Consultar despliegue/vercel_proyectos.json. Backend y frontend se despliegan separados.
- Android: gestion-residuos-dsu/movil, APK demo ARM64. GPS y dictado usan servicios del teléfono y la API existente. Sin fotos ni cola offline.
- Responder en español. Commits y publicaciones solo cuando el usuario los solicite; el cierre, publicación y limpieza histórica de esta sesión sí fueron solicitados.
