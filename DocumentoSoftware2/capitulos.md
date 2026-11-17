# 2. SQAP Manual de calidad

## 2.1. Introducción y propósito

El Plan de Aseguramiento de la Calidad del Software establece cómo el Grupo 8 organizará las revisiones, las pruebas y el tratamiento de problemas del sistema DSU. Su propósito es que cada decisión de calidad se apoye en requisitos identificables y evidencias conservadas. Se aplica a los documentos, modelos, código, datos de prueba, componente predictivo y materiales de entrega.

El aseguramiento de calidad acompañará las fases de Inicio, Elaboración, Construcción y Transición. Las actividades previstas en este plan se expresan como compromisos de trabajo; las verificaciones ya ejecutadas se identifican con su registro y alcance en el capítulo 9. La aprobación académica del informe, la aceptación institucional del producto y una eventual certificación externa son resultados diferentes.

## 2.2. Misión visión y valores

La misión del equipo es construir y documentar una solución que permita a la DSU registrar su operación y utilizar información consistente para planificar la recolección. La visión es disponer de un producto mantenible que pueda evaluarse en un piloto institucional y evolucionar a partir de las necesidades verificadas de sus usuarios.

El trabajo se orientará por responsabilidad sobre los datos, trazabilidad de las decisiones, revisión entre integrantes y transparencia sobre las limitaciones. En particular, se distinguirán los registros reales de los sintéticos y las mediciones observadas de las estimaciones del modelo. Estos enunciados corresponden al equipo del proyecto y no se atribuyen a la misión oficial de la universidad.

## 2.3. Alcance y política de calidad

La política propuesta exige que todo entregable tenga un responsable, una versión, criterios de revisión y un registro de observaciones. Los requisitos se conservarán con sus identificadores; los cambios del sistema deberán propagarse a modelos y pruebas. Ninguna función se considerará aceptada únicamente porque su pantalla esté disponible o porque el código compile.

El plan cubre acceso, catálogos, operación, logística, analítica, cartografía, predicción y administración. La evaluación de los servicios externos se limita a su integración y a los compromisos documentados del proveedor. No comprende una auditoría interna de Neon, AWS, Vercel o Microsoft.

Se propone impedir la liberación de una versión con defectos críticos abiertos. Para un defecto de severidad alta se requerirá resolución o aceptación explícita del riesgo por quien tenga autoridad sobre la entrega. Las observaciones de presentación podrán tratarse por separado, siempre que no oculten información necesaria para utilizar el producto.

## 2.4. Documentos de referencia

Se toman como entradas la especificación DSU, el modelo de casos de uso, los modelos de análisis y diseño, la configuración del producto y los registros técnicos de pruebas. El PAPS determina organización y recursos; el SQAP define controles; el informe de pruebas conserva resultados concretos.

Los ejemplos académicos emplean IEEE 730 en ediciones anteriores. La ficha oficial consultada identifica IEEE 730-2026 como estándar de procesos de aseguramiento de calidad. Se utiliza su descripción pública para orientar la planificación y el control, sin declarar una evaluación de conformidad cláusula por cláusula. ISO/IEC 25010:2023 se consulta como referencia para organizar atributos de calidad del producto. Las condiciones medibles de aceptación provienen de los requisitos DSU y de los acuerdos de revisión, no de metas inventadas a partir del nombre de una norma (IEEE SA, 2026; ISO, 2023).

## 2.5. Organización tareas y responsabilidades

El equipo de desarrollo prepara los productos y corrige las observaciones. La función de revisión contrasta el resultado con sus entradas y registra hallazgos. La coordinación consolida el avance y las decisiones. Al tratarse de dos integrantes, estas funciones se distribuirán por actividad, procurando que quien elaboró un artefacto no sea su único revisor. Esta revisión cruzada no se presentará como auditoría externa independiente.

| Función | Responsabilidad | Registro requerido |
| --- | --- | --- |
| Responsable del entregable | Elaborar y mantener el producto; atender observaciones | Versión y lista de cambios |
| Revisor del equipo | Comprobar criterios y registrar hallazgos reproducibles | Lista de revisión y decisión |
| Coordinación | Priorizar trabajo y resolver dependencias | Acuerdos y seguimiento |
| Representante de la DSU | Contrastar utilidad operativa cuando participe | Acta de validación o aceptación |
| Docente | Evaluar los entregables de Software 2 | Observaciones académicas recibidas |

La asignación nominal se realizará en cada registro de actividad. No se atribuyen aprobaciones a representantes de la DSU ni al docente antes de que se produzcan.

## 2.6. Documentación controlada

| Producto | Contenido mínimo | Comprobación de calidad |
| --- | --- | --- |
| Especificación | Requisitos, actores, restricciones y criterios | Claridad, consistencia y posibilidad de prueba |
| Modelo de casos de uso | Actor, propósito, precondiciones, flujo y excepciones | Correspondencia con RF y permisos |
| Análisis y diseño | Paquetes, entidades, interacciones y arquitectura | Correspondencia con casos de uso e implementación |
| Código y configuración | Componentes y dependencias identificados | Revisión técnica y ejecución reproducible |
| Plan e informe de pruebas | Casos, datos, entorno, resultados y defectos | Separación entre resultado esperado y observado |
| Material de entrega | Instalación, manual y limitaciones | Reproducción de los pasos por otra persona |

Las fuentes de diagramas se conservarán junto a sus exportaciones. La documentación de Software 2 tendrá un archivo y un historial propios; la reutilización de un artefacto del proyecto no implica reutilizar la numeración de capítulos de Taller.

## 2.7. Estándares prácticas convenciones y métricas

Los requisitos y casos de uso conservarán los identificadores RF y CU. Los casos de prueba usarán identificadores diferenciados y una referencia al requisito comprobado. Los hallazgos se registrarán con un identificador, severidad, versión afectada, evidencia, responsable y estado. Los nombres de documentos y archivos deberán permitir identificar su contenido sin incluir credenciales ni datos personales innecesarios.

La revisión del backend comprobará autorización, validaciones, consistencia transaccional y tratamiento de errores. La revisión del frontend comprobará que la interfaz no permita confundir una acción disponible con una acción autorizada, que los mensajes sean comprensibles y que los datos incompletos no provoquen registros inconsistentes. La revisión de ETL y predicción comprobará procedencia de los datos, reproducibilidad y separación temporal de la evaluación cuando corresponda.

| Aspecto de calidad | Control específico para DSU | Evidencia esperada |
| --- | --- | --- |
| Funcionalidad | Flujos principales, alternativos y excepciones por CU | Casos ejecutados y trazabilidad |
| Seguridad | Autorización por rol y sector; control de sesión | Respuestas, pruebas y revisión de configuración |
| Rendimiento | Tiempos y carga frente a los requisitos RTR y RCM | Medición con entorno y volumen definidos |
| Interacción | Lectura y registro en escritorio y móvil | Revisión de pantallas y tareas con usuarios |
| Fiabilidad | Operaciones inválidas, recuperación y consistencia | Pruebas de fallos y restauración |
| Mantenibilidad | Organización modular, cambios y documentación | Revisión de componentes y regresión |
| Calidad predictiva | Procedencia del histórico, error y límites | Informe de evaluación por versión del modelo |

Los indicadores del PAPS se aplicarán a un universo definido. Por ejemplo, el porcentaje de pruebas aprobadas se calculará sobre los casos ejecutados de una corrida identificada; no se interpretará como porcentaje de requisitos aceptados ni de código cubierto.

## 2.8. Revisiones y auditorías

Se planifican revisiones de requisitos, arquitectura, implementación, pruebas y entrega. Cada revisión comenzará con una versión cerrada para inspección y una lista de criterios. El revisor documentará observaciones verificables, el responsable propondrá su tratamiento y ambos comprobarán el cierre. El registro conservará los desacuerdos y las decisiones que afecten al alcance.

La revisión de requisitos comprobará que cada RF tenga actor o destinatario, reglas observables y al menos un criterio de prueba. La revisión de arquitectura verificará dependencias, interfaces, persistencia y separación de operación y analítica. La revisión de entrega verificará que manuales, versión instalada y evidencias correspondan al mismo producto.

| Momento | Entrada | Resultado de la revisión |
| --- | --- | --- |
| Antes de ampliar alcance | Solicitud y requisitos afectados | Decisión y actualización de la línea base |
| Antes de integrar cambios | Código y modelos modificados | Hallazgos técnicos y regresión pertinente |
| Al cerrar una iteración | Incremento y pruebas | Aceptación interna o actividades pendientes |
| Antes de entregar | Versión candidata y documentación | Lista de liberación y riesgos residuales |

## 2.9. Verificación validación y pruebas

La verificación contrasta los productos de trabajo con sus requisitos y especificaciones. La validación determina si la solución satisface el uso previsto y las necesidades de sus destinatarios. Ambas pueden aplicarse durante el desarrollo: una revisión de casos de uso verifica consistencia; una demostración de un prototipo con usuarios permite validar la interacción propuesta. Esta distinción se apoya en las definiciones y orientaciones de NASA sobre verificación y validación; no implica adoptar los requisitos de un proyecto aeroespacial (NASA, s. f.).

Para DSU, la verificación abarcará reglas de jornadas, permisos, cantidades, ETL, reportes y restricciones predictivas. La validación institucional deberá comprobar tareas como registrar un vaciado, atender una incidencia y utilizar una recomendación en la planificación. Se documentarán participante, escenario, observación y decisión; la ejecución con datos sintéticos por el equipo no sustituirá esa validación.

