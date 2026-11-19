# Software 2 — estado de la entrega

La entrega canónica es revision_documental_final/entrega/Documento_Software_2_DSU_Entrega.docx y su PDF. Consultar su Informe_validacion_final.md, Matriz_revision_13_puntos.md y las guías de defensa. Los apuntes anteriores se conservan en el respaldo local; ya no describen la versión vigente.

PUDS y trece capítulos. Manual por rol en capítulo 12; estándares en sección 3.9.3 y anexo I. No se modifica el documento académico para añadir Flutter. Sus generadores antiguos fueron retirados de GitHub por pedido del usuario.

El código y sus límites están en gestion-residuos-dsu/backend/docs/ESTADO.md. La app Android está en gestion-residuos-dsu/movil y usa la misma API de Azure. El índice de materiales está en Entregables/INDICE_ENTREGA_ACTUAL.md. Drive se organiza en doce carpetas por tipo de material.

PostgreSQL sigue en Neon. .env es local, no se versiona ni se publica en Drive. No ejecutar seed, ETL, entrenamiento ni restauraciones para preparar un clon. Las pruebas usan bases aisladas. La limpieza histórica implica clones nuevos y no sustituye la rotación de credenciales.
