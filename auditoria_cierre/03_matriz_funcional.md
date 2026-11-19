# Matriz funcional y de trazabilidad del cierre

Fuente de requisitos: docs/Documento_Taller_de_Grado_I_Grupo_8.docx, capítulo 4, extraído del XML vigente. Fuente de CU: generador/fase2/datos.py. Evidencia: regresion_final.xml y demo_ui/resultados.json. Todas las apps comparten PostgreSQL en Neon en el piloto; las pruebas nuevas usan PostgreSQL local sintético. No se atribuye autoría individual.

Los archivos de pruebas relacionados son evidencia de dominio: NO implican cobertura de cada cláusula de un RF. Cada resultado JUnit conserva su testcase exacto y la matriz JSON permite consultarlo.

|RF|Nombre oficial|CU|API|Pantallas|Estado|
|---|---|---|---|---|---|
|RF1|Gestionar Usuarios|CU3|/api/{usuarios,roles,permisos,auth}/|Admin.tsx; Login.tsx|Implementado; cobertura relacionada aprobada, no aceptación integral del RF|
|RF2|Gestionar Roles y Permisos|CU4|/api/{usuarios,roles,permisos,auth}/|Admin.tsx; Login.tsx|Implementado; cobertura relacionada aprobada, no aceptación integral del RF|
|RF3|Autenticar y Controlar el Acceso|CU1, CU2|/api/{usuarios,roles,permisos,auth}/|Admin.tsx; Login.tsx|Implementado; cobertura relacionada aprobada, no aceptación integral del RF|
|RF4|Gestionar Sectores y Facultades|CU5|/api/{sectores,puntos,contenedores}/|Maestros.tsx; MapaCampus.tsx|Implementado; cobertura relacionada aprobada, no aceptación integral del RF|
|RF5|Gestionar Puntos de Recolección Georreferenciados|CU6|/api/{sectores,puntos,contenedores}/|Maestros.tsx; MapaCampus.tsx|Implementado; cobertura relacionada aprobada, no aceptación integral del RF|
|RF6|Gestionar Tipos de Residuo y Unidades de Medida|CU8|/api/{unidades,tipos-residuo,periodos,parametros}/|Maestros.tsx; Sistema.tsx|Implementado; cobertura relacionada aprobada, no aceptación integral del RF|
|RF7|Gestionar Contenedores|CU7|/api/{sectores,puntos,contenedores}/|Maestros.tsx; MapaCampus.tsx|Implementado; cobertura relacionada aprobada, no aceptación integral del RF|
|RF8|Registrar Generación y Vaciado de Residuos|CU9|/api/{vehiculos,jornadas,registros,incidencias}/|Jornadas.tsx; Campo.tsx; Registros.tsx|Implementado; cobertura relacionada aprobada, no aceptación integral del RF|
|RF9|Consultar el Histórico de Residuos|CU12|/api/{vehiculos,jornadas,registros,incidencias}/|Jornadas.tsx; Campo.tsx; Registros.tsx|Implementado; cobertura relacionada aprobada, no aceptación integral del RF|
|RF10|Registrar Incidencias Operativas|CU10, CU11|/api/{vehiculos,jornadas,registros,incidencias}/|Jornadas.tsx; Campo.tsx; Registros.tsx|Implementado; cobertura relacionada aprobada, no aceptación integral del RF|
|RF11|Planificar Jornadas y Rutas de Recolección|CU14|/api/{vehiculos,jornadas,registros,incidencias}/|Jornadas.tsx; Campo.tsx; Registros.tsx|Implementado; cobertura relacionada aprobada, no aceptación integral del RF|
|RF12|Registrar la Ejecución de la Recolección|CU16, CU17, CU18|/api/{vehiculos,jornadas,registros,incidencias}/|Jornadas.tsx; Campo.tsx; Registros.tsx|Implementado; cobertura relacionada aprobada, no aceptación integral del RF|
|RF13|Asignar Personal y Vehículos a las Jornadas|CU13, CU15|/api/{vehiculos,jornadas,registros,incidencias}/|Jornadas.tsx; Campo.tsx; Registros.tsx|Implementado; cobertura relacionada aprobada, no aceptación integral del RF|
|RF14|Consultar el Historial de Recolecciones|CU19|/api/{vehiculos,jornadas,registros,incidencias}/|Jornadas.tsx; Campo.tsx; Registros.tsx|Implementado; cobertura relacionada aprobada, no aceptación integral del RF|
|RF15|Ejecutar los Procesos de Extracción, Transformación y Carga|CU20|/api/{etl,analitica,reportes}/|Tablero.tsx; MapaCampus.tsx; Reportes.tsx; Sistema.tsx|Implementado; cobertura relacionada aprobada, no aceptación integral del RF|
|RF16|Calcular los Indicadores Clave de Rendimiento|CU21|/api/{etl,analitica,reportes}/|Tablero.tsx; MapaCampus.tsx; Reportes.tsx; Sistema.tsx|Implementado; cobertura relacionada aprobada, no aceptación integral del RF|
|RF17|Visualizar los Tableros Interactivos|CU21|/api/{etl,analitica,reportes}/|Tablero.tsx; MapaCampus.tsx; Reportes.tsx; Sistema.tsx|Implementado; cobertura relacionada aprobada, no aceptación integral del RF|
|RF18|Comparar Periodos e Identificar Tendencias|CU22|/api/{etl,analitica,reportes}/|Tablero.tsx; MapaCampus.tsx; Reportes.tsx; Sistema.tsx|Implementado; cobertura relacionada aprobada, no aceptación integral del RF|
|RF19|Visualizar los Puntos de Recolección en el Mapa Interactivo|CU23|/api/{etl,analitica,reportes}/|Tablero.tsx; MapaCampus.tsx; Reportes.tsx; Sistema.tsx|Implementado; cobertura relacionada aprobada, no aceptación integral del RF|
|RF20|Generar el Mapa de Calor de Zonas Críticas|CU24|/api/{etl,analitica,reportes}/|Tablero.tsx; MapaCampus.tsx; Reportes.tsx; Sistema.tsx|Implementado; cobertura relacionada aprobada, no aceptación integral del RF|
|RF21|Filtrar el Mapa por Periodo, Sector y Tipo de Residuo|CU25|/api/{etl,analitica,reportes}/|Tablero.tsx; MapaCampus.tsx; Reportes.tsx; Sistema.tsx|Implementado; cobertura relacionada aprobada, no aceptación integral del RF|
|RF22|Entrenar y Evaluar el Modelo Random Forest Regressor|CU26, CU27|/api/{modelos,predicciones,recomendaciones}/|Modelo.tsx; Prediccion.tsx; Recomendaciones.tsx|Implementado; cobertura relacionada aprobada, no aceptación integral del RF|
|RF23|Predecir la Generación Futura de Residuos|CU28|/api/{modelos,predicciones,recomendaciones}/|Modelo.tsx; Prediccion.tsx; Recomendaciones.tsx|Implementado; cobertura relacionada aprobada, no aceptación integral del RF|
|RF24|Generar Alertas y Recomendaciones Logísticas|CU28, CU29, CU30|/api/{modelos,predicciones,recomendaciones}/|Modelo.tsx; Prediccion.tsx; Recomendaciones.tsx|Implementado; cobertura relacionada aprobada, no aceptación integral del RF|
|RF25|Administrar Catálogos y Parámetros del Modelo|CU31|/api/{unidades,tipos-residuo,periodos,parametros}/|Maestros.tsx; Sistema.tsx|Implementado; cobertura relacionada aprobada, no aceptación integral del RF|
|RF26|Registrar y Consultar la Bitácora de Auditoría|CU32|/api/{bitacora}/|Admin.tsx|Implementado; cobertura relacionada aprobada, no aceptación integral del RF|
|RF27|Generar, Exportar e Imprimir Reportes|CU33, CU34|/api/{etl,analitica,reportes}/|Tablero.tsx; MapaCampus.tsx; Reportes.tsx; Sistema.tsx|Implementado; cobertura relacionada aprobada, no aceptación integral del RF|