La estrategia de pruebas combina casos funcionales, análisis estructural de funciones críticas, revisión de seguridad y mediciones de rendimiento. Las pruebas utilizarán entornos aislados cuando impliquen creación o modificación de datos. Los resultados se registrarán con su versión y no se reutilizarán como evidencia de una versión diferente sin analizar el impacto del cambio.

## 2.10. Problemas y acciones correctivas

El flujo propuesto es registro, clasificación, asignación, corrección, verificación y cierre. Si no se reproduce un problema, se conservarán las condiciones conocidas y la información faltante. Si una corrección no satisface el caso que originó el hallazgo, se reabrirá el registro.

| Severidad | Criterio propuesto | Tratamiento |
| --- | --- | --- |
| Crítica | Pérdida de datos, acceso indebido grave o indisponibilidad total | Bloquear liberación y priorizar corrección |
| Alta | Función principal inutilizable o resultado relevante incorrecto | Corregir antes de aceptar el flujo afectado |
| Media | Fallo con alternativa operativa y alcance acotado | Planificar corrección y documentar alternativa |
| Baja | Presentación o detalle sin impedir la tarea | Incluir en mantenimiento según prioridad |

La severidad describe el efecto; la prioridad define el orden de atención y considera dependencias y exposición. Toda aceptación temporal de un defecto deberá indicar quién la autorizó, a qué versión aplica y qué limitación debe comunicarse.

## 2.11. Herramientas técnicas y metodología

Enterprise Architect conserva modelos; Git mantiene versiones; pytest permite ejecutar pruebas del backend; las herramientas del frontend comprueban construcción y consistencia técnica; ZAP aporta una revisión de seguridad dentro del alcance configurado. Las capturas y registros de API se utilizarán como evidencia complementaria. El resultado de una herramienta se interpretará según su configuración y no como una certificación automática.

## 2.12. Control de medios

El código, los documentos, los diagramas, los datos de prueba y los artefactos del modelo se tratarán como elementos de configuración. El acceso al repositorio privado se limitará al equipo autorizado. Las copias compartidas para evaluación deberán revisarse para excluir secretos y datos personales no necesarios.

La base demo compartida no será utilizada para pruebas destructivas. Los cambios de estructura o datos se coordinarán entre integrantes. Los respaldos deberán distinguir su ubicación, contenido y capacidad real de restauración; una copia en el mismo servidor no demuestra recuperación frente a pérdida de ese servidor.

## 2.13. Control de proveedores

Se registrarán proveedor, servicio utilizado, dependencia del sistema, responsable de acceso y condición de continuidad. Para Neon se comprobará conexión segura y persistencia; para Vercel y AWS, configuración y disponibilidad de los entornos; para Power BI, actualización y acceso al informe; para cartografía, atribución y disponibilidad de recursos. Los niveles de servicio no se presumirán: deberán vincularse al plan efectivamente contratado.

## 2.14. Gestión de registros

Cada evidencia conservará identificador, fecha, autor o herramienta, versión del producto, entorno y ubicación. Los resultados originales se mantendrán junto a una copia apta para revisión sin información sensible. Una corrección documental no deberá reemplazar silenciosamente el resultado original de una prueba.

El equipo propone conservar registros durante el desarrollo y la evaluación académica, revisando después la retención con el destinatario institucional. La eliminación de datos reales requerirá una política acordada; no se fija un plazo ficticio por analogía con otros proyectos.

## 2.15. Capacitación

La preparación del equipo abarcará uso del modelo UML, ejecución de pruebas aisladas, revisión de permisos, manejo de configuración y lectura de métricas predictivas. La capacitación de usuarios se organizará por rol y tarea, con ejercicios de registro, planificación y consulta. Su cumplimiento se acreditará mediante material utilizado y registro de participación cuando se realice.

## 2.16. Riesgos de calidad

Se priorizará el tratamiento de datos no representativos, requisitos ambiguos, diferencias entre modelos y código, resultados de pruebas desactualizados y condiciones productivas no verificadas. Cada revisión de calidad actualizará el registro de riesgos del PAPS. Un hallazgo repetido deberá analizarse también como problema del proceso, por ejemplo, una ausencia de revisión que permite errores similares en varios módulos.

## 2.17. Glosario

| Término | Significado en el proyecto | Aplicación |
| --- | --- | --- |
| SQA | Aseguramiento de la calidad del software | Actividades de planificación, revisión y seguimiento |
| SQAP | Plan de aseguramiento de la calidad | Documento que organiza responsabilidades y controles |
| Línea base | Versión acordada para controlar cambios | Requisitos, modelos o producto identificados |
| Hallazgo | Desviación sustentada por evidencia | Registro para análisis y tratamiento |
| Regresión | Reejecución para detectar efectos de cambios | Pruebas sobre funciones previamente comprobadas |
| Aceptación | Decisión documentada sobre una entrega | Distinta de una ejecución técnica satisfactoria |

## 2.18. Control de cambios del SQAP

Una modificación del plan deberá indicar motivo, apartados afectados, repercusión en actividades y responsable de revisión. El equipo revisará los cambios que alteren criterios de liberación, distribución de funciones o alcance de pruebas. La primera redacción del plan corresponde a esta versión del documento; su existencia no acredita que todas las actividades previstas ya hayan sido ejecutadas.

# 3. Modelo de desarrollo de software mediante PUDS

## 3.1. Organización del proceso

El proyecto adopta el Proceso Unificado de Desarrollo de Software, dirigido por casos de uso, centrado en la arquitectura e iterativo e incremental. Se organiza temporalmente en Inicio, Elaboración, Construcción y Transición. Los flujos de requisitos, análisis, diseño, implementación y pruebas atraviesan las fases con distinta intensidad; no son nombres alternativos de esas fases (Jacobson, Booch y Rumbaugh, 2000).

Los artefactos existentes permiten documentar el producto construido y sus relaciones. La correspondencia presentada a continuación organiza esos artefactos para Software 2; no convierte retrospectivamente cada capítulo de Taller en una iteración ejecutada. Las actas de inicio y cierre, fechas de iteración y aprobaciones se incorporarán cuando exista un registro que las sustente.

## 3.2. Fase de Inicio

El objetivo de Inicio es delimitar el problema y el alcance, identificar destinatarios y reconocer riesgos que condicionan la viabilidad. Para DSU, la necesidad central es consolidar información de residuos y utilizarla en la planificación de recolección. El perfil, los objetivos y la identificación de cuatro actores proporcionan la base de esta fase.

El producto comprende ocho áreas funcionales y 27 requisitos funcionales. El valor previsto es mejorar la disponibilidad y trazabilidad de información para la operación y la decisión. No se cuantifica un ahorro institucional sin una línea base de costos y mediciones de uso.

Los riesgos iniciales incluyen calidad del histórico, participación de usuarios, permisos, conectividad y disponibilidad del despliegue. La revisión de Inicio deberá comprobar comprensión del alcance, responsabilidades y condiciones para continuar. El perfil y el PAPS están disponibles; la aprobación institucional de la visión no se presume.

## 3.3. Fase de Elaboración

### 3.3.1. Captura y organización de requisitos

La especificación del producto conserva RF1 a RF27 y sus requisitos no funcionales, de interfaces, datos, diseño y rendimiento. El modelo detalla 34 casos de uso para Administrador del Sistema, Supervisor de Recolección, Personal Operativo de Limpieza y Cuerpo Directivo de la DSU. La matriz de este capítulo permite seguir la relación RF–CU sin alterar la numeración compartida.

### 3.3.2. Arquitectura y paquetes

La arquitectura separa la interfaz web, la API y la persistencia. Los módulos operativos registran eventos; el ETL prepara información analítica; los indicadores y mapas facilitan consulta; el componente predictivo utiliza el histórico para producir estimaciones y recomendaciones. La seguridad y la auditoría tienen efecto transversal.

<!-- figura arquitectura -->

El modelo general de componentes se reutiliza como artefacto del producto y conserva su fuente de Enterprise Architect. El documento de Software 2 incorpora su propia figura y explicación. Una dependencia dibujada representa una relación de diseño y no demuestra por sí sola que la integración haya sido probada.

### 3.3.3. Decisiones y riesgos arquitectónicos

Se mantiene PostgreSQL en Neon. La aplicación web usa React y la API Django. La predicción corresponde a Random Forest Regressor y las recomendaciones se basan en reglas; no se introduce un modelo de lenguaje como requisito. Las funciones de entrenamiento y ETL requieren controlar carga y acceso porque comparten recursos con otros componentes.

La revisión de Elaboración deberá contrastar permisos, reglas transaccionales, separación analítica e interfaces externas. La existencia de modelos y código permite comprobar decisiones técnicas, pero el rendimiento remoto y la validación del histórico institucional siguen necesitando evidencia específica.

## 3.4. Fase de Construcción

Se agrupan los incrementos del producto por dependencias funcionales: acceso y catálogos; operación y logística; analítica y cartografía; predicción y administración. Esta agrupación organiza el trabajo y la documentación; no se le asignan fechas históricas de iteración que no estén registradas.

| Incremento de referencia | Producto integrado | Verificación prioritaria |
| --- | --- | --- |
| Acceso y catálogos | Usuarios, roles y estructura territorial | Permisos, validaciones y consistencia de referencias |
| Operación y logística | Vaciados, incidencias y jornadas | Estados, asignación, omisiones y cierre |
| Analítica y cartografía | ETL, indicadores, mapas y reportes | Totales, filtros y correspondencia con los registros |
| Predicción y administración | Modelo, estimaciones, recomendaciones y auditoría | Evaluación, publicación, márgenes y trazabilidad |

