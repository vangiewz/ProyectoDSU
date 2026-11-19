# 1. Plan de administración del proyecto de software

## 1.1. Perfil del proyecto

### 1.1.1. Introducción

El proyecto desarrolla un sistema web para centralizar la información de generación y recolección de residuos sólidos de la Dirección de Servicios Universitarios de la UAGRM. Integra el registro de vaciados e incidencias, la planificación de jornadas, el análisis de indicadores y la representación geográfica de los puntos de recolección. Sobre el histórico registrado, incorpora Random Forest Regressor para estimar generación futura y apoyar decisiones logísticas.

El Plan de Administración del Proyecto de Software establece el alcance del producto, los recursos de trabajo, la organización del equipo y los mecanismos para controlar avances y riesgos. Su finalidad es vincular el trabajo técnico con entregables revisables y criterios de terminación. El desarrollo se organiza mediante PUDS y utiliza los casos de uso como referencia para relacionar necesidades, modelos y pruebas.

### 1.1.2. Problema y necesidad

El perfil del proyecto identifica la dispersión de registros operativos y la dificultad para consolidar un histórico de residuos por punto, sector y tipo. Esta situación limita la consulta de información para planificar jornadas, identificar puntos críticos y comparar periodos. La solución reúne estos registros en una plataforma con acceso por roles y trazabilidad de las operaciones.

La incorporación de predicciones busca complementar el análisis histórico. Su utilidad institucional dependerá de disponer de datos representativos y de evaluar el error del modelo en condiciones de uso.

### 1.1.3. Objetivo general del producto

Desarrollar un sistema web de gestión de residuos sólidos para la DSU de la UAGRM que digitalice y centralice la información operativa, permita su análisis y visualización e incorpore Random Forest Regressor para estimar la generación futura y apoyar la planificación de la recolección.

### 1.1.4. Objetivos de administración del proyecto

- Mantener un alcance trazable a los requisitos funcionales RF1 a RF27 y a sus restricciones de calidad, datos, interfaces y diseño.
- Organizar el desarrollo y la documentación mediante fases e iteraciones de PUDS, con productos revisables y responsabilidades explícitas.
- Planificar recursos y esfuerzo a partir de actividades identificables, registrando los supuestos de cada estimación.
- Aplicar seguimiento de avances, riesgos y cambios, conservando evidencias de los resultados obtenidos.
- Preparar una entrega cuya funcionalidad, documentación y condiciones de operación puedan verificarse.

Fuente del perfil y del alcance: especificación del proyecto DSU, la especificación de requisitos del proyecto, versión consultada el 16 de noviembre de 2026. La organización administrativa se desarrolla específicamente para Ingeniería de Software 2.



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

La validación con información real, la aceptación por usuarios y la puesta en marcha dependen de actividades específicas. El alcance académico no presupone contratos comerciales, certificaciones de calidad ni constitución de una empresa.

### 1.1.8. Productos del proyecto

Se prevén el sistema web y su API, la estructura de datos, los modelos UML, la documentación de administración y calidad, los registros de pruebas, las instrucciones de despliegue y el material de usuario. Cada entrega debe identificar versión, contenido, responsable de revisión y limitaciones conocidas.



## 1.2. Métricas

Se analizan tres productos comerciales de gestión inteligente de residuos y el propio sistema DSU. Para cada producto se describen sus funcionalidades y su desarrollador y se aplica la métrica orientada a la función. El código y el esfuerzo de los productos comerciales no son públicos: sus conteos son estimaciones del equipo a partir de la documentación de cada proveedor y abarcan solo el software de gestión, sin firmware ni dispositivos. Los factores de ajuste de los cuatro productos se reúnen en la sección 1.2.5.

### 1.2.1. Sensoneo

**Funcionalidades importantes.** Monitoreo del nivel de llenado de contenedores mediante sensores, planificación y optimización de rutas de recolección, aplicación para conductores, inventario de contenedores, analítica de generación y reportes para municipios y empresas (Sensoneo, s. f.).

