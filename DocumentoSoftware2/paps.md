# 1. Plan de administración del proyecto de software

## 1.1. Perfil del proyecto

### 1.1.1. Introducción

El proyecto desarrolla un sistema web para centralizar la información de generación y recolección de residuos sólidos de la Dirección de Servicios Universitarios de la UAGRM. Integra el registro de vaciados e incidencias, la planificación de jornadas, el análisis de indicadores y la representación geográfica de los puntos de recolección. Sobre el histórico registrado, incorpora Random Forest Regressor para estimar generación futura y apoyar decisiones logísticas.

El Plan de Administración del Proyecto de Software establece el alcance del producto, los recursos de trabajo, la organización del equipo y los mecanismos para controlar avances y riesgos. Su finalidad es vincular el trabajo técnico con entregables revisables y criterios de terminación. El desarrollo se organiza mediante PUDS y utiliza los casos de uso como referencia para relacionar necesidades, modelos y pruebas.

### 1.1.2. Problema y necesidad

El perfil del proyecto identifica la dispersión de registros operativos y la dificultad para consolidar un histórico de residuos por punto, sector y tipo. Esta situación limita la consulta de información para planificar jornadas, identificar puntos críticos y comparar periodos. La solución propuesta reúne estos registros en una plataforma con acceso por roles y trazabilidad de las operaciones.

La incorporación de predicciones busca complementar el análisis histórico. Su utilidad institucional dependerá de disponer de datos representativos y de evaluar el error del modelo en condiciones de uso. La existencia de una implementación predictiva no demuestra, por sí sola, reducción de costos ni mejora de la recolección.

### 1.1.3. Objetivo general del producto

Desarrollar un sistema web de gestión de residuos sólidos para la DSU de la UAGRM que digitalice y centralice la información operativa, permita su análisis y visualización e incorpore Random Forest Regressor para estimar la generación futura y apoyar la planificación de la recolección.

### 1.1.4. Objetivos de administración del proyecto

- Mantener un alcance trazable a los requisitos funcionales RF1 a RF27 y a sus restricciones de calidad, datos, interfaces y diseño.
- Organizar el desarrollo y la documentación mediante fases e iteraciones de PUDS, con productos revisables y responsabilidades explícitas.
- Planificar recursos y esfuerzo a partir de actividades identificables, registrando los supuestos de cada estimación.
- Aplicar seguimiento de avances, riesgos y cambios, conservando evidencias de los resultados obtenidos.
- Preparar una entrega cuya funcionalidad, documentación y condiciones de operación puedan verificarse.

Fuente del perfil y del alcance: especificación del proyecto DSU, capítulos 1 y 4 del documento de Taller de Grado I, versión consultada el 16 de noviembre de 2026. La organización administrativa se desarrolla específicamente para Ingeniería de Software 2.



### 1.1.5. Alcance funcional

El alcance conserva los identificadores de requisitos del sistema compartido. Los siguientes grupos resumen el producto; el detalle de reglas, permisos y condiciones se mantiene en la especificación de requisitos.

| Área | Funciones incluidas | Requisitos |
| --- | --- | --- |
| Acceso | Usuarios, roles, permisos y autenticación | RF1 a RF3 |
| Catálogos y territorio | Sectores, facultades, puntos, tipos de residuo, unidades y contenedores | RF4 a RF7 |
| Registro operativo | Vaciados, histórico de residuos e incidencias | RF8 a RF10 |
| Recolección y logística | Jornadas, rutas, ejecución, personal, vehículos e historial | RF11 a RF14 |
| Analítica | ETL, indicadores, tableros y comparación de periodos | RF15 a RF18 |
| Cartografía | Puntos georreferenciados, mapas de calor y filtros | RF19 a RF21 |
| Predicción | Entrenamiento y evaluación, estimaciones, alertas y recomendaciones | RF22 a RF24 |
| Administración | Parámetros, auditoría y reportes exportables | RF25 a RF27 |

### 1.1.6. Usuarios y beneficiarios

El sistema contempla cuatro actores: Administrador, Supervisor, Operativo y Directivo. El Administrador gestiona accesos y configuración conforme a sus permisos; el Supervisor organiza y supervisa la operación; el Operativo registra las actividades de campo autorizadas; el Directivo consulta información para la toma de decisiones. Los permisos detallados se verifican por caso de uso y no se amplían por la denominación del cargo.

### 1.1.7. Límites y dependencias

La aplicación es web y requiere conectividad para registrar operaciones. La versión actual no encola registros de campo sin conexión. Las recomendaciones apoyan al personal responsable y no sustituyen su decisión sobre las jornadas. La planificación logística no supone que exista un algoritmo de optimización automática de rutas.