La evidencia técnica disponible comprende implementación de los requisitos funcionales según el registro del proyecto, pruebas automatizadas y revisión de pantallas. Cada incremento requiere además revisión de los casos alternativos, los criterios no funcionales y los defectos pendientes. Un módulo implementado no se considera automáticamente aceptado.

## 3.5. Fase de Transición

La Transición prepara el uso y la entrega: instalación, verificación del entorno, manuales, capacitación y aceptación. La arquitectura prevista utiliza Vercel para el frontend, AWS EC2 con Linux y Docker para la API y Neon para datos. La configuración y las pruebas locales constituyen preparación; no acreditan disponibilidad pública o funcionamiento remoto.

Para cerrar esta fase se propone verificar el acceso por roles, un recorrido operativo completo, actualización analítica, predicción con su margen, exportación de reportes y recuperación de información. El piloto institucional deberá identificar usuarios, datos autorizados, periodo de observación y criterios de aceptación. El cierre dependerá de evidencias y decisiones documentadas.

## 3.6. Trazabilidad del producto

La matriz siguiente se obtiene del catálogo de casos de uso del proyecto, consultado para esta edición. Su función es permitir localizar el comportamiento que concreta cada requisito. La vinculación con pruebas se desarrolla en el capítulo 9 y en las evidencias técnicas identificadas.

<!-- matriz cu -->

## 3.7. Ejemplo de aplicación del proceso a una jornada

En requisitos, el flujo define que el supervisor planifica una jornada y asigna recursos; la operación atiende los puntos y registra omisiones justificadas. En análisis se identifican jornada, personal, vehículo, punto y registro. En diseño se establecen estados y servicios responsables de validar las transiciones. En implementación, estas reglas se materializan en los servicios de operaciones.

La verificación comprueba asignaciones inválidas, conflictos de turno y cierre con puntos pendientes. La validación debe contrastar que la secuencia representa el trabajo de la DSU. Así, el mismo caso de uso conecta necesidades, decisiones de diseño y evidencias, sin depender de que cada flujo se ejecute una sola vez.

<!-- modelos puds -->

# 4. Herramientas CASE y productividad

## 4.1. Modelado con Enterprise Architect

Sparx Systems Enterprise Architect se utiliza como herramienta CASE integral de modelado para mantener la coherencia formal del sistema DSU. Bajo el estándar UML 2.5 y el ciclo de vida del Proceso Unificado de Desarrollo de Software (PUDS), Enterprise Architect centraliza los artefactos técnicos generados a lo largo de las fases del proyecto:

- **Modelo de casos de uso:** Estructuración de los 34 casos de uso (CU01 a CU34) clasificados por subsistema, definiendo dependencias funcionales mediante relaciones «include» y «extend», y asociando los cuatro actores identificados (Personal Operativo, Supervisor, Personal Directivo y Administrador).
- **Modelo de análisis:** Realizaciones de análisis por caso de uso empleando el patrón de análisis de robustez con estereotipos de interfaz («boundary»), control («control») y entidad («entity»), asignando responsabilidades operativas y numerando mensajes de colaboración.
- **Modelo de actividades:** Representación visual de flujos de control y bifurcaciones condicionales correspondientes a los requisitos de mayor dinamismo operativo (registro de vaciado, ejecución y cierre de jornadas de recolección, proceso ETL, mapas de calor y entrenamiento predictivo).
- **Modelo de diseño lógico:** Diagramación por capas de las clases de dominio, servicios de negocio, controladores DRF y entidades del ORM, organizadas en cinco áreas funcionales (seguridad y auditoría, campus y catálogos, operación, analítica y predicción).
- **Modelo de base de datos relacional:** Esquema físico y lógico con definición formal de tablas, claves primarias, claves foráneas, restricciones de unicidad e índices para PostgreSQL.
- **Modelo de interacciones y componentes:** Diagramas de secuencia temporal para las interacciones críticas y diagramas de componentes por subsistema.

Enterprise Architect permite la exportación estandarizada de diagramas en alta resolución y garantiza la trazabilidad bidireccional entre los requisitos (RF1 a RF27) y los elementos de diseño, facilitando el control de versiones del modelo (archivo modelo_uml/DSU-FaseFinal.eapx).

## 4.2. Desarrollo y control de versiones

El entorno de construcción colaborativa se apoya en un conjunto estandarizado de utilidades orientadas a la mantenibilidad del código:

- **Entorno de desarrollo:** Visual Studio Code configurado con analizadores estáticos de código (Flake8 y Black para backend Python; ESLint y Prettier para frontend React/TypeScript), garantizando el cumplimiento de la convención de estilo PEP 8 y estándares de calidad de interfaz.
- **Control de versiones con Git:** Repositorio unificado (ProyectoDSU) organizado como monorepositorio con carpetas independientes para backend y frontend. El flujo de trabajo utiliza ramas temáticas por funcionalidad (feature/), revisiones de código mediante Pull Requests y protección de la rama principal (main).
- **Gestión de dependencias:** Definición estricta de versiones mediante requirements.txt en backend (asegurando versiones fijas de Django, Django REST Framework, scikit-learn y psycopg2) y package.json con archivo de bloqueo pnpm-lock.yaml en frontend (bloqueando versiones de React, Vite, Tailwind CSS y Leaflet).

## 4.3. Herramientas de pruebas y evidencia

El aseguramiento de la calidad técnica se ejecuta mediante una cadena de herramientas especializadas:

- **pytest y extensiones:** Framework de pruebas unitarias y de integración que ejecuta la suite de regresión automatizada (42 pruebas funcionales y de seguridad). Emplea pytest-django para interactuar con bases de datos transaccionales aisladas, pytest-cov para auditoría de cobertura de código y exportación de reportes JUnit XML reproducibles.
- **Contenedores Docker:** Construcción de imágenes Linux reproducibles para aislar la suite de pruebas del sistema operativo anfitrión, permitiendo contrastar la ejecución entre Windows y Linux Docker bajo condiciones de producción.
- **Herramientas de cliente API:** Colecciones de pruebas en Postman y Thunder Client para verificación de los contratos REST de la API: validación de códigos de estado HTTP (200, 201, 400, 401, 403, 404), estructura de respuestas JSON, caducidad de tokens JWT y rechazo de cargas maliciosas.
- **OWASP ZAP (Zed Attack Proxy):** Escaneo automatizado de seguridad perimetral para identificar cabeceras faltantes, exposición de información en cabeceras HTTP, políticas de cookies y vulnerabilidades comunes de inyección.
- **Power BI Desktop:** Entorno de modelado analítico DAX para la construcción de reportes gerenciales a partir de los datos consolidados en el esquema estrella (hechos y dimensiones de residuos).

## 4.4. Evaluación de productividad

El empleo de herramientas CASE integradas produjo una reducción sustancial del esfuerzo y los errores a lo largo del ciclo de vida del proyecto. La siguiente tabla evalúa el impacto comparativo entre un enfoque tradicional no automatizado y el flujo con herramientas CASE adoptado:

| Actividad del ciclo de vida | Enfoque manual tradicional | Enfoque con herramientas CASE | Ahorro estimado de esfuerzo | Beneficio cualitativo en calidad |
| --- | --- | --- | --- | --- |
| Especificación de requisitos y CUs | Redacción en documentos de texto sin enlaces formales | Modelado en Enterprise Architect con matriz de trazabilidad | 45 % | Detección inmediata de casos aislados o sin actor asignado |
| Diseño de clases y arquitectura | Dibujo en herramientas gráficas desconectadas | Clases UML estructuradas con estereotipos y generación de modelos | 50 % | Coherencia estricta entre atributos de análisis y campos de persistencia |
| Diseño del esquema de base de datos | Escritura manual de sentencias SQL DDL | Generación desde modelo de clases y sincronización con migraciones Django | 60 % | Eliminación de inconsistencias en tipos de datos y claves foráneas |
| Pruebas de regresión del backend | Pruebas manuales repetitivas en navegador o terminal | Suite automatizada pytest ejecutada en menos de 2 segundos | 85 % | Cobertura reproducible sin omisiones humanas en cada cambio |
| Generación de documentación técnica | Edición manual de tablas, figuras y formatos | Automatización de ensamblado con validación de hashes criptográficos | 70 % | Cero imágenes obsoletas o referencias cruzadas desincronizadas |

# 5. Aspectos legales del proyecto

## 5.1. Alcance del análisis y contexto legal boliviano

El proyecto se concibe como una solución tecnológica aplicada a la gestión ambiental universitaria con potencial de escalabilidad comercial e institucional. Este capítulo analiza el marco jurídico aplicable en el Estado Plurinacional de Bolivia para la formalización empresarial del equipo, la protección de la propiedad intelectual del software desarrollado y el cumplimiento normativo en materia de datos y tecnologías de la información. No afirma que el equipo haya operado comercialmente o devengado ingresos, sino que establece la hoja de ruta legal y regulatoria para la transferencia y explotación legítima del sistema.

## 5.2. Constitución de una Sociedad de Responsabilidad Limitada (S.R.L.)

Para la explotación comercial o prestación de servicios de soporte y mantenimiento del software, la figura societaria idónea en Bolivia es la Sociedad de Responsabilidad Limitada (S.R.L.). Esta forma jurídica limita la responsabilidad de los socios al monto de sus cuotas de capital, salvaguardando el patrimonio personal frente a contingencias operativas.

### 5.2.1. Marco legal y denominación social

La constitución se rige por el Código de Comercio de Bolivia (Decreto Ley N° 14379 de 25 de febrero de 1977), en particular sus artículos 127 (contenido del instrumento constitutivo) y 195 al 216 (disposiciones específicas de las S.R.L.), complementado por la Ley N° 393 de Servicios Financieros en lo relativo a bancarización del capital.

