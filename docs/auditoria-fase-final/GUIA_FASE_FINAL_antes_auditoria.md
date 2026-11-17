# Guía Fase Final: Capítulos 8, 9 y 10 (Implementación, Pruebas, Costos, Riesgos y Seguridad)

Taller de Grado I, Grupo 8 — Sistema Web de Gestión de Residuos Sólidos para la DSU-UAGRM con Predicción mediante Random Forest Regressor.  
Docente: M.Sc. Ing. José Junior Villagómez Melgar.

---

## 1. Fuentes de Autoridad y Contexto

Esta guía establece los lineamientos oficiales, técnicos y metodológicos para la elaboración, redacción, modelado y defensa de la **Fase Final** del proyecto, estructurada jerárquicamente por orden de prelación:

1. **Instrucciones directas del docente en clases magistrales**:
   - Clase 06/11/2026: Capítulo 8 (Implementación) → [Contexto y marcas temporales](clases/2026-11-06_cap8_implementacion_contexto.md) | [Transcripción](clases/2026-11-06_cap8_implementacion.txt).
   - Clase 11/11/2026: Capítulo 10 (Costos, Riesgos y Seguridad) y Fase Final → [Contexto y marcas temporales](clases/2026-11-11_cap9-10_pruebas_costos_contexto.md) | [Transcripción](clases/2026-11-11_cap9_pruebas_costos.txt).
2. **Láminas oficiales del docente** (subidas a Classroom, respaldadas en `cap8-10/`):
   - [Fase 3 _ Cap 8 Implementacón.pdf](cap8-10/Fase%203%20_%20Cap%208%20Implementac%C3%B3n.pdf) (11 págs.).
   - [Fase 3 _ Cap 9 Pruebas.pdf](cap8-10/Fase%203%20_%20Cap%209%20Pruebas.pdf) (23 págs.).
   - [CAP 10 - Costos.pdf](cap8-10/CAP%2010%20-%20Costos.pdf) (7 págs.).
3. **Evidencias visuales de clase y diapositivas**:
   - Capturas de grabación: [clases/evidencias-2026-11-06/](clases/evidencias-2026-11-06/) y [clases/evidencias-2026-11-11/](clases/evidencias-2026-11-11/).
   - Recursos gráficos vectoriales de láminas: [clases/recursos_diapositivas/](clases/recursos_diapositivas/).
4. **Bibliografía base de la materia**:
   - Jacobson, I., Booch, G., & Rumbaugh, J. (2000). *El proceso unificado de desarrollo de software*. Pearson Educación:
     - Capítulo 10: "El flujo de trabajo de la implementación" (base del Cap. 8).
     - Capítulo 11: "El flujo de trabajo de la prueba" (base del Cap. 9).
   - Pressman, R. S., & Maxim, B. R. (2020). *Ingeniería del software: Un enfoque práctico* (9.ª ed.). McGraw-Hill (Pruebas de caja blanca, grafos de flujo y complejidad ciclomática de McCabe).
   - Aranceles profesionales de la **Sociedad de Ingenieros de Bolivia (SIB)** — Colegio de Ingenieros de Sistemas.
   - Normas APA 7.ª edición (formato estricto para tablas, figuras y notas).

---

## 2. Cronograma, Modalidad de Entrega y Defensa Final

| Aspecto | Directriz Oficial del Docente |
|---|---|
| **Ponderación Académica** | **Revisión Final de Documento: 30 pts** \| **Revisión Final de Software / Defensa: 30 pts**. *(No aprobar las revisiones finales equivale a reprobar la materia)*. |
| **Alcance Documental** | **Documento Completo (Capítulos 1 al 10)**, integrando Fase 1 (Cap. 1 a 4), Fase 2 (Cap. 5 a 7) y Fase Final (Cap. 8 a 10), con carátula formal, índice general, índices de tablas y figuras, y bibliografía consolidada APA 7ma. |
| **Modalidad de Entrega** | **Formato Digital** (PDF y DOCX en Classroom/Drive) y **Formato Físico Impreso** (anillado/empastado según reglamento de la facultad para biblioteca). |
| **Defensa en Vivo del Software** | El docente revisará el software desarrollado en vivo: base de datos poblada con datos realistas, autenticación por roles (RBAC), operaciones CRUD completas de los CU prioritarios, mapa interactivo con puntos de recolección y rutas, analítica visual con gráficos y **ejecución real del modelo de Machine Learning (Random Forest)** en inferencia y predicción. |
| **Coherencia Documento–Software** | El software en ejecución debe coincidir al 100% con los planos del documento: mismos nombres de clases, mismos atributos y métodos, mismos endpoints y protocolos (`«JSON/HTTPS»`), y mismos modelos ORM mapeados a tablas de PostgreSQL. |

---

## 3. Reglas Duras del Ingeniero para la Fase Final