Los datos de demostración y los históricos sintéticos permiten comprobar comportamientos técnicos, pero no acreditan precisión predictiva institucional. La validación con información real, la aceptación por usuarios y la puesta en marcha dependen de actividades específicas. El alcance académico no presupone contratos comerciales, certificaciones de calidad ni constitución de una empresa.

### 1.1.8. Productos del proyecto

Se prevén el sistema web y su API, la estructura de datos, los modelos UML, la documentación de administración y calidad, los registros de pruebas, las instrucciones de despliegue y el material de usuario. Cada entrega deberá identificar versión, contenido, responsable de revisión y limitaciones conocidas.



## 1.2. Métricas

### 1.2.1. Base de medición

La especificación y el modelo de casos de uso constituyen la base inicial para medir alcance y trazabilidad. El inventario documental vigente comprende 27 requisitos funcionales, 34 casos de uso y cuatro actores. Estos recuentos describen el tamaño funcional documentado; no equivalen a puntos de función ni permiten deducir directamente esfuerzo o porcentaje de terminación.

El capítulo 8 presenta una primera comparación documental de Sensoneo, Ecube Labs y Bigbelly, con fuentes de los proveedores. Esta revisión identifica funciones observables y límites de información. El conteo funcional deberá explicar sus reglas y distinguir las funcionalidades verificadas de las inferidas. No se asignará un tamaño a productos externos únicamente por sus pantallas comerciales.

### 1.2.2. Indicadores propuestos

| Indicador | Cálculo o registro | Uso |
| --- | --- | --- |
| Trazabilidad de requisitos | RF con vínculos revisados a CU, diseño y pruebas / 27 × 100 | Detectar requisitos sin evidencia asociada |
| Avance de entregables | Entregables revisados y aceptados / entregables planificados × 100 | Controlar productos terminados |
| Ejecución de pruebas | Casos ejecutados / casos planificados × 100 | Separar planificación y ejecución |
| Resultado de pruebas | Casos aprobados / casos ejecutados × 100 | Evaluar una ejecución identificada |
| Defectos pendientes | Recuento por severidad, estado y versión | Priorizar correcciones |
| Esfuerzo | Horas estimadas y registradas por actividad | Revisar la estimación y la capacidad |

Cada medición deberá indicar fecha de corte, responsable, versión y evidencia. Si no existe denominador definido o evidencia suficiente, el indicador se registrará como no calculado. Una tasa de aprobación de pruebas no representa por sí sola la cobertura del sistema.

## 1.3. Estimaciones

### 1.3.1. Dimensiones y complejidad

La complejidad se concentra en la integración de operación, analítica y predicción. El control de acceso requiere comprobar permisos por rol y alcance; el ETL debe conservar consistencia entre datos transaccionales y analíticos; el componente predictivo requiere un histórico apropiado y evaluación del error. Estas dependencias orientan la descomposición del trabajo y la identificación de riesgos.

### 1.3.2. Procedimiento de estimación

Se propone descomponer cada entregable en actividades de análisis, preparación, elaboración, revisión y corrección. Para cada actividad se registrarán esfuerzo estimado, responsable, dependencia y criterio de cierre. La suma de horas se convertirá en duración utilizando la disponibilidad efectiva del equipo. Las actividades simultáneas no se sumarán como si fueran consecutivas.

La estimación inicial de esfuerzo se presenta a continuación. Su adopción como línea base requiere revisar actividades y dedicación de los integrantes. El costo monetario se calculará cuando existan tarifas y servicios identificados. Si se incorpora una estimación por puntos de función o COCOMO, deberá conservarse el conteo, los parámetros y su justificación; sus resultados se contrastarán con la estimación por actividades. Los gastos del proyecto se separarán del valor estimado del trabajo académico.



### 1.3.3. Estimación inicial del trabajo pendiente

Se presenta una estimación de planificación del trabajo restante, no una reconstrucción de las horas de desarrollo ya ejecutadas. Los valores constituyen una propuesta inicial para revisión conjunta por los integrantes. No proceden de una medición histórica ni de una sesión de estimación registrada.

Para cada actividad se definen tres escenarios de horas persona: optimista O, probable M y pesimista P. Se calcula una referencia ponderada E = (O + 4M + P) / 6. El intervalo O–P expresa escenarios de planificación y no es un intervalo estadístico de confianza. Las actividades incluyen elaboración y corrección ordinaria; los defectos mayores que amplíen alcance requerirán reestimación.

