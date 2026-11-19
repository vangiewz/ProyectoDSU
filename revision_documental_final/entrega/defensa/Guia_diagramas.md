# Guía de lectura y defensa de diagramas

Las clases de análisis representan responsabilidades; los nombres literales del ORM están en el anexo K. Recorrer origen, relación, destino, regla y evidencia.

## CU1. Iniciar sesión

Explicación breve: Autenticar al usuario y abrir una sesión con acceso únicamente a las funciones de su rol. Requisito: RF3.

Explicación de detalle: el actor inicia la tarea, la interfaz solicita una operación y el control coordina entidades. La numeración de la colaboración identifica mensajes conceptuales, no firmas literales de Python.

Actores normativos: Personal Operativo de Limpieza, Supervisor de Recolección, Cuerpo Directivo de la DSU, Administrador del Sistema. Contrastarlos con los permisos observados en QA.

Precondición: El usuario cuenta con una cuenta activa registrada en el sistema.

Postcondición: La sesión queda abierta y el usuario accede solo a las funciones autorizadas para su rol.

Evidencia: generador/fase2/datos.py y matriz_casos_uso.json del paquete gráfico. Una visita al módulo no acredita todas sus alternativas.

## CU2. Cerrar sesión

Explicación breve: Terminar la sesión del usuario e invalidar sus credenciales de acceso. Requisito: RF3.

Explicación de detalle: el actor inicia la tarea, la interfaz solicita una operación y el control coordina entidades. La numeración de la colaboración identifica mensajes conceptuales, no firmas literales de Python.

Actores normativos: Personal Operativo de Limpieza, Supervisor de Recolección, Cuerpo Directivo de la DSU, Administrador del Sistema. Contrastarlos con los permisos observados en QA.

Precondición: El usuario tiene una sesión abierta.

Postcondición: La sesión queda cerrada, registrada en la bitácora, y el token ya no permite el acceso.

Evidencia: generador/fase2/datos.py y matriz_casos_uso.json del paquete gráfico. Una visita al módulo no acredita todas sus alternativas.

## CU3. Gestionar usuarios

Explicación breve: Administrar las cuentas del personal que accede al sistema. Requisito: RF1.

Explicación de detalle: el actor inicia la tarea, la interfaz solicita una operación y el control coordina entidades. La numeración de la colaboración identifica mensajes conceptuales, no firmas literales de Python.

Actores normativos: Administrador del Sistema. Contrastarlos con los permisos observados en QA.

Precondición: El administrador inició sesión con permisos de administración.

Postcondición: La cuenta queda registrada o actualizada con sus roles.

Evidencia: generador/fase2/datos.py y matriz_casos_uso.json del paquete gráfico. Una visita al módulo no acredita todas sus alternativas.

## CU4. Gestionar roles y permisos

Explicación breve: Definir los niveles de acceso a los módulos del sistema. Requisito: RF2.

Explicación de detalle: el actor inicia la tarea, la interfaz solicita una operación y el control coordina entidades. La numeración de la colaboración identifica mensajes conceptuales, no firmas literales de Python.

Actores normativos: Administrador del Sistema. Contrastarlos con los permisos observados en QA.

Precondición: El administrador inició sesión con permisos de administración.

Postcondición: Los roles quedan definidos con sus permisos y se aplican a los usuarios que los tienen asignados.

Evidencia: generador/fase2/datos.py y matriz_casos_uso.json del paquete gráfico. Una visita al módulo no acredita todas sus alternativas.

## CU5. Gestionar sectores y facultades

Explicación breve: Mantener la estructura territorial del campus sobre la que se agregan los indicadores y las predicciones. Requisito: RF4.

Explicación de detalle: el actor inicia la tarea, la interfaz solicita una operación y el control coordina entidades. La numeración de la colaboración identifica mensajes conceptuales, no firmas literales de Python.

Actores normativos: Administrador del Sistema, Supervisor de Recolección. Contrastarlos con los permisos observados en QA.

Precondición: El usuario inició sesión con permisos sobre sectores.

Postcondición: La estructura de sectores queda actualizada.

Evidencia: generador/fase2/datos.py y matriz_casos_uso.json del paquete gráfico. Una visita al módulo no acredita todas sus alternativas.

## CU6. Gestionar puntos de recolección

Explicación breve: Registrar los puntos de recolección georreferenciados que alimentan la operación, el mapa y el modelo. Requisito: RF5.

Explicación de detalle: el actor inicia la tarea, la interfaz solicita una operación y el control coordina entidades. La numeración de la colaboración identifica mensajes conceptuales, no firmas literales de Python.

Actores normativos: Administrador del Sistema, Supervisor de Recolección. Contrastarlos con los permisos observados en QA.

Precondición: Existe al menos un sector activo.

Postcondición: El punto queda registrado y visible en el mapa.

Evidencia: generador/fase2/datos.py y matriz_casos_uso.json del paquete gráfico. Una visita al módulo no acredita todas sus alternativas.

## CU7. Gestionar contenedores

Explicación breve: Registrar la capacidad instalada de cada punto. Requisito: RF7.

Explicación de detalle: el actor inicia la tarea, la interfaz solicita una operación y el control coordina entidades. La numeración de la colaboración identifica mensajes conceptuales, no firmas literales de Python.

Actores normativos: Administrador del Sistema, Supervisor de Recolección. Contrastarlos con los permisos observados en QA.

Precondición: Existe al menos un punto de recolección activo.

Postcondición: La capacidad instalada del punto queda actualizada.

Evidencia: generador/fase2/datos.py y matriz_casos_uso.json del paquete gráfico. Una visita al módulo no acredita todas sus alternativas.

