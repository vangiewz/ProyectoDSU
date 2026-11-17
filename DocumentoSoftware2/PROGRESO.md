# Software 2 — avance y trazabilidad

Actualizado: 16/11/2026.

## Decisiones y presentación

Documento independiente de Taller para el mismo sistema DSU. El usuario autorizó usar los ejemplos como estructura, confirmó PUDS y Grupo 8 y pidió retirar la fecha de entrega. Carátula con escudo FICCT existente, formato académico del ejemplo 2025, Times New Roman, índice automático y bordes dobles. El nombre del docente procede de los ejemplos y sigue pendiente de confirmación; no fue proporcionado por el usuario. La estructura adoptada no equivale a una rúbrica confirmada.

## Versión vigente

- **Documento_Software_2_DSU.docx**: Versión oficial consolidada de 12 capítulos completos, 34 tablas y 135 figuras numeradas (134 diagramas UML + 1 captura de interfaz con datos sintéticos, más el escudo en portada). Sin bordes de página artificiales (páginas limpias con márgenes académicos estándar), con láminas horizontales A3 (42 x 29.7 cm) en los diagramas densos para legibilidad total.
- Fuentes editables: `paps.md` y `capitulos.md`. El inventario estructurado de diagramas reutilizados reside en `modelos.py`. `ensamblar.py` es el generador vigente; `generar.py` lo invoca por compatibilidad. Soporta tablas dinámicas de cualquier número de columnas.
- Automatización de revisión: `revisar.ps1` actualiza los campos, repagina y exporta a PDF mediante Word COM. `verificar_modelos.py` realiza auditoría estructural completa (dimensiones, márgenes, campos rotos, páginas vacías, congruencia de hashes con Taller y planchas de contacto). No ejecutar el generador de Taller.

## Contenido y procedencia

- PAPS (Cap. 1): alcance RF1–RF27, métricas propuestas, organización, riesgos y planificación. estimaciones.json contiene 16 actividades pendientes con estimación O/M/P: 112/190/316 horas-persona y media ponderada de 198 horas-persona.
- SQAP (Cap. 2): políticas, roles, documentación, revisiones, verificación y validación, defectos, herramientas, registros, formación y control de cambios bajo IEEE 730-2026, ISO/IEC 25010:2023 y NASA.
- PUDS (Cap. 3): fases, artefactos, trazabilidad de 34 CU y 130+ modelos integrados (dominio, flujos, casos de uso, paquetes, 34 realizaciones de análisis, clases, base de datos, secuencias y subsistemas).
- Herramientas CASE (Cap. 4): Sparx Systems Enterprise Architect (UML 2.5), VS Code, Git/GitHub, pytest/Docker/ZAP/Power BI, y tabla comparativa de productividad por etapa con ahorros del 45% al 85%.
- Aspectos Legales (Cap. 5): Marco jurídico boliviano exhaustivo. Constitución de S.R.L. (Código de Comercio D.L. 14379, arts. 127 y 195–216), SEPREC (reserva de nombre, aranceles oficiales de Bs. 455 matrícula + Bs. 192 gaceta, total Bs. 647), SIN (NIT Régimen General, Facturación Electrónica en Línea, IVA, IT, IUE), Patente Municipal GAMSC (Quinta Municipal, Form. 101, impacto ambiental Cat. IV), ROE Ministerio de Trabajo, Gestora Pública y CNS. Registro SENAPI de Marca y Logotipo (Decisión 486 CAN, Clases 9 y 42 de Niza, Form. PI-101, Gaceta Oficial) y Derecho de Autor de Software (Ley 1322 y D.S. 23907, Form. DDA-01, depósito de código y manuales, derechos morales inalienables a Lobo Gutiérrez y Serrate Basma, y cesión/licencia institucional para UAGRM/DSU). Ley 164 de Telecomunicaciones y TIC, comercio electrónico, firma digital, SLA y gobernanza de datos.
- Infraestructura (Cap. 6): Elementos de configuración, entornos (dev local, test Docker, prod híbrido), control de versiones y tabla de versiones observadas.
- Sitio Web de Presentación (Cap. 7): Arquitectura de información, landing page institucional, tabla de mesa de ayuda multicanal en tres niveles (Nivel 1 autoservicio/FAQ, Nivel 2 soporte funcional, Nivel 3 ingeniería) con SLAs de respuesta, y hoja de ruta (PWA offline con IndexedDB y telemetría IoT ultrasónica).
- Estudio de Mercado (Cap. 8): Diagnóstico del contexto de gestión de residuos en Santa Cruz y UAGRM. Tabla comparativa profunda de 7 columnas entre soluciones internacionales (Sensoneo, Ecube Labs CleanCityNetworks, Bigbelly CLEAN) y DSU-UAGRM. Propuesta de valor adaptada al medio local y estrategia de adopción con prueba piloto y medición de usabilidad estandarizada SUS.
- Pruebas (Cap. 9): reportes JUnit del 16/11/2026 (42 pruebas en Windows y 42 en Linux Docker sin fallos ni errores), escenarios de API, análisis de caja blanca con grafos de complejidad ciclomática de Asignar (7) y Generar (9).
- Marketing y Difusión (Cap. 10): Propuesta de valor, cuatro Buyer-Personas institucionales (Directivo, Supervisor, Personal Operativo, Evaluador), canales y fases de la campaña, y tabla de KPIs con metas objetivas.
- Puesta en Marcha y Despliegue (Cap. 11): Comparativa técnica y de costos mensuales entre AWS, Azure, GCP y la Arquitectura Híbrida Adoptada (VPS Docker Caddy + Neon PostgreSQL + Vercel). Plan de continuidad operativa y recuperación ante desastres (DRP con respaldos diarios pg_dump, RPO <= 24 h, RTO <= 2 h y protocolo de restauración). Hardening perimetral (cabeceras HTTP HSTS/CSP, JWT, CORS, RBAC).
- Software como Producto (Cap. 12): Guía por roles, guiones de video, inventario de entrega y anexos de control A a E (incluyendo fichas de prueba CP-10, CP-15 y CP-21).

## Pendientes reales

Confirmar docente y criterios finales de evaluación. Acordar disponibilidad, responsables, calendario y costos. Ampliar manual y producir videos. Completar inventario de licencias y condiciones de titularidad. Validar adopción con usuarios, precisión con datos institucionales, rendimiento y despliegue remoto; acreditar respaldo y restauración. Completar informe Power BI, RLS y publicación según el estado técnico. No presentar estos puntos como realizados.

## Revisión y preservación

Revisión visual por páginas de carátula, índice, cuerpo, tablas, figuras y anexos. Word actualizó campos e índice mediante COM (`revisar.ps1`). El script `verificar_modelos.py` auditó las 186 páginas del PDF resultante (`tmp/software2_diagramas/revision.pdf`): 0 campos rotos, 0 páginas vacías, 0 imágenes fuera de margen y correspondencia exacta de 132/132 hashes SHA256 contra las imágenes originales de Taller. Se generaron 16 láminas de contacto (`plancha-01.png` a `plancha-16.png`) en `tmp/software2_diagramas/` para inspección rápida en cuadrícula 3x4. Los PDF e imágenes en `tmp/` son intermediarios de auditoría, no entregables finales. La versión inicial de nueve páginas se conserva en `versiones/2026-11-16_inicial_9p.docx`.

No se modificaron Taller, su generador, código o base de datos. No se hicieron commits ni publicaciones. Las demás modificaciones del repositorio pertenecen a trabajo previo o paralelo del usuario.