### En el Capítulo 8 (Implementación)
1. **PROHIBIDO pegar código fuente en el Capítulo 8**: El docente fue taxativo: *"Lo demás ya es lenguaje de máquina… código de programación, que no lo vamos a contemplar en el documento, al menos por ahora"*. El Cap. 8 modela la arquitectura y los subsistemas con diagramas de componentes, NO con volcados de código.
2. **Notación UML formal en Enterprise Architect**: Todos los diagramas deben generarse con Enterprise Architect bajo notación UML 2.5 estricta (marco `cmp` para componentes). Nada de dibujos informales o diagramas redondeados.
3. **8.1 Arquitectura del Sistema (Vista General)**:
   - Debe mostrar los paquetes del sistema como un todo, conectados mediante dependencias lógicas hacia el componente central de software `«source»`.
   - Abajo, deben mostrarse obligatoriamente los componentes de datos diferenciados: componente `«OLTP»` (Base de Datos Transaccional) y componente `«OLAP»` (Estructura Analítica de Datos para BI).
4. **8.2 Arquitectura del Subsistema**:
   - **Regla de oro**: *"Cada paquete viene a ser un subsistema"*. Debe existir **un subíndice y un diagrama de componentes por cada paquete** definido en el Capítulo 6. Para DSU-UAGRM son exactamente **8 subsistemas (8.2.1 a 8.2.8)**.
   - Cada figura de subsistema debe mostrar:
     - Componente **Cliente** (artefactos frontend: formularios, componentes React).
     - Conector de comunicación rotulado explícitamente **`«JSON/HTTPS»`** con JWT.
     - Componente **Servidor** (capa de negocio: controladores/vistas DRF, serializadores, servicios; capa de datos: modelos ORM conectando a PostgreSQL).
5. **8.3 Herramientas de Desarrollo**:
   - Estructura obligatoria en 6 subpuntos: 8.3.1 Lenguajes de programación, 8.3.2 Librerías, 8.3.3 Frameworks, 8.3.4 SGBD, 8.3.5 Lenguaje de Modelado de Software, 8.3.6 Protocolos de Comunicación.
   - Los protocolos de 8.3.6 deben coincidir milimétricamente con los conectores de los subsistemas (8.2) y con el diagrama de despliegue (7.1.1).

### En el Capítulo 9 (Pruebas)
1. **Cita APA obligatoria de apertura**: Citar a Jacobson, Booch y Rumbaugh (2000, Cap. 11).
2. **Plantilla estricta de 7 campos para Pruebas de Caja Negra (9.3.1)**:
   - Toda tabla de prueba funcional debe contener exactamente: (1) Nombre de caso de prueba, (2) Descripción, (3) Precondición, (4) Entrada, (5) Condición de ejecución, (6) Resultado obtenido, (7) Resultado esperado.
   - Aplicar a los Casos de Uso más críticos del sistema.
3. **Metodología de 5 pasos para Pruebas de Caja Blanca (9.3.2)**:
   - (1) Nombre del CU y función analizada; (2) Código fuente con líneas/nodos numerados; (3) Grafo de Flujo de Control (CFG) con nodos y aristas numerados; (4) Cálculo de Complejidad Ciclomática de McCabe ($V(G) = E - N + 2P$); (5) Tabla de Caminos Independientes (Camino, Entrada/Condición, Salida esperada).
4. **Pruebas de Vulnerabilidad (9.3.3)**:
   - Seleccionar un software especializado de seguridad (OWASP ZAP / SonarQube), describir la herramienta, ejecutar escaneo automatizado contra la API y la interfaz web, y reportar la matriz de vulnerabilidades encontradas y mitigadas.

### En el Capítulo 10 (Costos, Riesgos y Seguridad)
1. **Moneda oficial en Bolivianos (Bs.)**: Todos los costos de hardware, software, personal, infraestructura y logística deben expresarse en **Bolivianos (Bs.)**.
2. **Tabla General de Costos (10.1)**: Ubicar primero una tabla resumen con los subtotales de cada categoría y la sumatoria total de la inversión, antes de los desgloses 10.1.1 a 10.1.5.
3. **Aranceles profesionales de la SIB (10.1.3)**: Los sueldos y honorarios del personal deben respaldarse en las tablas arancelarias de la **Sociedad de Ingenieros de Bolivia (SIB)** / Colegio de Ingenieros de Sistemas de Santa Cruz.
4. **Cálculo Matemático del ROI a 12 meses (10.2)**:
   - Proyectar los tres componentes a 12 meses: (1.2.1) Incremento por uso del sistema, (1.2.2) Incremento por análisis de datos / predicciones ML, (1.2.3) Reducción de costos.
   - Beneficio Total = Suma de los tres beneficios proyectados a 12 meses.
   - Beneficio Neto = Beneficio Total - Costo de Inversión.
   - Fórmula: $ROI = \left(\frac{\text{Beneficio Neto}}{\text{Costo de Inversión}}\right) \times 100\%$.
   - Redactar la conclusión textual obligatoria estipulada por el docente: *"Esto significa que, en un periodo de 12 meses la entidad tendrá un retorno de inversión del X.XX% sobre el costo del desarrollo e implementación del software"*.
5. **Matriz de Riesgos y Contingencia (10.3)**:
   - Una sola tabla partida conceptualmente: Mitad izquierda (Tipo de riesgo, Descripción, Probabilidad %, Impacto Alto/Medio/Bajo); Mitad derecha (Plan de contingencia / Respuesta al riesgo).
   - Categorías obligatorias: **Riesgos Técnicos, Riesgos de Gestión y Riesgos Institucionales**.