## CU8. Gestionar tipos de residuo y unidades de medida

Explicación breve: Homogeneizar la clasificación y la cuantificación de los residuos. Requisito: RF6.

Explicación de detalle: el actor inicia la tarea, la interfaz solicita una operación y el control coordina entidades. La numeración de la colaboración identifica mensajes conceptuales, no firmas literales de Python.

Actores normativos: Administrador del Sistema. Contrastarlos con los permisos observados en QA.

Precondición: El usuario inició sesión con permisos sobre catálogos.

Postcondición: El catálogo queda disponible para el registro y la analítica.

Evidencia: generador/fase2/datos.py y matriz_casos_uso.json del paquete gráfico. Una visita al módulo no acredita todas sus alternativas.

## CU9. Registrar vaciado de residuos

Explicación breve: Capturar en campo la unidad básica de información del sistema: cuánto residuo, de qué tipo y de qué punto. Requisito: RF8.

Explicación de detalle: el actor inicia la tarea, la interfaz solicita una operación y el control coordina entidades. La numeración de la colaboración identifica mensajes conceptuales, no firmas literales de Python.

Actores normativos: Personal Operativo de Limpieza, Supervisor de Recolección. Contrastarlos con los permisos observados en QA.

Precondición: El operario inició sesión y su jornada está abierta (en ejecución).

Postcondición: El vaciado queda vinculado al punto, sector, jornada y operario, disponible para el ETL.

Evidencia: generador/fase2/datos.py y matriz_casos_uso.json del paquete gráfico. Una visita al módulo no acredita todas sus alternativas.

## CU10. Registrar incidencia operativa

Explicación breve: Documentar las situaciones que afectan la recolección. Requisito: RF10.

Explicación de detalle: el actor inicia la tarea, la interfaz solicita una operación y el control coordina entidades. La numeración de la colaboración identifica mensajes conceptuales, no firmas literales de Python.

Actores normativos: Personal Operativo de Limpieza, Supervisor de Recolección. Contrastarlos con los permisos observados en QA.

Precondición: El usuario inició sesión; si es operario, está dentro de una jornada en ejecución.

Postcondición: La incidencia queda registrada y pendiente de atención.

Evidencia: generador/fase2/datos.py y matriz_casos_uso.json del paquete gráfico. Una visita al módulo no acredita todas sus alternativas.

## CU11. Atender incidencia

Explicación breve: Cerrar las incidencias con la acción adoptada. Requisito: RF10.

Explicación de detalle: el actor inicia la tarea, la interfaz solicita una operación y el control coordina entidades. La numeración de la colaboración identifica mensajes conceptuales, no firmas literales de Python.

Actores normativos: Supervisor de Recolección. Contrastarlos con los permisos observados en QA.

Precondición: Existe al menos una incidencia pendiente en un sector del supervisor.

Postcondición: La incidencia queda atendida y conserva su trazabilidad.

Evidencia: generador/fase2/datos.py y matriz_casos_uso.json del paquete gráfico. Una visita al módulo no acredita todas sus alternativas.

## CU12. Consultar histórico de residuos

Explicación breve: Recuperar los registros históricos con filtros y totales. Requisito: RF9.

Explicación de detalle: el actor inicia la tarea, la interfaz solicita una operación y el control coordina entidades. La numeración de la colaboración identifica mensajes conceptuales, no firmas literales de Python.

Actores normativos: Supervisor de Recolección, Administrador del Sistema, Cuerpo Directivo de la DSU, Personal Operativo de Limpieza. Contrastarlos con los permisos observados en QA.

Precondición: Existen registros de residuos almacenados.

Postcondición: El usuario obtiene el histórico solicitado.

Evidencia: generador/fase2/datos.py y matriz_casos_uso.json del paquete gráfico. Una visita al módulo no acredita todas sus alternativas.

## CU13. Gestionar vehículos

Explicación breve: Mantener el registro de los vehículos disponibles para las jornadas. Requisito: RF13.

Explicación de detalle: el actor inicia la tarea, la interfaz solicita una operación y el control coordina entidades. La numeración de la colaboración identifica mensajes conceptuales, no firmas literales de Python.

Actores normativos: Administrador del Sistema, Supervisor de Recolección. Contrastarlos con los permisos observados en QA.

Precondición: El usuario inició sesión con permisos sobre vehículos.

Postcondición: El vehículo queda disponible (o fuera de servicio) para asignar.

Evidencia: generador/fase2/datos.py y matriz_casos_uso.json del paquete gráfico. Una visita al módulo no acredita todas sus alternativas.

## CU14. Planificar jornada y ruta de recolección

Explicación breve: Definir cuándo, dónde y en qué orden se recolecta. Requisito: RF11.

Explicación de detalle: el actor inicia la tarea, la interfaz solicita una operación y el control coordina entidades. La numeración de la colaboración identifica mensajes conceptuales, no firmas literales de Python.

Actores normativos: Supervisor de Recolección, Administrador del Sistema. Contrastarlos con los permisos observados en QA.

Precondición: Existen sectores y puntos activos.

Postcondición: La jornada queda planificada y confirmada con su ruta.

Evidencia: generador/fase2/datos.py y matriz_casos_uso.json del paquete gráfico. Una visita al módulo no acredita todas sus alternativas.

## CU15. Asignar personal y vehículos a la jornada

Explicación breve: Dotar a la jornada de responsable, personal y vehículos sin superposiciones. Requisito: RF13.

Explicación de detalle: el actor inicia la tarea, la interfaz solicita una operación y el control coordina entidades. La numeración de la colaboración identifica mensajes conceptuales, no firmas literales de Python.

