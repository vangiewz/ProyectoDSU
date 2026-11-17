# Capítulo 8 — Implementación (clase del 06/11/2026)

Contexto oficial y técnico consolidado para la **Fase Final** (Fase 3) del proyecto DSU-UAGRM, validado contra la grabación de la clase del 06/11/2026 y las láminas oficiales del docente (`cap8-10/Fase 3 _ Cap 8 Implementacón.pdf`).

## Fuente y alcance

- **Video**: `C:\Users\rekte\Videos\Captures\2026-11-06 20-44-29.mp4` (19 min 43 s; viernes 06/11/2026, clase por Google Meet, inicio ~20:44).
  - La grabación previa `2026-11-06 20-35-11.mp4` (9 min) correspondió a la sala de espera sin audio útil y se descartó.
- **Transcripción**: [Transcripción completa](2026-11-06_cap8_implementacion.txt) y [segmentos temporales](2026-11-06_cap8_implementacion.json) generados con `faster-whisper large-v3-turbo` en español.
- **Láminas Oficiales**: [Fase 3 _ Cap 8 Implementacón.pdf](../cap8-10/Fase%203%20_%20Cap%208%20Implementac%C3%B3n.pdf) (**11 páginas**), subidas por el docente MSc. Ing. José Junior Villagómez Melgar al Classroom.
- **Evidencias Visuales de la Grabación**: [clases/evidencias-2026-11-06/](evidencias-2026-11-06/) y recursos vectoriales extraídos de las láminas en [clases/recursos_diapositivas/](recursos_diapositivas/):

| Fotograma | Lámina Oficial | Contenido |
|---|---|---|
| [11-30](evidencias-2026-11-06/11-30.jpg) | p. 2, cronograma de fases | Fase final: Cap. 8 en adelante, Documento completo + Software desarrollado, en digital y físico, defensa final. |
| [12-15](evidencias-2026-11-06/12-15.jpg) | p. 3, cita de Jacobson | Cita textual obligatoria de Jacobson, Booch & Rumbaugh (2000, Cap. 10). |
| [12-45](evidencias-2026-11-06/12-45.jpg) | p. 4, Modelo de Implementación | Definición teórica del Modelo de Implementación: subsistemas, componentes y vista de arquitectura. |
| [13-30](evidencias-2026-11-06/13-30.jpg) | p. 5–6, índice del capítulo | Los tres puntos estructurales obligatorios: 1. Arquitectura del Sistema, 2. Arquitectura del Subsistema, 3. Herramientas. |
| [13-45](evidencias-2026-11-06/13-45.jpg), [14-15](evidencias-2026-11-06/14-15.jpg) | p. 7, punto 1 | Diagrama general de componentes: paquetes, componente software `«source»` y componentes de base de datos (`«OLTP»` y `«OLAP»`). |
| [14-45](evidencias-2026-11-06/14-45.jpg) | p. 8, punto 2 | Regla: Un diagrama de componentes por cada subsistema/paquete, cada uno con su subtítulo propio. |
| [15-15](evidencias-2026-11-06/15-15.jpg) a [16-00](evidencias-2026-11-06/16-00.jpg) | p. 9, ejemplo 8.2.1 | Ejemplo de la lámina: Subsistema Usuarios (Figura 55): capas Cliente (`«Form»`), conector `«JSON/HTTPS»`, Servidor (`Controller`, `Service`, `Repository`). |
| [16-30](evidencias-2026-11-06/16-30.jpg) | p. 10, punto 3 | Desglose de herramientas: 3.1 Lenguajes, 3.2 Librerías, 3.3 Frameworks, 3.4 SGBD, 3.5 Lenguaje de Modelado, 3.6 Protocolos. |

---

## Criterios e Instrucciones del Docente con Marcas Temporales

