# Contraste con el material del docente

Revisión del 16/11/2026. Las láminas, las capturas y la transcripción original prevalecen sobre interpretaciones anteriores. Esta matriz distingue estructura documentada de validación operativa pendiente.

| Criterio | Fuente original | Aplicación y evidencia | Estado |
|---|---|---|---|
| Implementación vinculada al diseño y sus componentes | Cap. 8, pp. 3–8 | 8.1: arquitectura y diagrama general; correspondencia con los ocho paquetes del análisis | Integrado; revisión visual registrada por separado |
| Diagrama de componentes de cada subsistema con subtítulo | Cap. 8, p. 8 | Ocho apartados 8.2 y ocho diagramas EA; rutas reales comprobadas por `componentes.py` | Verificado estructuralmente |
| Seis grupos de herramientas realmente utilizadas | Cap. 8, p. 10 | 8.3.1–8.3.6; inventarios de desarrollo y de imagen Linux diferenciados | Verificado |
| Producción en despliegue; pruebas locales diferenciadas | Revisión del 26/10 y decisión del equipo | Vercel, AWS EC2 Linux/Docker São Paulo y Neon; modelo EA independiente y corrección puntual del capítulo 7 | Arquitectura definida; despliegue remoto pendiente |
| Objetivo y planificación de pruebas | Cap. 9, pp. 3–7 | 9.1 identifica alcance, entorno aislado, tipos de comprobación y límites de la evidencia sintética | Integrado |
| Plantilla de siete campos y explicación de cada uno | Cap. 9, p. 8 | 9.2.1 y 27 tablas; precondiciones comprensibles, entradas reales sanitizadas y expectativas concretas | Verificado estructuralmente |
| Caja negra en funciones importantes con los mismos campos | Cap. 9, p. 9 | Autenticación, permisos, jornada, registro, analítica, predicción y reportes; respuestas vinculadas a tests aprobados | 27 escenarios documentados de la suite de 42 pruebas |
| Caja blanca con código numerado, grafo, caminos y McCabe | Cap. 9, apartado 3.2 | CU15 y CU28: fuente y hash, nodos/aristas, trazas ejecutadas y rango racional de caminos factibles | Verificado; no se afirma cobertura del interior de bibliotecas |
| Vulnerabilidad con evidencia real | Cap. 9, apartado 3.3 | ZAP baseline pasivo autenticado en entorno aislado; reportes anteriores y posteriores, correcciones y residuales | Ejecutado con alcance limitado; no equivale a pentest completo |
| Referencia de Jacobson de 2000, capítulos 10 y 11 | Cap. 8 p. 3 y cap. 9 p. 3 | Año contrastado en página legal de la edición española y bibliografía unificada | Verificado |
| Introducción, tabla general, desgloses y montos en Bs. | Cap. 10, pp. 2–4 | 10.1.1: hardware, software, personal, infraestructura y logística/material/refrigerio; cálculos Decimal reproducibles | Integrado y comprobado aritméticamente |
| Personal respaldado y duración coherente con el cronograma | Cap. 10 p. 4 y clase 07:07–09:30 / 21:34–24:43 | Tabla histórica CITI Santa Cruz 2021 visible en el material; cuatro funciones, dedicaciones explícitas, cuatro meses y dos integrantes | Presupuesto de referencia; no cuatro contrataciones ni arancel certificado vigente |
| ROI a doce meses adaptado al proyecto y conclusión | Cap. 10, pp. 4–5 | 10.1.2 separa inversión, operación y beneficios hipotéticos, sin duplicación; resultado negativo y sensibilidad explicados | Proyección condicionada; línea base DSU pendiente |
| Riesgos y planes de respuesta | Cap. 10, estructura y clase | 10.2: riesgos técnicos, de gestión e institucionales; probabilidades declaradas como juicio de planificación | Integrado; no estadística institucional |
| Seguridad lógica y física: teoría citada y riesgos/soluciones | Cap. 10, pp. 6–7 | 10.3.1–10.3.2; NIST, responsabilidad compartida, controles actuales y medidas previstas diferenciados | Integrado; verificaciones productivas pendientes |

## Segunda revisión contra los ejemplos del docente (16/11/2026, tarde)

Contraste de la versión de 449 páginas con las láminas, la presentación de la materia y la tesis modelo de la Farmacia. Los ejemplos se adaptan a la arquitectura real; no se inventan capas, archivos ni servidores.

| ID | Hallazgo | Fuente | Corrección | Estado |
|---|---|---|---|---|
| H1 | Faltaban Resultados, Conclusiones, Recomendaciones y Anexos | Presentación de la materia p. 2 | `finales.py`: secciones finales en el orden oficial; Anexos tras las referencias | Integrado |
| H2 | Subsistemas 8.2 sin la estructura cliente/servidor/BD del ejemplo | Cap. 8 p. 9 | `ea_final.subsistema()`: nodos reales (Vercel, AWS EC2, Neon), capas por imports reales y tablas existentes en `esquema.json`, OLTP/OLAP | Integrado |
| H3 | Dependencia de 8.1 que no tocaba el paquete Logística | Cap. 8 p. 7 | Conectores anclados al cuerpo de cada paquete; CU dentro de paquetes no agregados (sugerencia opcional) | Integrado |
| H4 | Diagrama general de CU solo con identificadores y relaciones ilegibles | Clase 30/09, 39:09–40:31; cap. 5 p. 17 | `ea_general_cu.py`: nombres completos, include/extend rotulados a 13 pt, A3 apaisada (~8 pt impresos) | Integrado; 20 líneas aún cruzan elipses |
| H5 | Caja negra sin evidencia visual | Cap. 9 pp. 10–11 | `evidencia_cp.py`: 27 figuras con pantalla y resultado técnico de la misma acción, contrastadas con su oráculo | 27/27 conformes |
| H6 | Código de caja blanca sin marcas de nodo, con cortes dentro de identificadores; explicación 9/7 en jerga; etiquetas superpuestas | Cap. 9 pp. 12–19 | Marcas `(n)`, cortes sintácticos, texto simplificado conservando la comprobación de rango; grafos solo con «sí»/«no» | Integrado |
| H7 | Vulnerabilidad sin figuras | Cap. 9 pp. 20–22 | `zap_figuras.py`: consola antes/después y reportes HTML de ZAP | Integrado |
| H8 | Power BI con un solo gráfico y sin auditoría de medidas | V02 | Medidas contrastadas con SQL (`powerbi_medidas.json`); `powerbi/tablero.py` con los visuales del README | Pendiente: validación en Desktop, captura y publicación por el titular |
| H9 | Letra impresa de los diagramas EA de cap. 5–7 entre 3 y 5 pt | Revisión 26/10 | Medido por figura; corregido en las figuras nuevas (5.5, 8.1–8.2, 9.3.2) | Pendiente decisión: regenerar las figuras de los cap. 5–7 |

La numeración de seguridad del índice del PDF de costos contradice su cuerpo. Se sigue el cuerpo: lógica primero y física después. Los ejemplos comerciales de ventas de las láminas no se trasladan como ingresos reales de DSU. Los detalles de maquetación y los límites externos permanecen en `AUDITORIA.md`.