Actores normativos: Supervisor de Recolección, Administrador del Sistema. Contrastarlos con los permisos observados en QA.

Precondición: Existe una jornada planificada y personal registrado.

Postcondición: La jornada queda con personal, vehículos y responsable.

Evidencia: generador/fase2/datos.py y matriz_casos_uso.json del paquete gráfico. Una visita al módulo no acredita todas sus alternativas.

## CU16. Ejecutar jornada de recolección

Explicación breve: Controlar la ejecución real de la jornada punto por punto. Requisito: RF12.

Explicación de detalle: el actor inicia la tarea, la interfaz solicita una operación y el control coordina entidades. La numeración de la colaboración identifica mensajes conceptuales, no firmas literales de Python.

Actores normativos: Supervisor de Recolección, Personal Operativo de Limpieza. Contrastarlos con los permisos observados en QA.

Precondición: Existe una jornada confirmada para la fecha, con personal asignado.

Postcondición: Todos los puntos quedan visitados u omitidos con motivo.

Evidencia: generador/fase2/datos.py y matriz_casos_uso.json del paquete gráfico. Una visita al módulo no acredita todas sus alternativas.

## CU17. Omitir punto de la ruta

Explicación breve: Dejar constancia de los puntos planificados que no se atendieron y por qué. Requisito: RF12.

Explicación de detalle: el actor inicia la tarea, la interfaz solicita una operación y el control coordina entidades. La numeración de la colaboración identifica mensajes conceptuales, no firmas literales de Python.

Actores normativos: Personal Operativo de Limpieza, Supervisor de Recolección. Contrastarlos con los permisos observados en QA.

Precondición: La jornada está en ejecución y el punto está pendiente.

Postcondición: El punto queda omitido con su motivo y cuenta en la desviación de la jornada.

Evidencia: generador/fase2/datos.py y matriz_casos_uso.json del paquete gráfico. Una visita al módulo no acredita todas sus alternativas.

## CU18. Cerrar jornada de recolección

Explicación breve: Consolidar la jornada y bloquear cambios posteriores. Requisito: RF12.

Explicación de detalle: el actor inicia la tarea, la interfaz solicita una operación y el control coordina entidades. La numeración de la colaboración identifica mensajes conceptuales, no firmas literales de Python.

Actores normativos: Supervisor de Recolección. Contrastarlos con los permisos observados en QA.

Precondición: La jornada está en ejecución y todos sus puntos fueron visitados u omitidos.

Postcondición: La jornada queda cerrada con su resumen consolidado.

Evidencia: generador/fase2/datos.py y matriz_casos_uso.json del paquete gráfico. Una visita al módulo no acredita todas sus alternativas.

## CU19. Consultar historial de recolecciones

Explicación breve: Revisar las jornadas ejecutadas y su cobertura. Requisito: RF14.

Explicación de detalle: el actor inicia la tarea, la interfaz solicita una operación y el control coordina entidades. La numeración de la colaboración identifica mensajes conceptuales, no firmas literales de Python.

Actores normativos: Supervisor de Recolección, Administrador del Sistema, Cuerpo Directivo de la DSU, Personal Operativo de Limpieza. Contrastarlos con los permisos observados en QA.

Precondición: Existen jornadas registradas.

Postcondición: El usuario obtiene el historial solicitado.

Evidencia: generador/fase2/datos.py y matriz_casos_uso.json del paquete gráfico. Una visita al módulo no acredita todas sus alternativas.

## CU20. Ejecutar proceso ETL

Explicación breve: Consolidar y depurar la información transaccional para la analítica y el modelo. Requisito: RF15.

Explicación de detalle: el actor inicia la tarea, la interfaz solicita una operación y el control coordina entidades. La numeración de la colaboración identifica mensajes conceptuales, no firmas literales de Python.

Actores normativos: Administrador del Sistema. Contrastarlos con los permisos observados en QA.

Precondición: Existen registros transaccionales nuevos desde la última ejecución.

Postcondición: La tabla de hechos queda actualizada para indicadores, mapas y modelo.

Evidencia: generador/fase2/datos.py y matriz_casos_uso.json del paquete gráfico. Una visita al módulo no acredita todas sus alternativas.

## CU21. Visualizar tablero interactivo

Explicación breve: Calcular los indicadores clave y presentarlos con sus series de forma interactiva. Requisito: RF16, RF17.

Explicación de detalle: el actor inicia la tarea, la interfaz solicita una operación y el control coordina entidades. La numeración de la colaboración identifica mensajes conceptuales, no firmas literales de Python.

Actores normativos: Cuerpo Directivo de la DSU, Supervisor de Recolección, Administrador del Sistema. Contrastarlos con los permisos observados en QA.

Precondición: El usuario inició sesión con permisos de consulta analítica y el proceso ETL se ejecutó al menos una vez.

Postcondición: El usuario interpreta el comportamiento histórico de los residuos.

Evidencia: generador/fase2/datos.py y matriz_casos_uso.json del paquete gráfico. Una visita al módulo no acredita todas sus alternativas.

## CU22. Comparar periodos e identificar tendencias

Explicación breve: Medir la variación entre dos periodos y detectar crecimiento sostenido. Requisito: RF18.

Explicación de detalle: el actor inicia la tarea, la interfaz solicita una operación y el control coordina entidades. La numeración de la colaboración identifica mensajes conceptuales, no firmas literales de Python.

Actores normativos: Cuerpo Directivo de la DSU, Supervisor de Recolección, Administrador del Sistema. Contrastarlos con los permisos observados en QA.