| ID | Tiempo | Lo que dijo / mostró el docente | Aplicación técnica al proyecto DSU-UAGRM |
|---|---|---|---|
| C8-01 | 06:10–08:47 | Transición de fases: requisitos (acuerdo), análisis (mirada conceptual interna), diseño (planos: clases, BD, despliegue, secuencias). Ahora con los planos listos, se construye la implementación. | El Cap. 8 materializa exactamente el Cap. 7. No se inventa arquitectura nueva; se implementa la arquitectura y los subsistemas modelados en 6.1 y 7.1. |
| C8-02 | 07:17–07:38 | Reitera enfáticamente que el diagrama de clases y el de base de datos no son lo mismo. | El diagrama de componentes del Cap. 8 debe conectarse con componentes lógicos de base de datos (`«OLTP»` y `«OLAP»`) diferenciados del código backend. |
| C8-03 | 07:42–08:21 | Despliegue vs. Implementación: cómo se distribuyen los componentes en nodos y cómo se comunican. | Total coherencia entre los protocolos del despliegue (7.1.1) y los conectores de los diagramas de componentes de implementación (8.2 y 8.3.6). |
| C8-04 | 09:10–10:47 | Rigor en ingeniería de software: el docente destaca que es muy estricto con el modelado y la coincidencia de clases y componentes con la realidad. | Los diagramas de componentes deben reflejar fielmente la estructura real del código de DSU (Django REST Framework + React TypeScript), no esquemas teóricos genéricos. |
| C8-05 | 10:50–11:26 | Analogía arquitecto–albañil: aunque el software se construye en la computadora, **la implementación también se plasma obligatoriamente en el documento**. | El Capítulo 8 documenta formalmente la arquitectura y subsistemas de implementación. |
| C8-06 | 11:34–12:13 + p. 2 | **Estructura de la Fase Final**: anuncia que tras el Cap. 8 viene un capítulo de pruebas (Cap. 9) y un capítulo de costos/presupuestos (Cap. 10). Exige **revisión final del documento completo (Cap. 1 al 10) y del software desarrollado, en digital y físico con defensa**. | Planificar el documento completo integrado y tener el sistema DSU 100% operativo en producción/despliegue local para la defensa en vivo. |
| C8-07 | 12:13–12:28 + p. 3 | Cita obligatoria de apertura: *"La mayor parte de la arquitectura del sistema es capturada durante el Diseño, siendo el propósito principal de la Implementación el desarrollar la arquitectura y el sistema como un todo"* (Jacobson, Booch & Rumbaugh, 2000, Cap. 10). | Utilizar esta cita formal en formato APA 7 en el primer párrafo introductorio del Capítulo 8. |
| C8-08 | 12:38–13:14 + p. 4 | Elementos del Modelo de Implementación según el PUDS: (1) Subsistemas de implementación, dependencias, interfaces; (2) Componentes (ficheros, ejecutables); (3) Vista de arquitectura de implementación. | Estructurar el capítulo exactamente bajo estos conceptos del PUDS. |
| C8-09 | 13:14–13:42 + p. 5–6 | Tres puntos obligatorios del Capítulo 8: 1. Implementación de la Arquitectura del Sistema, 2. Implementación de la Arquitectura del Subsistema, 3. Herramientas para el Desarrollo. | Seguir la numeración canónica 8.1, 8.2 y 8.3. |
| C8-10 | 13:42–14:28 + p. 7 | **Punto 8.1 Arquitectura del Sistema**: Vista macro. Muestra paquetes del sistema con sus dependencias, un componente principal `«source»` del software, y abajo componentes de datos `«OLTP»` y `«OLAP»`. | En DSU: mostrar los 8 paquetes de 6.1/6.3, el componente `«source» Sistema de Gestión de Residuos DSU`, y las dos vistas lógicas de BD: `«OLTP» Base de Datos Transaccional (PostgreSQL)` y `«OLAP» Estructura Analítica (HechoResiduo / Vistas BI)`. |
| C8-11 | 14:28–15:09 + p. 8 | **Punto 8.2 Arquitectura del Subsistema**: "Se realiza el diagrama de componentes de cada subsistema", "cada diagrama con su respectivo subtítulo". "Cada paquete viene a ser un subsistema". | Crear exactamente 8 subtítulos (8.2.1 a 8.2.8) y 8 figuras de diagramas de componentes en Enterprise Architect (marco `cmp`), correspondientes a los 8 paquetes de DSU. |
| C8-12 | 15:09–16:10 + p. 9 | Ejemplo en lámina: Figura 55 (Subsistema Usuarios): muestra componente Cliente (formularios), conector rotulado **`«JSON/HTTPS»`**, componente Servidor con controladores, servicios y repositorios. Recalca: *"lo importante es la ingeniería; tiene que estar bien modelado"*. | Adaptar la estructura a Django/React real: Frontend (páginas/componentes React), conector `«JSON/HTTPS»` con JWT, Backend Django (vistas DRF, serializadores, servicios, modelos ORM) conectando a PostgreSQL. |
| C8-13 | 16:10–17:25 + p. 10 | **Punto 8.3 Herramientas de Desarrollo**: Explicar en subpuntos: 3.1 Lenguajes, 3.2 Librerías, 3.3 Frameworks, 3.4 SGBD, 3.5 Lenguaje de Modelado, 3.6 Protocolos de Comunicación. | Secciones 8.3.1 a 8.3.6 con versiones exactas del repositorio de código y coherencia total con el protocolo `«JSON/HTTPS»` de 8.2 y el despliegue de 7.1.1. |
| C8-14 | 17:25–17:34 | *"Lo demás ya es lenguaje de máquina… código de programación, que no lo vamos a contemplar en el documento, al menos por ahora"*. | **Regla estricta**: NO pegar código fuente en el Capítulo 8. El código se evalúa en el software y en el Capítulo 9 (caja blanca). |