<!-- estimacion esfuerzo -->

La estimación excluye tiempos de espera por autorización, entrega de datos, contratación o disponibilidad de usuarios. Las tareas de evaluación institucional solo podrán ejecutarse cuando existan sus entradas. Dos integrantes no reducen automáticamente a la mitad la duración: deben considerarse dependencias, revisión cruzada y disponibilidad efectiva. No se fija una fecha de entrega en este plan.

### 1.3.4. Recursos económicos por presupuestar

El presupuesto deberá separar esfuerzo del equipo, servicios de infraestructura, herramientas o licencias, preparación de material y contingencias. El costo de trabajo se calculará multiplicando horas por una tarifa justificada; el costo operativo identificará servicio, plan, periodo e impuestos aplicables. No se asigna un precio de venta a partir del esfuerzo estimado ni se presentan gastos académicos como pagos efectivamente realizados.

## 1.4. Recursos

El equipo está integrado por Carlos Gabriel Lobo Gutiérrez y Leonardo Serrate Basma. Ambos participan en el mismo producto; la asignación por actividad se registrará en el seguimiento del proyecto. Las responsabilidades de desarrollo y revisión deberán quedar diferenciadas en cada entrega, aun cuando sean asumidas de forma alternada por los dos integrantes.

| Recurso | Aplicación | Condición de planificación |
| --- | --- | --- |
| Equipo de dos integrantes | Desarrollo, documentación y revisión | Registrar disponibilidad y distribución de tareas |
| Equipos de desarrollo | Edición, ejecución local y modelado | Inventariar características antes de estimar capacidad |
| PostgreSQL en Neon | Persistencia compartida del sistema | Coordinar migraciones y cambios de datos |
| Repositorio privado ProyectoDSU | Código, documentación y evidencias | Mantener control de versiones y accesos |
| Enterprise Architect | Modelos UML | Conservar fuentes y exportaciones consistentes |
| Entorno aislado de pruebas | Verificaciones sin afectar la base compartida | Identificar configuración y datos de cada ejecución |
| Vercel y AWS EC2 con Docker | Arquitectura de despliegue prevista | Verificar instalación y operación remotas |

## 1.5. Planificación del tiempo

### 1.5.1. Organización del trabajo con PUDS

La planificación se organiza en Inicio, Elaboración, Construcción y Transición. Los flujos de requisitos, análisis, diseño, implementación y pruebas se distribuyen dentro de las iteraciones según sus objetivos. La reconstrucción documental del trabajo ya existente conservará sus fechas y evidencias; no se registrarán como realizadas actividades para las que solo existe una propuesta.

| Fase | Resultado que se revisará | Condición de cierre propuesta |
| --- | --- | --- |
| Inicio | Problema, alcance, actores y PAPS | Alcance delimitado, riesgos iniciales y organización revisados |
| Elaboración | Requisitos, CU y arquitectura | Trazabilidad revisada y riesgos técnicos principales tratados |
| Construcción | Incrementos integrados del sistema | Funciones previstas verificadas y defectos documentados |
| Transición | Instalación, manuales y entrega | Entorno verificado y aceptación documentada con sus límites |

### 1.5.2. Secuencia de preparación de la entrega

La secuencia propuesta comienza con la revisión del PAPS y del inventario de fuentes; continúa con el SQAP y la organización de artefactos por PUDS; integra después las pruebas, los apartados de producción y los materiales de entrega; y termina con una revisión cruzada del documento y del producto. La programación de actividades se ajustará a partir de los hitos académicos y de la capacidad acordada del equipo.



## 1.6. Gestión de riesgos

El registro inicial identifica riesgos pertinentes al estado del proyecto. Los tratamientos planteados son propuestas de planificación; no representan medidas aprobadas por la DSU. En la siguiente revisión se asignarán responsables nominales, probabilidad, impacto, fecha objetivo y evidencia de seguimiento.

| Riesgo | Consecuencia | Tratamiento propuesto |
| --- | --- | --- |
| Histórico institucional insuficiente | Predicciones sin validación representativa | Separar evaluación técnica y validación con datos reales; documentar procedencia y límites |
| Diferencias entre código y documentos | Entrega incoherente | Revisar enlaces RF, CU, modelos y pruebas en cada cambio de alcance |
| Cambios no coordinados en la base compartida | Interrupción o pérdida de consistencia | Acordar migraciones y escrituras; ejecutar pruebas en un entorno aislado |
| Despliegue remoto no comprobado | Fallos durante la entrega | Verificar configuración, acceso, dependencias y recuperación antes de liberar |
| Rendimiento insuficiente en condiciones representativas | Operación lenta o rechazo de la solución | Repetir carga y tiempos de respuesta en un entorno comparable al previsto |
| Tiempo académico insuficiente | Apartados o evidencias incompletos | Priorizar entregables, estimar capacidad y revisar desviaciones |
| Manejo inadecuado de información sensible | Acceso o divulgación indebidos | Limitar accesos y excluir credenciales de documentos, capturas y exportaciones |