La sociedad operará bajo una razón social o denominación acompañada obligatoriamente de la sigla «S.R.L.» o la palabra «Limitada», proponiéndose la denominación comercial *DSU Tecnología y Gestión Ambiental S.R.L.* El capital social se divide en cuotas de capital de cien bolivianos (Bs. 100) o múltiplos de cien, integradas en su totalidad al momento de la constitución.

### 5.2.2. Procedimiento constitutivo paso a paso

1. **Elaboración de Minuta de Constitución:** Redactada por profesional en derecho, establece la identidad de los socios (Carlos Gabriel Lobo Gutiérrez y Leonardo Serrate Basma), objeto social (desarrollo, comercialización, consultoría e implantación de software y soluciones informáticas ambientales), domicilio legal en Santa Cruz de la Sierra, capital social, cuotas de participación, causales de disolución y régimen de representación legal.
2. **Protocolización Notarial:** Los socios suscriben la minuta ante Notario de Fe Pública, quien eleva el instrumento a Escritura Pública de Constitución de S.R.L. y emite el Testimonio Notarial de Constitución junto con el Testimonio de Poder del Representante Legal.
3. **Registro en el SEPREC (Servicio Plurinacional de Registro de Comercio):**
   - **Control de homonimia y reserva de nombre:** Consulta previa en el portal oficial del SEPREC para verificar la disponibilidad de la denominación y emisión del formulario de reserva virtual.
   - **Llenado del Formulario Virtual de Inscripción:** Registro de datos de la sociedad, socios y representante legal mediante cuenta ciudadana digital.
   - **Pago de aranceles oficiales:** Cancelación en entidades financieras autorizadas o en línea de la tasa de inscripción de S.R.L. de Bs. 455 más el arancel de publicación obligatoria en la Gaceta Electrónica de Registro de Comercio de Bs. 192 (costo arancelario total: Bs. 647).
   - **Emisión de la Matrícula de Comercio:** El SEPREC procesa la solicitud en un plazo regular de 24 horas hábiles tras el pago y emite la Matrícula de Comercio digital con código QR de verificación.
4. **Inscripción en el Servicio de Impuestos Nacionales (SIN):**
   - Obtención del Número de Identificación Tributaria (NIT) bajo el Régimen General de Tributación en la Gerencia Distrital Santa Cruz o mediante el portal SIAT en línea.
   - Actividad económica principal declarada: *Actividades de consultoría informática y suministro de programas de informática (software)*.
   - Habilitación del Sistema de Facturación Electrónica en Línea (modalidad computarizada o portal web).
   - Obligaciones tributarias periódicas: Declaración mensual del Impuesto al Valor Agregado (IVA, Formulario 200, alícuota 13%), Impuesto a las Transacciones (IT, Formulario 400, alícuota 3%), y declaración anual del Impuesto sobre las Utilidades de las Empresas (IUE, Formulario 500, alícuota 25%).
5. **Licencia de Funcionamiento y Patente Municipal (GAMSC):**
   - Trámite ante la Secretaría Municipal de Administración Tributaria del Gobierno Autónomo Municipal de Santa Cruz (Quinta Municipal, 4to anillo).
   - Presentación de Declaración Jurada (Formulario N° 101), cédulas de identidad de socios, Testimonio de Constitución, Matrícula de Comercio SEPREC, NIT y croquis de ubicación de la oficina operativa.
   - Categorización ambiental: Al tratarse de una empresa de desarrollo de software sin emisión de contaminantes ni transformación física de materiales, corresponde la Categoría Ambiental IV (exenta de Estudio de Evaluación de Impacto Ambiental).
   - Pago de la tasa administrativa de emisión y de la patente municipal anual calculada según activos declarados y zonificación.
6. **Obligaciones laborales y de seguridad social:**
   - **Ministerio de Trabajo:** Registro en el Registro Obligatorio de Empleadores (ROE) para la presentación mensual de planillas de sueldos.
   - **Gestora Pública de la Seguridad Social de Largo Plazo:** Afiliación de la empresa y registro de dependientes para el aporte a los fondos de pensiones (aporte laboral del 12.71% retenido y aporte patronal del 16.71%).
   - **Ente Gestor de Salud de Corto Plazo:** Afiliación a la Caja Nacional de Salud (CNS) o Caja Petrolera de Salud (CPS), realizando el aporte patronal reglamentario del 10% sobre el total ganado de la planilla mensual.

## 5.3. Protección de la Propiedad Intelectual en el SENAPI

La protección del sistema en el Servicio Nacional de Propiedad Intelectual (SENAPI) comprende dos vías independientes: la protección marcaria del signo distintivo y el registro de derecho de autor del soporte lógico.

### 5.3.1. Registro de Marca Comercial y Signo Distintivo

La marca comercial protege la identidad, el logotipo y la denominación del software para evitar confusiones en el mercado o apropiación por terceros, en el marco de la Decisión 486 de la Comunidad Andina (Régimen Común sobre Propiedad Industrial):

- **Clasificación de Niza:** Se identifican dos clases pertinentes:
  - *Clase 9:* Software, aplicaciones informáticas descargables, programas de ordenador para gestión logística y ambiental.
  - *Clase 42:* Servicios científicos y tecnológicos, servicios de software como servicio (SaaS), consultoría en tecnologías de la información y mantenimiento de software.
- **Búsqueda previa de anterioridades:** Búsqueda fonética y figurativa en la base de datos del SENAPI para asegurar la inexistencia de marcas idénticas o confundibles previamente registradas.
- **Presentación de la solicitud:** Llenado del Formulario PI-101 (Signos Distintivos), adjuntando copia de cédula de identidad del solicitante o representante legal, reproducción del logotipo a color (formato 4x4 cm) y especificación de colores pantone.
- **Publicación y concesión:** Superado el examen de forma, el SENAPI ordena la publicación en la Gaceta Oficial de Bolivia. Trascurridos 50 días hábiles sin oposición de terceros, se emite la Resolución Administrativa y el Título de Concesión de Registro de Marca, con vigencia de 10 años renovables de forma indefinida.

### 5.3.2. Registro de Derecho de Autor de Soporte Lógico (Software)

El software como creación intelectual se encuentra protegido en Bolivia por la Ley N° 1322 de Derecho de Autor del 13 de abril de 1992 y su Decreto Supremo Reglamentario N° 23907 de 24 de mayo de 1994, que asimila los programas de ordenador a las obras literarias:

- **Formulario DDA-01:** Solicitud de registro de obra inédita en la categoría de programa de ordenador (soporte lógico).
- **Depósito legal:** Presentación de dos ejemplares en soporte digital conteniendo:
  1. Código fuente representativo del backend Django y frontend React (sanitizado de secretos, claves criptográficas y contraseñas).
  2. Manual de usuario con capturas explicativas de la interfaz por rol.
  3. Memoria técnica descriptiva con la arquitectura del sistema, esquema relacional de datos y especificación del modelo predictivo Random Forest Regressor.
- **Derechos Morales:** De carácter inalienable, irrenunciable e imprescriptible, corresponden exclusivamente a sus desarrolladores: Carlos Gabriel Lobo Gutiérrez y Leonardo Serrate Basma.
- **Derechos Patrimoniales:** Comprenden las facultades exclusivas de reproducción, distribución, comunicación pública y transformación del software. El equipo conserva la titularidad patrimonial originaria; en caso de entrega formal a la UAGRM, se formalizará mediante un convenio de cesión de derechos patrimoniales o una licencia institucional de uso no exclusiva, permanente y gratuita para fines académicos y de gestión universitaria.

## 5.4. Normativa TIC, firma digital y comercio electrónico

El funcionamiento de la plataforma web se ajusta a la Ley N° 164 (Ley General de Telecomunicaciones, Tecnologías de Información y Comunicación) y su Decreto Supremo Reglamentario N° 1793:

- **Validez jurídica de mensajes de datos:** Los registros electrónicos de pesaje, incidencias operativas, asignación de turnos y reportes analíticos generados por el sistema tienen plena validez legal y eficacia probatoria de acuerdo con los artículos 6 y 7 de la Ley N° 164.
- **Comercio electrónico y pasarelas de pago:** Si en fases futuras el sistema ofrece suscripciones o cobro de tasas por recolección especializada, se integrarán pasarelas autorizadas por ASFI (pago con código QR interoperable y tarjetas de débito/crédito nacionales), cumpliendo los estándares de seguridad PCI-DSS.

## 5.5. Términos de uso, confidencialidad y gobernanza de datos

La gobernanza de datos del sistema protege la información de pesaje, ubicación de puntos de acopio y cuentas de usuario:

- **Términos y condiciones de uso:** Delimitan que el acceso al sistema está restringido a usuarios autorizados por la DSU-UAGRM según sus cuatro roles (Operativo, Supervisor, Directivo, Administrador). Se prohíbe el uso no autorizado, la alteración deliberada de registros de pesaje y la extracción no consentida de información.
- **Acuerdos de nivel de servicio (SLA):** Se establece como objetivo de disponibilidad un 99.0 % de tiempo en línea en horario laboral institucional (06:00 a 20:00), con ventanas de mantenimiento programadas en horarios nocturnos.
- **Política de privacidad y seguridad de datos:**
  - Almacenamiento cifrado de contraseñas mediante algoritmos de derivación de claves de alta resistencia (PBKDF2 / Argon2 con salt aleatorio).
  - Tránsito seguro de información mediante certificados TLS/SSL forzando conexiones HTTPS estrictas.
  - Gestión de credenciales y variables de entorno fuera del código fuente en archivos de configuración protegidos.
  - Trazabilidad y no repudio mediante registro de auditoría de cada modificación transaccional (usuario, fecha, hora e IP de origen).