Precondición: Existen hechos en ambos periodos.

Postcondición: La comparación y las tendencias quedan visibles en el tablero.

Evidencia: generador/fase2/datos.py y matriz_casos_uso.json del paquete gráfico. Una visita al módulo no acredita todas sus alternativas.

## CU23. Visualizar puntos en el mapa interactivo

Explicación breve: Mostrar la distribución geográfica de los puntos. Requisito: RF19.

Explicación de detalle: el actor inicia la tarea, la interfaz solicita una operación y el control coordina entidades. La numeración de la colaboración identifica mensajes conceptuales, no firmas literales de Python.

Actores normativos: Cuerpo Directivo de la DSU, Supervisor de Recolección, Administrador del Sistema. Contrastarlos con los permisos observados en QA.

Precondición: Existen puntos con coordenadas válidas.

Postcondición: El usuario visualiza la distribución de los puntos.

Evidencia: generador/fase2/datos.py y matriz_casos_uso.json del paquete gráfico. Una visita al módulo no acredita todas sus alternativas.

## CU24. Generar mapa de calor

Explicación breve: Identificar visualmente las zonas críticas del campus. Requisito: RF20.

Explicación de detalle: el actor inicia la tarea, la interfaz solicita una operación y el control coordina entidades. La numeración de la colaboración identifica mensajes conceptuales, no firmas literales de Python.

Actores normativos: Cuerpo Directivo de la DSU, Supervisor de Recolección, Administrador del Sistema. Contrastarlos con los permisos observados en QA.

Precondición: Existen hechos (o predicciones vigentes, para la capa proyectada) en el alcance.

Postcondición: El mapa de calor queda dibujado con las zonas críticas.

Evidencia: generador/fase2/datos.py y matriz_casos_uso.json del paquete gráfico. Una visita al módulo no acredita todas sus alternativas.

## CU25. Filtrar mapa por periodo, sector y tipo de residuo

Explicación breve: Acotar la vista cartográfica. Requisito: RF21.

Explicación de detalle: el actor inicia la tarea, la interfaz solicita una operación y el control coordina entidades. La numeración de la colaboración identifica mensajes conceptuales, no firmas literales de Python.

Actores normativos: Cuerpo Directivo de la DSU, Supervisor de Recolección, Administrador del Sistema. Contrastarlos con los permisos observados en QA.

Precondición: El mapa está cargado.

Postcondición: El mapa refleja solo la información filtrada.

Evidencia: generador/fase2/datos.py y matriz_casos_uso.json del paquete gráfico. Una visita al módulo no acredita todas sus alternativas.

## CU26. Entrenar y evaluar el modelo Random Forest Regressor

Explicación breve: Obtener una nueva versión del modelo y medir su desempeño. Requisito: RF22.

Explicación de detalle: el actor inicia la tarea, la interfaz solicita una operación y el control coordina entidades. La numeración de la colaboración identifica mensajes conceptuales, no firmas literales de Python.

Actores normativos: Administrador del Sistema. Contrastarlos con los permisos observados en QA.

Precondición: Existe el volumen mínimo de hechos depurados configurado.

Postcondición: Queda una nueva versión entrenada y evaluada.

Evidencia: generador/fase2/datos.py y matriz_casos_uso.json del paquete gráfico. Una visita al módulo no acredita todas sus alternativas.

## CU27. Publicar o revertir versión del modelo

Explicación breve: Decidir qué versión del modelo usan las predicciones. Requisito: RF22.

Explicación de detalle: el actor inicia la tarea, la interfaz solicita una operación y el control coordina entidades. La numeración de la colaboración identifica mensajes conceptuales, no firmas literales de Python.

Actores normativos: Administrador del Sistema. Contrastarlos con los permisos observados en QA.

Precondición: Existe al menos una versión entrenada que superó el umbral.

Postcondición: La versión elegida queda vigente para las predicciones.

Evidencia: generador/fase2/datos.py y matriz_casos_uso.json del paquete gráfico. Una visita al módulo no acredita todas sus alternativas.

## CU28. Predecir generación futura y emitir alertas

Explicación breve: Estimar cuánto residuo se generará por punto y sector, con su margen de error, y traducir la estimación en alertas y recomendaciones logísticas. Requisito: RF23, RF24.

Explicación de detalle: el actor inicia la tarea, la interfaz solicita una operación y el control coordina entidades. La numeración de la colaboración identifica mensajes conceptuales, no firmas literales de Python.

Actores normativos: Supervisor de Recolección, Cuerpo Directivo de la DSU, Administrador del Sistema. Contrastarlos con los permisos observados en QA.

Precondición: Existe un modelo publicado vigente.

Postcondición: El lote de predicciones queda guardado y las recomendaciones, pendientes de resolución.

Evidencia: generador/fase2/datos.py y matriz_casos_uso.json del paquete gráfico. Una visita al módulo no acredita todas sus alternativas.

## CU29. Consultar alertas y recomendaciones logísticas

Explicación breve: Revisar las alertas tempranas y las recomendaciones emitidas con su evidencia. Requisito: RF24.

Explicación de detalle: el actor inicia la tarea, la interfaz solicita una operación y el control coordina entidades. La numeración de la colaboración identifica mensajes conceptuales, no firmas literales de Python.

Actores normativos: Supervisor de Recolección, Cuerpo Directivo de la DSU, Administrador del Sistema. Contrastarlos con los permisos observados en QA.

Precondición: El usuario inició sesión con permiso para ver las recomendaciones.

Postcondición: El usuario conoce las alertas y recomendaciones vigentes.