**Captura de interfaces.**

<!-- fig: DocumentoSoftware2/recursos/web/sensoneo.png | Plataforma de gestión de Sensoneo -->

**Características del desarrollador.** Empresa de Eslovaquia especializada en gestión inteligente de residuos, con hardware propio (sensores) y plataforma en la nube. Su equipo combina desarrollo web y móvil, sistemas embebidos, comunicaciones IoT y optimización de rutas.

**Métrica orientada a la función.** El conteo se realizó sobre las funciones del software de gestión descritas en la documentación pública del proveedor.

| Parámetro de medición | Cuenta | Peso medio | Total |
| --- | --- | --- | --- |
| Entradas de usuario | 30 | 4 | 120 |
| Salidas de usuario | 20 | 5 | 100 |
| Peticiones de usuario | 20 | 4 | 80 |
| Archivos lógicos | 25 | 10 | 250 |
| Interfaces externas | 6 | 7 | 42 |
| Cuenta total | | | 592 |

PF = cuenta total × [0,65 + 0,01 × ΣFi] = 592 × [0,65 + 0,01 × 48] = 669,0 puntos de función.

### 1.2.2. Ecube Labs

**Funcionalidades importantes.** Plataforma CleanCityNetworks para monitorear en tiempo real contenedores y compactadores solares, generar rutas de recolección, emitir alertas de llenado y producir reportes y analítica histórica (Ecube Labs, s. f.).

**Captura de interfaces.**

<!-- fig: DocumentoSoftware2/recursos/web/ecube.png | Plataforma CleanCityNetworks de Ecube Labs -->

**Características del desarrollador.** Empresa de Corea del Sur que fabrica compactadores solares y sensores de llenado y desarrolla su propia plataforma. Requiere perfiles de hardware, IoT, desarrollo web y análisis de datos.

**Métrica orientada a la función.** El conteo se realizó sobre las funciones del software de gestión descritas en la documentación pública del proveedor.

| Parámetro de medición | Cuenta | Peso medio | Total |
| --- | --- | --- | --- |
| Entradas de usuario | 26 | 4 | 104 |
| Salidas de usuario | 16 | 5 | 80 |
| Peticiones de usuario | 18 | 4 | 72 |
| Archivos lógicos | 20 | 10 | 200 |
| Interfaces externas | 5 | 7 | 35 |
| Cuenta total | | | 491 |

PF = cuenta total × [0,65 + 0,01 × ΣFi] = 491 × [0,65 + 0,01 × 46] = 545,0 puntos de función.

### 1.2.3. Bigbelly

**Funcionalidades importantes.** Software CLEAN para consultar el estado de estaciones compactadoras, recibir notificaciones de llenado, revisar históricos de recolección y administrar los activos desplegados (Bigbelly, s. f.).

**Captura de interfaces.**

<!-- fig: DocumentoSoftware2/recursos/web/bigbelly.png | Estación inteligente de Bigbelly -->

**Características del desarrollador.** Empresa de Estados Unidos que comercializa estaciones compactadoras solares con un servicio de software asociado. Su desarrollo se orienta a plataforma en la nube, telemetría y soporte de operación para ciudades y campus.

**Métrica orientada a la función.** El conteo se realizó sobre las funciones del software de gestión descritas en la documentación pública del proveedor.

| Parámetro de medición | Cuenta | Peso medio | Total |
| --- | --- | --- | --- |
| Entradas de usuario | 20 | 4 | 80 |
| Salidas de usuario | 14 | 5 | 70 |
| Peticiones de usuario | 14 | 4 | 56 |
| Archivos lógicos | 16 | 10 | 160 |
| Interfaces externas | 4 | 7 | 28 |
| Cuenta total | | | 394 |

PF = cuenta total × [0,65 + 0,01 × ΣFi] = 394 × [0,65 + 0,01 × 44] = 429,5 puntos de función.

### 1.2.4. Sistema DSU

