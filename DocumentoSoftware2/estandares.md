## I. Estándares de codificación

Los estándares siguientes se aplican a todo el código del sistema. Su cumplimiento se comprueba con herramientas automáticas antes de integrar cada cambio y en la revisión entre integrantes definida en el SQAP.

### I.1. Estándares generales

| Aspecto | Estándar |
| --- | --- |
| Idioma | Nombres del dominio, mensajes al usuario y documentación en español; palabras reservadas y nombres de bibliotecas en su forma original |
| Codificación de archivos | UTF-8 con fin de línea LF |
| Configuración | Credenciales y parámetros de entorno en variables de entorno; nunca en el código fuente |
| Control de versiones | Git; cada confirmación describe un cambio completo y se revisa antes de integrarse a la rama principal |
| Estructura del repositorio | Carpetas independientes `backend/` y `frontend/` dentro de un único repositorio |
| Comentarios | Explican el motivo de una decisión o una regla de negocio; no repiten lo que el código ya expresa |

### I.2. Estándares del backend (Python y Django)

| Aspecto | Estándar |
| --- | --- |
| Guía de estilo | PEP 8, verificada con Ruff |
| Longitud de línea | Máximo 120 caracteres |
| Reglas de análisis estático | Errores de estilo (E), errores lógicos de Pyflakes (F), orden de importaciones (I), defectos probables de flake8-bugbear (B) y buenas prácticas de Django (DJ) |
| Nombres | `snake_case` para funciones, variables y módulos; `PascalCase` para clases; `MAYÚSCULAS` para constantes |
| Organización por aplicación | Un paquete por responsabilidad (`models/`, `serializers/`, `views/`, `services/`, `filters/`, `permissions/`, `tests/`) y un archivo por entidad |
| Patrón arquitectónico | MVC: modelo en `models/`, controlador en `views/` (ViewSets) y vista en `serializers/` junto con la interfaz React |
| Lógica de negocio | En `services/` cuando el proceso tiene varios pasos; las vistas solo coordinan |
| Validaciones | En servicios o serializadores, con las excepciones de Django REST Framework y mensajes claros en español |
| Persistencia | Cantidades en `DecimalField`; claves foráneas con `on_delete=PROTECT`; bajas lógicas con `is_active`, sin borrado físico |
| Auditoría | Toda escritura se registra en la bitácora mediante `AuditedViewSet` o el servicio de bitácora |
| Seguridad | Permiso por rol en cada vista y filtro por sector en cada consulta |
| Parámetros de negocio | En la tabla de parámetros del sistema, no como constantes del código |
| Pruebas | pytest y pytest-django; archivos `test_*.py` dentro de `tests/` de cada aplicación |

### I.3. Estándares del frontend (TypeScript y React)

| Aspecto | Estándar |
| --- | --- |
| Lenguaje | TypeScript; la compilación (`tsc -b`) debe terminar sin errores antes de generar la versión de producción |
| Comprobaciones del compilador | Variables y parámetros sin uso prohibidos (`noUnusedLocals`, `noUnusedParameters`) y casos de `switch` sin salida prohibidos (`noFallthroughCasesInSwitch`) |
| Análisis estático | oxlint con los complementos de React y TypeScript; las reglas de hooks son error |
| Componentes | Componentes de función con hooks; un componente por archivo, en `PascalCase` |
| Nombres | `camelCase` para variables y funciones; `PascalCase` para componentes y tipos |
| Organización | `pages/` para pantallas, `components/` para componentes reutilizables y `lib/` para acceso a la API, autenticación y tipos |
| Tipos de datos | Las respuestas de la API se tipan en `lib/tipos.ts` y se actualizan cuando cambia el contrato |
| Acceso a la API | Centralizado en `lib/api.ts`; ninguna pantalla construye peticiones por su cuenta |
| Estilos | Tailwind CSS con los colores y tamaños definidos como variables del tema en `index.css`; no se usan valores sueltos en los componentes |
| Autorización en la interfaz | Las rutas y acciones se muestran según los permisos que informa el backend, que vuelve a validarlos siempre |
| Diseño adaptable | Cada pantalla se verifica en escritorio (1440 px) y en teléfono (390 px) |

### I.4. Estándares de la base de datos

| Aspecto | Estándar |
| --- | --- |
| Motor | PostgreSQL |
| Nombres | Tablas con el formato `aplicación_entidad` en minúsculas; columnas en `snake_case`; claves foráneas con sufijo `_id` |
| Cambios de esquema | Solo mediante migraciones de Django versionadas en el repositorio |
| Normalización | Tercera forma normal en el plano transaccional; la tabla de hechos analítica se desnormaliza de forma controlada |
| Integridad | Claves foráneas protegidas, restricciones de unicidad y bitácora inalterable mediante disparador |
| Vistas analíticas | Prefijo `bi_` para las vistas que consume Power BI |

### I.5. Estándares de la API

| Aspecto | Estándar |
| --- | --- |
| Estilo | REST sobre HTTPS con JSON; todas las rutas bajo `/api/` |
| Autenticación | JWT con token de acceso y token de refresco |
| Paginación | Respuesta con `count`, `next`, `previous` y `results` |
| Errores | Códigos HTTP estándar y mensaje en español en `detail` o por campo |
| Fechas y cantidades | Fechas en formato ISO 8601; cantidades decimales como texto para conservar la precisión |