Evidencia: generador/fase2/datos.py y matriz_casos_uso.json del paquete gráfico. Una visita al módulo no acredita todas sus alternativas.

## CU30. Atender recomendación logística

Explicación breve: Aceptar o descartar cada recomendación dejando constancia. Requisito: RF24.

Explicación de detalle: el actor inicia la tarea, la interfaz solicita una operación y el control coordina entidades. La numeración de la colaboración identifica mensajes conceptuales, no firmas literales de Python.

Actores normativos: Supervisor de Recolección, Administrador del Sistema. Contrastarlos con los permisos observados en QA.

Precondición: Existen recomendaciones pendientes en sectores del supervisor.

Postcondición: La recomendación queda resuelta y, si se aceptó, incorporada.

Evidencia: generador/fase2/datos.py y matriz_casos_uso.json del paquete gráfico. Una visita al módulo no acredita todas sus alternativas.

## CU31. Configurar periodos académicos y parámetros

Explicación breve: Ajustar el comportamiento analítico y predictivo sin tocar el código. Requisito: RF25.

Explicación de detalle: el actor inicia la tarea, la interfaz solicita una operación y el control coordina entidades. La numeración de la colaboración identifica mensajes conceptuales, no firmas literales de Python.

Actores normativos: Administrador del Sistema. Contrastarlos con los permisos observados en QA.

Precondición: El administrador inició sesión con permisos de administración.

Postcondición: Los parámetros y periodos quedan aplicados a las siguientes ejecuciones.

Evidencia: generador/fase2/datos.py y matriz_casos_uso.json del paquete gráfico. Una visita al módulo no acredita todas sus alternativas.

## CU32. Consultar bitácora de auditoría

Explicación breve: Revisar quién hizo qué y cuándo. Requisito: RF26.

Explicación de detalle: el actor inicia la tarea, la interfaz solicita una operación y el control coordina entidades. La numeración de la colaboración identifica mensajes conceptuales, no firmas literales de Python.

Actores normativos: Administrador del Sistema. Contrastarlos con los permisos observados en QA.

Precondición: El usuario tiene permiso de auditoría.

Postcondición: El usuario obtiene la traza solicitada.

Evidencia: generador/fase2/datos.py y matriz_casos_uso.json del paquete gráfico. Una visita al módulo no acredita todas sus alternativas.

## CU33. Generar reporte

Explicación breve: Emitir reportes operativos y gerenciales. Requisito: RF27.

Explicación de detalle: el actor inicia la tarea, la interfaz solicita una operación y el control coordina entidades. La numeración de la colaboración identifica mensajes conceptuales, no firmas literales de Python.

Actores normativos: Administrador del Sistema, Supervisor de Recolección, Cuerpo Directivo de la DSU. Contrastarlos con los permisos observados en QA.

Precondición: Existe información para el periodo y filtros.

Postcondición: El reporte queda generado en pantalla.

Evidencia: generador/fase2/datos.py y matriz_casos_uso.json del paquete gráfico. Una visita al módulo no acredita todas sus alternativas.

## CU34. Exportar reporte a Excel o PDF

Explicación breve: Obtener el reporte como archivo con encabezado institucional para archivarlo, compartirlo o imprimirlo. Requisito: RF27.

Explicación de detalle: el actor inicia la tarea, la interfaz solicita una operación y el control coordina entidades. La numeración de la colaboración identifica mensajes conceptuales, no firmas literales de Python.

Actores normativos: Administrador del Sistema, Supervisor de Recolección, Cuerpo Directivo de la DSU. Contrastarlos con los permisos observados en QA.

Precondición: El reporte está generado en pantalla.

Postcondición: El archivo queda descargado y la emisión registrada.

Evidencia: generador/fase2/datos.py y matriz_casos_uso.json del paquete gráfico. Una visita al módulo no acredita todas sus alternativas.

## auth.Permission

Explicación breve: modelo de la tabla auth_permission; fuente Django auth.

Explicación detallada: la caja izquierda muestra los campos del ORM. Cada flecha parte de un campo de relación y termina en el modelo destino. * representa 0..*; 0..1 indica opcionalidad; 1 indica referencia obligatoria.

- `content_type` → `contenttypes.ContentType`: ForeignKey; referencia obligatoria.

Pregunta difícil: ¿una multiplicidad permite borrar el destino? No. Describe cantidad y opcionalidad; las políticas de borrado y las validaciones se consultan en el campo y los servicios.

## auth.Group

Explicación breve: modelo de la tabla auth_group; fuente Django auth.

Explicación detallada: la caja izquierda muestra los campos del ORM. Cada flecha parte de un campo de relación y termina en el modelo destino. * representa 0..*; 0..1 indica opcionalidad; 1 indica referencia obligatoria.

- `permissions` → `auth.Permission`: ManyToManyField; muchos a muchos con tabla intermedia.

Pregunta difícil: ¿una multiplicidad permite borrar el destino? No. Describe cantidad y opcionalidad; las políticas de borrado y las validaciones se consultan en el campo y los servicios.

## accounts.User

Explicación breve: modelo de la tabla accounts_user; fuente gestion-residuos-dsu\backend\apps\accounts\models\user.py.

Explicación detallada: la caja izquierda muestra los campos del ORM. Cada flecha parte de un campo de relación y termina en el modelo destino. * representa 0..*; 0..1 indica opcionalidad; 1 indica referencia obligatoria.

- `groups` → `auth.Group`: ManyToManyField; muchos a muchos con tabla intermedia.

- `user_permissions` → `auth.Permission`: ManyToManyField; muchos a muchos con tabla intermedia.