**Funcionalidades importantes.** Control de acceso por roles, catálogos del campus, registro de residuos en campo, planificación y cierre de jornadas, tablero de indicadores, mapa de calor, predicción con Random Forest Regressor, recomendaciones logísticas, reportes y bitácora de auditoría.

**Características del desarrollador.** Equipo de dos estudiantes de la FICCT con conocimientos de Django, React, PostgreSQL, modelado UML y aprendizaje automático con scikit-learn.

**Métrica orientada a la función.** Los 22 archivos lógicos son agrupaciones funcionales asumidas para estimar; no equivalen al recuento de modelos ORM o tablas; las interfaces externas son OpenStreetMap y Power BI.

| Parámetro de medición | Cuenta | Peso medio | Total |
| --- | --- | --- | --- |
| Entradas de usuario | 24 | 4 | 96 |
| Salidas de usuario | 12 | 5 | 60 |
| Peticiones de usuario | 14 | 4 | 56 |
| Archivos lógicos | 22 | 10 | 220 |
| Interfaces externas | 2 | 7 | 14 |
| Cuenta total | | | 446 |

PF = cuenta total × [0,65 + 0,01 × ΣFi] = 446 × [0,65 + 0,01 × 42] = 477,2 puntos de función.

**Métricas orientadas al tamaño.** El tamaño se midió sobre el repositorio del proyecto el 16 de noviembre de 2026, contando líneas no vacías de los archivos fuente versionados (Python, TypeScript, CSS, SQL y HTML) y excluyendo migraciones generadas, dependencias y artefactos de compilación. El esfuerzo y el costo proceden del presupuesto de referencia del proyecto (sección 1.4): son valores de planificación, no horas ni pagos registrados.

| Medida | Valor | Procedencia |
| --- | --- | --- |
| Líneas de código del backend | 5.434 LDC | Conteo del repositorio, 153 archivos fuente |
| Líneas de código del frontend | 4.983 LDC | Conteo del repositorio, 31 archivos fuente |
| Tamaño total | 10,42 KLDC | Suma de ambos componentes |
| Requisitos funcionales y casos de uso | 27 RF y 34 CU | Especificación y catálogo de casos de uso |
| Pantallas principales de la aplicación | 13 | Páginas de la interfaz React |
| Pruebas automatizadas | 42 | Suite de regresión del 16/11/2026 |
| Esfuerzo presupuestado | 7 personas-mes | Dedicaciones del presupuesto de referencia |
| Costo presupuestado | Bs. 108.268,30 | Presupuesto de referencia |

| Métrica orientada al tamaño | Cálculo | Resultado |
| --- | --- | --- |
| Productividad | 10,42 KLDC / 7 personas-mes | 1,49 KLDC por persona-mes |
| Costo por línea | Bs. 108.268,30 / 10.417 LDC | Bs. 10,39 por LDC |
| Densidad de pruebas | 42 pruebas / 10,42 KLDC | 4,03 pruebas por KLDC |
| Tamaño por caso de uso | 10.417 LDC / 34 CU | 306 LDC por CU |
| Tamaño por punto de función | 10.417 LDC / 477,2 PF | 21,8 LDC por PF |

### 1.2.5. Factores de ajuste y resumen comparativo

| Factor de ajuste (0 a 5) | Sensoneo | Ecube Labs | Bigbelly | DSU |
| --- | --- | --- | --- | --- |
| ¿Requiere respaldo y recuperación confiables? | 4 | 4 | 4 | 4 |
| ¿Requiere comunicaciones de datos especializadas? | 5 | 5 | 5 | 3 |
| ¿Existen funciones de procesamiento distribuido? | 4 | 4 | 3 | 2 |
| ¿El desempeño es crítico? | 3 | 3 | 3 | 2 |
| ¿Opera en un entorno existente muy utilizado? | 3 | 3 | 3 | 3 |
| ¿Requiere entrada de datos en línea? | 5 | 4 | 4 | 5 |
| ¿La entrada en línea abarca varias pantallas u operaciones? | 3 | 3 | 2 | 3 |
| ¿Los archivos maestros se actualizan en línea? | 4 | 4 | 4 | 4 |
| ¿Las entradas, salidas, archivos o consultas son complejos? | 3 | 3 | 3 | 3 |
| ¿El procesamiento interno es complejo? | 4 | 4 | 3 | 4 |
| ¿El código se diseña para ser reutilizable? | 2 | 2 | 2 | 3 |
| ¿El diseño incluye conversión e instalación? | 1 | 1 | 1 | 2 |
| ¿Se diseña para instalaciones múltiples en distintas organizaciones? | 5 | 5 | 5 | 0 |
| ¿Se diseña para facilitar el cambio y el uso? | 2 | 1 | 2 | 4 |
| Suma ΣFi | 48 | 46 | 44 | 42 |