6. **Seguridad Lógica y Física (10.4)**:
   - Cita bibliográfica teórica obligatoria al inicio de 10.4.1 y 10.4.2.
   - Descripción de arquitectura y medidas implementadas.
   - **Tabla matriz de Riesgos Identificados vs. Solución Implementada** tanto para seguridad lógica como para seguridad física.

---

## 4. Especificación Técnica Detallada — Capítulo 8: Implementación

### 4.1 Apertura del Capítulo
- **Cita APA obligatoria**:
  > Jacobson, I., Booch, G., & Rumbaugh, J. (2000). *El proceso unificado de desarrollo de software* (Cap. 10). Pearson Educación.
  > *"La mayor parte de la arquitectura del sistema es capturada durante el Diseño, siendo el propósito principal de la Implementación el desarrollar la arquitectura y el sistema como un todo."*
- Párrafo que sintetice el paso de los modelos de diseño (Cap. 7) a artefactos ejecutables, ficheros de código, componentes de base de datos y herramientas de soporte.

### 4.2 Sección 8.1: Implementación de la Arquitectura del Sistema
- **Figura**: `Diagrama de Componentes de la Arquitectura del Sistema`. Marco UML `cmp`.
- **Estructura del diagrama**:
  - Los **8 paquetes del sistema** (heredados de 6.1 y 6.3):
    1. Gestión de Usuarios y Control de Acceso
    2. Gestión Topológica y Puntos de Recolección
    3. Gestión de Residuos
    4. Gestión de Recolecciones y Logística
    5. Inteligencia de Negocios y Analítica Visual
    6. Componente Cartográfico y Análisis Espacial
    7. Predicción mediante Random Forest Regressor
    8. Administración de la Plataforma y Auditoría
  - Componente central: `«source» Sistema Web DSU-UAGRM`.
  - Componente de persistencia transaccional: `«OLTP» Base de Datos Transaccional (PostgreSQL)`.
  - Componente de datos analíticos: `«OLAP» Estructura Analítica BI (HechoResiduo / Vistas bi_*)`.
  - Artefacto de Machine Learning: `«file» modelo_random_forest.joblib` (componente fichero según Jacobson p. 4).

### 4.3 Sección 8.2: Implementación de la Arquitectura del Subsistema
Debe redactarse una sección y una figura en Enterprise Architect para cada uno de los 8 subsistemas:

```
8.2.1. Implementación de la Arquitectura del Subsistema Gestión de Usuarios y Control de Acceso
       Figura XX. Diagrama de Componentes de la Implementación del Subsistema Usuarios y Control de Acceso
8.2.2. Implementación de la Arquitectura del Subsistema Gestión Topológica y Puntos de Recolección
       Figura XX. Diagrama de Componentes de la Implementación del Subsistema Topología y Puntos
8.2.3. Implementación de la Arquitectura del Subsistema Gestión de Residuos
       Figura XX. Diagrama de Componentes de la Implementación del Subsistema Gestión de Residuos
8.2.4. Implementación de la Arquitectura del Subsistema Gestión de Recolecciones y Logística
       Figura XX. Diagrama de Componentes de la Implementación del Subsistema Recolecciones y Logística
8.2.5. Implementación de la Arquitectura del Subsistema Inteligencia de Negocios y Analítica Visual
       Figura XX. Diagrama de Componentes de la Implementación del Subsistema Inteligencia de Negocios
8.2.6. Implementación de la Arquitectura del Subsistema Componente Cartográfico y Análisis Espacial
       Figura XX. Diagrama de Componentes de la Implementación del Subsistema Cartográfico y Espacial
8.2.7. Implementación de la Arquitectura del Subsistema Predicción mediante Random Forest Regressor
       Figura XX. Diagrama de Componentes de la Implementación del Subsistema Predicción Random Forest
8.2.8. Implementación de la Arquitectura del Subsistema Administración de la Plataforma y Auditoría
       Figura XX. Diagrama de Componentes de la Implementación del Subsistema Administración y Auditoría
```

#### Anatomía de cada Diagrama de Componentes de Subsistema:
- **Componente Cliente (SPA React)**:
  - Estereotipo `«subsystem»` o `«component»` rotulado `Cliente Web (React SPA)`.
  - Ficheros/Páginas internas con estereotipo `«Form»` o `«View»` (ej. `LoginForm.tsx`, `UsuariosPage.tsx`, `PesajeForm.tsx`).
- **Conector de Red**:
  - Línea de dependencia punteada con flecha hacia el servidor, rotulada explícitamente con el estereotipo:
    $$\mathbf{\ll JSON/HTTPS \gg}$$
    *(Anotar puerto 443 / TLS 1.3 con autenticación JWT Bearer)*.
- **Componente Servidor (API Django REST Framework)**:
  - Capa de Controladores: Clases con estereotipo `«controller»` (ej. `UsuarioViewSet`, `PesajeViewSet`).
  - Capa de Serializadores y Validación: Clases con estereotipo `«serializer»` (ej. `UsuarioSerializer`, `PesajeSerializer`).
  - Capa de Servicios: Clases con estereotipo `«service»` (ej. `LogisticaService`, `PrediccionMLService`).
  - Capa de Persistencia: Clases con estereotipo `«entity»` o `«model»` del ORM Django conectando mediante psycopg 3 a PostgreSQL.

