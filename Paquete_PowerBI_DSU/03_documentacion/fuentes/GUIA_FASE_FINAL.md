# Guía auditada de la fase final de Taller

Actualizada el 16/11/2026. Proyecto DSU-UAGRM, Grupo 8. Esta guía organiza el trabajo; las fuentes originales del docente prevalecen sobre ella. La versión anterior mezclaba instrucciones con ejemplos técnicos y cifras sin verificar. Esos ejemplos no constituyen requisitos ni resultados del proyecto. Se conserva en `docs/auditoria-fase-final/GUIA_FASE_FINAL_antes_auditoria.md` únicamente como antecedente.

## Fuentes y autoridad

1. Instrucciones del docente: transcripciones de 06/11 y 11/11 en `clases/`, contrastadas con video/capturas cuando sean ambiguas.
2. Láminas originales de `cap8-10/`: implementación (11 páginas), pruebas (23 páginas), costos (7 páginas).
3. Capítulo 4 del DOCX vigente y decisiones expresas del equipo.
4. Notas de contexto y ejemplos ajenos como apoyo, nunca como prueba de actividades o requisitos de DSU.

La entrega exige documento completo, digital y físico, y defensa del software (p. 2 de implementación y pruebas). No inferir una fecha o tipo de empastado no confirmados.

## Arquitectura y preservación

- Producción: cliente en Vercel, API en AWS EC2 con Linux/Docker en São Paulo (`sa-east-1`), PostgreSQL en Neon, Power BI y OpenStreetMap. EC2 confirmado por el usuario el 16/11/2026.
- El despliegue del capítulo 7 representa producción, sin localhost ni Vite de desarrollo como servidores. PC y teléfono del usuario sí son clientes. El entorno local se declara en las pruebas efectivamente realizadas allí.
- Conservar cuatro actores, 34 CU y ocho paquetes de `generador/fase2/datos.py`. No usar identificadores anteriores.
- Preservar el vigente y comparar antes de regenerar. No ejecutar `generador/build.py` ni modificar la base histórica del 28/09.
- No ejecutar pruebas con escrituras, entrenamiento o escaneos activos en la demo compartida. Usar entorno aislado.

## Capítulo 8 — Implementación

Estructura de pp. 6–10: 8.1 Arquitectura del sistema; 8.2 Arquitectura del subsistema, con 8.2.1–8.2.8; 8.3 Herramientas, con seis subpuntos: lenguajes, librerías, frameworks, SGBD, lenguaje de modelado y protocolos.

Apertura sustentada en Jacobson, Booch y Rumbaugh (2000, cap. 10), referencia de p. 3. Si se cita literalmente el libro, comprobar edición y localizador; no atribuir una página no consultada.

- Un diagrama general y ocho de subsistemas en Enterprise Architect. Contrastar los ejemplos visuales de pp. 7 y 9: paquetes/componentes, software, estructuras OLTP/OLAP, cliente/servidor y JSON/HTTPS.
- Los ocho paquetes no equivalen a ocho apps Django: mostrar la correspondencia real y los módulos compartidos.
- OLTP y OLAP son estructuras lógicas diferenciadas en la base existente; no inventar otra BD física ni cubos.
- Modelar los servicios como módulos de funciones cuando así están implementados. Usar archivos y símbolos reales.
- Las versiones salen del entorno inspeccionado y los lockfiles, con fecha. Los rangos de requirements no son versiones exactas del servidor productivo.
- No afirmar TLS 1.3 exclusivo ni nombres de artefactos no verificados. Distinguir HTTPS, JSON, JWT y PostgreSQL/TLS.
- Sin código fuente en cap. 8 (clase 06/11, 17:25–17:34).

## Capítulo 9 — Pruebas

Estructura de p. 6: 9.1 Planificación; 9.2 Diseño; 9.2.1 Identificación y estructuración del procedimiento; 9.3 Pruebas realizadas; 9.3.1 Caja negra; 9.3.2 Caja blanca; 9.3.3 Vulnerabilidad.