El tamaño de los productos comerciales se estima por analogía, aplicando a sus puntos de función la relación medida en DSU (21,8 LDC por PF). Son órdenes de magnitud para estimar, no datos de los proveedores.

| Producto | Puntos de función | Tamaño | Procedencia del tamaño |
| --- | --- | --- | --- |
| Sensoneo | 669,0 | 14,6 KLDC | Estimado por analogía |
| Ecube Labs | 545,0 | 11,9 KLDC | Estimado por analogía |
| Bigbelly | 429,5 | 9,4 KLDC | Estimado por analogía |
| DSU | 477,2 | 10,4 KLDC | Medido en el repositorio |

### 1.2.6. Indicadores de seguimiento

| Indicador | Cálculo o registro | Uso |
| --- | --- | --- |
| Trazabilidad de requisitos | RF con vínculos revisados a CU, diseño y pruebas / 27 × 100 | Detectar requisitos sin evidencia asociada |
| Avance de entregables | Entregables revisados y aceptados / entregables planificados × 100 | Controlar productos terminados |
| Ejecución de pruebas | Casos ejecutados / casos planificados × 100 | Separar planificación y ejecución |
| Resultado de pruebas | Casos aprobados / casos ejecutados × 100 | Evaluar una ejecución identificada |
| Defectos pendientes | Recuento por severidad, estado y versión | Priorizar correcciones |
| Esfuerzo | Horas estimadas y registradas por actividad | Revisar la estimación y la capacidad |

Cada medición debe indicar fecha de corte, responsable, versión y evidencia. Si no existe denominador definido o evidencia suficiente, el indicador se registrará como no calculado.

## 1.3. Estimaciones

### 1.3.1. Dimensiones del proyecto

**Tamaño.** El sistema comprende ocho módulos, 27 requisitos funcionales, 34 casos de uso, cuatro actores y 23 modelos ORM inspeccionados (21 propios y dos de Django), con una interfaz web adaptable a escritorio y móvil.

**Complejidad.** 
La complejidad se concentra en la integración de operación, analítica y predicción. El control de acceso requiere comprobar permisos por rol y alcance; el ETL debe conservar consistencia entre datos transaccionales y analíticos; el componente predictivo requiere un histórico apropiado y evaluación del error. Estas dependencias orientan la descomposición del trabajo y la identificación de riesgos.

**Estructuración del cliente.** El cliente es la Dirección de Servicios Universitarios de la UAGRM. Sus usuarios se organizan en cuatro roles: Operativo, Supervisor, Directivo y Administrador. El equipo de desarrollo son dos integrantes que asumen análisis, diseño, programación, pruebas y documentación.

### 1.3.2. Ámbito del proyecto

**Funciones principales.** Las descritas en el alcance funcional de la sección 1.1.5, agrupadas en acceso, campus y catálogos, registro de residuos, recolecciones, inteligencia de negocios, análisis geográfico, predicción y administración.

**Rendimiento.** El registro en campo y las consultas habituales deben responder sin demoras perceptibles. El ETL, el entrenamiento y la predicción se ejecutan como procesos separados para no bloquear la operación diaria. Los valores medibles son los requisitos no funcionales de la especificación.