Pregunta difícil: ¿una multiplicidad permite borrar el destino? No. Describe cantidad y opcionalidad; las políticas de borrado y las validaciones se consultan en el campo y los servicios.

## audit.AuditLog

Explicación breve: modelo de la tabla audit_auditlog; fuente gestion-residuos-dsu\backend\apps\audit\models\audit_log.py.

Explicación detallada: la caja izquierda muestra los campos del ORM. Cada flecha parte de un campo de relación y termina en el modelo destino. * representa 0..*; 0..1 indica opcionalidad; 1 indica referencia obligatoria.

- `usuario` → `accounts.User`: ForeignKey; referencia opcional.

Pregunta difícil: ¿una multiplicidad permite borrar el destino? No. Describe cantidad y opcionalidad; las políticas de borrado y las validaciones se consultan en el campo y los servicios.

## catalogs.ParametrosSistema

Explicación breve: modelo de la tabla catalogs_parametrossistema; fuente gestion-residuos-dsu\backend\apps\catalogs\models\parametros.py.

Explicación detallada: la caja izquierda muestra los campos del ORM. Cada flecha parte de un campo de relación y termina en el modelo destino. * representa 0..*; 0..1 indica opcionalidad; 1 indica referencia obligatoria.

- `actualizado_por` → `accounts.User`: ForeignKey; referencia opcional.

Pregunta difícil: ¿una multiplicidad permite borrar el destino? No. Describe cantidad y opcionalidad; las políticas de borrado y las validaciones se consultan en el campo y los servicios.

## catalogs.PeriodoAcademico

Explicación breve: modelo de la tabla catalogs_periodoacademico; fuente gestion-residuos-dsu\backend\apps\catalogs\models\periodo_academico.py.

Explicación detallada: la caja izquierda muestra los campos del ORM. Cada flecha parte de un campo de relación y termina en el modelo destino. * representa 0..*; 0..1 indica opcionalidad; 1 indica referencia obligatoria.

Pregunta difícil: ¿una multiplicidad permite borrar el destino? No. Describe cantidad y opcionalidad; las políticas de borrado y las validaciones se consultan en el campo y los servicios.

## catalogs.UnidadMedida

Explicación breve: modelo de la tabla catalogs_unidadmedida; fuente gestion-residuos-dsu\backend\apps\catalogs\models\unidad_medida.py.

Explicación detallada: la caja izquierda muestra los campos del ORM. Cada flecha parte de un campo de relación y termina en el modelo destino. * representa 0..*; 0..1 indica opcionalidad; 1 indica referencia obligatoria.

Pregunta difícil: ¿una multiplicidad permite borrar el destino? No. Describe cantidad y opcionalidad; las políticas de borrado y las validaciones se consultan en el campo y los servicios.

## catalogs.TipoResiduo

Explicación breve: modelo de la tabla catalogs_tiporesiduo; fuente gestion-residuos-dsu\backend\apps\catalogs\models\tipo_residuo.py.

Explicación detallada: la caja izquierda muestra los campos del ORM. Cada flecha parte de un campo de relación y termina en el modelo destino. * representa 0..*; 0..1 indica opcionalidad; 1 indica referencia obligatoria.

- `unidad` → `catalogs.UnidadMedida`: ForeignKey; referencia obligatoria.

Pregunta difícil: ¿una multiplicidad permite borrar el destino? No. Describe cantidad y opcionalidad; las políticas de borrado y las validaciones se consultan en el campo y los servicios.

## campus.Sector

Explicación breve: modelo de la tabla campus_sector; fuente gestion-residuos-dsu\backend\apps\campus\models\sector.py.

Explicación detallada: la caja izquierda muestra los campos del ORM. Cada flecha parte de un campo de relación y termina en el modelo destino. * representa 0..*; 0..1 indica opcionalidad; 1 indica referencia obligatoria.

- `supervisor` → `accounts.User`: ForeignKey; referencia opcional.

Pregunta difícil: ¿una multiplicidad permite borrar el destino? No. Describe cantidad y opcionalidad; las políticas de borrado y las validaciones se consultan en el campo y los servicios.

## campus.PuntoRecoleccion

Explicación breve: modelo de la tabla campus_puntorecoleccion; fuente gestion-residuos-dsu\backend\apps\campus\models\punto_recoleccion.py.

Explicación detallada: la caja izquierda muestra los campos del ORM. Cada flecha parte de un campo de relación y termina en el modelo destino. * representa 0..*; 0..1 indica opcionalidad; 1 indica referencia obligatoria.

- `sector` → `campus.Sector`: ForeignKey; referencia obligatoria.

Pregunta difícil: ¿una multiplicidad permite borrar el destino? No. Describe cantidad y opcionalidad; las políticas de borrado y las validaciones se consultan en el campo y los servicios.

## campus.Contenedor

Explicación breve: modelo de la tabla campus_contenedor; fuente gestion-residuos-dsu\backend\apps\campus\models\contenedor.py.

Explicación detallada: la caja izquierda muestra los campos del ORM. Cada flecha parte de un campo de relación y termina en el modelo destino. * representa 0..*; 0..1 indica opcionalidad; 1 indica referencia obligatoria.

- `punto` → `campus.PuntoRecoleccion`: ForeignKey; referencia obligatoria.

Pregunta difícil: ¿una multiplicidad permite borrar el destino? No. Describe cantidad y opcionalidad; las políticas de borrado y las validaciones se consultan en el campo y los servicios.

## operations.Vehiculo

Explicación breve: modelo de la tabla operations_vehiculo; fuente gestion-residuos-dsu\backend\apps\operations\models\vehiculo.py.

