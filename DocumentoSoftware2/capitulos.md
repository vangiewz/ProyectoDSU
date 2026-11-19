# 2. Modelo de desarrollo de software mediante PUDS

## 2.1. Organización del proceso

El proyecto adopta el Proceso Unificado de Desarrollo de Software, dirigido por casos de uso, centrado en la arquitectura e iterativo e incremental. Se organiza temporalmente en Inicio, Elaboración, Construcción y Transición. Los flujos de requisitos, análisis, diseño, implementación y pruebas atraviesan las fases con distinta intensidad; no son nombres alternativos de esas fases (Jacobson, Booch y Rumbaugh, 2000).

Los artefactos existentes permiten documentar el producto construido y sus relaciones. La correspondencia presentada a continuación organiza esos artefactos según las fases de PUDS.

## 2.2. Fase de Inicio

El objetivo de Inicio es delimitar el problema y el alcance, identificar destinatarios y reconocer riesgos que condicionan la viabilidad. Para DSU, la necesidad central es consolidar información de residuos y utilizarla en la planificación de recolección. El perfil, los objetivos y la identificación de cuatro actores proporcionan la base de esta fase.

El producto comprende ocho áreas funcionales y 27 requisitos funcionales. El valor previsto es mejorar la disponibilidad y trazabilidad de información para la operación y la decisión. No se cuantifica un ahorro institucional sin una línea base de costos y mediciones de uso.

Los riesgos iniciales incluyen calidad del histórico, participación de usuarios, permisos, conectividad y disponibilidad del despliegue. La revisión de Inicio debe comprobar comprensión del alcance, responsabilidades y condiciones para continuar.

## 2.3. Fase de Elaboración

### 2.3.1. Captura y organización de requisitos

La especificación del producto conserva RF1 a RF27 y sus requisitos no funcionales, de interfaces, datos, diseño y rendimiento. El modelo detalla 34 casos de uso para Administrador del Sistema, Supervisor de Recolección, Personal Operativo de Limpieza y Cuerpo Directivo de la DSU. La matriz de este capítulo permite seguir la relación RF–CU sin alterar la numeración compartida.

### 2.3.2. Arquitectura y paquetes

La arquitectura separa la interfaz web, la API y la persistencia. Los módulos operativos registran eventos; el ETL prepara información analítica; los indicadores y mapas facilitan consulta; el componente predictivo utiliza el histórico para producir estimaciones y recomendaciones. La seguridad y la auditoría tienen efecto transversal.

<!-- figura arquitectura -->

El modelo general de componentes se reutiliza como artefacto del producto y conserva su fuente de Enterprise Architect.

### 2.3.3. Decisiones y riesgos arquitectónicos

Se mantiene PostgreSQL en Neon. La aplicación web usa React y la API Django. La predicción corresponde a Random Forest Regressor y las recomendaciones se basan en reglas; no se introduce un modelo de lenguaje como requisito. Las funciones de entrenamiento y ETL requieren controlar carga y acceso porque comparten recursos con otros componentes.

La revisión de Elaboración debe contrastar permisos, reglas transaccionales, separación analítica e interfaces externas. La existencia de modelos y código permite comprobar decisiones técnicas, pero el rendimiento remoto y la validación del histórico institucional siguen necesitando evidencia específica.

## 2.4. Fase de Construcción

Se agrupan los incrementos del producto por dependencias funcionales: acceso y catálogos; operación y logística; analítica y cartografía; predicción y administración. Esta agrupación organiza el trabajo y la documentación; no se le asignan fechas históricas de iteración que no estén registradas.

| Incremento de referencia | Producto integrado | Verificación prioritaria |
| --- | --- | --- |
| Acceso y catálogos | Usuarios, roles y estructura territorial | Permisos, validaciones y consistencia de referencias |
| Operación y logística | Vaciados, incidencias y jornadas | Estados, asignación, omisiones y cierre |
| Analítica y cartografía | ETL, indicadores, mapas y reportes | Totales, filtros y correspondencia con los registros |
| Predicción y administración | Modelo, estimaciones, recomendaciones y auditoría | Evaluación, publicación, márgenes y trazabilidad |

La evidencia técnica disponible comprende implementación de los requisitos funcionales según el registro del proyecto, pruebas automatizadas y revisión de pantallas. Un módulo implementado no se considera automáticamente aceptado.

## 2.5. Fase de Transición

La Transición prepara el uso y la entrega: instalación, verificación del entorno, manuales, capacitación y aceptación. La arquitectura utiliza Vercel para el frontend, AWS EC2 con Linux y Docker para la API y Neon para datos.

Para cerrar esta fase se propone verificar el acceso por roles, un recorrido operativo completo, actualización analítica, predicción con su margen, exportación de reportes y recuperación de información. El piloto institucional debe identificar usuarios, datos autorizados, periodo de observación y criterios de aceptación. El cierre dependerá de evidencias y decisiones documentadas.

## 2.6. Trazabilidad del producto

La matriz siguiente se obtiene del catálogo de casos de uso del proyecto, consultado para esta edición. Su función es permitir localizar el comportamiento que concreta cada requisito. La vinculación con pruebas se desarrolla en el capítulo 9 y en las evidencias técnicas identificadas.

<!-- matriz cu -->

## 2.7. Ejemplo de aplicación del proceso a una jornada

En requisitos, el flujo define que el supervisor planifica una jornada y asigna recursos; la operación atiende los puntos y registra omisiones justificadas. En análisis se identifican jornada, personal, vehículo, punto y registro. En diseño se establecen estados y servicios responsables de validar las transiciones. En implementación, estas reglas se materializan en los servicios de operaciones.

La verificación comprueba asignaciones inválidas, conflictos de turno y cierre con puntos pendientes. La validación debe contrastar que la secuencia representa el trabajo de la DSU. Así, el mismo caso de uso conecta necesidades, decisiones de diseño y evidencias, sin depender de que cada flujo se ejecute una sola vez.

<!-- modelos puds -->

# 3. Manual de calidad (SQAP)

## 3.1. Introducción

El aseguramiento de la calidad del software (SQA) es el conjunto de actividades de protección que se aplican a lo largo de todo el ciclo de vida del software con el propósito de asegurar su calidad. El SQAP es el manual de calidad que documenta esas actividades. El PAPS organiza el proceso de ingeniería de software que produce el sistema; el SQAP define las actividades de SQA que, aplicadas a ese proceso y a sus productos, permiten aspirar a una certificación. Por eso SQA y el proceso de ingeniería de software trabajan juntos en todas las fases.

El Plan de Aseguramiento de la Calidad del Software establece cómo el Grupo 8 organizará las revisiones, las pruebas y el tratamiento de problemas del sistema DSU. Su propósito es que cada decisión de calidad se apoye en requisitos identificables y evidencias conservadas. Se aplica a los documentos, modelos, código, datos de prueba, componente predictivo y materiales de entrega.

El aseguramiento de calidad acompañará las fases de Inicio, Elaboración, Construcción y Transición. Las actividades previstas en este plan se expresan como compromisos de trabajo; las verificaciones ya ejecutadas se identifican con su registro y alcance en el capítulo 9. La aprobación académica del informe, la aceptación institucional del producto y una eventual certificación externa son resultados diferentes.

Aplicar SQA tiene costos: más tiempo y esfuerzo en el proceso, más documentación y riesgo de burocracia, que en proyectos pequeños puede volverlo poco práctico. Por eso este plan se ajusta a un equipo de dos integrantes y concentra los controles en los productos críticos. A cambio, reduce los defectos que llegan al usuario y facilita el mantenimiento del sistema.

### 3.1.1. Objetivo general

Asegurar que el sistema web de gestión de residuos sólidos de la DSU-UAGRM y su documentación cumplan los requisitos acordados, mediante revisiones, pruebas y registros que permitan demostrar la calidad de cada entrega.

### 3.1.2. Objetivos específicos

- Desarrollar el software a partir del análisis de las necesidades de la DSU, con requisitos identificados y verificables.
- Diseñar e implementar el sistema según los estándares de codificación, comentarios y base de datos definidos en este plan.
- Definir los atributos de calidad que se verificarán en el producto y la evidencia que los respalda.
- Describir las tareas de calidad de cada fase de PUDS, sus responsables y sus registros.
- Controlar la configuración y las versiones del código, los modelos y los documentos.
- Registrar los problemas detectados y comprobar sus correcciones antes de liberar una versión.

## 3.2. Misión

La misión del equipo es construir y documentar una solución que permita a la DSU registrar su operación y utilizar información consistente para planificar la recolección.

## 3.3. Visión

La visión del equipo es disponer de un producto mantenible que pueda evaluarse en un piloto institucional y evolucionar a partir de las necesidades verificadas de sus usuarios.

## 3.4. Valores

El trabajo se orientará por responsabilidad sobre los datos, trazabilidad de las decisiones, revisión entre integrantes y transparencia sobre las limitaciones.

### 3.4.1. Lema

**«Datos confiables, campus limpio».** El lema resume el compromiso del equipo: la calidad del sistema se mide por la confiabilidad de los datos que registra, analiza y proyecta, porque de ellos dependen la planificación de la recolección y la limpieza del campus universitario.

## 3.5. Propósito

Este plan define las actividades, los responsables y los registros con los que el equipo asegurará la calidad del sistema DSU durante las cuatro fases de PUDS. Su objetivo es detectar defectos antes de la entrega y dejar evidencia de cada comprobación.

### 3.5.1. Descripción

Con la aplicación de este SQAP se busca que el sistema DSU cumpla los siguientes atributos de calidad del software, organizados según ISO/IEC 25010:2023 y controlados con la evidencia indicada en la sección 3.9:

- **Correcto:** cada función responde a un requisito RF y a un caso de uso identificados.
- **Eficiente:** los tiempos de respuesta y la carga se miden frente a los requisitos de rendimiento.
- **Fiable:** las operaciones inválidas se rechazan sin dejar registros inconsistentes y la base de datos cuenta con respaldo diario.
- **Fácil de usar:** las tareas de registro y consulta pueden realizarse en escritorio y en teléfono.
- **Fácil de mantener:** el código se organiza en módulos por responsabilidad y cada cambio se acompaña de su prueba de regresión.
- **Seguro e íntegro:** el acceso se controla por rol y sector, y toda escritura queda en una bitácora inalterable.
- **Portable:** el backend se ejecuta en contenedores Docker y el frontend en cualquier navegador actualizado.

El plan se aplica a todo el producto y a cualquier versión posterior que el equipo desarrolle para la DSU.

### 3.5.2. Política de calidad

La política exige que todo entregable tenga un responsable, una versión, criterios de revisión y un registro de observaciones. Los requisitos se conservarán con sus identificadores; los cambios del sistema deben propagarse a modelos y pruebas. Ninguna función se considerará aceptada únicamente porque su pantalla esté disponible o porque el código compile.

### 3.5.3. Alcance

El plan cubre acceso, catálogos, operación, logística, analítica, cartografía, predicción y administración. La evaluación de los servicios externos se limita a su integración y a los compromisos documentados del proveedor. No comprende una auditoría interna de Neon, AWS, Vercel o Microsoft.

### 3.5.4. Criterio de liberación

Se impide la liberación de una versión con defectos críticos abiertos. Para un defecto de severidad alta se requerirá resolución o aceptación explícita del riesgo por quien tenga autoridad sobre la entrega. Las observaciones de presentación podrán tratarse por separado, siempre que no oculten información necesaria para utilizar el producto.

## 3.6. Documentos de referencia

Se toman como entradas la especificación DSU, el modelo de casos de uso, los modelos de análisis y diseño, la configuración del producto y los registros técnicos de pruebas. El PAPS determina organización y recursos; el SQAP define controles; el informe de pruebas conserva resultados concretos.

Los ejemplos académicos emplean IEEE 730 en ediciones anteriores. La ficha oficial consultada identifica IEEE 730-2026 como estándar de procesos de aseguramiento de calidad. Se utiliza su descripción pública para orientar la planificación y el control, sin declarar una evaluación de conformidad cláusula por cláusula. ISO/IEC 25010:2023 se consulta como referencia para organizar atributos de calidad del producto. Las condiciones medibles de aceptación provienen de los requisitos DSU y de los acuerdos de revisión, no de metas inventadas a partir del nombre de una norma (IEEE SA, 2026; ISO, 2023).