**Fiabilidad.** El sistema debe validar los datos de entrada, conservar el histórico, mantener la consistencia entre jornadas, puntos y registros, registrar las operaciones en la bitácora y contar con respaldo diario. Las predicciones son apoyo a la decisión y no sustituyen el criterio del personal de la DSU.

| Restricción | Descripción |
| --- | --- |
| Datos | El histórico institucional disponible es limitado y crece con el uso del sistema |
| Predicción | La precisión depende de la cantidad y calidad del histórico acumulado |
| Tiempo | El desarrollo se ajusta al semestre académico, de agosto a diciembre de 2026 |
| Recursos humanos | Equipo de dos integrantes |
| Presupuesto | Se priorizan herramientas abiertas y planes básicos de servicios en la nube |
| Conectividad | La versión actual requiere conexión; no registra fuera de línea |

| Interfaz externa | Tipo | Uso |
| --- | --- | --- |
| PostgreSQL en Neon | Software | Persistencia transaccional y analítica |
| OpenStreetMap | Software | Mapa base de la cartografía con Leaflet |
| Power BI | Software | Tablero analítico complementario |
| Usuarios de la DSU | Personas | Interacción mediante la aplicación web según su rol |
| Computadoras y teléfonos | Hardware | Acceso por navegador; el registro en campo se hace desde el teléfono |

### 1.3.3. Procedimiento de estimación

Se descompone cada entregable en actividades de análisis, preparación, elaboración, revisión y corrección. Para cada actividad se registrarán esfuerzo estimado, responsable, dependencia y criterio de cierre. La suma de horas se convertirá en duración utilizando la disponibilidad efectiva del equipo. Las actividades simultáneas no se sumarán como si fueran consecutivas.

El tamaño del producto se estima con el valor esperado, y su esfuerzo con COCOMO II en su modelo de composición de aplicación y con la ecuación del software. El trabajo restante se estima con tres puntos por actividad. Los resultados se contrastan con el presupuesto de referencia de la sección 1.4.

### 1.3.4. Valor esperado

Los tamaños estimados de los tres productos de referencia se toman como escenarios optimista, más probable y pesimista.

| Escenario | Producto de referencia | KLDC |
| --- | --- | --- |
| Optimista (O) | Bigbelly | 9,4 |
| Más probable (M) | Ecube Labs | 11,9 |
| Pesimista (P) | Sensoneo | 14,6 |
| Valor esperado (VE) | DSU | 11,93 |

VE = (O + 4M + P) / 6 = (9,4 + 4 × 11,9 + 14,6) / 6 = 11,93 KLDC. El tamaño medido del sistema, 10,42 KLDC, queda dentro del intervalo y por debajo del valor esperado.

### 1.3.5. COCOMO II

El modelo de composición de aplicación cuenta puntos objeto: pantallas, reportes y componentes escritos en lenguaje de tercera generación, ponderados por su complejidad (Boehm et al., 2000). Las pantallas son las 13 páginas de la interfaz; los reportes son los seis tipos que emite el módulo de reportes; los componentes 3GL son los cuatro servicios algorítmicos del backend: ETL, entrenamiento del modelo, predicción y recomendaciones. La clasificación de complejidad es un juicio del equipo.

| Tipo de objeto | Cantidad | Peso | Puntos objeto |
| --- | --- | --- | --- |
| Pantalla simple (inicio de sesión) | 1 | 1 | 1 |
| Pantalla media (administración, maestros, registros, recomendaciones, reportes y sistema) | 6 | 2 | 12 |
| Pantalla compleja (jornadas, campo, tablero, mapa, modelo y predicción) | 6 | 3 | 18 |
| Reporte de complejidad media | 6 | 5 | 30 |
| Componente 3GL | 4 | 10 | 40 |
| Total de puntos objeto (PO) | | | 101 |

No se asume reutilización de objetos previos, por lo que los nuevos puntos objeto son NOP = PO × (100 − 0) / 100 = 101. Con capacidad del desarrollador y madurez del entorno nominales, la productividad de referencia del modelo es PROD = 13 NOP por persona-mes. El esfuerzo estimado es E = NOP / PROD = 101 / 13 = 7,8 personas-mes. Con dos integrantes equivale a unos 3,9 meses de trabajo a dedicación completa.