Caja negra (pp. 8–9): exactamente siete campos: Nombre de caso de prueba; Descripción; Precondición; Entrada; Condición de ejecución; Resultado obtenido; Resultado esperado. El esperado se establece antes de ejecutar; el obtenido recoge respuestas reales. El veredicto se explica fuera de la plantilla o dentro del análisis, sin añadir campos.

Cubrir funciones críticas de los CU actuales: autenticación/RBAC, operación, logística, ETL, analítica/mapa, modelo/predicción, recomendaciones y reportes/bitácora, con escenarios correctos, inválidos y permisos/alcances. No inventar un mínimo numérico del docente.

Caja blanca (p. 12 y ejemplos pp. 13–19): CU, código enumerado, flujo numerado y tabla Camino/Entrada/Salida. Como técnica del proyecto se emplearán caminos básicos y McCabe sobre el grafo real: V(G)=E−N+2P. No copiar V(G)=5 de la guía previa. Funciones seleccionadas: `prediction.services.prediccion.generar` (CU28) y `operations.services.jornada.asignar` (CU15). Declarar límites de llamadas internas, comprensiones y excepciones; no afirmar cobertura completa sin ejecución.

Vulnerabilidad (p. 20): describir herramienta y mostrar pruebas. El proyecto elige OWASP ZAP; registrar la versión realmente utilizada. API bajo `/api/`, no `/api/v1/`. Registrar alcance, autenticación, límites, alertas, revisión, correcciones y nuevo escaneo. Los números de alertas de la guía previa eran ejemplos sin evidencia. JWT está en localStorage; no afirmar cookies HttpOnly o defensas no implementadas.

## Capítulo 10 — Costos, riesgos y seguridad

Conservar la jerarquía de las láminas al anteponer el capítulo:

- 10.1 Costos; 10.1.1 Estimación; 10.1.1.1–10.1.1.5 Hardware, Software, Personal, Infraestructura y Logística/material/refrigerio.
- 10.1.2 Retorno de la inversión; subapartados adaptados a las fuentes de beneficio justificadas para DSU.
- 10.2 Riesgos y plan de respuesta.
- 10.3 Seguridad; 10.3.1 Lógica; 10.3.2 Física. El índice de p. 1 invierte lógica/física; se sigue el desarrollo de pp. 6–7 y la clase.

Tabla general de costos antes de desgloses, todo en Bs. (p. 2). Documentar fuente, fecha, conversión y naturaleza del costo. Contrastar aranceles SIB y dedicación del equipo; cuatro funciones profesionales no demuestran cuatro integrantes. Evitar duplicar recursos existentes, inversión y operación recurrente.

ROI a doce meses con beneficio total, beneficio neto y ROI=(beneficio neto/inversión)×100. El docente permite adaptar los componentes de beneficio (p. 4 y clase 11/11, 36:00–40:15). Usuario eligió estimaciones sustentadas: declarar supuestos y no atribuir ventas, tarifas, ahorros o volúmenes no confirmados a la DSU. No copiar Bs. 101.500 ni ROI 24,14 % de la guía anterior. La conclusión debe interpretar el porcentaje calculado a doce meses como proyección, aunque sea negativo.

Riesgos: matriz con clasificación, descripción, probabilidad, impacto y respuesta; incluir técnicos, gestión e institucionales. Justificar probabilidades estimadas. Seguridad lógica y física: fundamento con cita y matriz riesgo/solución (pp. 6–7); diferenciar medidas implementadas, propuestas y del proveedor. No afirmar inspecciones de instalaciones no realizadas.

## Auditoría y entrega

Registrar fuente, evidencia, hallazgo, corrección y estado en `docs/auditoria-fase-final/`. Estados: verificado; corregido y verificado; pendiente; bloqueado por dependencia externa; no aplicable justificado.

Cada bloque pasa revisión de contenido, coherencia con código, ejecución cuando corresponda e inspección visual del documento renderizado. Revisar todas las páginas, índices, notas, referencias y secretos. No declarar final una versión con pruebas por ejecutar o dependencias abiertas. No hacer commits, publicaciones ni contrataciones sin solicitud expresa.
