# Proyecto DSU — contexto para agentes

## Proyecto y materias

Este repositorio reúne el **Sistema web de gestión de residuos sólidos para la DSU-UAGRM con predicción mediante Random Forest Regressor**, su código y su documentación académica. El equipo realiza **el mismo proyecto para Taller de Grado I y Software 2**, trabajando en grupo en ambas materias. No crear sistemas ni requisitos de negocio divergentes para cada materia.

- **Taller:** documento vigente en `docs/Documento_Taller_de_Grado_I_Grupo_8.docx`; capítulo 4 como fuente de requisitos. Consultar `CLAUDE.md`, `GUIA_FASE2.md`, `GUIA_FASE_FINAL.md` y `generador/fase2/PROGRESO.md` según el trabajo.
- **Software 2:** se eligió **PUDS (Proceso Unificado de Desarrollo de Software)**. Aún no hay entregables propios. Se requiere SQAP; falta confirmar el listado completo y los criterios del docente. Leer `DocumentoSoftware2/CONTEXTO.md`.
- Reutilizar requisitos, análisis, diseño y evidencias de Taller cuando correspondan, adaptándolos a cada entregable. Los ejemplos de otros proyectos no son requisitos oficiales ni trabajo del equipo. No inventar pruebas, actividades ni resultados.

## Código y colaboración

La raíz es el único repositorio Git (`vangiewz/ProyectoDSU`). `gestion-residuos-dsu/backend/` y `gestion-residuos-dsu/frontend/` son carpetas normales, no submódulos. Los antiguos remotos BackendDSU y FrontendDSU se conservan como antecedentes; el trabajo nuevo se comparte aquí.

Antes de tocar código, leer `gestion-residuos-dsu/CLAUDE.md`, el `CLAUDE.md` del componente y `gestion-residuos-dsu/backend/docs/ESTADO.md`. Actualizar el estado al terminar trabajo relevante. Los despliegues de frontend y backend siguen separados aunque comparten repositorio.

## Decisiones vigentes del 15/11/2026

- **Se mantiene PostgreSQL en Neon.** La propuesta de migrar a una base local fue descartada por el usuario. No cambiar proveedor, documentos ni diagramas por aquella propuesta.
- Ambos integrantes usan la base demo existente. No ejecutar `seed`, restauraciones, limpieza, ETL o entrenamiento solo para preparar el clon del compañero. Las escrituras afectan a ambos; coordinar cambios de datos y migraciones.
- Por instrucción explícita del usuario, **solo `gestion-residuos-dsu/backend/.env` se incluye con sus valores actuales en el repositorio privado**. No imprimirlos, copiarlos a documentación o `.env.example`, ni publicar otros secretos. Mantener excluidas las configuraciones personales de herramientas.
- **Antes de hacer público el repositorio:** rotar/revocar todas las credenciales incluidas en `.env` (incluida la clave de Django), retirar el archivo del seguimiento, restaurar su exclusión y limpiar el historial que lo contiene. Verificar también ramas, etiquetas y otros archivos. Borrar el archivo o esta nota no elimina secretos de commits anteriores; coordinar nuevos clones después de reescribir el historial.

## Cuidado con los documentos

No ejecutar `generador/build.py` sin consultar: regeneraría los capítulos 1–4 desde fuentes antiguas y perdería correcciones manuales. Conservar `docs/versiones/2026-09-28_cap1-4.docx`, base usada por el generador de fase 2. Comparar el documento vigente antes de regenerar para preservar modificaciones manuales. Los diagramas se mantienen en Enterprise Architect y sus fuentes en `generador/`.

Responder en español. No hacer commits ni publicaciones salvo que el usuario lo solicite; la creación y publicación inicial de este repositorio sí fueron solicitadas.