Explicación detallada: la caja izquierda muestra los campos del ORM. Cada flecha parte de un campo de relación y termina en el modelo destino. * representa 0..*; 0..1 indica opcionalidad; 1 indica referencia obligatoria.

Pregunta difícil: ¿una multiplicidad permite borrar el destino? No. Describe cantidad y opcionalidad; las políticas de borrado y las validaciones se consultan en el campo y los servicios.

## operations.Jornada

Explicación breve: modelo de la tabla operations_jornada; fuente gestion-residuos-dsu\backend\apps\operations\models\jornada.py.

Explicación detallada: la caja izquierda muestra los campos del ORM. Cada flecha parte de un campo de relación y termina en el modelo destino. * representa 0..*; 0..1 indica opcionalidad; 1 indica referencia obligatoria.

- `sector` → `campus.Sector`: ForeignKey; referencia obligatoria.

- `planificada_por` → `accounts.User`: ForeignKey; referencia obligatoria.

- `responsable` → `accounts.User`: ForeignKey; referencia opcional.

- `personal` → `accounts.User`: ManyToManyField; muchos a muchos con tabla intermedia.

- `vehiculos` → `operations.Vehiculo`: ManyToManyField; muchos a muchos con tabla intermedia.

Pregunta difícil: ¿una multiplicidad permite borrar el destino? No. Describe cantidad y opcionalidad; las políticas de borrado y las validaciones se consultan en el campo y los servicios.

## operations.JornadaPunto

Explicación breve: modelo de la tabla operations_jornadapunto; fuente gestion-residuos-dsu\backend\apps\operations\models\jornada.py.

Explicación detallada: la caja izquierda muestra los campos del ORM. Cada flecha parte de un campo de relación y termina en el modelo destino. * representa 0..*; 0..1 indica opcionalidad; 1 indica referencia obligatoria.

- `jornada` → `operations.Jornada`: ForeignKey; referencia obligatoria.

- `punto` → `campus.PuntoRecoleccion`: ForeignKey; referencia obligatoria.

Pregunta difícil: ¿una multiplicidad permite borrar el destino? No. Describe cantidad y opcionalidad; las políticas de borrado y las validaciones se consultan en el campo y los servicios.

## operations.Incidencia

Explicación breve: modelo de la tabla operations_incidencia; fuente gestion-residuos-dsu\backend\apps\operations\models\incidencia.py.

Explicación detallada: la caja izquierda muestra los campos del ORM. Cada flecha parte de un campo de relación y termina en el modelo destino. * representa 0..*; 0..1 indica opcionalidad; 1 indica referencia obligatoria.

- `jornada` → `operations.Jornada`: ForeignKey; referencia opcional.

- `punto` → `campus.PuntoRecoleccion`: ForeignKey; referencia obligatoria.

- `reportada_por` → `accounts.User`: ForeignKey; referencia obligatoria.

- `atendida_por` → `accounts.User`: ForeignKey; referencia opcional.

Pregunta difícil: ¿una multiplicidad permite borrar el destino? No. Describe cantidad y opcionalidad; las políticas de borrado y las validaciones se consultan en el campo y los servicios.

## operations.RegistroResiduo

Explicación breve: modelo de la tabla operations_registroresiduo; fuente gestion-residuos-dsu\backend\apps\operations\models\registro_residuo.py.

Explicación detallada: la caja izquierda muestra los campos del ORM. Cada flecha parte de un campo de relación y termina en el modelo destino. * representa 0..*; 0..1 indica opcionalidad; 1 indica referencia obligatoria.

- `jornada` → `operations.Jornada`: ForeignKey; referencia obligatoria.

- `punto` → `campus.PuntoRecoleccion`: ForeignKey; referencia obligatoria.

- `tipo_residuo` → `catalogs.TipoResiduo`: ForeignKey; referencia obligatoria.

- `unidad` → `catalogs.UnidadMedida`: ForeignKey; referencia obligatoria.

- `registrado_por` → `accounts.User`: ForeignKey; referencia obligatoria.

Pregunta difícil: ¿una multiplicidad permite borrar el destino? No. Describe cantidad y opcionalidad; las políticas de borrado y las validaciones se consultan en el campo y los servicios.

## analytics.EjecucionETL

Explicación breve: modelo de la tabla analytics_ejecucionetl; fuente gestion-residuos-dsu\backend\apps\analytics\models\ejecucion_etl.py.

Explicación detallada: la caja izquierda muestra los campos del ORM. Cada flecha parte de un campo de relación y termina en el modelo destino. * representa 0..*; 0..1 indica opcionalidad; 1 indica referencia obligatoria.

- `disparada_por` → `accounts.User`: ForeignKey; referencia opcional.

Pregunta difícil: ¿una multiplicidad permite borrar el destino? No. Describe cantidad y opcionalidad; las políticas de borrado y las validaciones se consultan en el campo y los servicios.

## analytics.HechoResiduo

Explicación breve: modelo de la tabla analytics_hechoresiduo; fuente gestion-residuos-dsu\backend\apps\analytics\models\hecho_residuo.py.

Explicación detallada: la caja izquierda muestra los campos del ORM. Cada flecha parte de un campo de relación y termina en el modelo destino. * representa 0..*; 0..1 indica opcionalidad; 1 indica referencia obligatoria.

- `registro` → `operations.RegistroResiduo`: OneToOneField; referencia obligatoria.

- `punto` → `campus.PuntoRecoleccion`: ForeignKey; referencia obligatoria.

- `sector` → `campus.Sector`: ForeignKey; referencia obligatoria.