# 6. Infraestructura para la producción de software

## 6.1. Elementos de configuración

Se consideran elementos de configuración el código, las dependencias, las migraciones, los parámetros de despliegue, los modelos UML, los documentos, las pruebas y los artefactos predictivos. El control de cambios deberá permitir relacionar una versión entregada con sus entradas y evidencias.

| Elemento | Ubicación del proyecto | Control previsto |
| --- | --- | --- |
| Backend | gestion-residuos-dsu/backend | Revisión de API, servicios, migraciones y dependencias |
| Frontend | gestion-residuos-dsu/frontend | Revisión de interfaz, construcción y configuración |
| Modelos UML | modelo_uml y generador/figuras | Conservación de fuentes y exportaciones |
| Documento Software 2 | DocumentoSoftware2 | Fuente editable, versiones y revisión visual |
| Evidencias de pruebas | docs/auditoria-fase-final | Conservación del resultado original y su contexto |

## 6.2. Control de versiones y colaboración

La raíz del proyecto es el único repositorio Git. Backend y frontend no son submódulos. Antes de integrar cambios se revisará el estado del repositorio y se identificarán los archivos propios de cada actividad. Las modificaciones de documentación no deben sobrescribir correcciones manuales o alterar artefactos de otra materia.

Para una entrega se registrarán identificador de versión, archivos incluidos, dependencias y cambios relevantes. El acceso al repositorio privado no equivale a permiso de publicación. La revisión de los materiales compartidos deberá proteger las configuraciones sensibles y verificar que las evidencias no contengan credenciales.

## 6.3. Gestión documental

Cada materia mantiene su documento, estructura y criterios de evaluación. Los requisitos y el producto permanecen compartidos. Un cambio funcional se analiza en ambos documentos; un ajuste de portada, numeración o capítulo se aplica solo a la materia correspondiente.

El documento de Software 2 se genera desde fuentes propias y conserva una copia anterior antes de una revisión mayor. Si se edita manualmente el Word, los cambios deberán incorporarse a la fuente antes de regenerar. El control documental incluye revisión de tablas, índices, imágenes y referencias cruzadas.

## 6.4. Entornos

El entorno de desarrollo permite ejecutar y revisar componentes. El entorno de pruebas utiliza bases aisladas y datos controlados. La base demo compartida en Neon sirve al trabajo conjunto y debe preservarse de cambios no coordinados. El entorno productivo previsto separa interfaz, API y persistencia administrada; su verificación se describe en el capítulo 11.

## 6.5. Inventario técnico observado

Las versiones de la tabla proceden del registro técnico del proyecto del 16 de noviembre de 2026. Corresponden a esa captura del entorno y del archivo de dependencias del frontend; no se presentan como las versiones más recientes disponibles en el mercado.

<!-- versiones -->

# 7. Sitio web de presentación

## 7.1. Propósito y destinatarios

Para respaldar la difusión institucional, la transferencia tecnológica y la transparencia del proyecto, se define la especificación del portal web promocional e informativo del Sistema DSU. Este sitio público cumple el rol de vitrina tecnológica para la comunidad universitaria de la UAGRM, directivos de la Dirección Universitaria de Servicios (DSU), evaluadores académicos y administraciones municipales interesadas en la modernización ecológica.

El portal de presentación se implementa de manera desacoplada del aplicativo operativo transaccional, sirviendo como canal de comunicación, demostración interactiva de capacidades y plataforma de atención y soporte a usuarios.

## 7.2. Estructura de contenidos y arquitectura de información

El portal se organiza bajo un diseño responsive moderno, optimizado para navegación ágil desde computadoras de escritorio y dispositivos móviles. La estructura se distribuye en las siguientes secciones clave:

| Sección | Componentes y contenido visual | Llamada a la acción (CTA) | Finalidad informativa |
| --- | --- | --- | --- |
| Portada (Hero Section) | Titular de impacto, propuesta de valor ecológica, métricas sintéticas destacadas y video teaser de 60 segundos | «Solicitar Demostración» y «Acceso Institucional» | Capturar el interés inmediato y contextualizar la solución |
| Módulos Funcionales | Tarjetas interactivas detallando los módulos de Operación, Analítica Gerencial y Predicción con Random Forest | «Explorar Características» | Describir el alcance funcional sin abrumar técnicamente |
| Demostración Interactiva | Simulador guiado del registro de pesaje y visualización de mapas de calor con datos de prueba controlados | «Probar Simulador» | Permitir una experiencia práctica del flujo de usuario |
| Beneficios e Impacto | Gráficos explicativos de optimización de rutas, reducción de viajes ociosos y trazabilidad ambiental | «Ver Informe Técnico» | Justificar el retorno de inversión y el valor institucional |
| Centro de Recursos | Enlaces a manuales de usuario descargables en PDF, guías rápidas en video y documentación académica | «Descargar Manual» | Proveer autoservicio de capacitación a los operadores |
| Mesa de Ayuda y Contacto | Formulario de contacto, canal de reporte de incidencias y preguntas frecuentes (FAQ) | «Enviar Mensaje» | Canalizar consultas, sugerencias y solicitudes de soporte |

## 7.3. Mecanismos de interacción y mesa de ayuda (Help-Desk)

Para garantizar la continuidad operativa y la resolución oportuna de problemas funcionales o técnicos, el portal incorpora un modelo de atención escalonada de soporte técnico estructurado en tres niveles de atención:

| Nivel de soporte | Canal de atención | Responsable | Cobertura horaria | Tiempo de primera respuesta |
| --- | --- | --- | --- | --- |
| Nivel 1 (Autoservicio) | Base de conocimiento, repositorio FAQ y chatbot de respuestas guiadas en el portal | Sistema automatizado | 24/7 (Continuo) | Inmediato (< 1 minuto) |
| Nivel 2 (Soporte Funcional) | Formulario web de tickets e incidencias y correo electrónico institucional | Agente de mesa de ayuda técnica | Lunes a Viernes 07:00 a 19:00 | Menor a 2 horas laborables |
| Nivel 3 (Soporte Especializado) | Canal directo de ingeniería y seguimiento de bugs en el repositorio | Ingenieros de software y DBA | Lunes a Viernes 08:00 a 16:00 | Menor a 6 horas laborables |

## 7.4. Estrategia progresiva de mejoras tecnológicas

La hoja de ruta de evolución del producto contempla tres líneas de modernización continua:

1. **Transformación a Progressive Web App (PWA):** Incorporación de Service Workers y almacenamiento local en IndexedDB en el frontend para habilitar el registro de pesaje en modo fuera de línea (offline). Esto permitirá a las cuadrillas registrar vaciados en zonas del campus con sombra de cobertura móvil, sincronizando automáticamente los datos al recuperar la conectividad.
2. **Telemetría IoT en contenedores:** Integración futura de sensores ultrasónicos de nivel de llenado con microcontroladores ESP32 y conectividad LoRaWAN / GSM, enviando telemetría directa a los endpoints de la API Django sin requerir registro manual en puntos críticos.
3. **Localización e internacionalización:** Soporte multi-idioma (español e inglés) en la interfaz pública y analítica para facilitar su evaluación en congresos científicos internacionales de gestión ambiental y ciudades inteligentes.

# 8. Estudio de mercado y adopción

## 8.1. Diagnóstico del contexto de gestión de residuos en Santa Cruz y Bolivia

La gestión de residuos sólidos en los municipios e instituciones de educación superior de Bolivia enfrenta desafíos estructurales derivados de la recolección reactiva y la carencia de digitalización:

- **Procesos manuales y fragmentados:** En el campus de la UAGRM (con una población flotante que supera los 100 000 integrantes entre estudiantes, docentes y administrativos), los registros de vaciado y pesaje se han gestionado históricamente mediante anotaciones en libretas de papel o planillas Excel aisladas. Esta práctica ocasiona demoras en la consolidación, pérdida de información y discrepancias en los pesajes.
- **Rutas empíricas de recolección:** La asignación de recorridos y frecuencias de vaciado depende de la experiencia informal del personal, lo que produce viajes ociosos hacia contenedores a medio llenar o desbordes en puntos críticos con alta afluencia estudiantil en horarios pico.
- **Ausencia de modelos predictivos:** Las instituciones carecen de herramientas cuantitativas para proyectar la generación de residuos según el calendario académico (periodos de clases regulares, semanas de exámenes, recesos o eventos masivos), imposibilitando una planificación presupuestaria basada en evidencia.

## 8.2. Soluciones comerciales de referencia internacional

En el mercado internacional existen soluciones tecnológicas consolidadas de gestión inteligente de residuos (Smart Waste Management):

- **Sensoneo (Eslovaquia):** Plataforma líder global enfocada en optimización de rutas y monitoreo de contenedores mediante sensores IoT y software de planificación logística en la nube.
- **Ecube Labs / CleanCityNetworks (Corea del Sur):** Ecosistema integral que combina contenedores compactadores solares (Clean Cube) y sensores de llenado (Clean Cap) integrados a la plataforma analítica SaaS CleanCityNetworks (CCN).
- **Bigbelly (Estados Unidos):** Estaciones inteligentes de recolección compactadora con enlace celular y plataforma de gestión remota CLEAN para seguimiento en tiempo real de cuadrillas y llenado en campus universitarios y espacios públicos.
- **SmartBin (Reino Unido / Países Bajos):** Solución de telemetría por sensores para monitoreo de contenedores de reciclaje y optimización de flotas de camiones recolectores.

