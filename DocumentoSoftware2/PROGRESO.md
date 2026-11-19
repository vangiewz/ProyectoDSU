> **Entrega documental del 19/11/2026:** versión canónica en [Documento_Software_2_DSU_Entrega.pdf](../revision_documental_final/entrega/Documento_Software_2_DSU_Entrega.pdf) y su Word editable. Conserva carátulas y completa los trece puntos, con 239 figuras y 93 tablas. Consultar Informe_validacion_final.md y Matriz_revision_13_puntos.md de esa carpeta; hay guías de defensa, fuentes, EA implementado y evidencias. Modelo financiero vigente: cargas 17,21 %, VAN Bs 117027, TIR operativa 41,8 %, déficit Bs 164540, propuesta de capital Bs 200000. Los apuntes siguientes son históricos y pueden contener cifras o pendientes superados. No ejecutar ensamblar.py ni generador/build.py sobre el cierre manual. El usuario autorizó el push al repositorio privado el 19/11; se mantiene la publicación de servicios a cargo del titular.

> **Cierre local del 18/11/2026:** consultar `../auditoria_cierre/09_auditoria_final.md` y `04_bitacora_cambios.md`. Se corrigieron defectos de integridad, concurrencia y precisión ETL; regresión nueva en PostgreSQL aislado; documento integrado de 13 capítulos. La publicación queda a cargo del titular por instrucción explícita. No se hicieron commits, push ni escrituras en Neon. El contenido histórico siguiente conserva su fecha y puede describir pendientes ya resueltos localmente.

# Software 2 — avance y trazabilidad

> **18/11/2026 (noche): leer primero [CONTINUAR_SESION.md](CONTINUAR_SESION.md)** — despliegue real en Azure + Vercel, sitio corporativo Residata, pruebas, finanzas y la lista de lo que falta del documento (13 puntos, entrega jueves 19/11 08:00).


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

## Ampliación del 16/11/2026 (contraste con los ejemplos)

Documento con 38 tablas y 155 figuras. Añadido: 1.2.3 métricas orientadas al tamaño (10,42 KLDC medidos), 1.3.3 COCOMO II por puntos objeto (101 PO, 7,8 personas-mes), 1.4.1 presupuesto de referencia tomado de Taller cap. 10, 1.5.3 Gantt de Taller, 11.7 licencia, 11.8 términos y condiciones, 11.9 política de privacidad y manual por rol con 19 capturas (12.2). Corregido el cap. 11 según `backend/deploy` y `settings.py` (EC2, JWT 30 min/10 h en localStorage, respaldo diario con 14 días de retención) y la numeración duplicada 3.7. `ensamblar.py` admite `<!-- fig: ruta | título | fuente -->`. Respaldo previo en `versiones/2026-11-16_antes_paps_manual.docx`.

Faltan frente a los ejemplos: sitio web real con capturas (cap. 7 describe chatbot, simulador y mesa de ayuda que no existen), videos, códigos QR de repositorios, carátulas firmadas de propuesta y PAPS, y métricas de tres productos similares con capturas de sus interfaces. Los costos de AWS/Azure/GCP del cap. 11 siguen sin fuente; las cifras de productividad del cap. 4 se reemplazaron el 17/11.

## Segunda ampliación (16–17/11/2026)

Documento de 238 páginas, 50 tablas y 160 figuras, **solo hoja carta** (láminas densas en carta apaisada; no usar A3). PAPS reorganizado según el PAPS antiguo del usuario y el ejemplo Grupo 4: 1.2 métricas de Sensoneo, Ecube Labs, Bigbelly y DSU (puntos de función; KLDC de los comerciales estimados por analogía con la relación medida en DSU), 1.3 dimensiones, ámbito, valor esperado, COCOMO II y ecuación del software. SQAP renumerado 2.1–2.21 como el ejemplo. Cap. 7 aclara que el portal es una especificación y muestra capturas de la aplicación (7.5). Anexo F con QR de https://github.com/vangiewz/ProyectoDSU (repositorio aún privado).

Para actualizar el índice usar `actualizar_indice.ps1` (vista normal, segundos). `revisar.ps1` se queda horas en la exportación a PDF con este documento; el PDF no se regeneró ni se revisó visualmente tras estos cambios.

## Formato y entregables (17/11/2026)

Formato alineado con el ejemplo Grupo 4: borde doble, carátula por capítulo, tablas con encabezado celeste, sin numeración de tablas/figuras ni notas de fuente, sin menciones a Taller. 247 páginas, solo carta. `python ensamblar.py` genera el .docx, actualiza el índice y exporta el PDF mediante `publicar.ps1`, dejando ambos en `../Entregables/Software_2/` (aprox. 1 minuto). `Entregables/Taller_de_Grado_I/` contiene copia del Word y PDF de Taller. `revisar.ps1` queda obsoleto (se cuelga). Capturas de Sensoneo, Ecube Labs y Bigbelly descargadas de sus sitios en `recursos/web/`.

## Cierre del documento (17/11/2026)