- `tipo_residuo` → `catalogs.TipoResiduo`: ForeignKey; referencia obligatoria.

- `jornada` → `operations.Jornada`: ForeignKey; referencia obligatoria.

- `unidad` → `catalogs.UnidadMedida`: ForeignKey; referencia obligatoria.

- `periodo` → `catalogs.PeriodoAcademico`: ForeignKey; referencia opcional.

- `ejecucion` → `analytics.EjecucionETL`: ForeignKey; referencia obligatoria.

Pregunta difícil: ¿una multiplicidad permite borrar el destino? No. Describe cantidad y opcionalidad; las políticas de borrado y las validaciones se consultan en el campo y los servicios.

## analytics.RegistroDescartado

Explicación breve: modelo de la tabla analytics_registrodescartado; fuente gestion-residuos-dsu\backend\apps\analytics\models\registro_descartado.py.

Explicación detallada: la caja izquierda muestra los campos del ORM. Cada flecha parte de un campo de relación y termina en el modelo destino. * representa 0..*; 0..1 indica opcionalidad; 1 indica referencia obligatoria.

- `registro` → `operations.RegistroResiduo`: OneToOneField; referencia obligatoria.

- `ejecucion` → `analytics.EjecucionETL`: ForeignKey; referencia obligatoria.

Pregunta difícil: ¿una multiplicidad permite borrar el destino? No. Describe cantidad y opcionalidad; las políticas de borrado y las validaciones se consultan en el campo y los servicios.

## prediction.ModeloEntrenado

Explicación breve: modelo de la tabla prediction_modeloentrenado; fuente gestion-residuos-dsu\backend\apps\prediction\models\modelo_entrenado.py.

Explicación detallada: la caja izquierda muestra los campos del ORM. Cada flecha parte de un campo de relación y termina en el modelo destino. * representa 0..*; 0..1 indica opcionalidad; 1 indica referencia obligatoria.

- `entrenado_por` → `accounts.User`: ForeignKey; referencia opcional.

Pregunta difícil: ¿una multiplicidad permite borrar el destino? No. Describe cantidad y opcionalidad; las políticas de borrado y las validaciones se consultan en el campo y los servicios.

## prediction.LotePrediccion

Explicación breve: modelo de la tabla prediction_loteprediccion; fuente gestion-residuos-dsu\backend\apps\prediction\models\lote_prediccion.py.

Explicación detallada: la caja izquierda muestra los campos del ORM. Cada flecha parte de un campo de relación y termina en el modelo destino. * representa 0..*; 0..1 indica opcionalidad; 1 indica referencia obligatoria.

- `modelo` → `prediction.ModeloEntrenado`: ForeignKey; referencia obligatoria.

- `solicitado_por` → `accounts.User`: ForeignKey; referencia obligatoria.

- `sector` → `campus.Sector`: ForeignKey; referencia opcional.

- `punto` → `campus.PuntoRecoleccion`: ForeignKey; referencia opcional.

Pregunta difícil: ¿una multiplicidad permite borrar el destino? No. Describe cantidad y opcionalidad; las políticas de borrado y las validaciones se consultan en el campo y los servicios.

## prediction.Prediccion

Explicación breve: modelo de la tabla prediction_prediccion; fuente gestion-residuos-dsu\backend\apps\prediction\models\prediccion.py.

Explicación detallada: la caja izquierda muestra los campos del ORM. Cada flecha parte de un campo de relación y termina en el modelo destino. * representa 0..*; 0..1 indica opcionalidad; 1 indica referencia obligatoria.

- `lote` → `prediction.LotePrediccion`: ForeignKey; referencia obligatoria.

- `punto` → `campus.PuntoRecoleccion`: ForeignKey; referencia obligatoria.

- `sector` → `campus.Sector`: ForeignKey; referencia obligatoria.

- `tipo_residuo` → `catalogs.TipoResiduo`: ForeignKey; referencia obligatoria.

Pregunta difícil: ¿una multiplicidad permite borrar el destino? No. Describe cantidad y opcionalidad; las políticas de borrado y las validaciones se consultan en el campo y los servicios.

## prediction.Recomendacion

Explicación breve: modelo de la tabla prediction_recomendacion; fuente gestion-residuos-dsu\backend\apps\prediction\models\recomendacion.py.

Explicación detallada: la caja izquierda muestra los campos del ORM. Cada flecha parte de un campo de relación y termina en el modelo destino. * representa 0..*; 0..1 indica opcionalidad; 1 indica referencia obligatoria.

- `lote` → `prediction.LotePrediccion`: ForeignKey; referencia obligatoria.

- `punto` → `campus.PuntoRecoleccion`: ForeignKey; referencia obligatoria.

- `sector` → `campus.Sector`: ForeignKey; referencia obligatoria.

- `resuelta_por` → `accounts.User`: ForeignKey; referencia opcional.

- `jornada` → `operations.Jornada`: ForeignKey; referencia opcional.

Pregunta difícil: ¿una multiplicidad permite borrar el destino? No. Describe cantidad y opcionalidad; las políticas de borrado y las validaciones se consultan en el campo y los servicios.

## Secuencias y caja blanca

CU9 evita altas parciales de vaciados; CU15 preserva consistencia y disponibilidad de asignación; CU28 verifica horizonte, alcance, historial y modelo publicado. Elegir una guarda break/opt, ubicar sus mensajes y nodo, seguir aristas, leer la matriz y abrir la fila de datos de prueba. La base independiente no es la lista de todos los caminos posibles. Los rechazos parametrizados usan servicios y, en predicción, dobles controlados; no se presentan como respuestas HTTP observadas cuando no lo son.