Los estándares con los que puede certificarse la calidad del software son ISO 9001, que para el software se aplica con la guía ISO 9000-3 (actualmente ISO/IEC/IEEE 90003); IEEE 730, que define el plan de aseguramiento de la calidad; y CMMI, que evalúa la madurez del proceso en niveles progresivos. Este plan sigue la estructura de IEEE 730 porque se orienta a un proyecto concreto y no a la certificación de una organización; ISO 9001 y CMMI quedan como referencia para una certificación futura.

## 3.7. Gestión

### 3.7.1. Organización

Las organizaciones que intervienen en el desarrollo y en el aseguramiento de la calidad del sistema DSU son el grupo de desarrollo, el consultor o especialista en SQA, el cliente y el grupo SQA.

#### 3.7.1.1. Organización del grupo de desarrollo

Es la organización encargada de construir el sistema. La integran los dos miembros del Grupo 8, que trabajan según la especificación de requisitos acordada con la DSU y los criterios de la materia. Prepara los productos de cada fase, corrige las observaciones e informa su avance al consultor. Carlos Gabriel Lobo Gutiérrez asume la coordinación, que consolida el avance, la programación y las decisiones.

#### 3.7.1.2. Organización del consultor o especialista en SQA

El docente de Ingeniería de Software 2 cumple este papel. Establece los criterios de los entregables, revisa los avances en las presentaciones y verifica que se cumplan los acuerdos. Actúa como intermediario entre las necesidades de la DSU y el trabajo del grupo de desarrollo.

#### 3.7.1.3. Organización del cliente

El cliente es quien patrocina el proyecto y busca una solución de software: la Dirección de Servicios Universitarios (DSU) de la UAGRM. Intervienen la dirección, que decide la aceptación institucional; los supervisores de recolección, que conocen la planificación y el control de las jornadas; y el personal operativo de limpieza, que realiza el registro en campo. La DSU proporciona la información operativa y valida la utilidad del sistema.

#### 3.7.1.4. Organización del grupo SQA

Se conforma con representantes de las tres organizaciones anteriores: el responsable de SQA del grupo de desarrollo, el consultor y el representante designado por la DSU. Analiza las observaciones, decide su tratamiento y aprueba las versiones sucesivas de este plan. Al tratarse de un equipo de dos integrantes, la función de revisión se alterna por actividad, de modo que quien elaboró un artefacto no sea su único revisor.

### 3.7.2. Tareas y actividades

<!-- anchos: 3.2,5.5,3.8,4.29 -->
| Fase de PUDS | Actividad de aseguramiento de calidad | Producto revisado | Registro |
| --- | --- | --- | --- |
| Inicio | Revisar alcance, actores y riesgos iniciales | PAPS y perfil | Lista de revisión |
| Elaboración | Revisar requisitos, casos de uso y arquitectura | Especificación y modelos UML | Hallazgos y trazabilidad RF–CU |
| Construcción | Revisar código, ejecutar regresión y registrar defectos | Incrementos del sistema | Reportes de pruebas y problemas |
| Transición | Verificar instalación, manual y versión de entrega | Producto y documentación | Lista de liberación |
| Todas | Controlar cambios y actualizar riesgos | Línea base | Registro de cambios |

Las tareas del grupo de desarrollo asociadas al ciclo de vida son las siguientes:

| Fase | Actividades del grupo de desarrollo | Productos |
| --- | --- | --- |
| Inicio | Identificar actores y necesidades con la DSU, delimitar el alcance, estimar el esfuerzo e identificar los riesgos iniciales | Perfil, PAPS y registro de riesgos |
| Elaboración | Especificar RF1–RF27 y los requisitos no funcionales, modelar los 34 casos de uso, definir paquetes, clases, base de datos y arquitectura | Especificación de requisitos, modelos UML y arquitectura |
| Construcción | Implementar backend, frontend, ETL y componente predictivo por incrementos, escribir las pruebas automatizadas y corregir defectos | Código, migraciones, pruebas y registros de problemas |
| Transición | Preparar el despliegue, el manual de usuario y la capacitación, ejecutar las pruebas de aceptación y entregar la versión | Versión liberada, manual y evidencias |

Las actividades del grupo SQA y sus entregables son:

| Actividad del grupo SQA | Entregable asociado |
| --- | --- |
| Elaborar el plan de SQA | Plan de SQA (este capítulo) |
| Identificar los atributos de calidad del producto | Descripción de atributos (2.5.1) y aspectos de calidad (2.9.2) |
| Evaluar la calidad de los productos | Informe de revisión SQA |
| Revisar el ajuste al proceso | Informe de revisión SQA del ajuste al proceso |
| Realizar las revisiones técnicas formales | Informe de RTF |
| Verificar la gestión de configuración | Registro de líneas base y de cambios |
| Dar seguimiento a los problemas y acciones correctivas | Registro de problema y acción correctiva (anexo B) |
| Realizar las auditorías funcional y física | Informes de auditoría y lista de liberación |
| Evaluar y ajustar el plan de SQA | Historial de cambios del SQAP |

### 3.7.3. Roles y responsabilidades

| Función | Responsabilidad | Registro requerido |
| --- | --- | --- |
| Responsable del entregable | Elaborar y mantener el producto; atender observaciones | Versión y lista de cambios |
| Revisor del equipo | Comprobar criterios y registrar hallazgos reproducibles | Lista de revisión y decisión |
| Coordinación | Priorizar trabajo y resolver dependencias | Acuerdos y seguimiento |
| Representante de la DSU | Contrastar la utilidad operativa en las revisiones y validaciones | Acta de validación o aceptación |
| Docente (consultor SQA) | Evaluar los entregables de Software 2 y verificar que se atiendan sus observaciones | Observaciones académicas recibidas |

Las funciones se asignan a los integrantes del grupo de la siguiente forma:

<!-- anchos: 4.4,4.4,7.99 -->
| Integrante | Función | Responsabilidades de calidad |
| --- | --- | --- |
| Carlos Gabriel Lobo Gutiérrez | Coordinador y responsable de la configuración | Programación del trabajo, inventario de entregables, control de las líneas base y de los cambios, e integración a la rama principal |
| Leonardo Serrate Basma | Responsable de SQA | Mantenimiento de este plan, conducción de las RTF y auditorías, registro de hallazgos y seguimiento de problemas |

Ambos integrantes desarrollan y cada uno revisa los productos que elaboró el otro; la liberación de una versión requiere la conformidad de los dos.

#### 3.7.3.1. Responsabilidades del grupo de desarrollo

- Elaborar los productos de cada fase conforme a la especificación y a los estándares de la sección 3.9.
- Mantener la trazabilidad entre requisitos, casos de uso, modelos, código y pruebas.
- Ejecutar las pruebas automatizadas antes de integrar cada cambio.
- Corregir los defectos asignados y dejar evidencia de la corrección.
- Entregar los productos a revisión en una versión identificada.

#### 3.7.3.2. Responsabilidades del cliente

- Proporcionar la información operativa: sectores, puntos de recolección, tipos de residuo y forma de trabajo de las cuadrillas.
- Designar un representante para las revisiones y validaciones.
- Revisar los prototipos y las versiones entregadas, y comunicar sus observaciones.
- Decidir la aceptación institucional del producto.

#### 3.7.3.3. Responsabilidades del grupo SQA

- Mantener y actualizar este plan.
- Planificar y conducir las revisiones de la agenda (2.10.5).
- Verificar el cumplimiento de los estándares y del proceso.
- Dar seguimiento a los problemas hasta su cierre y autorizar la liberación según el criterio de 2.5.4.
- Conservar los registros de calidad.

## 3.8. Documentación

### 3.8.1. Propósito

Esta sección identifica los documentos que gobiernan el desarrollo, la verificación y el uso del sistema, y la comprobación de calidad que se aplica a cada uno.

### 3.8.2. Documentación mínima requerida

| Producto | Contenido mínimo | Comprobación de calidad |
| --- | --- | --- |
| Especificación | Requisitos, actores, restricciones y criterios | Claridad, consistencia y posibilidad de prueba |
| Modelo de casos de uso | Actor, propósito, precondiciones, flujo y excepciones | Correspondencia con RF y permisos |
| Análisis y diseño | Paquetes, entidades, interacciones y arquitectura | Correspondencia con casos de uso e implementación |
| Código y configuración | Componentes y dependencias identificados | Revisión técnica y ejecución reproducible |
| Plan e informe de pruebas | Casos, datos, entorno, resultados y defectos | Separación entre resultado esperado y observado |
| Material de entrega | Instalación, manual y limitaciones | Reproducción de los pasos por otra persona |

Las fuentes de diagramas se conservarán junto a sus exportaciones.

#### 3.8.2.1. Especificación de requisitos de software (ERS)

La especificación sigue la estructura de IEEE 830-1998: introducción (propósito, ámbito, definiciones y referencias), descripción general (perspectiva y funciones del producto, características de los usuarios, restricciones, dependencias y modelo de dominio) y requisitos específicos. Es la entrada de la revisión de requisitos y la referencia de todas las pruebas. Sus requisitos se agrupan así:

<!-- anchos: 4,3,9.79 -->
| Grupo | Identificadores | Contenido |
| --- | --- | --- |
| Requisitos funcionales | RF1–RF27 | Acceso, catálogos, registro operativo, recolección, analítica, cartografía, predicción y administración |
| Requisitos no funcionales | RNF1–RNF26 | Rendimiento, usabilidad, fiabilidad, seguridad, portabilidad, mantenibilidad, precisión, auditabilidad e interoperabilidad |
| Interfaces | RI1–RI17 | Interfaces de usuario, de hardware, de software y de comunicación |
| Base de datos | RBD1–RBD22 | Entidades, unicidad, integridad, precisión de cantidades y coordenadas, histórico y bitácora inalterable |
| Diseño | RD1–RD15 | Python, Django REST Framework, React, PostgreSQL, scikit-learn, Leaflet, Power BI, arquitectura modular y UML |
| Tiempo de respuesta | RTR1–RTR12 | Desde 2 segundos para autenticación y búsquedas hasta 10 minutos para el entrenamiento asíncrono |
| Capacidad y carga | RCM1–RCM8 | 12 usuarios concurrentes, 500 puntos de recolección, 100 000 observaciones y horizonte de 30 días |
| Uso de recursos | RUR1–RUR7 | Límites de procesador y memoria, procesos asíncronos y ancho de banda reducido en campo |
| Disponibilidad | RDI1–RDI7 | 99 % en horario laboral, captura en campo durante los turnos y recuperación ante fallos |

Cada requisito debe ser correcto, completo, consistente, no ambiguo, verificable, modificable y trazable a su origen y a sus casos de uso.

#### 3.8.2.2. Descripción del diseño del software (SDD)

La descripción del diseño detalla cómo se estructura el sistema para cumplir la ERS. Se documenta con los modelos UML de PUDS del capítulo 2 y cubre cuatro vistas:

- **Descomposición en módulos.** Ocho paquetes: Gestión de Usuarios y Control de Acceso; Gestión Topológica y Puntos de Recolección; Gestión de Residuos; Gestión de Recolecciones y Logística; Inteligencia de Negocios y Analítica Visual; Componente Cartográfico y Análisis Espacial; Predicción mediante Random Forest Regressor; y Administración de la Plataforma y Auditoría. Se implementan en las aplicaciones de Django `accounts`, `campus`, `catalogs`, `operations`, `analytics`, `prediction` y `audit`, y en las pantallas de React.
- **Descomposición en procesos concurrentes.** La API atiende las peticiones con varios procesos de Gunicorn; el ETL y el entrenamiento del modelo se ejecutan en segundo plano para no bloquear la operación (RD10); el ETL programado se lanza con un comando de Django desde cron, y el respaldo de la base de datos corre en un contenedor propio.
- **Descomposición de datos.** Base PostgreSQL en tercera forma normal para el plano transaccional, con una tabla de hechos y vistas `bi_` para el plano analítico, y una bitácora protegida por disparador.
- **Interfaces.** API REST con JSON sobre HTTPS bajo `/api/`, autenticación con JWT, conexión de solo lectura para Power BI y cartografía de OpenStreetMap.

El diseño detallado (clases, secuencias, diseño lógico de la base de datos y componentes) se presenta en las secciones 3.12 a 3.15.

### 3.8.3. Plan de verificación y validación

La verificación y validación acompañan el ciclo de vida completo: cada fase de PUDS entrega productos que se verifican contra sus entradas antes de servir de base a la siguiente, y la validación con usuarios de la DSU se realiza sobre el producto de cada incremento. El plan genera los siguientes informes:

<!-- anchos: 3.6,3.4,5.6,4.19 -->
| Informe | Momento | Contenido | Ubicación |
| --- | --- | --- | --- |
| Reporte sumario de fase de V&V | Al cerrar cada fase de PUDS | Productos revisados, pruebas ejecutadas, hallazgos abiertos y cerrados, y decisión de continuar | Registro de revisión técnica (anexo A) |
| Reporte de anomalías | Cuando se detecta una desviación | Identificador, versión, pasos de reproducción, severidad, responsable y estado | Registro de problema y acción correctiva (anexo B) |
| Reporte final de V&V | Antes de la entrega | Resumen de todas las pruebas, defectos residuales, riesgos aceptados y recomendación de liberación | Capítulo 9 y lista de liberación |

La verificación y validación se aplican a los procesos del ciclo de vida de la siguiente forma:

| Proceso | Tareas de V&V en el proyecto DSU |
| --- | --- |
| Gestión | Planificar las revisiones de la agenda, asignar responsables y evaluar los resultados de cada fase |
| Adquisición | Contrastar con la DSU las necesidades y el alcance antes de fijar la línea base de requisitos |
| Suministro | Verificar que cada entrega contenga la versión, la documentación y las evidencias acordadas |
| Desarrollo | Verificar requisitos, diseño, código e integración, y ejecutar las pruebas en cada incremento |
| Operación | Validar con usuarios de la DSU las tareas de registro, planificación y consulta en producción |
| Mantenimiento | Analizar el impacto de cada cambio y repetir la regresión pertinente |

### 3.8.4. Documentación de usuario

La documentación de usuario permite que cada rol opere el sistema sin asistencia del equipo. Toma como referencia IEEE 1063 y se entrega como manual por rol en el capítulo 12 y como documento independiente en la carpeta del proyecto.

| Componente | Contenido | Destinatario |
| --- | --- | --- |
| Acceso al sistema | Inicio y cierre de sesión | Todos los roles |
| Registro en campo | Jornada asignada, vaciados e incidencias desde el teléfono | Personal operativo |
| Planificación y control | Jornadas, personal, vehículos, seguimiento, cierre, incidencias y recomendaciones | Supervisor |
| Consulta y decisión | Tableros, mapa de calor, predicciones y reportes | Directivo |
| Administración | Usuarios, roles, catálogos, parámetros, ETL, modelo y bitácora | Administrador |

Cada tarea se describe con pasos y la pantalla donde se realiza. Antes de la entrega, otra persona reproduce los pasos del manual con la versión entregada.

## 3.9. Estándares, prácticas, convenciones y métricas

### 3.9.1. Propósito

Esta sección fija las convenciones de identificación y revisión que deben cumplir los productos del proyecto y las métricas con que se evalúan.

### 3.9.2. Contenido

Los requisitos y casos de uso conservarán los identificadores RF y CU. Los casos de prueba usarán identificadores diferenciados y una referencia al requisito comprobado. Los hallazgos se registrarán con un identificador, severidad, versión afectada, evidencia, responsable y estado. Los nombres de documentos y archivos deben permitir identificar su contenido sin incluir credenciales ni datos personales innecesarios.

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

Los indicadores del PAPS se aplicarán a un universo definido.

### 3.9.3. Estándar de codificación

Las normas de codificación del sistema se detallan en el anexo I y se resumen así:

- El software se divide en módulos independientes según el diseño: una aplicación de Django por área funcional y, dentro de cada una, un paquete por responsabilidad (`models/`, `serializers/`, `views/`, `services/`, `permissions/`, `tests/`) con un archivo por entidad.
- Los nombres de funciones, clases y variables indican su función: `snake_case` y `PascalCase` en Python; `camelCase` y `PascalCase` en TypeScript.
- El backend sigue PEP 8 con un máximo de 120 caracteres por línea, verificado con Ruff; el frontend se verifica con oxlint y con la compilación de TypeScript sin errores.
- Los mensajes de error indican el campo o la regla que los originó, en español, con los códigos HTTP estándar.
- Las credenciales y los parámetros de entorno nunca se escriben en el código fuente.
- Cada archivo conserva su autoría, fecha e historial de cambios en el control de versiones de Git, sin repetirlos en cabeceras manuales.

### 3.9.4. Estándar de comentarios

- Un comentario explica por qué se realiza una acción o qué regla de negocio se aplica; no repite lo que el código ya expresa.
- Los comentarios se escriben en español y en líneas separadas del código que explican.
- Las descripciones de módulos, clases y funciones se escriben en comentarios de varias líneas (docstrings en Python); las aclaraciones puntuales, en comentarios de una línea.
- Un comentario que deja de corresponder al código se corrige o se elimina en el mismo cambio.

### 3.9.5. Responsables de verificar el cumplimiento

El cumplimiento de los estándares lo verifican:

- El coordinador del grupo de desarrollo, que revisa cada cambio antes de integrarlo a la rama principal.
- El grupo SQA, que comprueba los estándares en las revisiones técnicas formales y en las auditorías previas a la entrega.
- Las herramientas automáticas (Ruff, oxlint y el compilador de TypeScript), cuya ejecución sin errores es condición para integrar un cambio.

## 3.10. Revisiones de software

### 3.10.1. Propósito

Las revisiones comprueban cada producto contra sus entradas antes de que sirva de base al siguiente flujo de trabajo.

### 3.10.2. Requisitos mínimos

Se planifican revisiones de requisitos, arquitectura, implementación, pruebas y entrega. Cada revisión comenzará con una versión cerrada para inspección y una lista de criterios. El revisor documentará observaciones verificables, el responsable propondrá su tratamiento y ambos comprobarán el cierre. El registro conservará los desacuerdos y las decisiones que afecten al alcance.

La revisión de requisitos comprobará que cada RF tenga actor o destinatario, reglas observables y al menos un criterio de prueba. La revisión de arquitectura verificará dependencias, interfaces, persistencia y separación de operación y analítica. La revisión de entrega verificará que manuales, versión instalada y evidencias correspondan al mismo producto.

Las revisiones y auditorías mínimas son las siguientes:

<!-- anchos: 3.4,5.2,8.19 -->
| Revisión | Objetivo | Criterios principales en DSU |
| --- | --- | --- |
| Revisión de requisitos (SRR) | Asegurar que la ERS es correcta, completa y verificable | Cada RF tiene actor, reglas observables y criterio de prueba, y está cubierto por al menos un caso de uso; los requisitos no funcionales tienen valores medibles |
| Revisión del diseño preliminar (PDR) | Evaluar la arquitectura antes del diseño detallado | Interfaces externas (Neon, AWS, Vercel, Power BI, OpenStreetMap) identificadas con su protocolo; planos transaccional y analítico separados; procesos pesados asíncronos; control de acceso en interfaz y servicios |
| Revisión del diseño crítico (CDR) | Confirmar que el diseño detallado satisface la ERS antes de codificar | Clases con atributos, métodos, visibilidad y multiplicidades; base de datos en 3FN con desnormalización justificada; interacciones con la base de datos expresadas |
| Revisión del plan de V&V (SVVPR) | Evaluar si los métodos de V&V son adecuados | Cada requisito tiene caso de prueba con entrada, resultado esperado y entorno; la programación indica qué se prueba, cuándo y quién |
| Auditoría funcional | Verificar antes de la entrega que el sistema hace todo y solo lo que indica la ERS | Cada RF1–RF27 con evidencia de prueba aprobada; las pruebas no ejecutadas se listan con su justificación |
| Auditoría física | Verificar que el código y su documentación son consistentes | Los modelos UML coinciden con las clases y tablas implementadas; el manual describe las pantallas entregadas; el despliegue se reproduce con sus instrucciones |
| Auditoría del proceso | Verificar la consistencia del producto durante el desarrollo | Código frente a diseño, interfaces frente a requisitos y pruebas frente a RF al cerrar cada incremento |
| Revisión de gestión | Evaluar la ejecución de este plan | Observaciones del consultor en cada presentación de avance y actualización del SQAP |

Cada revisión registra su objetivo, el producto evaluado, el responsable, los participantes, los criterios aplicados y la ubicación de sus resultados.

### 3.10.3. Otras revisiones y auditorías

Además de las revisiones por producto, se revisa el proceso en los momentos siguientes. No se prevé una auditoría externa al proyecto.

| Momento | Entrada | Resultado de la revisión |
| --- | --- | --- |
| Antes de ampliar alcance | Solicitud y requisitos afectados | Decisión y actualización de la línea base |
| Antes de integrar cambios | Código y modelos modificados | Hallazgos técnicos y regresión pertinente |
| Al cerrar una iteración | Incremento y pruebas | Aceptación interna o actividades pendientes |
| Antes de entregar | Versión candidata y documentación | Lista de liberación y riesgos residuales |

### 3.10.4. Tipos de revisión

<!-- anchos: 3.4,4.6,5.4,3.39 -->
| Revisión | Objetivo | Mecanismo | Salida |
| --- | --- | --- | --- |
| Evaluación de la calidad de los productos | Revisar los productos clave y detectar desviaciones respecto de los estándares y objetivos de calidad | Se revisa cada producto con su lista de criterios; se comprueba que no queden observaciones pendientes de revisiones anteriores | Informe de revisión SQA con las desviaciones y sus responsables |
| Revisión del ajuste al proceso | Comprobar que los productos se obtuvieron con las actividades definidas en PUDS | Se rastrean hacia atrás los productos de entrada (PAPS, plan de iteración y plan de V&V) y se verifica que cada paso se haya seguido | Informe de revisión SQA del ajuste al proceso |
| Revisión técnica formal (RTF) | Descubrir errores de función, lógica o implementación y verificar que el producto satisface su especificación y los estándares | Reunión convocada con anticipación entre el responsable de SQA y el grupo de desarrollo; los participantes estudian el producto antes y llevan sus preguntas | Informe de RTF con hallazgos, decisiones y responsables |

La RTF se reserva para los productos de mayor importancia. Como mínimo se revisan la especificación de requisitos, el modelo de diseño, el plan de verificación y validación, el PAPS, la gestión de configuración, el diseño frente a la especificación, la implementación frente al diseño y las pruebas frente a la especificación.

### 3.10.5. Agenda de revisiones

Las revisiones de calidad se organizan por fase e iteración de PUDS. Los periodos siguen el cronograma del proyecto (sección 1.5.3), del 18 de agosto al 19 de diciembre de 2026, y cada revisión se realiza al cierre de su iteración:

<!-- anchos: 3.2,2.6,5.2,5.79 -->
<!-- anchos: 2.5,2.1,2.9,4.6,4.69 -->
| Fase | Iteración | Periodo previsto | Revisiones | Productos revisados |
| --- | --- | --- | --- | --- |
| Inicio | Iteración 1 | 18/08 al 14/09 | Evaluación de calidad y RTF del alcance | Perfil, PAPS, actores y riesgos iniciales |
| Elaboración | Iteración 2 | 15/09 al 05/10 | Revisión de requisitos (SRR) | Especificación RF1–RF27 y modelo de casos de uso |
| Elaboración | Iteración 3 | 06/10 al 26/10 | PDR, CDR, revisión del plan de V&V y ajuste al proceso | Paquetes, realizaciones, clases, base de datos, arquitectura y plan de pruebas |
| Construcción | Iteración 4 | 27/10 al 05/11 | Evaluación de calidad y auditoría del proceso | Acceso y catálogos |
| Construcción | Iteración 5 | 06/11 al 16/11 | Evaluación de calidad y auditoría del proceso | Registro de residuos, recolección y logística |
| Construcción | Iteración 6 | 17/11 al 26/11 | Evaluación de calidad y auditoría del proceso | ETL, indicadores, tableros y cartografía |
| Construcción | Iteración 7 | 27/11 al 07/12 | Evaluación de calidad y RTF del componente predictivo | Predicción, recomendaciones y administración |
| Transición | Iteración 8 | 08/12 al 19/12 | Auditoría funcional, auditoría física, revisión de la documentación de usuario y revisión de gestión | Versión candidata, manual de usuario y evidencias de pruebas |

## 3.11. Prueba

La verificación responde a la pregunta «¿estamos construyendo el producto correctamente?» y se enfoca en el proceso: contrasta los productos de trabajo con sus requisitos y especificaciones. La validación responde a la pregunta «¿estamos construyendo el producto correcto?» y se enfoca en el producto: determina si la solución satisface el uso previsto y las necesidades de sus destinatarios. Ambas pueden aplicarse durante el desarrollo: una revisión de casos de uso verifica consistencia; una demostración de un prototipo con usuarios permite validar la interacción propuesta. Esta distinción se apoya en las definiciones y orientaciones de NASA sobre verificación y validación; no implica adoptar los requisitos de un proyecto aeroespacial (NASA, s. f.).