El resultado es coherente con las 7 personas-mes del presupuesto de referencia y con el periodo de cuatro meses del cronograma.

### 1.3.6. Ecuación del software

Se aplican las expresiones simplificadas de Putnam y Myers (Pressman, 2010) con LDC = 11933 (valor esperado), parámetro de productividad P = 28.000 para aplicaciones de gestión y factor B = 0,16 para programas de 5 a 15 KLDC.

t mín = 8,14 × (LDC / P)^0,43 = 8,14 × (11933 / 28.000)^0,43 = 5,64 meses = 0,47 años.

E = 180 × B × t³ = 180 × 0,16 × 0,47³ = 2,99 personas-mes.

Estas expresiones están definidas para duraciones mínimas mayores a seis meses y esfuerzos desde 20 personas-mes. El proyecto queda fuera de ese intervalo, por lo que el resultado se toma solo como cota inferior y se mantiene la estimación de COCOMO II como referencia.




### 1.3.7. Estimación por actividades

Se presenta una estimación de planificación del trabajo restante, no una reconstrucción de las horas de desarrollo ya ejecutadas.

Para cada actividad se definen tres escenarios de horas persona: optimista O, probable M y pesimista P. Se calcula una referencia ponderada E = (O + 4M + P) / 6. El intervalo O–P expresa escenarios de planificación y no es un intervalo estadístico de confianza. Las actividades incluyen elaboración y corrección ordinaria; los defectos mayores que amplíen alcance requerirán reestimación.

<!-- estimacion esfuerzo -->

La estimación excluye tiempos de espera por autorización, entrega de datos, contratación o disponibilidad de usuarios. Dos integrantes no reducen automáticamente a la mitad la duración: deben considerarse dependencias, revisión cruzada y disponibilidad efectiva.

## 1.4. Recursos

El equipo está integrado por Carlos Gabriel Lobo Gutiérrez y Leonardo Serrate Basma. Ambos participan en el mismo producto; la asignación por actividad se registrará en el seguimiento del proyecto. Las responsabilidades de desarrollo y revisión deben quedar diferenciadas en cada entrega, aun cuando sean asumidas de forma alternada por los dos integrantes.

| Recurso | Aplicación | Condición de planificación |
| --- | --- | --- |
| Equipo de dos integrantes | Desarrollo, documentación y revisión | Registrar disponibilidad y distribución de tareas |
| Equipos de desarrollo | Edición, ejecución local y modelado | Inventariar características antes de estimar capacidad |
| PostgreSQL en Neon | Persistencia compartida del sistema | Coordinar migraciones y cambios de datos |
| Repositorio privado ProyectoDSU | Código, documentación y evidencias | Mantener control de versiones y accesos |
| Enterprise Architect | Modelos UML | Conservar fuentes y exportaciones consistentes |
| Entorno aislado de pruebas | Verificaciones sin afectar la base compartida | Identificar configuración y datos de cada ejecución |
| Vercel y Azure VM con Docker | Arquitectura de despliegue | Verificar instalación y operación remotas |

### 1.4.1. Presupuesto de referencia

El presupuesto cubre un periodo de desarrollo de cuatro meses, valora funciones profesionales equivalentes con los honorarios de referencia del CITI Santa Cruz (2021) y convierte los precios en dólares a Bs. 11,67 por dólar. Es un presupuesto de planificación, no una relación de gastos ejecutados.

| Categoría | Recursos considerados | Subtotal (Bs.) | Participación |
| --- | --- | --- | --- |
| Hardware | Dos computadoras de desarrollo y una balanza portátil digital | 12.450,00 | 11,50 % |
| Software | Dos licencias de Enterprise Architect Professional; el resto es software libre | 5.718,30 | 5,28 % |
| Personal | Análisis, dirección y arquitectura al 25 % y desarrollo al 100 %, cuatro meses | 82.800,00 | 76,48 % |
| Infraestructura | Espacio de trabajo y conectividad, cuatro meses | 6.000,00 | 5,54 % |
| Logística | Movilización, impresión, material y refrigerio | 1.300,00 | 1,20 % |
| Total inversión | | 108.268,30 | 100,00 % |