---

## Estructura Oficial Confirmada del Capítulo 8

```
Capítulo 8
8. Implementación
   (Párrafo introductorio con cita APA: Jacobson, Booch & Rumbaugh, 2000, Cap. 10)
8.1. Implementación de la Arquitectura del Sistema
     Figura: Diagrama de Componentes de la Arquitectura del Sistema (8 paquetes + software + BD OLTP/OLAP)
8.2. Implementación de la Arquitectura del Subsistema
     8.2.1. Implementación de la Arquitectura del Subsistema Gestión de Usuarios y Control de Acceso
            Figura: Diagrama de Componentes del Subsistema Usuarios y Control de Acceso
     8.2.2. Implementación de la Arquitectura del Subsistema Gestión Topológica y Puntos de Recolección
            Figura: Diagrama de Componentes del Subsistema Topología y Puntos
     8.2.3. Implementación de la Arquitectura del Subsistema Gestión de Residuos
            Figura: Diagrama de Componentes del Subsistema Gestión de Residuos
     8.2.4. Implementación de la Arquitectura del Subsistema Gestión de Recolecciones y Logística
            Figura: Diagrama de Componentes del Subsistema Recolecciones y Logística
     8.2.5. Implementación de la Arquitectura del Subsistema Inteligencia de Negocios y Analítica Visual
            Figura: Diagrama de Componentes del Subsistema Inteligencia de Negocios
     8.2.6. Implementación de la Arquitectura del Subsistema Componente Cartográfico y Análisis Espacial
            Figura: Diagrama de Componentes del Subsistema Cartográfico y Espacial
     8.2.7. Implementación de la Arquitectura del Subsistema Predicción mediante Random Forest Regressor
            Figura: Diagrama de Componentes del Subsistema Predicción Random Forest
     8.2.8. Implementación de la Arquitectura del Subsistema Administración de la Plataforma y Auditoría
            Figura: Diagrama de Componentes del Subsistema Administración y Auditoría
8.3. Herramientas para el Desarrollo
     8.3.1. Lenguajes de Programación
     8.3.2. Librerías
     8.3.3. Frameworks
     8.3.4. Sistema Gestor de Base de Datos
     8.3.5. Lenguaje de Modelado de Software
     8.3.6. Protocolos de Comunicación
```

---