### 4.4 Sección 8.3: Herramientas para el Desarrollo (Ficha Técnica Real DSU)

| Subsección | Herramienta | Versión Exacta | Rol en el Sistema DSU-UAGRM |
|---|---|---|---|
| **8.3.1. Lenguajes de Programación** | Python | 3.12.7 | Lenguaje backend, procesamiento matemático, analítica de datos y algoritmos de Machine Learning. |
| | TypeScript | 5.8 | Lenguaje frontend tipado estáticamente para la interfaz SPA, garantizando robustez y control de tipos en tiempo de compilación. |
| | SQL (PL/pgSQL) | ANSI / PG 17 | Lenguaje para consultas relacionales, definición de esquemas, vistas analíticas (`bi_*`) y funciones trigger. |
| **8.3.2. Librerías** | scikit-learn | 1.5.2 | Entrenamiento, validación cruzada y serialización del algoritmo `RandomForestRegressor`. |
| | pandas & numpy | 2.2.3 / 2.1.3 | Manipulación de estructuras de datos tabulares (`DataFrame`), preprocesamiento matricial y cálculo de residuos. |
| | joblib | 1.4.2 | Persistencia y deserialización eficiente en disco del modelo entrenado (`modelo_rf.joblib`). |
| | psycopg | 3.2.3 | Adaptador de conexión de alto rendimiento entre Python/Django y PostgreSQL con soporte nativo de tipos. |
| | djangorestframework-simplejwt | 5.3.1 | Generación, firma y verificación de tokens de acceso y refresco JSON Web Tokens (JWT). |
| | openpyxl & fpdf2 | 3.1.5 / 2.8.2 | Exportación masiva de reportes oficiales de recolección en hojas de cálculo Excel y actas en formato PDF. |
| | Leaflet & React-Leaflet | 1.9.4 / 5.0.0 | Renderizado interactivo de mapas cartográficos, capas de calor (`leaflet.heat`) y marcadores de contenedores. |
| | Recharts & Lucide-React | 2.15.0 / 0.475 | Visualización de gráficos estadísticos (barras, líneas de tendencia, pastel) e iconografía institucional. |
| **8.3.3. Frameworks** | Django & Django REST Framework | 5.1.4 / 3.15.2 | Framework backend MVC/MTV robusto para la construcción de la API RESTful segura, ORM y migraciones. |
| | React & Vite | 19.0.0 / 6.2.0 | Biblioteca declarativa de interfaces de usuario y empaquetador ultrarrápido con Hot Module Replacement. |
| | Tailwind CSS | 4.0.0 | Framework CSS de utilidades para diseño responsivo adaptado a monitores de escritorio y tablets de campo. |
| **8.3.4. Sistema Gestor de Base de Datos** | PostgreSQL | 17.2 | SGBD relacional de nivel empresarial con soporte ACID, extensiones espaciales e índices avanzados B-Tree y GIN. |
| **8.3.5. Lenguaje de Modelado** | UML 2.5 (Enterprise Architect) | v16.1 | Notación estandarizada por OMG para todos los artefactos de análisis, diseño e implementación bajo el PUDS. |
| **8.3.6. Protocolos de Comunicación** | HTTPS / TLS | 1.3 (TCP 443) | Canal de comunicación web cifrado de extremo a extremo con certificados SSL para clientes y administradores. |
| | RESTful API / JSON | HTTP/1.1 - HTTP/2 | Protocolo arquitectónico sin estado para intercambio de datos estructurados entre React y Django. |
| | PostgreSQL Wire Protocol | TCP 5432 (TLS) | Protocolo nativo de comunicación entre el servidor de aplicaciones Django y el clúster de base de datos con `sslmode=require`. |

---

## 5. Especificación Técnica Detallada — Capítulo 9: Pruebas

### 5.1 Apertura del Capítulo
- **Cita APA obligatoria**:
  > Jacobson, I., Booch, G., & Rumbaugh, J. (2000). *El proceso unificado de desarrollo de software* (Cap. 11, p. 273). Pearson Educación.
  > *"Este flujo de trabajo está enfocado en verificar y validar que el sistema cumple con los requisitos establecidos, detectando defectos lo antes posible y asegurando la calidad del producto desarrollado."*

### 5.2 Sección 9.1: Planificación de Pruebas
- Definir los objetivos de verificación (construir el producto correctamente según especificaciones) y validación (construir el producto correcto que satisface a la DSU).
- Describir los tres tipos de prueba a ejecutar: Caja Negra (funcionalidad externa), Caja Blanca (lógica y caminos internos) y Pruebas de Vulnerabilidad (seguridad de endpoints y sesiones).

### 5.3 Sección 9.2: Diseño de Pruebas
- **9.2.1. Identificación y estructuración del Procedimiento de Prueba**:
  Describir formalmente la plantilla de 7 campos que se empleará en las pruebas funcionales:

```markdown
| Campo del Procedimiento | Definición Metodológica |
|---|---|
| **Nombre de caso de prueba** | Identificador único y nombre completo del Caso de Uso evaluado (ej. CP-01 Registro de Pesaje). |
| **Descripción** | Breve resumen del objetivo funcional que se verificará durante la prueba. |
| **Precondición** | Estado inicial obligatorio del software, base de datos y sesión de usuario antes de iniciar el caso. |
| **Entrada** | Conjunto exacto de datos ingresados en el formulario o recibidos por el endpoint. |
| **Condición de ejecución** | Reglas de validación, permisos requeridos o restricciones lógicas del software. |
| **Resultado obtenido** | Transcripción de la respuesta devuelta por el sistema (mensajes, código de estado, actualización de BD). |
| **Resultado esperado** | Comportamiento previsto según la especificación de requisitos y veredicto (CONFORME / EXITOSO). |
```

### 5.4 Sección 9.3: Pruebas Realizadas

#### 9.3.1. Pruebas de Caja Negra
Seleccionar los Casos de Uso críticos del sistema DSU y redactar sus tablas oficiales en formato APA:
- **CP-01**: Autenticación de Usuario y Control de Acceso basado en Roles (`CU01 / CU02`).
- **CP-02**: Registro de Pesaje y Caracterización de Residuos Recolectados (`CU08`).
- **CP-03**: Planificación y Asignación de Ruta de Recolección en Campus (`CU12`).
- **CP-04**: Generación de Inferencia Predictiva de Generación de Residuos (`CU29`).
- **CP-05**: Consulta de Tablero Analítico y Filtrado Espacial de Puntos de Acopio (`CU18 / CU23`).

#### 9.3.2. Pruebas de Caja Blanca
Aplicar la técnica de caminos básicos de McCabe para 2 funciones algorítmicas centrales del sistema:

1. **Función 1: Pipeline de Predicción de Generación de Residuos (`predict_residue_volume`)**:
   - Mostrar código Python de la función con líneas numeradas (1 a 15).
   - Diagramar el Grafo de Flujo de Control (CFG) con nodos numerados y aristas de decisión.
   - Calcular la Complejidad Ciclomática:
     $$V(G) = E - N + 2 = 14 - 11 + 2 = 5$$
   - Construir la Tabla de Caminos Independientes:
     - Camino 1: Validación de entrada fallida (parámetros nulos → excepción HTTP 400).
     - Camino 2: Modelo no cargado en memoria (carga desde `.joblib` → predicción estándar).
     - Camino 3: Predicción con datos dentro de umbral normal (resultado retornado).
     - Camino 4: Predicción superior a capacidad máxima de contenedor (retorna predicción + alerta de desborde).
     - Camino 5: Inferencia fallida por formato incompatible (captura de excepción y log de auditoría).

2. **Función 2: Cálculo de Eficiencia y Priorización de Rutas de Recolección (`calculate_route_priority`)**:
   - Código, grafo CFG, cálculo de $V(G)$ y tabla de caminos independientes garantizando cobertura de ramas al 100%.

#### 9.3.3. Pruebas de Vulnerabilidad
- **Software empleado**: **OWASP Zed Attack Proxy (ZAP)** v2.15 (herramienta DAST estándar de la industria).
- **Alcance del escaneo**: Endpoints de la API Django REST (`/api/v1/*`) y rutas de la SPA React.
- **Resultados documentados**:
  - Matriz de Alertas por Nivel de Severidad (High: 0, Medium: 0, Low: 2 mitigadas, Informational: 3 mitigadas).
  - Medidas de mitigación aplicadas en el código:
    - Cabeceras de seguridad HTTP: `Content-Security-Policy`, `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`.
    - Sanitización y validación estricta de entradas en serializadores DRF contra Inyección SQL y XSS.
    - Manejo de sesiones JWT con vencimiento programado (Access Token 15 min, Refresh Token 24 h) y almacenamiento en cookies con flags `HttpOnly; Secure; SameSite=Strict`.

---

## 6. Especificación Técnica Detallada — Capítulo 10: Costos, Riesgos y Seguridad

### 6.1 Sección 10.1: Estimación de Costos
Presentar primeramente la **Tabla General de Costos del Proyecto** en Bolivianos (Bs.):

```markdown
Tabla General. Presupuesto Consolidado de Inversión del Proyecto
| Categoría de Costo | Subtotal en Bolivianos (Bs.) | Participación (%) |
|---|---|---|
| 10.1.1. Hardware | 18.500,00 | 18,2 % |
| 10.1.2. Software y Servicios en la Nube | 6.800,00 | 6,7 % |
| 10.1.3. Personal y Mano de Obra (según aranceles SIB) | 68.000,00 | 67,0 % |
| 10.1.4. Infraestructura y Espacio Operativo | 5.200,00 | 5,1 % |
| 10.1.5. Logística, Material y Refrigerios | 3.000,00 | 3,0 % |
| **TOTAL INVERSIÓN DEL PROYECTO** | **101.500,00 Bs.** | **100,0 %** |
Nota. Montos calculados para 4 meses de desarrollo y puesta en marcha bajo aranceles de la SIB Santa Cruz.
```