La operación en producción se presupuesta por separado en Bs. 1.192,56 mensuales (Bs. 26.235,72 anuales): instancia Azure VM, almacenamiento, Neon, Vercel y Power BI con las tarifas base consultadas el 16 de noviembre de 2026. El costo operativo no se suma a la inversión de desarrollo.

### 1.4.2. Conciliación de costos del cierre

El presupuesto inicial valora desarrollo y herramientas como planificación, no gastos efectivamente pagados. La referencia operativa revisada es USD 74,19/mes de plataforma más USD 28 para dos usuarios Power BI Pro: USD 102,19, aproximadamente Bs 1 192,56 al cambio de planificación 11,67. La proyección empresarial y su capital de trabajo están en los capítulos 8 y 13; no se suman indistintamente al costo de desarrollar el piloto.

## 1.5. Planificación del tiempo

### 1.5.1. Organización del trabajo con PUDS

La planificación se organiza en Inicio, Elaboración, Construcción y Transición. Los flujos de requisitos, análisis, diseño, implementación y pruebas se distribuyen dentro de las iteraciones según sus objetivos. La reconstrucción documental del trabajo ya existente conservará sus fechas y evidencias; no se registrarán como realizadas actividades para las que solo existe una propuesta.

| Fase | Resultado que se revisará | Condición de cierre |
| --- | --- | --- |
| Inicio | Problema, alcance, actores y PAPS | Alcance delimitado, riesgos iniciales y organización revisados |
| Elaboración | Requisitos, CU y arquitectura | Trazabilidad revisada y riesgos técnicos principales tratados |
| Construcción | Incrementos integrados del sistema | Funciones previstas verificadas y defectos documentados |
| Transición | Instalación, manuales y entrega | Entorno verificado y aceptación documentada con sus límites |

### 1.5.2. Secuencia de preparación de la entrega

La secuencia comienza con la revisión del PAPS y del inventario de fuentes; continúa con el SQAP y la organización de artefactos por PUDS; integra después las pruebas, los apartados de producción y los materiales de entrega; y termina con una revisión cruzada del documento y del producto. La programación de actividades se ajustará a partir de los hitos académicos y de la capacidad acordada del equipo.



### 1.5.3. Diagrama de Gantt

El cronograma del proyecto va del 18 de agosto al 19 de diciembre de 2026 y se organiza en ocho fases: inicio y planificación, captura y análisis de requisitos, diseño, desarrollo de módulos base, desarrollo de módulos analíticos, pruebas y ajustes, documentación y cierre.

<!-- fig: generador/figuras/gantt.png | Diagrama de Gantt del proyecto -->

## 1.6. Gestión de riesgos

El registro inicial identifica riesgos pertinentes al estado del proyecto. En la siguiente revisión se asignarán responsables nominales, probabilidad, impacto, fecha objetivo y evidencia de seguimiento.

| Riesgo | Consecuencia | Tratamiento |
| --- | --- | --- |
| Histórico institucional insuficiente | Predicciones sin validación representativa | Separar evaluación técnica y validación con datos reales; documentar procedencia y límites |
| Diferencias entre código y documentos | Entrega incoherente | Revisar enlaces RF, CU, modelos y pruebas en cada cambio de alcance |
| Cambios no coordinados en la base compartida | Interrupción o pérdida de consistencia | Acordar migraciones y escrituras; ejecutar pruebas en un entorno aislado |
| Fallas en el despliegue en producción | Interrupción del servicio | Verificar configuración, acceso, dependencias y recuperación antes de liberar |
| Rendimiento insuficiente en condiciones representativas | Operación lenta o rechazo de la solución | Repetir carga y tiempos de respuesta en un entorno comparable al previsto |
| Tiempo académico insuficiente | Apartados o evidencias incompletos | Priorizar entregables, estimar capacidad y revisar desviaciones |
| Manejo inadecuado de información sensible | Acceso o divulgación indebidos | Limitar accesos y excluir credenciales de documentos, capturas y exportaciones |

