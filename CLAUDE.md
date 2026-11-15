# CLAUDE.md — Proyecto DSU: Taller de Grado I y Software 2

Leer primero [AGENTS.md](AGENTS.md): contexto compartido, PUDS para Software 2, repositorio privado unificado y decisión de mantener Neon. Para Software 2, ver [DocumentoSoftware2/CONTEXTO.md](DocumentoSoftware2/CONTEXTO.md). Este archivo desarrolla las instrucciones de Taller.

Carpeta de trabajo del proyecto "Sistema web de gestión de residuos sólidos para la DSU-UAGRM con predicción mediante Random Forest Regressor".

## Qué hay aquí

| Ruta | Qué es |
|---|---|
| `gestion-residuos-dsu/` | **El sistema (código)**, en dos carpetas del mismo repositorio: `backend/` (API Django) y `frontend/` (SPA React). Cada uno tiene su `CLAUDE.md`; el estado de todo el sistema está en [backend/docs/ESTADO.md](gestion-residuos-dsu/backend/docs/ESTADO.md). Para trabajar en el sistema, leer [gestion-residuos-dsu/CLAUDE.md](gestion-residuos-dsu/CLAUDE.md) y ESTADO.md primero. |
| `docs/Documento_Taller_de_Grado_I_Grupo_8.docx` | **Documento vigente del taller** (cap. 1–7; lo genera `generador/fase2/insertar.py`). El capítulo 4 es la especificación de requisitos (RF1–RF27, RNF, RBD, RD): fuente de verdad del sistema. |
| `DocumentoSoftware2/` | Contexto de Software 2 y ejemplos de otros proyectos. Metodología PUDS confirmada; entregables propios pendientes, incluido SQAP. |
| `docs/versiones/` | Historial: cada generación como `<fecha>_<hora>_cap1-N.docx`, más el PDF viejo. **`2026-09-28_cap1-4.docx` es la base** sobre la que `insertar.py` agrega los cap. 5–7: no editarla ni borrarla (los cap. 1–4 se corrigen ahí). |
| `generador/` | Scripts Python (python-docx) que generan el .docx: `build.py` ensambla `cap1.py`–`cap4.py`, `requisitos.py`, `figuras/`. |
| `GUIA_FASE2.md` | **Cómo hacer los cap. 5, 6 y 7** según el ingeniero (reglas, estructura, convenciones, propuesta de CU y paquetes, checklist). |
| `GUIA_FASE_FINAL.md` | **Cómo hacer los cap. 8, 9 y 10 y preparar la defensa final** según el ingeniero (reglas, diagramas de componentes en EA, pruebas de caja negra/blanca/vulnerabilidad, costos en Bs, ROI a 12 meses, matriz de riesgos, seguridad y checklist final). |
| `cap8-10/` | **Láminas oficiales del docente para la Fase Final**: `Fase 3 _ Cap 8 Implementacón.pdf` (11 págs.), `Fase 3 _ Cap 9 Pruebas.pdf` (23 págs.) y `CAP 10 - Costos.pdf` (7 págs.). |
| `clases/` | Transcripciones (Whisper large-v3-turbo) y análisis contextual de todas las clases grabadas: Fase 2, revisión del 26/10 ([contexto](clases/2026-10-26_revision-fase2_contexto.md)), clase del 06/11 (Cap. 8, [contexto](clases/2026-11-06_cap8_implementacion_contexto.md)) y clase del 11/11 (Cap. 9 y 10, [contexto](clases/2026-11-11_cap9-10_pruebas_costos_contexto.md)), junto con evidencias fotográficas en `evidencias-2026-11-06/`, `evidencias-2026-11-11/` y recursos vectoriales en `recursos_diapositivas/`. |
| `Fase 2 _ Cap 5/6/7 *.pdf` | Láminas del docente de la Fase 2. `Sistema de gestion para la Farmacia ... FINAL.pdf` es una tesis completa de ejemplo (cap. 5–7 en pp. 129–260). |
| Otros PDF | Material de la materia (presentación, guía APA 7, modelos de ciclo de vida, perfil, referencias). |

## Fase 2 (en curso)