Para DSU, la verificación abarcará reglas de jornadas, permisos, cantidades, ETL, reportes y restricciones predictivas. La validación institucional debe comprobar tareas como registrar un vaciado, atender una incidencia y utilizar una recomendación en la planificación.

La estrategia de pruebas combina casos funcionales, análisis estructural de funciones críticas, revisión de seguridad y mediciones de rendimiento. Las pruebas utilizarán entornos aislados cuando impliquen creación o modificación de datos. Los resultados se registrarán con su versión y no se reutilizarán como evidencia de una versión diferente sin analizar el impacto del cambio.

En PUDS, la verificación revisa que cada fase y cada flujo de trabajo se hayan cumplido correctamente: por ejemplo, que la captura de requisitos haya producido los actores, los casos de uso con su detalle y el diagrama general antes de pasar al análisis. La validación se realiza con el cliente: mientras todavía no hay software, como en la captura de requisitos, se valida con prototipos de interfaz; desde la construcción, con la versión de cada incremento.

### 3.11.1. Niveles y tipos de prueba

<!-- anchos: 3,5.6,5,3.19 -->
| Nivel o tipo | Objetivo | Herramienta o técnica | Responsable |
| --- | --- | --- | --- |
| Unitaria | Comprobar reglas de servicios, modelos y validaciones | pytest y pytest-django | Grupo de desarrollo |
| Integración | Comprobar los endpoints de la API con permisos por rol y base de datos real | pytest sobre PostgreSQL desechable | Grupo de desarrollo |
| Sistema | Comprobar los flujos completos de los casos de uso críticos | Casos de caja negra (capítulo 9) | Grupo SQA |
| Caja blanca | Analizar los caminos de funciones críticas | Grafo de flujo y complejidad ciclomática | Grupo SQA |
| Seguridad | Detectar configuraciones inseguras | OWASP ZAP en entorno aislado | Grupo SQA |
| Interfaz | Verificar las pantallas por rol en escritorio y teléfono | Revisión a 1440 y 390 píxeles | Grupo SQA |
| Rendimiento y carga | Contrastar tiempos con RTR y carga con RCM | Medición en entorno comparable a producción | Grupo SQA |
| Aceptación | Validar tareas reales con usuarios de la DSU | Registro de validación (anexo C) | Cliente y grupo SQA |

### 3.11.2. Criterios de entrada y salida

Una prueba se inicia con una versión identificada, las migraciones aplicadas, los datos de prueba preparados en un entorno aislado y los casos revisados. Se da por concluida cuando todos los casos se ejecutaron o tienen justificación, no quedan defectos críticos abiertos, los defectos altos están resueltos o aceptados según 2.5.4 y los resultados quedan registrados con versión y entorno.

## 3.12. Gestión de configuración

El objetivo del aseguramiento de calidad en esta área es comprobar que las actividades de gestión de configuración descritas en el capítulo 6 se realizan según lo establecido. Los elementos de configuración son el código del backend y del frontend, las migraciones de la base de datos, la configuración de despliegue, el modelo UML de Enterprise Architect, los documentos del proyecto y los artefactos del modelo predictivo.

Las actividades mínimas de control son las siguientes:

- Comprobar que la línea base de cada fase se establece en el momento previsto por PUDS: requisitos al cerrar la elaboración, diseño antes de la construcción y versión candidata antes de la transición.
- Comprobar que la línea base es correcta, es decir, que el código, los modelos y los documentos registrados corresponden a la misma versión del producto.
- Verificar periódicamente que el responsable de la configuración (el coordinador del grupo de desarrollo) mantiene el control de la línea base y el registro completo de cambios de requisitos, diseño, código, pruebas y documentación.
- Verificar que toda solicitud de cambio pase por el grupo SQA, que actúa como comité de control de cambios: se registra el motivo, se analizan los productos afectados y se decide su aprobación antes de modificar la línea base.
- Comprobar que un cambio aprobado se propaga a todos los productos afectados: casos de uso, modelos de análisis y diseño, base de datos, pruebas e interfaces.

### 3.12.1. Elementos de configuración

<!-- anchos: 4,6.2,6.59 -->
| Elemento | Identificación | Ubicación |
| --- | --- | --- |
| Código del backend y del frontend | Confirmaciones de Git y etiqueta de versión | Carpetas `backend/` y `frontend/` del repositorio |
| Esquema de la base de datos | Migraciones numeradas de Django | Carpeta `migrations/` de cada aplicación |
| Configuración de despliegue | Dockerfile, archivos compose y Caddyfile versionados | Carpeta `deploy/` del backend |
| Modelo UML | Archivo de Enterprise Architect versionado | `modelo_uml/DSU-FaseFinal.eapx` |
| Documentos del proyecto | Nombre y fecha de versión | Repositorio y carpeta compartida |
| Modelo predictivo | Versión registrada en cada entrenamiento | Base de datos y artefacto `.joblib` |

### 3.12.2. Líneas base

| Línea base | Momento | Contenido |
| --- | --- | --- |
| Requisitos | Fin de la iteración 2 (elaboración) | ERS y modelo de casos de uso aprobados en la SRR |
| Diseño | Fin de la iteración 3 (elaboración) | Modelos de análisis y diseño aprobados en la PDR y la CDR |
| Producto | Cierre de cada incremento | Código, migraciones y pruebas del incremento |
| Entrega | Transición | Versión etiquetada, manual y evidencias auditadas |

## 3.13. Notificación de problemas y acción correctiva

### 3.13.1. Propósito

Esta sección establece cómo se registran, corrigen y cierran los problemas detectados en revisiones, pruebas u operación.

### 3.13.2. Flujo de trabajo

El flujo es registro, clasificación, asignación, corrección, verificación y cierre. Si no se reproduce un problema, se conservarán las condiciones conocidas y la información faltante. Si una corrección no satisface el caso que originó el hallazgo, se reabrirá el registro.

| Estado | Significado | Quién lo asigna |
| --- | --- | --- |
| Abierto | Problema registrado con su evidencia | Quien lo detecta |
| Asignado | Clasificado por severidad y con responsable | Grupo SQA |
| En corrección | El responsable trabaja en la solución | Grupo de desarrollo |
| En verificación | Corrección integrada, pendiente de prueba | Grupo de desarrollo |
| Cerrado | Corrección comprobada con la prueba que lo detectó y la regresión | Grupo SQA |
| Reabierto | La corrección no resolvió el caso | Grupo SQA |

### 3.13.3. Clasificación de severidad

| Severidad | Criterio | Tratamiento |
| --- | --- | --- |
| Crítica | Pérdida de datos, acceso indebido grave o indisponibilidad total | Bloquear liberación y priorizar corrección |
| Alta | Función principal inutilizable o resultado relevante incorrecto | Corregir antes de aceptar el flujo afectado |
| Media | Fallo con alternativa operativa y alcance acotado | Planificar corrección y documentar alternativa |
| Baja | Presentación o detalle sin impedir la tarea | Incluir en mantenimiento según prioridad |

La severidad describe el efecto; la prioridad define el orden de atención y considera dependencias y exposición. Toda aceptación temporal de un defecto debe indicar quién la autorizó, a qué versión aplica y qué limitación debe comunicarse.

### 3.13.4. Métricas de seguimiento

Se registrarán los defectos abiertos por severidad y versión, el tiempo entre registro y cierre, y los defectos reabiertos. Estos valores alimentan el indicador de defectos pendientes del PAPS.

## 3.14. Herramientas, técnicas y metodologías

| Herramienta, técnica o metodología | Uso en el aseguramiento de calidad |
| --- | --- |
| PUDS | Organiza el trabajo en fases e iteraciones dirigidas por casos de uso |
| Enterprise Architect | Modelos UML de requisitos, análisis y diseño, y trazabilidad RF–CU |
| Git y GitHub | Control de versiones, historial y revisión de cambios |
| pytest y pytest-django | Pruebas unitarias y de integración de la API con reportes JUnit |
| Ruff, oxlint y TypeScript | Análisis estático y comprobación de tipos del backend y del frontend |
| Docker | Entorno reproducible para las pruebas en Linux y para el despliegue |
| OWASP ZAP | Revisión de seguridad de la aplicación |
| Revisión técnica formal y listas de verificación | Detección temprana de defectos en documentos y modelos |
| Caja negra y caja blanca | Particiones de equivalencia, valores límite, caminos independientes y complejidad ciclomática |

Las capturas y registros de API se utilizarán como evidencia complementaria. El resultado de una herramienta se interpretará según su configuración y no como una certificación automática.

## 3.15. Control de código

Esta sección define los métodos y medios con que se controla el almacenamiento y el mantenimiento de las versiones del código:

- **Software controlado.** Todo el código del sistema: backend Django (`backend/`), frontend React (`frontend/`), migraciones de la base de datos, scripts de carga y respaldo, configuración de contenedores y despliegue, y los generadores de la documentación.
- **Identificación y catalogación.** Un único repositorio Git (ProyectoDSU) con la rama principal `main` como línea base. Cada confirmación describe un cambio completo; cada versión entregada se identifica con una etiqueta `vMAYOR.MENOR` que la relaciona con su documentación y sus evidencias de prueba.
- **Localización física.** Repositorio privado en GitHub (https://github.com/vangiewz/ProyectoDSU) y copias locales de trabajo de cada integrante.
- **Copias de seguridad.** El historial de Git queda replicado en GitHub y en cada copia local. La base de datos se respalda diariamente con `pg_dump` en un contenedor dedicado, que conserva los respaldos de los últimos 14 días.
- **Distribución de copias.** El acceso al repositorio se concede solo a los integrantes del equipo y a quienes el grupo autorice para la evaluación. Las copias entregadas para evaluación se publican en la carpeta compartida del proyecto, sin credenciales.
- **Documentación afectada.** Un cambio de código se acompaña de la actualización de los requisitos, modelos, pruebas y manual que describen el comportamiento modificado.
- **Construcción de una nueva versión.** Se ejecutan las comprobaciones de Ruff, oxlint y TypeScript y la regresión completa con pytest; se aplican las migraciones; se construye la imagen Docker del backend y la versión de producción del frontend, y se despliegan en sus entornos.

## 3.16. Control de medios

### 3.16.1. Propósito

El código, los documentos, los diagramas, los datos de prueba y los artefactos del modelo se tratarán como elementos de configuración. El acceso al repositorio privado se limitará al equipo autorizado. Las copias compartidas para evaluación deben revisarse para excluir secretos y datos personales no necesarios.

### 3.16.2. Matriz de control de medios

<!-- anchos: 3.4,5.2,3.6,4.59 -->
| Medio | Ubicación | Control de acceso | Respaldo |
| --- | --- | --- | --- |
| Código fuente | Repositorio Git ProyectoDSU en GitHub | Cuentas del equipo | Historial de Git y copias locales |
| Documentos y modelos UML | Repositorio y archivos de Enterprise Architect | Cuentas del equipo | Versiones fechadas del documento |
| Base de datos | PostgreSQL en Neon | Credenciales por variable de entorno | Respaldo diario con pg_dump |
| Evidencias de pruebas | Carpeta de auditoría del repositorio | Cuentas del equipo | Historial de Git |
| Modelo predictivo | Artefacto versionado por entrenamiento | Rol Administrador | Registro de versiones del modelo |

### 3.16.3. Roles y responsabilidades

Ambos integrantes administran el repositorio. Quien modifica un medio registra el cambio; el otro integrante lo revisa.

La base demo compartida no será utilizada para pruebas destructivas. Los cambios de estructura o datos se coordinarán entre integrantes.

## 3.17. Control de proveedores

Se registrarán proveedor, servicio utilizado, dependencia del sistema, responsable de acceso y condición de continuidad. Para Neon se comprobará conexión segura y persistencia; para Vercel y AWS, configuración y disponibilidad de los entornos; para Power BI, actualización y acceso al informe; para cartografía, atribución y disponibilidad de recursos.

<!-- anchos: 3.6,3.4,3.8,5.99 -->
| Proveedor | Servicio | Uso en DSU | Control |
| --- | --- | --- | --- |
| Neon | PostgreSQL gestionado | Base de datos de producción | Conexión cifrada y respaldo diario propio con pg_dump |
| Amazon Web Services | EC2 con Linux y Docker | Backend de producción | Configuración versionada y verificación de disponibilidad |
| Vercel | Hospedaje estático | Frontend | Publicación de la versión de producción con HTTPS |
| GitHub | Repositorio privado | Código y documentos | Acceso restringido y copias locales |
| Microsoft | Power BI | Tableros analíticos | Conexión de solo lectura a las vistas analíticas |
| OpenStreetMap | Teselas de mapa | Cartografía del campus | Atribución visible y disponibilidad del servicio |

## 3.18. Recopilación, mantenimiento y retención de registros

Cada evidencia conservará identificador, fecha, autor o herramienta, versión del producto, entorno y ubicación. Los resultados originales se mantendrán junto a una copia apta para revisión sin información sensible. Una corrección documental no debe reemplazar silenciosamente el resultado original de una prueba.

El equipo conserva registros durante el desarrollo y la evaluación académica, revisando después la retención con el destinatario institucional. El proceso es crear, identificar, almacenar, proteger, revisar y disponer cada registro.

<!-- anchos: 4.6,3.6,4.2,4.39 -->
| Tipo de registro | Formato | Ubicación | Retención mínima |
| --- | --- | --- | --- |
| Informes de revisión, RTF y auditoría | Documento | Repositorio | Hasta un año después del cierre del proyecto |
| Resultados de pruebas | XML JUnit, JSON y capturas | Carpeta de auditoría del repositorio | Vida útil de la versión probada |
| Registros de problemas | Formato del anexo B | Repositorio | Hasta un año después del cierre del proyecto |
| Bitácora de auditoría del sistema | Tabla de la base de datos | Neon | Permanente; no se modifica ni elimina |
| Respaldos de la base de datos | Archivo de pg_dump | Volumen de respaldos | 14 días |
| Historial de código y documentos | Git | GitHub | Permanente |

El acceso a los registros se limita al equipo y a quienes autorice la DSU. La gestión de registros cumple su objetivo cuando toda evidencia es localizable por su identificador, ninguna carece de versión y ninguna copia compartida contiene credenciales.

## 3.19. Capacitación

La preparación del equipo abarcará uso del modelo UML, ejecución de pruebas aisladas, revisión de permisos, manejo de configuración y lectura de métricas predictivas. La capacitación de usuarios se organizará por rol y tarea, con ejercicios de registro, planificación y consulta.

<!-- anchos: 5,3.6,4.4,3.79 -->
| Tema | Destinatarios | Modalidad | Evidencia |
| --- | --- | --- | --- |
| Revisión técnica formal y listas de verificación | Grupo de desarrollo | Sesión guiada sobre un producto real | Informe de RTF |
| Pruebas aisladas y regresión | Grupo de desarrollo | Práctica con la suite del proyecto | Reporte JUnit |
| Registro en campo desde el teléfono | Personal operativo | Práctica con datos de prueba | Registro de validación |
| Planificación y control de jornadas | Supervisores | Práctica guiada por el manual | Registro de validación |
| Tableros, mapa y predicciones | Directivos | Demostración | Registro de validación |
| Administración del sistema y del modelo | Administrador | Práctica guiada | Lista de tareas completadas |

## 3.20. Gestión de riesgos

Se priorizará el tratamiento de datos no representativos, requisitos ambiguos, diferencias entre modelos y código, resultados de pruebas desactualizados y condiciones productivas no verificadas. Cada revisión de calidad actualizará el registro de riesgos del PAPS. Un hallazgo repetido debe analizarse también como problema del proceso, por ejemplo, una ausencia de revisión que permite errores similares en varios módulos.

Se aplica la escala del PAPS: probabilidad (P) e impacto (I) de 1 a 5 y exposición P × I, tratando primero los valores de 15 a 25. Los riesgos propios de la calidad son:

<!-- anchos: 4.6,1.4,2.2,6,2.59 -->
| Riesgo de calidad | P e I | Exposición | Tratamiento | Responsable |
| --- | --- | --- | --- | --- |
| Datos históricos no representativos | 4 y 5 | 20 | Separar la evaluación técnica de la validación institucional | Grupo de desarrollo |
| Diferencias entre modelos, documentos y código | 3 y 4 | 12 | Auditoría física y revisión en cada cambio | Grupo SQA |
| Condiciones de producción no verificadas | 3 y 4 | 12 | Pruebas en un entorno comparable antes de liberar | Grupo SQA |
| Exposición de credenciales en entregas | 2 y 5 | 10 | Revisar las copias compartidas antes de publicarlas | Grupo de desarrollo |
| Resultados de pruebas desactualizados | 3 y 3 | 9 | Registrar la versión en cada resultado y repetir la regresión | Grupo de desarrollo |
| Requisitos ambiguos o sin criterio de prueba | 2 y 4 | 8 | SRR con lista de verificación | Grupo SQA |
| Defectos reabiertos repetidamente | 2 y 3 | 6 | Analizar la causa en el proceso | Grupo SQA |

Cada riesgo se trata evitando su causa, mitigando su efecto o aceptándolo de forma explícita, y se revisa al cerrar cada fase.

## 3.21. Glosario

| Término | Significado en el proyecto | Aplicación |
| --- | --- | --- |
| SQA | Aseguramiento de la calidad del software | Actividades de planificación, revisión y seguimiento |
| SQAP | Plan de aseguramiento de la calidad | Documento que organiza responsabilidades y controles |
| Línea base | Versión acordada para controlar cambios | Requisitos, modelos o producto identificados |
| Hallazgo | Desviación sustentada por evidencia | Registro para análisis y tratamiento |
| Regresión | Reejecución para detectar efectos de cambios | Pruebas sobre funciones previamente comprobadas |
| Aceptación | Decisión documentada sobre una entrega | Distinta de una ejecución técnica satisfactoria |
| Certificación | Reconocimiento formal de que un proceso o producto cumple un estándar | ISO 9001, IEEE 730 o CMMI |
| ERS | Especificación de requisitos de software | Requisitos RF, RNF y restricciones del sistema |
| SDD | Descripción del diseño del software | Módulos, procesos, datos e interfaces |
| V&V | Verificación y validación | Producto construido correctamente y producto correcto |
| RTF | Revisión técnica formal | Reunión planificada para detectar defectos en un producto |
| Elemento de configuración | Producto controlado por versiones | Código, esquema, modelos, documentos y modelo predictivo |
| Auditoría funcional | Comparación del sistema con la ERS | Previa a la entrega |
| Auditoría física | Comparación del código con su documentación | Previa a la entrega |

## 3.22. Procedimiento e historial de cambios del SQAP

Una modificación del plan debe indicar motivo, apartados afectados, repercusión en actividades y responsable de revisión. El equipo revisará los cambios que alteren criterios de liberación, distribución de funciones o alcance de pruebas.

<!-- anchos: 1.8,2.4,10,2.59 -->
| Versión | Fecha | Cambio | Responsable |
| --- | --- | --- | --- |
| 1.0 | 16/11/2026 | Primera redacción del plan | Grupo 8 |
| 1.1 | 17/11/2026 | Se agregan concepto de SQA y estándares de certificación, objetivos, lema, atributos de calidad, organizaciones y responsabilidades, resumen de ERS y SDD, plan de V&V, documentación de usuario, estándares de codificación y comentarios, revisiones y agenda, niveles de prueba, gestión de configuración, control de código, retención de registros y riesgos de calidad | Grupo 8 |

## 3.23. Anexos

Los formatos de registro de revisión técnica, de problema y acción correctiva y de validación con usuarios, junto con la localización de las evidencias, se encuentran en los anexos A a D al final del documento.

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

- **Entorno de desarrollo:** Visual Studio Code con los analizadores estáticos definidos en el repositorio: Ruff para el backend Python (configurado en pyproject.toml) y oxlint para el frontend React/TypeScript (configurado en .oxlintrc.json y ejecutado con el script lint), además de la verificación de tipos de TypeScript en cada construcción (tsc -b). Las reglas se detallan en el anexo I.
- **Control de versiones con Git y GitHub:** Repositorio unificado (ProyectoDSU) organizado como monorepositorio con carpetas independientes para backend y frontend, alojado en GitHub con acceso restringido al equipo. El plan gratuito de GitHub cubre repositorios privados ilimitados, por lo que el control de versiones no genera costo de licencia.
- **Gestión de dependencias:** Versiones acotadas en requirements.txt y requirements-dev.txt para el backend (Django, Django REST Framework, scikit-learn, psycopg, pytest y Ruff) y package.json con su archivo de bloqueo package-lock.json de npm para el frontend (React, Vite, Tailwind CSS y Leaflet).

## 4.3. Herramientas de pruebas y evidencia

El aseguramiento de la calidad técnica se ejecuta mediante una cadena de herramientas especializadas:

- **pytest y pytest-django:** Framework de pruebas unitarias y de integración que ejecuta la suite de regresión automatizada (42 pruebas funcionales y de seguridad) sobre una base de datos de prueba aislada y exporta reportes JUnit XML reproducibles. Las propias pruebas verifican los contratos REST de la API: códigos de estado HTTP (200, 201, 400, 401, 403), estructura de las respuestas JSON, emisión de tokens JWT y rechazo de accesos sin permiso.
- **Contenedores Docker:** Construcción de imágenes Linux reproducibles con el Dockerfile y el docker-compose.yml del backend, para aislar la suite de pruebas del sistema operativo anfitrión y contrastar la ejecución entre Windows y Linux. Docker Desktop es gratuito para uso personal, educativo y en organizaciones pequeñas.
- **OWASP ZAP (Zed Attack Proxy):** Escáner de seguridad de aplicaciones web, libre y de código abierto, empleado para identificar cabeceras faltantes, exposición de información en cabeceras HTTP, políticas de cookies y vulnerabilidades comunes de inyección.
- **Power BI Desktop:** Entorno de modelado analítico DAX para la construcción de reportes gerenciales a partir de las vistas analíticas del sistema. Power BI Desktop es gratuito; publicar y compartir informes en el servicio de Power BI requiere la licencia Pro por usuario.

Las figuras siguientes muestran las condiciones de licenciamiento publicadas por los proveedores de las herramientas, consultadas el 17 de noviembre de 2026.

<!-- fig: DocumentoSoftware2/recursos/web/docker.png | Planes de Docker -->

<!-- fig: DocumentoSoftware2/recursos/web/powerbi.png | Planes de Microsoft Power BI -->

<!-- fig: DocumentoSoftware2/recursos/web/zap.png | Sitio oficial de OWASP ZAP -->

La licencia de Enterprise Architect empleada para el modelado corresponde a la edición de evaluación instalada en el equipo de trabajo (EA Trial); la compra de dos licencias de la edición Professional para el mantenimiento del modelo está incluida en el presupuesto del capítulo 1.

## 4.4. Evaluación de productividad

La productividad aportada por las herramientas CASE se evalúa con evidencia medida en el propio proyecto y no con porcentajes de ahorro supuestos, que requerirían haber ejecutado el mismo trabajo sin herramientas para compararlo. La tabla siguiente relaciona cada actividad con la herramienta empleada, el resultado observable y la forma de verificarlo.

| Actividad del ciclo de vida | Herramienta | Evidencia medida en el proyecto | Verificación |
| --- | --- | --- | --- |
| Especificación de requisitos y casos de uso | Enterprise Architect | 27 requisitos funcionales trazados a 34 casos de uso y 4 actores en un único modelo | Modelo DSU-FaseFinal.eapx y matriz de trazabilidad del capítulo 2 |
| Análisis y diseño | Enterprise Architect | 34 realizaciones de análisis, diagramas de clases, secuencia, paquetes, componentes y despliegue exportados del mismo modelo | Figuras del capítulo 2, generadas desde el modelo y no redibujadas |
| Diseño del esquema de base de datos | Migraciones de Django | Esquema PostgreSQL creado y actualizado solo por migraciones versionadas, sin sentencias DDL escritas a mano | Carpetas migrations de cada aplicación del backend |
| Pruebas de regresión del backend | pytest y pytest-django | 42 pruebas sin fallos ni errores: 98,8 s en Windows y 41,4 s en Linux con Docker (16/11/2026) | Reportes JUnit XML de la carpeta de pruebas del material del proyecto |
| Calidad estática del código | Ruff, oxlint y TypeScript | Reglas de estilo y errores comunes revisados en cada cambio, sin revisión manual línea por línea | pyproject.toml, .oxlintrc.json y tsconfig del repositorio |
| Generación de la documentación | Python (python-docx) y Microsoft Word | Documento completo, índice y PDF regenerados en aproximadamente un minuto desde fuentes editables | ensamblar.py y publicar.ps1 de la carpeta del documento |

El beneficio común es la repetibilidad: cada resultado puede reproducirse con el mismo comando o modelo, lo que reduce los errores de transcripción entre artefactos y permite revisar un cambio sin rehacer el trabajo anterior.

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
   - **Emisión de la Matrícula de Comercio:** El SEPREC procesa la solicitud en un plazo de 24 horas desde el día hábil siguiente a la presentación y emite la Matrícula de Comercio digital con código QR de verificación.
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

La figura siguiente reproduce la ficha oficial del trámite 2 del SEPREC, con sus apartados y los aranceles citados en el paso 3.

<!-- fig: DocumentoSoftware2/recursos/web/seprec_srl.png | Ficha del SEPREC para la inscripción de una S.R.L. -->

La inscripción en el Registro Nacional de Contribuyentes del paso 4 se inicia desde el portal del Servicio de Impuestos Nacionales.

<!-- fig: DocumentoSoftware2/recursos/web/sin.png | Portal del Servicio de Impuestos Nacionales -->
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
- **Búsqueda previa de anterioridades:** Búsqueda fonética y figurativa en la base de datos del SENAPI para asegurar la inexistencia de marcas idénticas o confundibles previamente registradas. Se solicita con el formulario PI-112 en la plataforma del SENAPI o en sus oficinas, adjuntando el comprobante de depósito de Bs. 75 para persona natural o jurídica boliviana.
- **Presentación de la solicitud:** Llenado del Formulario PI-101 (Signos Distintivos), adjuntando copia de cédula de identidad del solicitante o representante legal, reproducción del logotipo a color (formato 4x4 cm) y especificación de colores pantone.
- **Publicación y concesión:** Superado el examen de forma, el SENAPI ordena la publicación en la Gaceta Oficial de Bolivia. Trascurridos 50 días hábiles sin oposición de terceros, se emite la Resolución Administrativa y el Título de Concesión de Registro de Marca, con vigencia de 10 años renovables de forma indefinida.

<!-- fig: DocumentoSoftware2/recursos/web/senapi_busqueda.png | Pasos del SENAPI para la búsqueda de signos distintivos -->

<!-- fig: DocumentoSoftware2/recursos/web/senapi_flujo_marca.png | Flujo de proceso del SENAPI para el registro de un signo distintivo -->

### 5.3.2. Registro de Derecho de Autor de Soporte Lógico (Software)

El software como creación intelectual se encuentra protegido en Bolivia por la Ley N° 1322 de Derecho de Autor del 13 de abril de 1992 y su Decreto Supremo Reglamentario N° 23907 de 24 de mayo de 1994, que asimila los programas de ordenador a las obras literarias:

- **Formulario de solicitud:** Formulario de registro de programas de ordenador, llenado en la plataforma SIPI del SENAPI (sipi.senapi.gob.bo), impreso y firmado junto con la carta de solicitud; ambos tienen carácter de declaración jurada.
- **Tasas:** Registro de programas de ordenador, Bs. 150 para persona nacional, depositados en la cuenta del SENAPI, más Bs. 60 de publicación en la Gaceta Oficial de Bolivia; el registro se resuelve en cinco días hábiles desde el día siguiente a la solicitud.
- **Ejemplar de la obra:** Para programas de computación el SENAPI solicita una copia ejecutable del programa, el manual de descripción en PDF y un video tutorial en MP4 o AVI; tratándose de una aplicación web, un video demostrativo del programa. Para el sistema DSU se preparan:
  1. Copia del código fuente y de la construcción del backend Django y del frontend React, depurada de secretos, claves y contraseñas.
  2. Manual de usuario por rol (capítulo 12) y memoria técnica con la arquitectura, el esquema de datos y el modelo Random Forest Regressor, en PDF.
  3. Video demostrativo del recorrido por los cuatro roles del sistema.
- **Derechos Morales:** De carácter inalienable, irrenunciable e imprescriptible, corresponden exclusivamente a sus desarrolladores: Carlos Gabriel Lobo Gutiérrez y Leonardo Serrate Basma.
- **Derechos Patrimoniales:** Comprenden las facultades exclusivas de reproducción, distribución, comunicación pública y transformación del software. El equipo conserva la titularidad patrimonial originaria; en caso de entrega formal a la UAGRM, se formalizará mediante un convenio de cesión de derechos patrimoniales o una licencia institucional de uso no exclusiva, permanente y gratuita para fines académicos y de gestión universitaria.

Las figuras siguientes muestran el procedimiento virtual, el flujo del trámite y las tasas publicadas por el SENAPI.

<!-- fig: DocumentoSoftware2/recursos/web/senapi_virtual.png | Pasos del registro virtual de derecho de autor en el SENAPI -->

<!-- fig: DocumentoSoftware2/recursos/web/senapi_flujo_autor.png | Flujo de proceso del SENAPI para el registro de derecho de autor -->

<!-- fig: DocumentoSoftware2/recursos/web/senapi_tasas.png | Tasas del SENAPI para el registro de derecho de autor -->

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

Se consideran elementos de configuración el código, las dependencias, las migraciones, los parámetros de despliegue, los modelos UML, los documentos, las pruebas y los artefactos predictivos. El control de cambios debe permitir relacionar una versión entregada con sus entradas y evidencias.

| Elemento | Ubicación del proyecto | Control previsto |
| --- | --- | --- |
| Backend | gestion-residuos-dsu/backend | Revisión de API, servicios, migraciones y dependencias |
| Frontend | gestion-residuos-dsu/frontend | Revisión de interfaz, construcción y configuración |
| Modelos UML | modelo_uml y generador/figuras | Conservación de fuentes y exportaciones |
| Documento Software 2 | DocumentoSoftware2 | Fuente editable, versiones y revisión visual |
| Evidencias de pruebas | docs/auditoria-fase-final | Conservación del resultado original y su contexto |

## 6.2. Control de versiones y colaboración

La raíz del proyecto es el único repositorio Git. Backend y frontend no son submódulos. Antes de integrar cambios se revisará el estado del repositorio y se identificarán los archivos propios de cada actividad. Las modificaciones de documentación no deben sobrescribir correcciones manuales o alterar artefactos de otra materia.

Para una entrega se registrarán identificador de versión, archivos incluidos, dependencias y cambios relevantes. La revisión de los materiales compartidos debe proteger las configuraciones sensibles y verificar que las evidencias no contengan credenciales.

El repositorio se aloja en GitHub como repositorio privado. El plan gratuito incluye repositorios públicos y privados ilimitados, suficiente para un equipo de dos integrantes.

<!-- fig: DocumentoSoftware2/recursos/web/github.png | Planes de GitHub -->

## 6.3. Gestión documental

Cada materia mantiene su documento, estructura y criterios de evaluación. Los requisitos y el producto permanecen compartidos. Un cambio funcional se analiza en ambos documentos; un ajuste de portada, numeración o capítulo se aplica solo a la materia correspondiente.

El documento de Software 2 se genera desde fuentes propias y conserva una copia anterior antes de una revisión mayor. El control documental incluye revisión de tablas, índices, imágenes y referencias cruzadas.

## 6.4. Entornos

El entorno de desarrollo permite ejecutar y revisar componentes. La base demo compartida en Neon sirve al trabajo conjunto y debe preservarse de cambios no coordinados. El entorno productivo separa interfaz, API y persistencia administrada; su verificación se describe en el capítulo 11.

La persistencia administrada se contrata en Neon (PostgreSQL sin servidor) y la interfaz se publica en Vercel. Ambos proveedores ofrecen un plan gratuito para el desarrollo y planes de pago por uso para producción; las figuras muestran sus condiciones publicadas el 17 de noviembre de 2026. El costo comparado de producción se analiza en el capítulo 11.

<!-- fig: DocumentoSoftware2/recursos/web/neon.png | Planes de Neon para PostgreSQL administrado -->

<!-- fig: DocumentoSoftware2/recursos/web/vercel.png | Planes de Vercel para la publicación del frontend -->

## 6.5. Inventario técnico observado

Las versiones de la tabla proceden del registro técnico del proyecto del 16 de noviembre de 2026.

<!-- versiones -->

# 7. Sitio web de presentación

## 7.1. Propósito y destinatarios

El portal del proyecto DSU es el punto de acceso de la Dirección de Servicios Universitarios a la gestión de residuos sólidos de la UAGRM. Está dirigido al personal operativo, a los supervisores, a los directivos y al administrador del sistema, y funciona en navegadores de computadoras y teléfonos sin instalar ninguna aplicación.

## 7.2. Estructura de contenidos y arquitectura de información

El portal tiene diseño adaptable y organiza su contenido en las secciones siguientes, visibles según el rol del usuario:

| Sección | Contenido | Finalidad |
| --- | --- | --- |
| Acceso | Identidad de la DSU e inicio de sesión | Ingresar con la cuenta institucional |
| Registro en campo | Jornada asignada, puntos de la ruta y formulario de vaciado | Registrar cantidades e incidencias desde el teléfono |
| Jornadas | Planificación, asignación de personal y vehículos, seguimiento y cierre | Organizar y controlar la recolección |
| Tablero de gestión | Indicadores, tendencias y comparación de periodos | Apoyar la decisión con datos |
| Mapa del campus | Puntos de recolección y mapa de calor | Ubicar zonas críticas |
| Predicción y recomendaciones | Generación proyectada, alertas y recomendaciones logísticas | Anticipar la demanda de recolección |
| Reportes | Reportes por sector, tipo de residuo, jornadas e incidencias, con exportación a Excel y PDF | Informar y respaldar la gestión |
| Administración | Usuarios, roles, catálogos, parámetros, procesos ETL, modelo y bitácora | Mantener el sistema |

## 7.3. Mecanismos de interacción y mesa de ayuda (Help-Desk)

Para garantizar la continuidad operativa y la resolución oportuna de problemas funcionales o técnicos, el portal cuenta con un modelo de atención escalonada de soporte técnico estructurado en tres niveles de atención:

| Nivel de soporte | Canal de atención | Responsable | Cobertura horaria | Tiempo de primera respuesta |
| --- | --- | --- | --- | --- |
| Nivel 1 (Autoservicio) | Manual de usuario por rol y videos de uso | Usuario | Permanente | Inmediato |
| Nivel 2 (Soporte Funcional) | Formulario web de tickets e incidencias y correo electrónico institucional | Agente de mesa de ayuda técnica | Lunes a Viernes 07:00 a 19:00 | Menor a 2 horas laborables |
| Nivel 3 (Soporte Especializado) | Canal directo de ingeniería y seguimiento de bugs en el repositorio | Ingenieros de software y DBA | Lunes a Viernes 08:00 a 16:00 | Menor a 6 horas laborables |

## 7.4. Estrategia progresiva de mejoras tecnológicas

La hoja de ruta de evolución del producto contempla tres líneas de modernización continua:

1. **Transformación a Progressive Web App (PWA):** Incorporación de Service Workers y almacenamiento local en IndexedDB en el frontend para habilitar el registro de pesaje en modo fuera de línea (offline). Esto permitirá a las cuadrillas registrar vaciados en zonas del campus con sombra de cobertura móvil, sincronizando automáticamente los datos al recuperar la conectividad.
2. **Telemetría IoT en contenedores:** Integración futura de sensores ultrasónicos de nivel de llenado con microcontroladores ESP32 y conectividad LoRaWAN / GSM, enviando telemetría directa a los endpoints de la API Django sin requerir registro manual en puntos críticos.
3. **Localización e internacionalización:** Soporte multi-idioma (español e inglés) en la interfaz pública y analítica para facilitar su evaluación en congresos científicos internacionales de gestión ambiental y ciudades inteligentes.

## 7.5. Imágenes

Las capturas siguientes muestran el portal en escritorio y en teléfono.


<!-- fig: docs/auditoria-fase-final/ui/login-anon-1440.png | Página de acceso al sitio en escritorio -->

<!-- fig: docs/auditoria-fase-final/ui/login-anon-390.png | Página de acceso al sitio en teléfono -->

<!-- fig: docs/auditoria-fase-final/ui/tablero-super_ui-390.png | Tablero de gestión en teléfono -->

<!-- fig: docs/auditoria-fase-final/ui/puntos-super_ui-1440.png | Puntos de recolección sobre el mapa del campus -->

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

El tamaño funcional de cada solución, calculado en el apartado 1.2 con el método de puntos de función, permite comparar el alcance de las alternativas. DSU, con 477,2 puntos de función, se ubica entre Bigbelly (429,5) y Ecube Labs (545,0), y por debajo de Sensoneo (669,0): un alcance comparable al de los productos comerciales sin depender de sensores ni estaciones propias.

<!-- fig: DocumentoSoftware2/recursos/web/mercado_pf.png | Puntos de función ajustados de las soluciones comparadas -->

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

El propósito es comprobar comportamientos definidos, identificar defectos y conservar evidencia reproducible.

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

Los reportes JUnit conservados registran 42 pruebas en Windows y 42 en Linux, sin fallos, errores ni omisiones en esas corridas. Son dos ejecuciones de la suite; no se presentan como 84 casos distintos.

<!-- resultados junit -->

Las duraciones corresponden al tiempo declarado por la suite, no a latencia de usuario ni a capacidad productiva.

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

La evaluación debe registrar versión del modelo, periodo del histórico, procedencia, variables, separación de entrenamiento y prueba, métricas y límites. Los errores se expresarán en unidades interpretables para el uso previsto y se conservará la forma de calcular el margen mostrado al usuario.

No se trasladan resultados de demostración como rendimiento predictivo institucional.

## 9.8. Pendientes y criterio de cierre

Permanecen por comprobar despliegue remoto, carga y rendimiento representativos, restauración externa, validación predictiva institucional y aceptación por usuarios. También debe completarse la revisión del informe Power BI y su publicación cuando corresponda. Cada cierre debe enlazar el requisito con evidencia, entorno y decisión; las observaciones de una fuente anterior no se reemplazarán por una declaración general de finalización.

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

- **Fase I: Concientización y expectativa (Semanas 1 a 2):** Campaña institucional bajo el lema *«Campus Limpio, Gestión Inteligente»*. Publicación de cápsulas audiovisuales breves en redes institucionales y colocación de afiches informativos con códigos QR en los 45 puntos de recolección del campus central de la UAGRM.
- **Fase II: Lanzamiento oficial e inducción (Semanas 3 a 5):** Presentación del portal del proyecto ante autoridades universitarias y realización de talleres presenciales de capacitación situados en los módulos de trabajo de la DSU, entregando guías plastificadas por rol.
- **Fase III: Consolidación e incentivos ecológicos (Semanas 6 en adelante):** Publicación mensual del ranking de facultades con mayor índice de reciclaje y presentación de los resultados del modelo predictivo en las jornadas científicas de la FICCT.

| Canal de difusión | Formato del material | Audiencia objetivo | Finalidad comunicacional |
| --- | --- | --- | --- |
| Portal Web del Proyecto | Landing page responsive con simulador y centro de recursos | Comunidad universitaria y evaluadores | Difusión integral, transparencia y autoservicio |
| Puntos Ecológicos del Campus | Afiches informativos y señalética con códigos QR | Estudiantes, docentes y personal de limpieza | Concientización ambiental y enlace al portal web |
| Talleres Presenciales | Demostraciones en vivo y sesiones prácticas guiadas | Cuadrillas operativas y supervisores | Capacitación práctica y reducción de la brecha digital |
| Canal de Video (YouTube) | Píldoras tutoriales de 2 minutos por caso de uso | Nuevos operarios y personal de reemplazo | Formación continua sin dependencia de instructores |

### 10.3.1. Afiche de la campaña

El afiche de la fase I se coloca en los puntos de recolección y en los módulos de la DSU. Usa los colores y la tipografía del propio sistema, muestra la pantalla de predicción en un teléfono y enlaza mediante código QR con el manual de usuario y el material del proyecto.

<!-- fig: DocumentoSoftware2/recursos/web/afiche_campana.png | Afiche de la campaña «Campus limpio, gestión inteligente» -->

## 10.4. Recursos e indicadores clave de rendimiento (KPIs)

El éxito del programa de difusión y adopción se evaluará de forma continua mediante los siguientes indicadores de desempeño:

| Indicador clave (KPI) | Definición y método de cálculo | Meta objetivo | Fuente de verificación |
| --- | --- | --- | --- |
| Tasa de digitalización de pesajes | (Pesajes registrados en el sistema / Total de pesajes ejecutados) * 100 | Mayor al 90 % en el primer mes | Base de datos relacional PostgreSQL |
| Adopción por sector del campus | Porcentaje de sectores universitarios activos con jornadas digitales | 100 % de los sectores cubiertos | Módulo de supervisión de jornadas |
| Tiempo medio de registro | Tiempo transcurrido en el registro móvil de un vaciado | Menor a 45 segundos por punto | Trazas de auditoría del sistema |
| Satisfacción de usuario (CSAT) | Encuesta de satisfacción aplicada tras los talleres de inducción | Mayor al 85 % de valoración positiva | Encuestas de usabilidad SUS aplicadas |

# 11. Puesta en marcha y despliegue

## 11.1. Arquitectura y comparativa de plataformas Cloud

Para la puesta en marcha del sistema en producción se evaluaron las alternativas de infraestructura en la nube más representativas frente a la arquitectura híbrida adoptada:

- **Amazon Web Services (AWS):** Infraestructura basada en contenedor ECS/Fargate para la API Django, servicio gestionado Amazon RDS para PostgreSQL y bucket S3 con CloudFront para el frontend y medios estáticos. Ofrece alta madurez y SLAs del 99.99 %, pero presenta costos elevados en dólares y mayor complejidad operativa para presupuestos universitarios.
- **Microsoft Azure:** Despliegue mediante Azure App Service para Linux conectado a Azure Database for PostgreSQL Flexible Server. Facilita la gobernanza mediante suscripciones educativas, aunque mantiene costos mensuales fijos superiores a soluciones serverless.
- **Google Cloud Platform (GCP):** Cómputo serverless mediante Cloud Run conectado a Cloud SQL para PostgreSQL y Cloud Storage. Destaca por su facturación por milisegundo de ejecución, siendo altamente escalable para cargas intermitentes.
- **Arquitectura Híbrida Adoptada:** Despliegue del backend en una instancia AWS EC2 Linux en São Paulo, en un contenedor Docker detrás del reverse proxy Caddy (con emisión y renovación automática de certificados SSL/TLS Let's Encrypt), base de datos PostgreSQL alojada en Neon (con pooling de conexiones pgbouncer) y frontend estático distribuido en la red global de Vercel Edge Network.

La siguiente tabla compara las opciones de despliegue evaluadas:

| Criterio | Amazon Web Services (AWS) | Microsoft Azure | Google Cloud Platform (GCP) | Arquitectura Híbrida Adoptada |
| --- | --- | --- | --- | --- |
| Cómputo Backend | ECS Fargate / EC2 Linux | Azure App Service | Cloud Run Serverless | Docker en AWS EC2 Linux con Caddy |
| Persistencia de Datos | Amazon RDS PostgreSQL | Azure Database PostgreSQL | Cloud SQL PostgreSQL | PostgreSQL administrado en Neon |
| Distribución Frontend | S3 + CloudFront CDN | Azure Static Web Apps | Cloud Storage + Cloud CDN | Vercel Edge Global Network |
| Complejidad de gestión | Alta (requiere DevSecOps) | Media-Alta | Media | Baja-Media (administración ágil) |
| Costo mensual | No cotizado | No cotizado | No cotizado | Bs. 2.186,31 (unos USD 187), presupuesto de referencia del proyecto |

## 11.2. Preparación del entorno y configuración técnica

La configuración de producción desacopla estrictamente los secretos y parámetros sensibles del código fuente mediante variables de entorno seguras almacenadas en archivos protegidos con permisos de lectura restringidos:

- **Aislamiento de credenciales:** La clave secreta de Django (SECRET_KEY), credenciales de conexión a Neon PostgreSQL, tokens de servicio y configuraciones de correo se inyectan en tiempo de ejecución sin incluirse en repositorios públicos.
- **Políticas de depuración:** Desactivación estricta del modo de depuración (DEBUG=False) en producción para evitar la exposición de trazas de error o variables de sesión ante fallos imprevistos.
- **Reverse Proxy Caddy:** Manejo automatizado de cifrado HTTPS con certificados TLS emitidos por Let's Encrypt, forzando redirección HTTP a HTTPS y balanceando peticiones hacia el socket WSGI de Django (Gunicorn con 3 workers).

## 11.3. Verificación de puesta en marcha

La aceptación técnica de la instalación en producción se verifica mediante siete controles de calidad estandarizados:

| Control de verificación | Evidencia requerida | Criterio de aceptación |
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

- **Frecuencia y retención de respaldos:** El servicio de respaldo ejecuta `pg_dump` en formato comprimido cada 24 horas y guarda la copia en el disco del servidor. Conserva los últimos 14 días, valor configurable.
- **Métricas de recuperación del servicio:**
  - *RPO (Recovery Point Objective):* Menor o igual a 24 horas, limitando la pérdida máxima tolerable de datos a los registros de la jornada inmediata anterior.
  - *RTO (Recovery Time Objective):* Menor o igual a 2 horas, tiempo máximo previsto para provisionar una nueva instancia y restaurar el dump de base de datos.
- **Protocolo paso a paso de restauración:**
  1. Aprovisionamiento o verificación del clúster de base de datos destino con versión compatible de PostgreSQL.
  2. Descarga y verificación de la suma de comprobación (checksum SHA-256) del archivo de respaldo más reciente.
  3. Ejecución del comando de restauración: `pg_restore --clean --if-exists --no-owner -d nombre_bd archivo_backup.dump`.
  4. Ejecución del script de comprobación de integridad referencial para verificar el conteo de tablas y consistencia de claves foráneas.
  5. Conexión de la API backend y ejecución de la suite de pruebas de salud de endpoints (healthcheck).

## 11.5. Seguridad perimetral, cabeceras HTTP y endurecimiento (Hardening)

El endurecimiento perimetral de la infraestructura de producción implementa las mejores prácticas de seguridad recomendadas por OWASP:

- **Cabeceras de seguridad HTTP:** Caddy y Django envían *Strict-Transport-Security* con vigencia de un año y *X-Content-Type-Options: nosniff*, y Caddy oculta la cabecera del servidor.
- **Aislamiento CORS:** Restricción estricta de la lista blanca de orígenes permitidos en Django (*CORS_ALLOWED_ORIGINS*) exclusivamente al dominio oficial del frontend en Vercel, rechazando solicitudes cross-origin no autorizadas.
- **Protección de tokens JWT:** El token de acceso caduca a los 30 minutos y el de refresco a las 10 horas, ambos valores configurables. La aplicación web los guarda en el almacenamiento local del navegador; pasarlos a cookies *HttpOnly* es una mejora prevista junto con la política CSP.
- **Rotación periódica de credenciales:** Se aplica la rotación semestral de contraseñas de servicio y claves secretas de la plataforma.

## 11.6. Estado de preparación y puesta en marcha

El proyecto cuenta con especificaciones de despliegue probadas en contenedores locales Linux y una base de datos demo compartida en Neon. La puesta en marcha definitiva en el dominio institucional de la universidad se encuentra planificada como fase de transición, condicionada a la autorización de la DSU-UAGRM y a la asignación del dominio correspondiente.

<!-- figura despliegue -->

## 11.7. Tipo de licencia

El sistema se distribuye como software propietario de sus autores, con una licencia de uso institucional, no exclusiva y sin costo para la DSU-UAGRM. La licencia permite instalar, operar y respaldar el sistema para la gestión de residuos de la universidad. No permite sublicenciarlo ni comercializarlo sin acuerdo escrito de los autores. Las bibliotecas de terceros (Django, React, scikit-learn, Leaflet y PostgreSQL, entre otras) conservan sus licencias abiertas originales. 

## 11.8. Términos y condiciones de uso


1. **Objeto.** Estos términos regulan el uso del Sistema web de gestión de residuos sólidos de la DSU-UAGRM.
2. **Usuarios autorizados.** El acceso se limita al personal habilitado por la DSU con uno de los cuatro roles: Operativo, Supervisor, Directivo o Administrador. La cuenta es personal e intransferible.
3. **Obligaciones del usuario.** Registrar datos veraces, custodiar su contraseña, cerrar la sesión al terminar y comunicar al administrador cualquier acceso indebido o error detectado.
4. **Usos prohibidos.** Alterar o eliminar registros sin autorización, compartir credenciales, extraer información para fines ajenos a la DSU e intentar eludir los controles de acceso.
5. **Registro de actividad.** Las operaciones relevantes quedan anotadas en la bitácora de auditoría con usuario, fecha y hora. El usuario acepta este registro al utilizar el sistema.
6. **Predicciones y recomendaciones.** Las proyecciones de generación y las recomendaciones logísticas son estimaciones de apoyo. La decisión operativa corresponde al personal responsable de la DSU.
7. **Disponibilidad.** El servicio puede interrumpirse por mantenimiento o por fallas de los proveedores de infraestructura. No se garantiza disponibilidad continua.
8. **Propiedad intelectual.** El software pertenece a sus autores y se utiliza según la licencia de la sección 11.7. Los datos operativos registrados pertenecen a la UAGRM.
9. **Modificaciones.** Los cambios a estos términos se comunicarán a los usuarios antes de su vigencia.
10. **Legislación aplicable.** Estos términos se rigen por las leyes del Estado Plurinacional de Bolivia.

## 11.9. Política de privacidad

Bolivia no cuenta con una ley general de protección de datos personales. La política se apoya en el derecho a la privacidad y en la acción de protección de privacidad de la Constitución Política del Estado (arts. 21 y 130) y en la Ley N° 164 con su reglamento, el Decreto Supremo N° 1793.

- **Datos que se tratan.** Nombre, usuario, correo electrónico y rol de cada cuenta; contraseña almacenada únicamente como resumen criptográfico; registros de operación con su autor, y la bitácora de auditoría. El sistema no solicita datos sensibles ni información de personas ajenas a la DSU.
- **Finalidad.** Autenticar usuarios, asignar responsabilidades en las jornadas, mantener la trazabilidad de los registros y elaborar indicadores y predicciones sobre residuos. Los análisis se realizan sobre cantidades de residuos, no sobre personas.
- **Acceso.** Cada usuario consulta la información que su rol permite. La bitácora solo es visible para el Administrador.
- **Encargados del tratamiento.** La base de datos se aloja en Neon, la aplicación en AWS y la interfaz en Vercel. Los datos se almacenan fuera de Bolivia y viajan cifrados mediante TLS.
- **Conservación.** Los registros operativos se conservan como histórico institucional. Las cuentas se desactivan en lugar de eliminarse para preservar la trazabilidad.
- **Derechos.** El titular puede solicitar al administrador el acceso, la rectificación o la desactivación de sus datos mediante la DSU.
- **Incidentes.** Un acceso indebido o una pérdida de datos se comunicará a la DSU y se registrará como problema según el SQAP.

# 12. Software como producto

## 12.1. Composición de la entrega

La entrega debe identificar versión del código, configuración de instalación, estructura de datos, documentación, pruebas y limitaciones. El código, el manual y las capturas deben describir la misma versión. El producto se evaluará por tareas y criterios observables, no por la cantidad de archivos incluidos.

## 12.2. Manual de usuario por rol

El manual se organiza por rol y reúne las tareas principales de cada uno con la pantalla donde se realizan.

### 12.2.1. Acceso al sistema

El usuario ingresa con su cuenta autorizada. Si el acceso es rechazado, verifica sus datos o consulta al administrador. Al finalizar utiliza Cerrar sesión y conserva sus credenciales de forma personal.

<!-- fig: docs/auditoria-fase-final/ui/login-anon-1440.png | Pantalla de inicio de sesión -->

### 12.2.2. Operación en campo

El operativo consulta su jornada, identifica el punto y registra cantidades por tipo de residuo. Revisa unidad y cantidad antes de guardar; corrige los errores indicados y comprueba la confirmación. Si pierde conectividad, no debe asumir que el envío fue guardado: la versión actual no encola operaciones fuera de línea.

<!-- fig: docs/auditoria-fase-final/ui/campo-oper_ui-390.png | Registro de campo en el teléfono del operativo -->

<!-- fig: docs/auditoria-fase-final/ui/campo-oper_ui-390-error.png | Mensaje de validación en el registro de campo -->

<!-- fig: docs/auditoria-fase-final/ui/historico-oper_ui-1440.png | Histórico de registros de residuos -->

### 12.2.3. Supervisión de jornadas

El supervisor planifica jornadas de sus sectores, ordena puntos y asigna personal y vehículos disponibles. Revisa el avance y registra el motivo de las omisiones autorizadas. Antes del cierre comprueba que cada punto esté atendido u omitido con justificación.

<!-- fig: docs/auditoria-fase-final/ui/jornadas-super_ui-1440.png | Listado de jornadas de recolección -->

<!-- fig: docs/auditoria-fase-final/ui/jornadas-nueva-super_ui-1440.png | Planificación de una jornada nueva -->

<!-- fig: docs/auditoria-fase-final/ui/jornadas-107-super_ui-1440.png | Detalle y seguimiento de una jornada -->

<!-- fig: docs/auditoria-fase-final/ui/incidencias-super_ui-1440.png | Incidencias operativas -->

<!-- fig: docs/auditoria-fase-final/ui/recomendaciones-super_ui-1440.png | Recomendaciones logísticas -->

### 12.2.4. Consulta directiva

El directivo consulta tableros, mapas y reportes dentro de su alcance. Antes de comparar resultados revisa periodo, sector y tipo de residuo. Distingue datos observados de proyecciones y considera el margen de error. La falta de histórico o de una predicción disponible no debe interpretarse como generación nula.

<!-- fig: docs/auditoria-fase-final/ui/tablero-dir_ui-1440.png | Tablero de indicadores del directivo -->

<!-- fig: docs/auditoria-fase-final/ui/mapa-super_ui-1440.png | Mapa del campus con puntos de recolección -->

<!-- fig: docs/auditoria-fase-final/ui/predicciones-super_ui-1440.png | Predicción de generación de residuos -->

<!-- fig: docs/auditoria-fase-final/ui/reportes-super_ui-1440.png | Generación y exportación de reportes -->

### 12.2.5. Administración

El administrador gestiona accesos, catálogos y parámetros según sus permisos. Las operaciones ETL, entrenamiento y publicación del modelo requieren verificar datos y resultados antes de utilizarlos en análisis. La administración del sistema no habilita por sí misma acciones de registro operativo en campo.

<!-- fig: docs/auditoria-fase-final/ui/usuarios-admin_ui-1440.png | Gestión de usuarios -->

<!-- fig: docs/auditoria-fase-final/ui/roles-admin_ui-1440.png | Roles y permisos -->

<!-- fig: docs/auditoria-fase-final/ui/parametros-admin_ui-1440.png | Parámetros del sistema -->

<!-- fig: docs/auditoria-fase-final/ui/procesos-admin_ui-1440.png | Procesos ETL -->

<!-- fig: docs/auditoria-fase-final/ui/modelo-admin_ui-1440.png | Entrenamiento y versiones del modelo -->

<!-- fig: docs/auditoria-fase-final/ui/bitacora-admin_ui-1440.png | Bitácora de auditoría -->

## 12.3. Material de apoyo

El material del proyecto está publicado en una carpeta compartida a la que se accede con el enlace https://drive.google.com/drive/folders/1GtrE_rtlimZ3zcj4aZsuvZf6RaErTHqg?usp=sharing o con el código QR de la carátula y del anexo F. La carpeta contiene este documento en Word y PDF, el PAPS, el SQAP y el manual de usuario como documentos independientes, las capturas del sistema en escritorio y teléfono, los diagramas UML, las evidencias de las pruebas y los documentos de respaldo del proyecto.

<!-- fig: DocumentoSoftware2/recursos/qr_drive.png | Código QR del material del proyecto -->

## 12.4. Soporte y mantenimiento

El reporte de incidente incluirá tarea, rol, momento, mensaje y pasos de reproducción, sin credenciales. El equipo aplicará el SQAP y verificará la corrección y la regresión pertinente antes de reemplazar una versión entregada.

## 12.5. Lista de entrega

| Elemento | Comprobación requerida | Situación documentada |
| --- | --- | --- |
| Sistema y API | Versión identificada y ejecución | Implementación y pruebas técnicas disponibles |
| Documento Software 2 | Capítulos, fuentes e índices consistentes | Completo |
| Modelos | Fuentes y figuras concordantes | Artefactos del proyecto disponibles |
| Pruebas | Registros y limitaciones | Evidencias técnicas identificadas en capítulo 9 |
| Instalación | Procedimiento reproducido | Procedimiento documentado en el capítulo 11 |
| Manual y videos | Tareas completas por rol | Manual por rol con capturas y material en la carpeta compartida |
| Respaldo institucional | Solicitud formal ante la DSU | Oficio recibido por la DSU el 11/09/2026 (anexo H) |

# Bibliografía

Bigbelly. (s. f.). CLEAN software. https://bigbelly.com/products/clean-software

Boehm, B. W., Abts, C., Brown, A. W., Chulani, S., Clark, B. K., Horowitz, E., Madachy, R., Reifer, D. J., y Steece, B. (2000). Software cost estimation with COCOMO II. Prentice Hall.

Bolivia. (1977). Código de Comercio de Bolivia (Decreto Ley N° 14379 de 25 de febrero de 1977). Gaceta Oficial del Estado Plurinacional de Bolivia.

Bolivia. (1992). Ley de Derecho de Autor (Ley N° 1322 de 13 de abril de 1992) y Decreto Supremo N° 23907 reglamentario de programas de ordenador y soporte lógico.

Bolivia. (2009). Constitución Política del Estado. Gaceta Oficial del Estado Plurinacional de Bolivia.

Bolivia. (2011). Ley General de Telecomunicaciones, Tecnologías de Información y Comunicación (Ley N° 164 de 8 de agosto de 2011) y Decreto Supremo N° 1793 reglamentario.

Comunidad Andina. (2000). Decisión 486: Régimen Común sobre Propiedad Industrial. Comisión de la Comunidad Andina.

Ecube Labs. (s. f.). Smart waste management solution. https://www.ecubelabs.com/solution/

IEEE Standards Association. (2026). IEEE 730-2026 IEEE Standard for Software Quality Assurance Processes. Ficha pública del estándar. https://standards.ieee.org/ieee/730/10854/

International Organization for Standardization. (2023). ISO/IEC 25010:2023 Product quality model. Ficha pública del estándar. https://www.iso.org/standard/78176.html

Jacobson, I., Booch, G., y Rumbaugh, J. (2000). El proceso unificado de desarrollo de software. Pearson Educación, Addison Wesley. ISBN 84-7829-036-2.

NASA. (s. f.). SWE-028 Verification Planning. NASA Software Engineering Handbook. https://swehb.nasa.gov/spaces/7150/pages/16450576/SWE-028+-+Verification+Planning

NASA. (s. f.). SWE-029 Validation Planning. NASA Software Engineering Handbook. https://swehb.nasa.gov/pages/viewpage.action?pageId=23200749

Pressman, R. S. (2010). Ingeniería del software: un enfoque práctico (7.ª ed.). McGraw-Hill.

Sensoneo. (s. f.). Route planning software for waste pickup and hauling. https://www.sensoneo.com/en-us/products/route-planning/

Servicio de Impuestos Nacionales. (s. f.). Procesos de inscripción en el Registro Nacional de Contribuyentes. https://siatanexo.impuestos.gob.bo/index.php/requisitos-para-la-inscripcion/procesos-de-insccripcion

Servicio Nacional de Propiedad Intelectual. (2024). Registro en derecho de autor y derechos conexos: virtual [Folleto]. https://www.senapi.gob.bo/derecho-de-autor-y-derechos-conexos

Servicio Nacional de Propiedad Intelectual. (2021). Flujo de proceso: registro de derecho de autor y derechos conexos. https://www.senapi.gob.bo/flujo-de-procesos

Servicio Nacional de Propiedad Intelectual. (2022). Flujo de proceso: registro de signo distintivo. https://www.senapi.gob.bo/flujo-de-procesos

Servicio Nacional de Propiedad Intelectual. (s. f.). Guía para la búsqueda de antecedentes de signos distintivos. https://www.senapi.gob.bo/guias-y-cartillas

Servicio Nacional de Propiedad Intelectual. (s. f.). Registro de programas de ordenador o software. Portal oficial del Estado. https://www.gob.bo/tramites/registro-de-programas-de-ordenador-o-software

Servicio Plurinacional de Registro de Comercio. (s. f.). Trámite 2: Inscripción de Sociedad de Responsabilidad Limitada (S.R.L.), Sociedad Colectiva o Sociedad en Comandita Simple. https://www.seprec.gob.bo/index.php/tramite2/

Servicio Plurinacional de Registro de Comercio. (2026). Guía de trámites de Registro de Comercio de Bolivia. https://www.seprec.gob.bo/wp-content/uploads/2026/05/GT2026v3_28_05_2026.pdf

Las fuentes web de esta edición se consultaron el 16 de noviembre de 2026. Las descripciones de productos comerciales proceden de sus proveedores y se emplean como comparación documental.