#### Desglose en Tablas Específicas:
- **10.1.1 Hardware**: Laptops de desarrollo de alto rendimiento (2 unidades, 14.000 Bs.), Dispositivo móvil Android para validación de interfaz de pesaje en campo (1.800 Bs.), Servidor local de pruebas / UPS (2.700 Bs.).
- **10.1.2 Software**: Entorno de desarrollo VS Code (0 Bs.), SGBD PostgreSQL (0 Bs.), Django/React (0 Bs.), Alojamiento cloud gestionado Neon/VPS por 12 meses (3.600 Bs.), Certificados SSL/Dominio (800 Bs.), Licencia Enterprise Architect (2.400 Bs.).
- **10.1.3 Personal**: Calculado sobre 4 meses de dedicación a jornada completa según escala de la SIB:
  - 1 Líder de Proyecto / Arquitecto de Software: 5.500 Bs./mes × 4 = 22.000 Bs.
  - 1 Desarrollador Backend Django / Base de Datos: 4.000 Bs./mes × 4 = 16.000 Bs.
  - 1 Desarrollador Frontend React / Cartografía: 4.000 Bs./mes × 4 = 16.000 Bs.
  - 1 Ingeniero de Datos / Machine Learning: 3.500 Bs./mes × 4 = 14.000 Bs.
  - *Subtotal Personal*: 68.000 Bs.
- **10.1.4 Infraestructura**: Internet simétrico empresarial por 4 meses (2.000 Bs.), Energía eléctrica y climatización (2.400 Bs.), Mobiliario ergonómico amortizado (800 Bs.).
- **10.1.5 Logística**: Relevamiento de campo en predios universitarios y transporte (1.200 Bs.), Material de escritorio y papelería (600 Bs.), Refrigerios de equipo en jornadas de prueba (1.200 Bs.).

---

### 6.2 Sección 10.2: Retorno de la Inversión (ROI)

#### Modelo Económico Adaptado a la DSU-UAGRM
El docente enfatizó en clase (minutos 36:00 a 40:15) que los proyectos institucionales universitarios poseen retorno económico tangible a través de ahorros operativos, optimización presupuestaria y generación de ingresos propios:

1. **10.2.1. Incremento de Ingresos por Uso del Sistema (Venta de Materiales Reciclables)**:
   - La DSU comercializa materiales reciclables recuperados (plástico PET, papel blanco, cartón prensado y latas de aluminio).
   - Con el sistema digital de pesaje y control de acopio, se eliminan pérdidas, mermas por acopio deteriorado y desvíos no autorizados.
   - *Incremento mensual estimado*: 4.500,00 Bs./mes.
   - Proyección anual (12 meses):
     $$\text{Beneficio por Venta de Reciclables} = 4.500,00 \times 12 = \mathbf{54.000,00\ \text{Bs.}}$$

2. **10.2.2. Incremento de Beneficios por Análisis de Datos y Predicción (Machine Learning)**:
   - El modelo `RandomForestRegressor` predice los picos de acumulación por facultad con antelación, permitiendo recolectar los materiales limpios antes de que se mezclen con residuos orgánicos o se degraden por lluvia e intemperie.
   - El material reciclable limpio y clasificado se vende con un sobreprecio del 35% en el mercado de reciclaje de Santa Cruz.
   - *Beneficio mensual estimado*: 2.800,00 Bs./mes.
   - Proyección anual (12 meses):
     $$\text{Beneficio por Predicción ML} = 2.800,00 \times 12 = \mathbf{33.600,00\ \text{Bs.}}$$

3. **10.2.3. Reducción de Costos Operativos y Logísticos**:
   - Optimización de rutas de recolección interna en el Campus Universitario (reducción de consumo de combustible y mantenimiento de maquinaria).
   - Disminución de pago de horas extras de personal de limpieza por desbordes imprevistos.
   - Disminución de la tasa de disposición final pagada por tonelada al operador municipal (EMACRUZ) al desviar mayor porcentaje de residuos hacia el reciclaje.
   - *Ahorro mensual estimado*: 3.200,00 Bs./mes.
   - Proyección anual (12 meses):
     $$\text{Ahorro por Reducción de Costos} = 3.200,00 \times 12 = \mathbf{38.400,00\ \text{Bs.}}$$

#### 10.2.4. Consolidación Matemática del ROI
- **Beneficio Total Anual**:
  $$\text{Beneficio Total} = 54.000,00 + 33.600,00 + 38.400,00 = \mathbf{126.000,00\ \text{Bs.}}$$
- **Beneficio Neto Anual**:
  $$\text{Beneficio Neto} = \text{Beneficio Total} - \text{Costo de Inversión}$$
  $$\text{Beneficio Neto} = 126.000,00 - 101.500,00 = \mathbf{24.500,00\ \text{Bs.}}$$
- **Cálculo Porcentual del Retorno de la Inversión (ROI)**:
  $$ROI = \left(\frac{\text{Beneficio Neto}}{\text{Costo de Inversión}}\right) \times 100\%$$
  $$ROI = \left(\frac{24.500,00}{101.500,00}\right) \times 100\% = \mathbf{24,14\%}$$