## Aplicación Quirúrgica al Proyecto DSU-UAGRM

1. **8.1 Arquitectura del Sistema**:
   - Marco: `cmp Diagrama de Componentes de la Arquitectura del Sistema`.
   - Elementos:
     - 8 paquetes idénticos a 6.1 y 6.3: Usuarios, Topología, Residuos, Logística, BI, Cartografía, Predicción, Auditoría.
     - Componente central: `«source» Sistema Web DSU-UAGRM`.
     - Dependencias hacia componentes de datos: `«OLTP» Base de Datos Transaccional PostgreSQL` y `«OLAP» Estructura Analítica BI (Hechos y Vistas)`.
     - Artefacto de modelo predictivo: `«file» modelo_random_forest.joblib` como componente fichero (Jacobson p. 4).
2. **8.2 Arquitectura de los 8 Subsistemas**:
   - **Frontend (Cliente)**: componentes React TypeScript (`frontend/src/pages/`, `frontend/src/components/`, `api.ts`).
   - **Conector**: rotulado **`«JSON/HTTPS»`** con JWT Bearer Token.
   - **Backend (Servidor)**:
     - Capa de Controladores: Vistas y ViewSets de Django REST Framework (`apps/*/views.py`).
     - Capa de Serializadores y Validación: (`apps/*/serializers.py`).
     - Capa de Servicios de Negocio: Algoritmos de optimización logística, pipeline de entrenamiento y predicción (`apps/*/services.py`).
     - Capa de Persistencia/Datos: Modelos del ORM de Django (`apps/*/models.py`) conectados mediante psycopg 3 a PostgreSQL.
3. **8.3 Herramientas de Desarrollo con Versiones Reales**:
   - **8.3.1 Lenguajes**: Python 3.12, TypeScript 5.8, SQL (PostgreSQL 17).
   - **8.3.2 Librerías**:
     - Backend: `scikit-learn 1.5`, `pandas 2.2`, `numpy 2.1`, `joblib 1.4`, `psycopg 3.2`, `djangorestframework-simplejwt 5.3`, `django-filter 24.3`, `openpyxl 3.1`, `fpdf2 2.8`.
     - Frontend: `leaflet 1.9`, `react-leaflet 5.0`, `leaflet.heat 0.2`, `lucide-react`, `recharts 2.15`, `axios 1.7`.
   - **8.3.3 Frameworks**: Django 5.1+, Django REST Framework 3.15+, React 19, Vite 6, Tailwind CSS 4.
   - **8.3.4 SGBD**: PostgreSQL 17 (alojamiento gestionado en la nube con soporte SSL/TLS).
   - **8.3.5 Lenguaje de Modelado**: UML 2.5 mediante Enterprise Architect v16, bajo el marco del Proceso Unificado de Desarrollo de Software (PUDS).
   - **8.3.6 Protocolos de Comunicación**:
     - HTTPS/TLS 1.3 (puerto 443) para tráfico web seguro.
     - RESTful API sobre HTTP/HTTPS con serialización JSON y autenticación JWT.
     - Protocolo PostgreSQL Wire (puerto 5432) con cifrado SSL obligatorio (`sslmode=require`).
     - Protocolo WMS/TMS sobre HTTPS para consumo de teselas OpenStreetMap.

---

## Resolución de Dudas Previas

- **¿Paquetes transversales llevan subsistema?** Sí. La regla del docente es categórica: cada paquete del capítulo 6 es un subsistema de implementación y lleva su figura individual (8.2.1 a 8.2.8).
- **¿Inclusión de CU dentro de los paquetes en 8.1?** La diapositiva indica "Los paquetes podrían incluir los CU que lo conforman", pero el docente aclaró que es opcional para evitar saturar el diagrama macro. Se mantendrán los paquetes limpios con dependencias y relaciones a datos.
- **¿Inclusión de código fuente en Cap. 8?** Prohibido por ahora en Cap. 8. El código se documenta en las pruebas de Caja Blanca del Cap. 9 y se demuestra en vivo en la defensa del software.