## Requisitos no funcionales y capacidad

|ID|Texto oficial|Evidencia y alcance|Estado|
|---|---|---|---|
|RNF1|El sistema deberá responder en un tiempo máximo de 2 segundos en las operaciones de búsqueda de puntos, sectores o tipos de residuo.|Código y pruebas de dominio; no acredita aceptación institucional de todas las condiciones.|PARCIAL|
|RNF2|El sistema deberá confirmar el registro de un vaciado en un tiempo máximo de 3 segundos desde un dispositivo móvil conectado a la red institucional.|Código y pruebas de dominio; no acredita aceptación institucional de todas las condiciones.|PARCIAL|
|RNF3|El sistema deberá renderizar el mapa de calor del campus en un tiempo máximo de 6 segundos para un periodo de hasta doce meses.|Código y pruebas de dominio; no acredita aceptación institucional de todas las condiciones.|PARCIAL|
|RNF4|El sistema deberá soportar al menos 12 usuarios concurrentes durante la jornada de recolección sin degradación crítica del servicio.|carga_12_usuarios.txt: 12 hilos, 60 s, 531 peticiones sin errores y 156 vaciados confirmados/persistidos; identidades compartidas de prueba. No mide la VM productiva.|CUMPLE EN ENTORNO LOCAL|
|RNF5|La ejecución del entrenamiento del modelo predictivo no deberá afectar la disponibilidad ni el tiempo de respuesta de las funciones transaccionales.|Hilos web y separación de modelos: riesgo de interrupción al reiniciar; no hay cola durable.|PARCIAL|
|RNF6|El sistema deberá presentar una interfaz clara y comprensible, considerando que el personal operativo no necesariamente posee conocimientos técnicos avanzados.|Código y pruebas de dominio; no acredita aceptación institucional de todas las condiciones.|PARCIAL|
|RNF7|Las interfaces de captura en campo deberán ser completamente responsivas y operables desde teléfonos móviles y tabletas.|Código y pruebas de dominio; no acredita aceptación institucional de todas las condiciones.|PARCIAL|
|RNF8|El registro de un vaciado no deberá requerir más de cuatro interacciones del usuario en el caso de uso más frecuente.|Interfaz Campo implementada; cuatro interacciones no instrumentadas de nuevo en todas las variantes.|PARCIAL|
|RNF9|El sistema deberá mostrar mensajes de validación y error comprensibles cuando existan datos incompletos, cantidades inválidas o puntos inexistentes.|Código y pruebas de dominio; no acredita aceptación institucional de todas las condiciones.|PARCIAL|
|RNF10|El sistema deberá validar la consistencia entre sectores, puntos, registros de residuos y jornadas antes de almacenar cualquier operación.|Código y pruebas de dominio; no acredita aceptación institucional de todas las condiciones.|PARCIAL|
|RNF11|El sistema deberá conservar íntegramente los registros históricos, que constituyen la base del componente predictivo, sin permitir su eliminación física.|Código y pruebas de dominio; no acredita aceptación institucional de todas las condiciones.|PARCIAL|
|RNF12|El sistema deberá realizar respaldos automáticos de la información al menos una vez por día.|scripts/respaldo.sh y restauracion.json sintética; copia externa y recuperación productiva no demostradas.|PARCIAL|
|RNF13|Las predicciones y recomendaciones deberán presentarse siempre como herramientas de apoyo y nunca deberán reemplazar automáticamente el criterio de los responsables de la dirección.|Código y pruebas de dominio; no acredita aceptación institucional de todas las condiciones.|PARCIAL|
|RNF14|El sistema deberá requerir autenticación mediante usuario y contraseña para el acceso a todas sus funcionalidades.|JUnit accounts/acceso/roles/bitácora y capturas de Directivo sin acceso.|PARCIAL|
|RNF15|Las contraseñas deberán almacenarse protegidas mediante un algoritmo de resumen criptográfico con sal, sin posibilidad de recuperación en texto plano.|JUnit accounts/acceso/roles/bitácora y capturas de Directivo sin acceso.|PARCIAL|
|RNF16|El sistema deberá aplicar control de acceso por roles y permisos tanto en la interfaz como en los servicios del servidor.|JUnit accounts/acceso/roles/bitácora y capturas de Directivo sin acceso.|PARCIAL|
|RNF17|Las comunicaciones entre el cliente y el servidor deberán realizarse sobre un canal cifrado.|Código y pruebas de dominio; no acredita aceptación institucional de todas las condiciones.|PARCIAL|
|RNF18|El sistema deberá ser accesible desde navegadores web modernos, como Google Chrome, Microsoft Edge y Mozilla Firefox, sin requerir software adicional.|Chrome aislado y perfiles móviles históricos; no se acredita toda la matriz de navegadores/equipos.|PARCIAL|
|RNF19|El sistema deberá funcionar correctamente en equipos de escritorio, portátiles, tabletas y teléfonos móviles.|Chrome aislado y perfiles móviles históricos; no se acredita toda la matriz de navegadores/equipos.|PARCIAL|
|RNF20|El sistema deberá desarrollarse con una estructura modular que separe el plano transaccional del plano analítico y facilite la incorporación de nuevos módulos.|Código y pruebas de dominio; no acredita aceptación institucional de todas las condiciones.|PARCIAL|
|RNF21|Los umbrales, parámetros del modelo y definiciones del calendario académico deberán ser configurables sin modificar el código fuente.|Código y pruebas de dominio; no acredita aceptación institucional de todas las condiciones.|PARCIAL|
|RNF22|El sistema deberá contar con documentación técnica y funcional suficiente para facilitar su mantenimiento y su evolución futura.|Código y pruebas de dominio; no acredita aceptación institucional de todas las condiciones.|PARCIAL|
|RNF23|Las cantidades de residuos deberán almacenarse mediante tipos decimales de precisión fija, evitando cálculos con tipos de coma flotante que introduzcan diferencias en los agregados.|test_etl_convierte_cantidades_sin_error_binario; conversión persistida Decimal, floats solo para estadísticas.|PARCIAL|
|RNF24|Las coordenadas geográficas deberán almacenarse con al menos seis decimales, precisión suficiente para distinguir puntos contiguos dentro del campus.|Código y pruebas de dominio; no acredita aceptación institucional de todas las condiciones.|PARCIAL|
|RNF25|El sistema deberá conservar el historial de las operaciones críticas, de las ejecuciones del proceso de carga y de las versiones del modelo predictivo, con su usuario, fecha y resultado.|JUnit accounts/acceso/roles/bitácora y capturas de Directivo sin acceso.|PARCIAL|
|RNF26|El sistema deberá exponer su información depurada mediante interfaces que permitan su consumo desde la herramienta de visualización seleccionada.|Power BI: vistas/modelo disponibles y lectura SQL comprobada previamente; publicación/enlace/RLS pendientes.|PARCIAL|
|RTR1|Menor o igual a 2 segundos|rendimiento_local.txt/json: API en proceso local, datos sintéticos y rollback; no mide latencia productiva.|CUMPLE EN ENTORNO LOCAL|
|RTR2|Menor o igual a 3 segundos|rendimiento_local.txt/json: API en proceso local, datos sintéticos y rollback; no mide latencia productiva.|CUMPLE EN ENTORNO LOCAL|
|RTR3|Menor o igual a 2 segundos|rendimiento_local.txt/json: API en proceso local, datos sintéticos y rollback; no mide latencia productiva.|CUMPLE EN ENTORNO LOCAL|
|RTR4|Menor o igual a 3 segundos|rendimiento_local.txt/json: API en proceso local, datos sintéticos y rollback; no mide latencia productiva.|CUMPLE EN ENTORNO LOCAL|
|RTR5|Menor o igual a 3 segundos|rendimiento_local.txt/json: API en proceso local, datos sintéticos y rollback; no mide latencia productiva.|CUMPLE EN ENTORNO LOCAL|
|RTR6|Menor o igual a 4 segundos|rendimiento_local.txt/json: API en proceso local, datos sintéticos y rollback; no mide latencia productiva.|CUMPLE EN ENTORNO LOCAL|
|RTR7|Menor o igual a 4 segundos|rendimiento_local.txt/json: API en proceso local, datos sintéticos y rollback; no mide latencia productiva.|CUMPLE EN ENTORNO LOCAL|
|RTR8|Menor o igual a 6 segundos|rendimiento_local.txt/json: API en proceso local, datos sintéticos y rollback; no mide latencia productiva.|CUMPLE EN ENTORNO LOCAL|
|RTR9|Menor o igual a 5 segundos|rendimiento_local.txt/json: API en proceso local, datos sintéticos y rollback; no mide latencia productiva.|CUMPLE EN ENTORNO LOCAL|
|RTR10|Menor o igual a 8 segundos|rendimiento_local.txt/json: API en proceso local, datos sintéticos y rollback; no mide latencia productiva.|CUMPLE EN ENTORNO LOCAL|
|RTR11|Menor o igual a 15 segundos|rendimiento_local.txt/json: API en proceso local, datos sintéticos y rollback; no mide latencia productiva.|CUMPLE EN ENTORNO LOCAL|
|RTR12|Menor o igual a 10 minutos, ejecutado de forma asíncrona|rendimiento_local.txt/json: API en proceso local, datos sintéticos y rollback; no mide latencia productiva.|CUMPLE EN ENTORNO LOCAL|
|RCM1|El sistema deberá soportar al menos 12 usuarios concurrentes durante la jornada de recolección sin degradación crítica del servicio.|carga_12_usuarios.txt: 12 hilos, 60 s, 531 peticiones sin errores y 156 vaciados confirmados/persistidos; identidades compartidas de prueba. No mide la VM productiva.|CUMPLE EN ENTORNO LOCAL|
|RCM2|El sistema deberá admitir el registro simultáneo de vaciados por parte de distintas cuadrillas sin pérdida de información ni bloqueos.|carga_12_usuarios.txt: 12 hilos, 60 s, 531 peticiones sin errores y 156 vaciados confirmados/persistidos; identidades compartidas de prueba. No mide la VM productiva.|CUMPLE EN ENTORNO LOCAL|
|RCM3|El sistema deberá soportar el manejo de al menos 500 puntos de recolección georreferenciados manteniendo tiempos de respuesta aceptables.|rendimiento_local.txt/json: API en proceso local, datos sintéticos y rollback; no mide latencia productiva.|CUMPLE EN ENTORNO LOCAL|
|RCM4|El componente cartográfico deberá representar simultáneamente la totalidad de los puntos activos sin degradar la fluidez de la navegación.|Código y pruebas de dominio; no acredita aceptación institucional de todas las condiciones.|PARCIAL|
|RCM5|El sistema deberá almacenar y procesar el histórico acumulado de registros de residuos sin afectar su funcionamiento general.|rendimiento_local.txt/json: API en proceso local, datos sintéticos y rollback; no mide latencia productiva.|CUMPLE EN ENTORNO LOCAL|
|RCM6|El sistema deberá soportar la generación de reportes por día, semana, mes, semestre o periodo académico.|Código y pruebas de dominio; no acredita aceptación institucional de todas las condiciones.|PARCIAL|
|RCM7|El componente predictivo deberá entrenar correctamente sobre conjuntos de al menos cien mil observaciones históricas.|rendimiento_local.txt/json: API en proceso local, datos sintéticos y rollback; no mide latencia productiva.|CUMPLE EN ENTORNO LOCAL|
|RCM8|El sistema deberá generar predicciones para un horizonte configurable de hasta treinta días.|rendimiento_local.txt/json: API en proceso local, datos sintéticos y rollback; no mide latencia productiva.|CUMPLE EN ENTORNO LOCAL|