El seguimiento distinguirá riesgo de problema ocurrido. Cada problema deberá registrar evidencia, acción correctiva, responsable y condición de cierre. La ejecución de una mitigación no cerrará automáticamente el riesgo si persiste su causa.

### 1.6.1. Escala y valoración inicial propuesta

Se propone una escala ordinal de probabilidad e impacto de 1 a 5. En probabilidad, 1 expresa posibilidad baja según información disponible y 5 exposición muy alta; no representan porcentajes medidos. En impacto, 1 es una corrección menor, 3 afecta un entregable y 5 compromete información, operación o aceptación. La exposición se calcula como P × I. Se propone tratar primero valores de 15 a 25, después 8 a 14 y finalmente 1 a 7.

| Riesgo | P e I propuestos | Exposición y razón |
| --- | --- | --- |
| Histórico real no disponible | P 4; I 5 | 20. Condiciona la validación institucional del modelo |
| Despliegue sin verificar | P 4; I 4 | 16. Existe configuración, pero falta evidencia remota |
| Cambios no coordinados en datos | P 3; I 5 | 15. La base demo es compartida |
| Desajuste documento código | P 3; I 4 | 12. Existen varios artefactos que deben mantenerse consistentes |
| Rendimiento no representativo | P 3; I 4 | 12. Se requieren mediciones en condiciones de operación |

Los valores son una evaluación inicial propuesta, pendiente de revisión conjunta. No describen incidentes ya ocurridos. El equipo actualizará prioridad y tratamiento cuando cambien las condiciones o se obtenga evidencia nueva.

## 1.7. Organización interna

Se propone que cada actividad tenga un integrante responsable de elaborarla y el otro encargado de revisarla. La coordinación del proyecto mantendrá el inventario de entregables y la programación; la responsabilidad técnica revisará consistencia de arquitectura e implementación; la función de calidad comprobará criterios y evidencias. Estas funciones se asignarán por actividad y no implican un equipo adicional.

La DSU es la organización destinataria del producto. La participación de sus representantes en validaciones y aceptación se coordinará y documentará cuando ocurra. La evaluación académica corresponde al docente de Ingeniería de Software 2 y se gestiona mediante los entregables de esta materia.



## 1.8. Seguimiento y control

Se propone una revisión semanal del avance, complementada por revisiones al cerrar cada entregable. El registro deberá incluir actividad, responsable, estado, fecha prevista, evidencia y observaciones. Los estados serán pendiente, en elaboración, en revisión, observado y cerrado. Un entregable solo pasará a cerrado cuando exista revisión y se hayan resuelto o aceptado explícitamente sus observaciones.

Los cambios de requisitos se evaluarán por su efecto sobre casos de uso, diseño, código, pruebas y documentación. La decisión y su justificación se registrarán antes de actualizar la línea base. Los cambios de presentación propios de una materia se gestionarán en su documento; los cambios del producto deberán conservar consistencia en ambas materias.

El estado técnico consultado el 16 de noviembre de 2026 informa implementación de RF1 a RF27 y una regresión de 42 pruebas aprobadas en un entorno PostgreSQL desechable, repetida en una imagen Linux. Este registro es una evidencia técnica existente, no una declaración de aceptación de todos los requisitos. El despliegue remoto, la validación predictiva con datos institucionales y otras comprobaciones de operación continúan sujetos a cierre específico.

## 1.9. Tecnologías de desarrollo

La solución utiliza Django y Django REST Framework para la API, React para la interfaz web y PostgreSQL gestionado por Neon para la persistencia. El componente predictivo se implementa con scikit-learn; el procesamiento de datos emplea herramientas del entorno Python. La visualización geográfica integra Leaflet y OpenStreetMap, y la analítica contempla tableros de la aplicación e integración con Power BI.

Los modelos UML se mantienen en Enterprise Architect y el código se versiona con Git en el repositorio privado del proyecto. La arquitectura productiva prevista separa el frontend en Vercel y el backend en AWS EC2 con Linux y Docker. Las versiones exactas y la configuración reproducible se documentarán en el inventario de infraestructura, evitando confundir una arquitectura prevista con un despliegue ya comprobado.