## 8.3. Matriz comparativa entre soluciones comerciales y el Sistema DSU

La siguiente tabla compara las soluciones de referencia internacional frente a la propuesta desarrollada para la DSU-UAGRM:

| Criterio de comparación | Sensoneo Route Planning | Ecube Labs CleanCityNetworks | Bigbelly Smart Waste | Sistema DSU-UAGRM |
| --- | --- | --- | --- | --- |
| País de origen y modelo | Eslovaquia — SaaS en la nube | Corea del Sur — Hardware + SaaS | EE.UU. — Hardware propietario | Bolivia — Web escalable híbrida |
| Requerimiento de sensores IoT | Obligatorio (sensores propios) | Obligatorio (sensores ultrasónicos) | Obligatorio (estaciones propias) | No obligatorio (registro manual/báscula) |
| Soporte de pesaje directo | Registro derivado de volumen | Estimación por volumen cúbico | Estimación por compactación | Registro exacto en balanza/báscula (kg) |
| Predicción con Machine Learning | Heurística básica de llenado | Algoritmo predictivo de alertas | Alertas por umbral de llenado | Random Forest Regressor institucional |
| Reportería gerencial interactiva | Módulo de reportes en la nube | Dashboard propietario CCN | Dashboard propietario CLEAN | Modelo semántico DAX en Power BI |
| Costo de implantación | Elevado (licencia en euros/dólares) | Muy elevado (importación hardware) | Crítico (estaciones solares costosas) | Muy bajo (tecnología web abierta) |
| Viabilidad en Bolivia | Limitada por aranceles y soporte | Limitada por mantenimiento de hardware | Inviable para presupuestos públicos | Plenamente viable y adaptada al medio |

## 8.4. Propuesta de valor diferencial de DSU-UAGRM

Frente a las alternativas comerciales, el Sistema DSU se distingue por cuatro ventajas estratégicas adaptadas a la realidad boliviana:

1. **Independencia de hardware costoso:** No supedita la modernización del servicio a la adquisición de miles de sensores ultrasónicos importados. Permite que el personal registre directamente los pesajes obtenidos en básculas mecánicas o digitales en campo mediante la interfaz web accesible desde cualquier teléfono inteligente.
2. **Modelo predictivo adaptado a la dinámica universitaria:** El algoritmo Random Forest Regressor está calibrado específicamente con variables del entorno universitario (tipo de residuo, sector del campus, estacionalidad académica y día de la semana), prediciendo la acumulación en kilogramos con su respectivo margen de error documentado.
3. **Soberanía tecnológica y costos controlados:** Al construirse sobre componentes de software libre de alta madurez (Python, Django REST Framework, React, PostgreSQL), elimina las ataduras de licenciamiento anual en moneda extranjera y permite su mantenimiento por profesionales bolivianos.
4. **Integración analítica con Power BI:** Aprovecha las herramientas de Business Intelligence corporativas ampliamente difundidas en el entorno universitario y empresarial para la toma de decisiones directivas.

## 8.5. Estrategia de adopción y gestión del cambio en la UAGRM

La implantación exitosa de la plataforma requiere un programa estructurado de gestión del cambio para asegurar la apropiación de la herramienta por parte de los trabajadores:

- **Fase 1: Piloto de marcha blanca:** Implementación en una zona delimitada del campus (por ejemplo, sectores de Ingeniería y Tecnología) durante un periodo de cuatro semanas, operando en paralelo con las planillas físicas para calibrar la usabilidad de las interfaces móviles.
- **Fase 2: Capacitación situada por roles:** Talleres prácticos adaptados al nivel de alfabetización digital de cada grupo: capacitación en campo para el personal operativo, entrenamiento en asignación de rutas para supervisores y sesiones ejecutivas de análisis de datos para directivos.
- **Fase 3: Medición de usabilidad estandarizada (SUS):** Aplicación de la escala estandarizada *System Usability Scale* (SUS) al finalizar el piloto, buscando una puntuación superior a 75 puntos sobre 100 como criterio de aceptación de usabilidad antes del despliegue masivo a todos los módulos de la universidad.
- **Fase 4: Incentivos y reconocimiento ambiental:** Publicación de indicadores de eficiencia y reducción de huella de carbono por facultad, reconociendo a los sectores del campus con mayor tasa de reciclaje y puntualidad en el registro.

# 9. Pruebas en el software

## 9.1. Objetivo y alcance

El propósito es comprobar comportamientos definidos, identificar defectos y conservar evidencia reproducible. Este capítulo integra resultados técnicos existentes del proyecto con las pruebas pendientes de aceptación y operación. El uso de los mismos registros en ambas materias conserva su fecha y alcance; no se cuentan como ejecuciones adicionales realizadas para Software 2.

## 9.2. Diseño y trazabilidad

Cada caso debe indicar requisito y CU, precondiciones, entrada, procedimiento, resultado esperado, resultado observado y estado. La evidencia incluirá entorno, datos y versión. Las pruebas funcionales se complementarán con condiciones inválidas y límites de autorización. Los defectos detectados se gestionarán según el SQAP.

### 9.2.1. Escenarios críticos

| Escenario | Referencia | Condición que se comprueba |
| --- | --- | --- |
| Autenticación y cierre | RF3; CU1 y CU2 | Credenciales, sesión y revocación según el contrato implementado |
| Registro de vaciado | RF8; CU9 | Cantidades válidas, usuario autorizado y vínculo con la operación |
| Asignación de jornada | RF13; CU15 | Responsable, disponibilidad y conflictos de recursos |
| Omisión y cierre | RF12; CU17 y CU18 | Motivo registrado y ausencia de puntos sin resolución |
| Indicadores y periodos | RF15–RF18; CU20–CU22 | Datos preparados y comparaciones consistentes |
| Predicción | RF22–RF24; CU26–CU30 | Modelo disponible, resultados y margen de error |

## 9.3. Regresión automatizada disponible

Los reportes JUnit conservados registran 42 pruebas en Windows y 42 en Linux, sin fallos, errores ni omisiones en esas corridas. Son dos ejecuciones de la suite; no se presentan como 84 casos distintos. El entorno utilizó PostgreSQL 18 aislado y datos sintéticos, sin escrituras en la base Neon compartida.

<!-- resultados junit -->

Las duraciones corresponden al tiempo declarado por la suite, no a latencia de usuario ni a capacidad productiva. La regresión verifica los escenarios incluidos en el código de prueba; no demuestra por sí sola cumplimiento de todos los requisitos no funcionales o aceptación institucional.

## 9.4. Ejemplos de resultados funcionales

Los siguientes registros resumen escenarios identificados en las evidencias del proyecto. Los archivos originales conservan los detalles de entrada y respuesta. No se incluyen contraseñas, tokens o información de acceso.

<!-- resultados api -->

## 9.5. Pruebas estructurales

El análisis de caja blanca existente examina las funciones de asignación de recursos y generación predictiva. La matriz de auditoría registra complejidad estructural 7 para asignar y 9 para generar. En generar, el rango factible y ejecutado informado es 7; por ello no se declara ejecución de nueve caminos independientes factibles. El análisis debe leerse junto a los grafos, las restricciones y las trazas conservadas.

La revisión estructural aporta evidencia sobre decisiones internas seleccionadas. No sustituye la verificación de otros servicios ni una medición general de cobertura del código.

<!-- grafos pruebas -->

## 9.6. Seguridad e interfaz

La revisión de seguridad disponible corresponde a un análisis pasivo ZAP en entorno aislado, con acceso autenticado comprobado. El registro técnico informa correcciones de cabeceras y advertencias residuales. Su alcance no equivale a una prueba de penetración completa ni permite afirmar ausencia de vulnerabilidades.

La revisión de interfaz registró 25 combinaciones de rol y ruta en anchos de 1440 y 390 píxeles, con 50 capturas. El registro informa ausencia de errores JavaScript, violaciones CSP y desbordamiento general en ese recorrido de carga y lectura. No cubre automáticamente todos los flujos interactivos.

<!-- figura interfaz -->

## 9.7. Evaluación del componente predictivo

La evaluación deberá registrar versión del modelo, periodo del histórico, procedencia, variables, separación de entrenamiento y prueba, métricas y límites. Los errores se expresarán en unidades interpretables para el uso previsto y se conservará la forma de calcular el margen mostrado al usuario.

Los históricos sintéticos permiten verificar el procesamiento y la integración. La precisión sobre operación real de la DSU requiere datos institucionales representativos y una evaluación independiente de la generación de esos datos. No se trasladan resultados de demostración como rendimiento predictivo institucional.

## 9.8. Pendientes y criterio de cierre

Permanecen por comprobar despliegue remoto, carga y rendimiento representativos, restauración externa, validación predictiva institucional y aceptación por usuarios. También debe completarse la revisión del informe Power BI y su publicación cuando corresponda. Cada cierre deberá enlazar el requisito con evidencia, entorno y decisión; las observaciones de una fuente anterior no se reemplazarán por una declaración general de finalización.

# 10. Marketing y difusión del proyecto

## 10.1. Objetivo y propuesta de valor

El plan de difusión y comercialización tiene como objetivo posicionar el Sistema DSU como la solución de referencia en transformación digital ecológica para instituciones educativas y municipios en Bolivia. La propuesta de valor se sintetiza en la transición desde una recolección manual y reactiva hacia una gestión inteligente basada en datos, garantizando tres beneficios estratégicos medibles:

1. **Eficiencia operativa y ahorro de recursos:** Eliminación de recorridos ociosos y optimización de las frecuencias de vaciado según la tasa real de llenado de los contenedores.
2. **Trazabilidad y transparencia ambiental:** Registro exacto en kilogramos por tipo de residuo (plásticos, papel, orgánicos, vidrio, no aprovechables), permitiendo a la universidad certificar sus metas de sostenibilidad y economía circular.
3. **Planificación predictiva proactiva:** Anticipación de picos de generación de residuos mediante el modelo Random Forest Regressor, permitiendo aprovisionar bolsas, turnos y vehículos antes de la ocurrencia de desbordes en el campus.

## 10.2. Segmentación y Buyer-Personas institucionales

Para adecuar los mensajes y materiales de difusión, se definen cuatro perfiles de usuario clave dentro del ecosistema universitario:

| Perfil / Rol | Responsabilidad principal | Dolor o problema actual | Mensaje de valor diferenciado |
| --- | --- | --- | --- |
| Directivo de la DSU | Gestión estratégica y presupuestaria del campus | Falta de indicadores consolidados y reportes manuales tardíos | «Toma decisiones respaldadas en analítica Power BI en tiempo real y predice tus necesidades presupuestarias» |
| Supervisor de Operaciones | Planificación de rutas, asignación de cuadrillas y vehículos | Pérdida de tiempo consolidando planillas de papel e incidentes no registrados | «Organiza las jornadas de tu equipo en minutos y supervisa el avance de recolección en un mapa interactivo» |
| Personal Operativo de Limpieza | Vaciado de contenedores y pesaje en campo | Formulario en papel engorroso y temor a interfaces complejas | «Registra los pesajes desde tu celular con tres toques simples, sin papeleos ni pérdida de datos» |
| Evaluador Académico / Auditor | Verificación de estándares técnicos y calidad de software | Sistemas sin trazabilidad metodológica ni evidencias formales | «Solución integral gobernada bajo PUDS, SQAP IEEE 730-2026 y regresión automatizada documentada» |

## 10.3. Canales, formatos y fases de la campaña de difusión

La estrategia de difusión se articula en tres fases progresivas:

- **Fase I: Concientización y expectativa (Semanas 1 a 2):** Campaña institucional bajo el lema *«Campus Limpio, Gestión Inteligente»*. Publicación de cápsulas audiovisuales breves en redes institucionales y colocación de afiches informativos con códigos QR en los 23 puntos de acopio ecológico del campus de la UAGRM.
- **Fase II: Lanzamiento oficial e inducción (Semanas 3 a 5):** Presentación del portal web del proyecto ante autoridades universitarias y realización de talleres presenciales de capacitación situados en los módulos de trabajo de la DSU, entregando guías plastificadas por rol.
- **Fase III: Consolidación e incentivos ecológicos (Semanas 6 en adelante):** Publicación mensual del ranking de facultades con mayor índice de reciclaje y presentación de los resultados del modelo predictivo en las jornadas científicas de la FICCT.

| Canal de difusión | Formato del material | Audiencia objetivo | Finalidad comunicacional |
| --- | --- | --- | --- |
| Portal Web del Proyecto | Landing page responsive con simulador y centro de recursos | Comunidad universitaria y evaluadores | Difusión integral, transparencia y autoservicio |
| Puntos Ecológicos del Campus | Afiches informativos y señalética con códigos QR | Estudiantes, docentes y personal de limpieza | Concientización ambiental y enlace al portal web |
| Talleres Presenciales | Demostraciones en vivo y sesiones prácticas guiadas | Cuadrillas operativas y supervisores | Capacitación práctica y reducción de la brecha digital |
| Canal de Video (YouTube) | Píldoras tutoriales de 2 minutos por caso de uso | Nuevos operarios y personal de reemplazo | Formación continua sin dependencia de instructores |

## 10.4. Recursos e indicadores clave de rendimiento (KPIs)

El éxito del programa de difusión y adopción se evaluará de forma continua mediante los siguientes indicadores de desempeño:

| Indicador clave (KPI) | Definición y método de cálculo | Meta objetivo | Fuente de verificación |
| --- | --- | --- | --- |
| Tasa de digitalización de pesajes | (Pesajes registrados en el sistema / Total de pesajes ejecutados) * 100 | Mayor al 90 % en el primer mes | Base de datos relacional PostgreSQL |
| Adopción por sector del campus | Porcentaje de sectores universitarios activos con jornadas digitales | 100 % de los sectores cubiertos | Módulo de supervisión de jornadas |
| Tiempo medio de registro | Tiempo transcurrido en el registro móvil de un vaciado | Menor a 45 segundos por punto | Trazas de auditoría del sistema |
| Satisfacción de usuario (CSAT) | Encuesta de satisfacción aplicada tras los talleres de inducción | Mayor al 85 % de valoración positiva | Encuestas de usabilidad SUS aplicadas |

# 11. Puesta en marcha y despliegue

## 11.1. Arquitectura prevista y comparativa de plataformas Cloud

Para la puesta en marcha del sistema en producción se evaluaron las alternativas de infraestructura en la nube más representativas frente a la arquitectura híbrida adoptada:

- **Amazon Web Services (AWS):** Infraestructura basada en contenedor ECS/Fargate para la API Django, servicio gestionado Amazon RDS para PostgreSQL y bucket S3 con CloudFront para el frontend y medios estáticos. Ofrece alta madurez y SLAs del 99.99 %, pero presenta costos elevados en dólares y mayor complejidad operativa para presupuestos universitarios.
- **Microsoft Azure:** Despliegue mediante Azure App Service para Linux conectado a Azure Database for PostgreSQL Flexible Server. Facilita la gobernanza mediante suscripciones educativas, aunque mantiene costos mensuales fijos superiores a soluciones serverless.
- **Google Cloud Platform (GCP):** Cómputo serverless mediante Cloud Run conectado a Cloud SQL para PostgreSQL y Cloud Storage. Destaca por su facturación por milisegundo de ejecución, siendo altamente escalable para cargas intermitentes.
- **Arquitectura Híbrida Adoptada:** Despliegue del backend en VPS Linux (o Render) gobernado por un contenedor Docker detrás del reverse proxy Caddy (con emisión y renovación automática de certificados SSL/TLS Let's Encrypt), base de datos PostgreSQL alojada en Neon (con pooling de conexiones pgbouncer) y frontend estático distribuido en la red global de Vercel Edge Network.

La siguiente tabla compara las opciones de despliegue evaluadas:

| Criterio | Amazon Web Services (AWS) | Microsoft Azure | Google Cloud Platform (GCP) | Arquitectura Híbrida Adoptada |
| --- | --- | --- | --- | --- |
| Cómputo Backend | ECS Fargate / EC2 Linux | Azure App Service | Cloud Run Serverless | Docker en VPS Linux con Caddy |
| Persistencia de Datos | Amazon RDS PostgreSQL | Azure Database PostgreSQL | Cloud SQL PostgreSQL | PostgreSQL administrado en Neon |
| Distribución Frontend | S3 + CloudFront CDN | Azure Static Web Apps | Cloud Storage + Cloud CDN | Vercel Edge Global Network |
| Complejidad de gestión | Alta (requiere DevSecOps) | Media-Alta | Media | Baja-Media (administración ágil) |
| Costo mensual estimado | 65 – 110 USD / mes | 70 – 120 USD / mes | 45 – 90 USD / mes | 15 – 35 USD / mes |
| Viabilidad institucional | Requiere partida de divisa | Requiere convenio Microsoft | Requiere tarjeta corporativa | Óptima para presupuesto universitario |

## 11.2. Preparación del entorno y configuración técnica

La configuración de producción desacopla estrictamente los secretos y parámetros sensibles del código fuente mediante variables de entorno seguras almacenadas en archivos protegidos con permisos de lectura restringidos:

- **Aislamiento de credenciales:** La clave secreta de Django (SECRET_KEY), credenciales de conexión a Neon PostgreSQL, tokens de servicio y configuraciones de correo se inyectan en tiempo de ejecución sin incluirse en repositorios públicos.
- **Políticas de depuración:** Desactivación estricta del modo de depuración (DEBUG=False) en producción para evitar la exposición de trazas de error o variables de sesión ante fallos imprevistos.
- **Reverse Proxy Caddy:** Manejo automatizado de cifrado HTTPS con certificados TLS emitidos por Let's Encrypt, forzando redirección HTTP a HTTPS y balanceando peticiones hacia el socket WSGI de Django (Gunicorn con 3 workers).

## 11.3. Verificación de puesta en marcha

La aceptación técnica de la instalación en producción se verifica mediante siete controles de calidad estandarizados:

| Control de verificación | Evidencia requerida | Criterio de aceptación propuesto |
| --- | --- | --- |
| Acceso seguro perimetral | Certificado SSL/TLS válido y redirección forzosa a HTTPS | Navegación segura sin advertencias de certificado en navegador |
| Autenticación y roles (RBAC) | Pruebas de acceso con cuentas de los cuatro roles | Restricción estricta de rutas y rechazo de accesos no autorizados |
| Registro operativo en campo | Ejecución de jornada de prueba completa en entorno productivo | Registro de pesaje, omisión justificada y cierre con totales consistentes |
| Procesamiento ETL analítico | Disparo del pipeline ETL hacia el esquema estrella de hechos | Inserción sin duplicados y cálculo exacto de métricas acumuladas |
| Consulta predictiva | Invocación del servicio con parámetros de fecha y sector | Retorno de estimación en kilogramos acompañada de margen de error |
| Exportación de reportes | Generación de reportes consolidados en Excel y PDF | Formato legible, filtros aplicados y totales coincidentes |
| Procedimiento de restauración | Prueba de restauración de copia de seguridad en entorno aislado | Integridad referencial comprobada al 100 % tras recuperar la base |

## 11.4. Plan de continuidad operativa y recuperación ante desastres (DRP)

Para garantizar la disponibilidad de la información histórica de la universidad frente a contingencias o corrupción de datos, se define una política formal de respaldo y recuperación:

- **Frecuencia y retención de respaldos:** Copias de seguridad completas automatizadas de la base de datos PostgreSQL mediante el utilitario `pg_dump` con compresión gzip, ejecutadas diariamente a las 02:00 horas (horario de nula actividad en el campus). Retención de copias diarias por 30 días y copias mensuales consolidadas por 12 meses en almacenamiento secundario cifrado y geográficamente independiente.
- **Métricas de recuperación del servicio:**
  - *RPO (Recovery Point Objective):* Menor o igual a 24 horas, limitando la pérdida máxima tolerable de datos a los registros de la jornada inmediata anterior.
  - *RTO (Recovery Time Objective):* Menor o igual a 2 horas, tiempo máximo previsto para provisionar una nueva instancia y restaurar el dump de base de datos.
- **Protocolo paso a paso de restauración:**
  1. Aprovisionamiento o verificación del clúster de base de datos destino con versión compatible de PostgreSQL (versión 16 o superior).
  2. Descarga y verificación de la suma de comprobación (checksum SHA-256) del archivo de respaldo más reciente.
  3. Ejecución del comando de restauración: `pg_restore --clean --if-exists -d nombre_bd archivo_backup.dump`.
  4. Ejecución del script de comprobación de integridad referencial para verificar el conteo de tablas y consistencia de claves foráneas.
  5. Conexión de la API backend y ejecución de la suite de pruebas de salud de endpoints (healthcheck).

## 11.5. Seguridad perimetral, cabeceras HTTP y endurecimiento (Hardening)

El endurecimiento perimetral de la infraestructura de producción implementa las mejores prácticas de seguridad recomendadas por OWASP:

- **Cabeceras de seguridad HTTP:** Inyección en Caddy de directivas HSTS (*Strict-Transport-Security* con max-age de un año), *X-Content-Type-Options: nosniff*, *X-Frame-Options: DENY* para prevenir ataques de clickjacking, y directivas de Content Security Policy (CSP) restrictivas.
- **Aislamiento CORS:** Restricción estricta de la lista blanca de orígenes permitidos en Django (*CORS_ALLOWED_ORIGINS*) exclusivamente al dominio oficial del frontend en Vercel, rechazando solicitudes cross-origin no autorizadas.
- **Protección de tokens JWT:** Emisión de tokens de acceso con caducidad corta (60 minutos) y tokens de refresco (refresh tokens) almacenados en cookies seguras con atributos *HttpOnly*, *Secure* y *SameSite=Lax*.
- **Rotación periódica de credenciales:** Procedimiento documentado para la rotación semestral de contraseñas de servicio y claves secretas de la plataforma.

## 11.6. Estado de preparación y puesta en marcha

El proyecto cuenta con especificaciones de despliegue probadas en contenedores locales Linux y una base de datos demo compartida en Neon. La puesta en marcha definitiva en el dominio institucional de la universidad se encuentra planificada como fase de transición, condicionada a la firma del convenio de adopción con las autoridades de la UAGRM y la asignación del subdominio oficial correspondiente.

<!-- figura despliegue -->

# 12. Software como producto

## 12.1. Composición de la entrega

La entrega debe identificar versión del código, configuración de instalación, estructura de datos, documentación, pruebas y limitaciones. El código, el manual y las capturas deberán describir la misma versión. El producto se evaluará por tareas y criterios observables, no por la cantidad de archivos incluidos.

## 12.2. Guía inicial por rol

### 12.2.1. Acceso al sistema

El usuario ingresa con su cuenta autorizada. Si el acceso es rechazado, verifica sus datos o consulta al administrador. Al finalizar utiliza Cerrar sesión y conserva sus credenciales de forma personal.

### 12.2.2. Operación en campo

El operativo consulta su jornada, identifica el punto y registra cantidades por tipo de residuo. Revisa unidad y cantidad antes de guardar; corrige los errores indicados y comprueba la confirmación. Si pierde conectividad, no debe asumir que el envío fue guardado: la versión actual no encola operaciones fuera de línea.

### 12.2.3. Supervisión de jornadas

El supervisor planifica jornadas de sus sectores, ordena puntos y asigna personal y vehículos disponibles. Revisa el avance y registra el motivo de las omisiones autorizadas. Antes del cierre comprueba que cada punto esté atendido u omitido con justificación.

### 12.2.4. Consulta directiva

El directivo consulta tableros, mapas y reportes dentro de su alcance. Antes de comparar resultados revisa periodo, sector y tipo de residuo. Distingue datos observados de proyecciones y considera el margen de error. La falta de histórico o de una predicción disponible no debe interpretarse como generación nula.

### 12.2.5. Administración

El administrador gestiona accesos, catálogos y parámetros según sus permisos. Las operaciones ETL, entrenamiento y publicación del modelo requieren verificar datos y resultados antes de utilizarlos en análisis. La administración del sistema no habilita por sí misma acciones de registro operativo en campo.

## 12.3. Guion de material audiovisual

Se propone un video de presentación del problema y cuatro recorridos breves: registro de campo, planificación y cierre de jornada, consulta de indicadores y mapas, y uso de predicción con sus límites. Cada grabación deberá identificar versión y carácter sintético de los datos cuando corresponda. Los videos no están incluidos como resultados realizados en esta edición.

## 12.4. Soporte y mantenimiento

El reporte de incidente incluirá tarea, rol, momento, mensaje y pasos de reproducción, sin credenciales. El equipo aplicará el SQAP y verificará la corrección y la regresión pertinente antes de reemplazar una versión entregada.

## 12.5. Lista de entrega

| Elemento | Comprobación requerida | Situación documentada |
| --- | --- | --- |
| Sistema y API | Versión identificada y ejecución | Implementación y pruebas técnicas disponibles |
| Documento Software 2 | Capítulos, fuentes e índices consistentes | En elaboración y revisión |
| Modelos | Fuentes y figuras concordantes | Artefactos del proyecto disponibles |
| Pruebas | Registros y limitaciones | Evidencias técnicas identificadas en capítulo 9 |
| Instalación | Procedimiento reproducido | Configuración preparada; operación remota pendiente |
| Manual y videos | Tareas completas por rol | Guía inicial y guion; ampliación pendiente |
| Aceptación institucional | Decisión de usuarios autorizados | No acreditada por las pruebas técnicas |

# Bibliografía

Bigbelly. (s. f.). CLEAN software. https://bigbelly.com/products/clean-software

Bolivia. (1977). Código de Comercio de Bolivia (Decreto Ley N° 14379 de 25 de febrero de 1977). Gaceta Oficial del Estado Plurinacional de Bolivia.

Bolivia. (1992). Ley de Derecho de Autor (Ley N° 1322 de 13 de abril de 1992) y Decreto Supremo N° 23907 reglamentario de programas de ordenador y soporte lógico.

Bolivia. (2011). Ley General de Telecomunicaciones, Tecnologías de Información y Comunicación (Ley N° 164 de 8 de agosto de 2011) y Decreto Supremo N° 1793 reglamentario.

Comunidad Andina. (2000). Decisión 486: Régimen Común sobre Propiedad Industrial. Comisión de la Comunidad Andina.

Ecube Labs. (s. f.). Smart waste management solution. https://www.ecubelabs.com/solution/

IEEE Standards Association. (2026). IEEE 730-2026 IEEE Standard for Software Quality Assurance Processes. Ficha pública del estándar. https://standards.ieee.org/ieee/730/10854/

International Organization for Standardization. (2023). ISO/IEC 25010:2023 Product quality model. Ficha pública del estándar. https://www.iso.org/standard/78176.html

Jacobson, I., Booch, G., y Rumbaugh, J. (2000). El proceso unificado de desarrollo de software. Pearson Educación, Addison Wesley. ISBN 84-7829-036-2.

Lobo Gutiérrez, C. G., y Serrate Basma, L. (2026). Sistema web de gestión de residuos sólidos para la DSU UAGRM con predicción mediante Random Forest Regressor. Documento de Taller de Grado I y artefactos del proyecto compartido. Versión consultada el 16 de noviembre de 2026.

NASA. (s. f.). SWE-028 Verification Planning. NASA Software Engineering Handbook. https://swehb.nasa.gov/spaces/7150/pages/16450576/SWE-028+-+Verification+Planning

NASA. (s. f.). SWE-029 Validation Planning. NASA Software Engineering Handbook. https://swehb.nasa.gov/pages/viewpage.action?pageId=23200749

Sensoneo. (s. f.). Route planning software for waste pickup and hauling. https://www.sensoneo.com/en-us/products/route-planning/

Servicio de Impuestos Nacionales. (s. f.). Procesos de inscripción en el Registro Nacional de Contribuyentes. https://siatanexo.impuestos.gob.bo/index.php/requisitos-para-la-inscripcion/procesos-de-insccripcion

Servicio Nacional de Propiedad Intelectual. (s. f.). Registro de programas de ordenador o software. Portal oficial del Estado. https://www.gob.bo/tramites/registro-de-programas-de-ordenador-o-software

Servicio Plurinacional de Registro de Comercio. (2026). Guía de trámites de Registro de Comercio de Bolivia. https://www.seprec.gob.bo/wp-content/uploads/2026/05/GT2026v3_28_05_2026.pdf

Las fuentes web de esta edición se consultaron el 16 de noviembre de 2026. Las descripciones de productos comerciales proceden de sus proveedores y se emplean como comparación documental.