El seguimiento distinguirá riesgo de problema ocurrido. Cada problema debe registrar evidencia, acción correctiva, responsable y condición de cierre. La ejecución de una mitigación no cerrará automáticamente el riesgo si persiste su causa.

### 1.6.1. Escala y valoración inicial

Se utiliza una escala ordinal de probabilidad e impacto de 1 a 5. En probabilidad, 1 expresa posibilidad baja según información disponible y 5 exposición muy alta; no representan porcentajes medidos. En impacto, 1 es una corrección menor, 3 afecta un entregable y 5 compromete información, operación o aceptación. La exposición se calcula como P × I. Se propone tratar primero valores de 15 a 25, después 8 a 14 y finalmente 1 a 7.

| Riesgo | P e I | Exposición y razón |
| --- | --- | --- |
| Histórico real no disponible | P 4; I 5 | 20. Condiciona la validación institucional del modelo |
| Fallas en el despliegue | P 3; I 4 | 12. Depende de servicios externos y de su configuración |
| Cambios no coordinados en datos | P 3; I 5 | 15. La base demo es compartida |
| Desajuste documento código | P 3; I 4 | 12. Existen varios artefactos que deben mantenerse consistentes |
| Rendimiento no representativo | P 3; I 4 | 12. Se requieren mediciones en condiciones de operación |

El equipo actualizará prioridad y tratamiento cuando cambien las condiciones o se obtenga evidencia nueva.

## 1.7. Organización interna

Cada actividad tiene un integrante responsable de elaborarla y el otro encargado de revisarla. La coordinación del proyecto mantendrá el inventario de entregables y la programación; la responsabilidad técnica revisará consistencia de arquitectura e implementación; la función de calidad comprobará criterios y evidencias.

La DSU es la organización destinataria del producto. La evaluación académica corresponde al docente de Ingeniería de Software 2 y se gestiona mediante los entregables de esta materia.



<!-- fig: DocumentoSoftware2/recursos/organigrama_equipo.png | Organización interna del equipo -->

## 1.8. Seguimiento y control

Se realiza una revisión semanal del avance, complementada por revisiones al cerrar cada entregable. El registro debe incluir actividad, responsable, estado, fecha prevista, evidencia y observaciones. Los estados serán pendiente, en elaboración, en revisión, observado y cerrado. Un entregable solo pasará a cerrado cuando exista revisión y se hayan resuelto o aceptado explícitamente sus observaciones.

Los cambios de requisitos se evaluarán por su efecto sobre casos de uso, diseño, código, pruebas y documentación. La decisión y su justificación se registrarán antes de actualizar la línea base.

El estado técnico consultado el 16 de noviembre de 2026 informa implementación de RF1 a RF27 y una regresión de 42 pruebas aprobadas en un entorno PostgreSQL desechable, repetida en una imagen Linux. Este registro es una evidencia técnica existente, no una declaración de aceptación de todos los requisitos.

## 1.9. Tecnologías de desarrollo

La solución utiliza Django y Django REST Framework para la API, React para la interfaz web y PostgreSQL gestionado por Neon para la persistencia. El componente predictivo se implementa con scikit-learn; el procesamiento de datos emplea herramientas del entorno Python. La visualización geográfica integra Leaflet y OpenStreetMap, y la analítica contempla tableros de la aplicación e integración con Power BI.

Los modelos UML se mantienen en Enterprise Architect y el código se versiona con Git en el repositorio privado del proyecto. La arquitectura productiva separa el frontend en Vercel y el backend en Azure VM con Linux y Docker. Las versiones exactas y la configuración reproducible se documentarán en el inventario de infraestructura, evitando confundir una arquitectura con un despliegue ya comprobado.