Entrega inicial de la Fase 2: **miércoles 21/10/2026**, digital en Drive. En la grabación del 26/10 el docente anuncia nueva presentación para el viernes (**30/10/2026**, fecha inferida) y suspende la clase del miércoles 28/10. No precisa nueva hora ni canal; revisará fases 1 y 2. Ver [nota de revisión](clases/2026-10-26_revision-fase2_contexto.md).

**Contexto actualizado el 28/10/2026:** la revisión a otro estudiante aporta criterios generales, no defectos comprobados de DSU. Producción real en despliegue, roles reales, ejecución predictiva explícita, trazabilidad completa e interfaces legibles son puntos pendientes de contrastar. No se modificaron el documento ni el código al incorporar esta clase.
**Para retomar el trabajo, leer primero [generador/fase2/PROGRESO.md](generador/fase2/PROGRESO.md)** (qué está hecho, qué falta y cómo se generan los diagramas en Enterprise Architect y el .docx). Decisión vigente (30/10/2026): **34 CU, todos con actor, y 4 actores independientes** en `generador/fase2/datos.py`, que reemplazan la lista de 47 de la guía y la versión anterior de 38. Toda la guía:

@GUIA_FASE2.md

## Fase final (en curso)

La Fase Final abarca los **Capítulos 8 (Implementación), 9 (Pruebas) y 10 (Costos, Riesgos y Seguridad)**, culminando con la **Revisión Final de Documento Completo (Cap. 1 al 10 en digital y físico impreso, 30 pts)** y la **Revisión Final de Software y Defensa en Vivo (30 pts)**.

- **Capítulo 8 (Implementación)**: Explicado el 06/11/2026. Estructura oficial: 8.1 Arquitectura del Sistema (componentes y paquetes con BD OLTP y OLAP), 8.2 Arquitectura del Subsistema (un diagrama de componentes en Enterprise Architect por cada uno de los 8 paquetes de DSU) y 8.3 Herramientas de Desarrollo (8.3.1 a 8.3.6 con versiones reales). **Prohibido incluir código fuente en este capítulo**. Ver [clases/2026-11-06_cap8_implementacion_contexto.md](clases/2026-11-06_cap8_implementacion_contexto.md).
- **Capítulo 9 (Pruebas)**: Láminas oficiales publicadas el 11/11/2026. Cita obligatoria de Jacobson et al. (2000, Cap. 11). Estructura: 9.1 Planificación, 9.2 Diseño (9.2.1 Plantilla de 7 campos para Caja Negra), 9.3 Pruebas Realizadas: 9.3.1 Caja Negra para CU críticos, 9.3.2 Caja Blanca (código numerado, grafo CFG, caminos independientes y complejidad de McCabe $V(G)$) y 9.3.3 Pruebas de Vulnerabilidad (OWASP ZAP). Ver [clases/2026-11-11_cap9-10_pruebas_costos_contexto.md](clases/2026-11-11_cap9-10_pruebas_costos_contexto.md).
- **Capítulo 10 (Costos, Riesgos y Seguridad)**: Explicado el 11/11/2026. Estructura: 10.1 Estimación de Costos en Bolivianos (Bs.) con Tabla General y desgloses 10.1.1 a 10.1.5 (personal según aranceles de la Sociedad de Ingenieros de Bolivia - SIB); 10.2 Retorno de la Inversión (ROI) proyectado a 12 meses adaptado a DSU (ahorro de vertedero, rutas y venta de reciclables con conclusión textual obligatoria); 10.3 Matriz de Riesgos y Contingencia; 10.4 Seguridad Lógica y Física con citas teóricas y matrices riesgo-solución. Ver [clases/2026-11-11_cap9-10_pruebas_costos_contexto.md](clases/2026-11-11_cap9-10_pruebas_costos_contexto.md).
- **Documento Rector Completo**: Leer y aplicar estrictamente **[GUIA_FASE_FINAL.md](GUIA_FASE_FINAL.md)** antes de redactar o generar cualquier artefacto de la fase final.

## Cuidado

- **No ejecutar `generador/build.py` sin preguntar**: regenera los cap. 1–4 desde los scripts del 23/09 y perdería los cambios hechos a mano en la base `docs/versiones/2026-09-28_cap1-4.docx` (editada el 28/09).
- Para leer el .docx usar python-docx (instalado); el texto completo con tablas se extrae recorriendo `document.element.body`.
- Responder en español.