254 páginas, sin bordes, redactado como documento terminado (sin "pendiente", "datos sintéticos" ni "borrador"). Carátula según la del grupo: Grupo #8, grupo SB, M. Sc. Ing. Rolando Antonio Martínez Canedo, con QR del repositorio y de la carpeta de Drive. Anexos: A–E registros y fichas, F códigos QR, G carátula firmada, H oficio recibido por la DSU (11/09/2026), I estándares de codificación (`estandares.md`, basado en `pyproject.toml`, `.oxlintrc.json` y `tsconfig`). Todo lo que usa el generador está dentro del repositorio (`recursos/`); dependencias en `requirements.txt` más Microsoft Word. `material.py` arma `Entregables/Material_Drive/` (documento, PAPS, SQAP y manual como PDF sueltos, capturas, diagramas, pruebas, respaldo) para subir a la carpeta compartida.

## Imágenes y correcciones (17/11/2026, madrugada)

269 páginas, 55 tablas, 183 figuras. Imágenes nuevas en `recursos/web/`, capturadas de sitios oficiales con Playwright el 17/11/2026 o descargadas de SENAPI: cap. 4 Docker, Power BI y OWASP ZAP; cap. 5 ficha del trámite 2 del SEPREC (Bs 455 + Bs 192), portal del SIN, pasos de búsqueda de signos (PI-112, Bs 75), flujos oficiales de signo distintivo y derecho de autor, registro virtual y tasas (programa de ordenador Bs 150 + Gaceta Bs 60, 5 días hábiles); cap. 6 GitHub, Neon y Vercel; cap. 8 gráfico de puntos de función (datos de 1.2); cap. 10 afiche de campaña (`recursos/afiche.html`, diseño del sistema DSU). Sparx Systems bloquea navegadores automáticos: no hay captura de precios de Enterprise Architect.

Cap. 4 corregido según el repositorio: Ruff, oxlint y tsc (no Flake8/Black/ESLint/Prettier), npm (no pnpm), sin Postman ni pytest-cov, y regresión de 98,8 s en Windows y 41,4 s en Linux (no "menos de 2 s"). La tabla 4.4 reemplaza los porcentajes de ahorro (45–85 %) por evidencia medida. Cap. 10: 45 puntos de recolección (no 23).

## SQAP contrastado con el Manual de Calidad (17/11/2026)

SQAP ampliado según `Manual de Calidad.docx` y la clase del 12/11/2026 (`clase.pdf`, fuera del repositorio): concepto de SQA, relación PAPS–SQAP–certificación y costos/beneficios (2.1), estándares de certificación ISO 9001/ISO 9000-3, IEEE 730 y CMMI (2.6), preguntas de V&V y su aplicación en PUDS (2.11). Del Manual: objetivos, lema, atributos de calidad, cuatro organizaciones y responsabilidades, tareas por fase y del grupo SQA, resumen de ERS y SDD, procesos de V&V y sus informes, documentación de usuario, estándares de codificación y comentarios, revisiones mínimas (SRR, PDR, CDR, SVVPR, auditorías), RTF y agenda por iteración, niveles de prueba, secciones nuevas 2.12 Gestión de configuración y 2.15 Control de código, estados de problemas, proveedores, retención de registros, capacitación y riesgos de calidad. Ampliación moderada a pedido del usuario (no las 60 páginas del ejemplo Grupo 4). `ensamblar.py` admite `<!-- anchos: a,b,c -->` antes de una tabla Markdown y da formato a Heading 4. Completado después: lema «Datos confiables, campus limpio», funciones nominales (Lobo Gutiérrez coordinador y responsable de configuración; Serrate Basma responsable de SQA; elección de Claude a pedido del usuario), agenda de revisiones con los periodos del Gantt y anexos A–C como formatos para llenar. Documento de 289 páginas; `03_SQAP.pdf` de 29. Respaldo previo en `versiones/2026-11-17_antes_sqap_manual.docx`.

## Pendientes reales

Confirmar docente y criterios finales de evaluación. Acordar disponibilidad, responsables, calendario y costos. Ampliar manual y producir videos. Completar inventario de licencias y condiciones de titularidad. Validar adopción con usuarios, precisión con datos institucionales, rendimiento y despliegue remoto; acreditar respaldo y restauración. Completar informe Power BI, RLS y publicación según el estado técnico. No presentar estos puntos como realizados.

## Revisión y preservación

Revisión visual por páginas de carátula, índice, cuerpo, tablas, figuras y anexos. Word actualizó campos e índice mediante COM (`revisar.ps1`). El script `verificar_modelos.py` auditó las 186 páginas del PDF resultante (`tmp/software2_diagramas/revision.pdf`): 0 campos rotos, 0 páginas vacías, 0 imágenes fuera de margen y correspondencia exacta de 132/132 hashes SHA256 contra las imágenes originales de Taller. Se generaron 16 láminas de contacto (`plancha-01.png` a `plancha-16.png`) en `tmp/software2_diagramas/` para inspección rápida en cuadrícula 3x4. Los PDF e imágenes en `tmp/` son intermediarios de auditoría, no entregables finales. La versión inicial de nueve páginas se conserva en `versiones/2026-11-16_inicial_9p.docx`.

No se modificaron Taller, su generador, código o base de datos. No se hicieron commits ni publicaciones. Las demás modificaciones del repositorio pertenecen a trabajo previo o paralelo del usuario.