> **Interpretación Textual Oficial**:  
> *"Esto significa que, en un periodo de 12 meses la Dirección de Servicios Universitarios (DSU-UAGRM) tendrá un retorno de inversión del 24,14% sobre el costo del desarrollo e implementación del software."*

---

### 6.3 Sección 10.3: Riesgos y Plan de Respuesta

Presentar en una sola tabla matriz estructurada según lo exigido por el docente (Lámina p. 5 y grabación 40:15–43:05):

```markdown
Tabla XX. Matriz de Riesgos del Proyecto y Plan de Contingencia
| Clasificación | Descripción del Riesgo | Probabilidad (%) | Impacto | Plan de Respuesta y Contingencia |
|---|---|---|---|---|
| **Riesgo Técnico** | Inestabilidad en la conectividad Wi-Fi/4G en puntos periféricos del campus universitario durante el pesaje. | 40 % | Medio | Implementación de almacenamiento local offline temporal en la SPA React (`IndexedDB`) con sincronización automática al reanudar conexión. |
| **Riesgo Técnico** | Drift conceptual o degradación de la precisión del modelo predictivo por cambios en el calendario académico. | 25 % | Medio | Pipeline automatizado de reentrenamiento periódico con reajuste de hiperparámetros y validación cruzada antes de publicar nuevo modelo. |
| **Riesgo Técnico** | Falla o indisponibilidad en el clúster de base de datos en la nube. | 15 % | Alto | Copias de respaldo automáticas diarias en almacenamiento frío (S3/GCS) y script de recuperación automatizado `pg_restore`. |
| **Riesgo de Gestión** | Retrasos en los tiempos de entrega por subestimación en la complejidad del modelado y la integración cartográfica. | 30 % | Alto | Monitoreo iterativo bajo el Proceso Unificado de Desarrollo, sprints cortos de 1 semana y priorización de CU indispensables. |
| **Riesgo de Gestión** | Resistencia de los operadores de recolección al uso del registro digital de pesaje en tablet o móvil. | 35 % | Medio | Programa de capacitación presencial práctica y diseño de interfaces simplificadas de alta usabilidad con teclado numérico ampliado. |
| **Riesgo Institucional** | Cambios administrativos o de autoridades en la DSU que modifiquen las políticas de recolección de residuos. | 20 % | Alto | Documentación de requisitos formalizada con actas de aprobación firmadas y parametrización flexible en base de datos. |
| **Riesgo Institucional** | Limitación de acceso físico a puntos de acopio en temporadas de receso universitario o conflictos gremiales. | 25 % | Medio | Habilitación de gestión remota de estados de contenedores y notificación de clausura preventiva de puntos en el mapa. |
```

---

### 6.4 Sección 10.4: Seguridad del Sistema

#### 10.4.1. Seguridad Lógica
- **Fundamento Teórico con Cita APA**: Definición formal de seguridad lógica (ej. Stallings, 2018; o Tanenbaum & Wetherall, 2012).
- **Descripción de Mecanismos Implementados**:
  - Seguridad en Capa de Red y Transporte: Cifrado HTTPS / TLS 1.3 con certificados X.509 de 2048 bits.
  - Seguridad en Capa de Aplicación: Tokens JSON Web Tokens (JWT) con firma HMAC-SHA256, expiración estricta y renovación mediante Refresh Token.
  - Cifrado Criptográfico de Contraseñas: Algoritmo PBKDF2 con hash SHA-256 y salting individual de 100.000 iteraciones en Django.
  - Control de Acceso Basado en Roles (RBAC): Matriz de permisos estricta a nivel de endpoint mediante `IsAuthenticated` y clases de permisos personalizadas.
- **Tabla Matriz de Riesgos Lógicos y Solución**:

```markdown
Tabla XX. Riesgos de Seguridad Lógica y Soluciones Aplicadas
| Riesgo de Seguridad Lógica | Vulnerabilidad Asociada | Solución Técnica Implementada en el Sistema |
|---|---|---|
| Inyección de código SQL | Manipulación maliciosa de parámetros en consultas. | Uso estricto del ORM de Django con consultas parametrizadas; validación tipada con serializadores. |
| Cross-Site Scripting (XSS) | Inyección de scripts JavaScript en campos de texto. | Sanitización automática de React en el renderizado del DOM y cabecera `Content-Security-Policy`. |
| Secuestro de Sesión / Interceptación | Captura de credenciales en tránsito por terceros. | Canal HTTPS obligatorio con flag HSTS (`Strict-Transport-Security`) y tokens transmitidos en cabecera `Authorization: Bearer`. |
| Escalación no autorizada de privilegios | Usuario recolector intentando invocar endpoints de administración. | Middleware de verificación de roles y validación de permisos en la capa de vistas (`PermissionClasses`). |
| Ataques de Fuerza Bruta en Login | Intentos masivos automatizados de adivinación de contraseñas. | Throttling / Rate Limiting configurado en Django REST Framework (máximo 5 intentos por minuto por IP). |
```

#### 10.4.2. Seguridad Física
- **Fundamento Teórico con Cita APA**: Definición formal de seguridad física en centros de procesamiento y equipos terminales.
- **Descripción de Infraestructura**:
  - Servidores y Equipos Centrales: Alojamiento en racks cerrados con control de acceso mediante llave y registro de visitas.
  - Climatización y Entorno: Salas climatizadas con aire acondicionado de precisión para evitar sobrecalentamiento de servidores.
  - Suministro Eléctrico Continuo: Sistema de alimentación ininterrumpida (UPS) de doble conversión y generador de respaldo para proteger contra cortes de energía.
  - Cableado Estructurado: Tendido bajo norma internacional TIA/EIA-568 en canaletas ignífugas y etiquetado normativo.
- **Tabla Matriz de Riesgos Físicos y Solución**:

```markdown
Tabla XX. Riesgos de Seguridad Física y Soluciones Aplicadas
| Riesgo de Seguridad Física | Amenaza Identificada | Solución y Medida de Seguridad Física |
|---|---|---|
| Sobrecalentamiento de equipamiento | Fallo térmico de hardware por altas temperaturas de Santa Cruz. | Sala técnica climatizada mantenida a temperatura constante (18 °C a 21 °C) con monitoreo térmico. |
| Pérdida o robo de dispositivos móviles de campo | Sustracción de tablets/móviles usados por operadores de recolección. | Bloqueo biométrico/PIN en el dispositivo móvil y mecanismo de revocación remota de tokens en el servidor. |
| Interrupción abrupta de energía eléctrica | Microcortes o apagones que puedan corromper datos en disco. | UPS con autonomía de 30 minutos y configuración de apagado seguro automatizado del servidor. |
| Acceso no autorizado al data center / servidor | Manipulación física indebida de cables de red o terminales. | Puertas con cerradura de seguridad biométrica/tarjeta magnética y bitácora física de ingreso a la sala técnica. |
| Deterioro o vandalismo de contenedores de acopio | Daño a sensores o puntos de pesaje en los campus. | Protección perimetral de puntos limpios, anclaje al suelo y supervisión por el personal de maestranza. |
```

---

## 7. Checklist de Verificación Quirúrgica para la Entrega y Defensa Final

### Auditoría del Documento DOCX / PDF (30 Puntos)
- [ ] Subcarátulas de capítulos 8, 9 y 10 presentes y en formato estándar.
- [ ] Párrafos de apertura de los capítulos 8 y 9 con citas textuales APA obligatorias de Jacobson, Booch y Rumbaugh (2000, Cap. 10 y 11).
- [ ] Capítulo 8 sin líneas de código fuente pegadas en el texto.
- [ ] 8.1 con diagrama general de componentes que incluye los 8 paquetes, software `«source»` y componentes `«OLTP»` y `«OLAP»`.
- [ ] 8.2 con exactamente 8 subíndices (8.2.1 a 8.2.8) y 8 figuras de componentes con marco `cmp` y conectores `«JSON/HTTPS»`.
- [ ] 8.3 con los 6 subpuntos obligatorios (8.3.1 a 8.3.6) y versiones reales exactas.
- [ ] 9.2.1 con la estructura oficial de 7 campos para Caja Negra.
- [ ] 9.3.1 con casos de prueba de caja negra para los CU críticos de DSU en tablas APA.
- [ ] 9.3.2 con análisis de caja blanca completo: código numerado, grafo CFG, cálculo de complejidad de McCabe $V(G)$ y tabla de caminos independientes.
- [ ] 9.3.3 con descripción de herramienta (OWASP ZAP) y reporte de vulnerabilidades mitigadas.
- [ ] 10.1 con Tabla General de Costos en Bolivianos (Bs.) y desgloses 10.1.1 a 10.1.5.
- [ ] Honorarios de personal calculados según aranceles de la SIB.
- [ ] 10.2 con beneficios proyectados a 12 meses (1.2.1, 1.2.2 y 1.2.3), Beneficio Neto, cálculo del ROI y la conclusión textual obligatoria.
- [ ] 10.3 con matriz de riesgos técnicos, de gestión e institucionales y plan de contingencia.
- [ ] 10.4 con citas teóricas y matrices de riesgos lógicos y físicos con soluciones.
- [ ] Continuidad estricta de numeración de figuras y tablas (`SEQ`).
- [ ] Todas las figuras y tablas con rótulo superior y `Nota. Elaboración Propia` inferior.

### Auditoría del Software y Defensa en Vivo (30 Puntos)
- [ ] Backend Django REST Framework y Frontend React desplegados y comunicándose fluidamente sobre HTTPS/TLS o localhost de demostración.
- [ ] Base de datos PostgreSQL con datos representativos de los campus de la UAGRM, facultades, puntos de acopio y pesajes históricos.
- [ ] Autenticación JWT operativa y cambio de vistas según el rol del usuario (Administrador DSU, Operador Recolector, Supervisor).
- [ ] Mapa Leaflet interactivo cargando contenedores, polígonos de campus y rutas de recolección en tiempo real.
- [ ] Pipeline de Machine Learning operativo: inferencia en vivo con el modelo `RandomForestRegressor` (`.joblib`) ante entradas del formulario.
- [ ] Trazabilidad demostrable en código: cada clase, modelo ORM y conector en el código coincide con los diagramas del documento.
