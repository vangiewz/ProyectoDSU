# Manual de usuario — Sistema de Gestión de Residuos DSU-UAGRM

Guía de uso por rol (RNF22). Cada persona ve en el menú lateral solo los módulos que su rol permite; si una opción no aparece, no corresponde a su rol.

## Ingreso

1. Abra la dirección del sistema en Chrome, Edge o Firefox (computadora, tableta o celular).
2. Escriba el usuario y la contraseña que le asignó el administrador y pulse **Ingresar al sistema**.
3. Para salir, use **Cerrar sesión** al pie del menú. La sesión también se cierra sola tras un tiempo sin uso.

El operario entra directo a **Registro en campo**; el directivo, al **Tablero**.

---

## Operario de limpieza (Operativo)

Se usa desde el celular, en el propio punto de recolección.

**Abrir la jornada.** En **Registro en campo** aparece la jornada del día que el supervisor le asignó. Pulse **Abrir jornada** al empezar el recorrido. Si dice *No tiene jornadas para hoy*, consulte al supervisor.

**Registrar un vaciado** (en cada punto del recorrido):
1. El punto actual aparece grande, con su código. Revise que sea el punto donde está.
2. En *¿Qué residuo retira?*, toque el tipo de residuo.
3. Escriba la cantidad (en la unidad que se muestra).
4. Pulse **Registrar vaciado**. El punto queda sellado como ATENDIDO y pasa al siguiente.

Otras opciones en el punto:
- **Sin residuos**: el punto estaba vacío; queda atendido sin cantidad.
- **No pude**: el punto no se pudo atender (por ejemplo, acceso bloqueado). Elija o escriba el motivo y pulse **Confirmar omisión**.
- **Incidencia**: contenedor dañado, desborde, residuos mal segregados, residuo peligroso, acceso bloqueado u otro. Elija tipo y gravedad, describa y envíe; el supervisor la ve como pendiente.

**Sin señal:** si el celular pierde conexión, el sistema avisa que el dato **no se guardó** y conserva lo escrito. Vuelva a pulsar **Registrar vaciado** cuando haya señal.

---

## Supervisor de recolección

**Planificar una jornada** (*Jornadas* → *Planificar jornada*):
1. Elija fecha, turno y sector.
2. Toque los puntos del sector **en el orden del recorrido** para armar la ruta.
3. Guarde. La jornada queda *Planificada*.
4. En la jornada, **Asignar cuadrilla y vehículos**: personal operativo, responsable y vehículos. El sistema avisa si alguien ya está asignado en ese turno.
5. **Confirmar y publicar**: la jornada se vuelve visible para la cuadrilla.

**Seguir y cerrar.** En la jornada se ve el recorrido sobre el eje horario 08:00–15:00 con el sello de cada punto en la hora en que se atendió. Al terminar, **Cerrar jornada** con observaciones; todos los puntos deben estar atendidos u omitidos. El *Consolidado* resume kilos por tipo y la cobertura.

**Incidencias.** En *Incidencias* aparecen las de sus sectores. Para resolver una, pulse **Atender**, escriba la acción adoptada y pulse **Asentar**.

**Predicción** (*Análisis → Predicción*):
1. Defina el horizonte en días (hasta el máximo configurado) y, si quiere, un sector o un punto.
2. Pulse **Generar predicción**.
3. Las cifras estimadas aparecen **a lápiz** (gris, subrayado punteado) y siempre como *≈ valor ± margen*: son una estimación de apoyo, no un dato exacto.

**Alertas y recomendaciones** (*Análisis → Alertas y recomendaciones*):
- Cada predicción genera alertas de desborde y recomendaciones (priorizar un punto, aumentar la frecuencia, redistribuir contenedores, reforzar la separación), con la evidencia que las sustenta.
- Escriba el **motivo de la decisión** y pulse **Aceptar** o **Descartar**. Al aceptar una alerta de desborde, el punto pasa al primer lugar de la siguiente jornada planificada de su sector.
- La decisión queda registrada con su nombre y fecha; no se puede cambiar después.

---

## Cuerpo directivo

- **Tablero**: indicadores del periodo (total recolectado, variación, cobertura, puntos críticos) con filtros por fecha, periodo académico, sector, punto y tipo. Toque una barra de sector o de tipo para filtrar todo el tablero; toque un punto para ver sus registros. La pestaña **Comparar periodos** contrasta dos rangos de fechas; **Power BI** muestra el informe institucional si ya fue publicado.
- **Mapa del campus**: mapa de calor o marcadores de la generación **observada**; con **Proyectada** se ve la generación estimada por el modelo.
- **Predicción**, **Alertas y recomendaciones** y **Reportes**: consulta.

---

## Administrador del sistema

- **Usuarios**: alta, edición y baja lógica (los usuarios no se borran). Cada usuario recibe uno o más roles.
- **Roles y permisos**: qué puede hacer cada rol.
- **Campus**: sectores (con su supervisor), puntos de recolección (ubicación con un clic en el mapa y capacidad en kg) y contenedores. Desactivar un punto pide el motivo; nada con historial se borra.
- **Parámetros**: umbral de punto crítico, tolerancia de capacidad, periodicidad del ETL, requisitos del modelo (registros mínimos, R² mínimo, horizonte máximo), umbrales de alertas y el enlace del informe de Power BI.
- **Modelo predictivo**:
  1. **Entrenar** con los valores propuestos (o ajustados). Corre en segundo plano y no afecta la captura en campo.
  2. La versión se publica sola si su R² alcanza el umbral; si no, se conserva la vigente.
  3. Cualquier versión aprobada puede volver a publicarse con **Publicar esta versión** (reversión).
- **Histórico de residuos**: consulte y filtre todos los registros (fechas, sector, punto, tipo); los totales por tipo se recalculan con cada filtro.
- **Procesamiento ETL**: depura los registros de campo para el análisis. Corre solo cada cierto tiempo; con **Ejecutar ahora** se lanza a pedido. Revise si alguna ejecución quedó *con alerta* (muchos registros observados).
- **Reportes**: elija el reporte, el periodo y los filtros; descargue en **Excel** o **PDF**, o **Imprimir**. Cada emisión queda en la bitácora.
- **Catálogos**: tipos de residuo, unidades de medida (con su factor de conversión) y periodos académicos con sus fechas.
- **Bitácora**: quién hizo qué y cuándo. No se puede modificar ni borrar.
- El administrador no registra vaciados, no abre ni cierra jornadas y no reporta ni atiende incidencias: eso corresponde al personal operativo y al supervisor.

---

## Mensajes frecuentes

| Mensaje | Qué hacer |
|---|---|
| *Sin conexión con el servidor… el dato no se guardó* | Revise la señal y vuelva a enviar; lo escrito se conserva. |
| *Aún no hay información analítica: ejecute el proceso ETL* | Pida al administrador ejecutar el ETL. |
| *No existe un modelo publicado vigente* | El administrador debe entrenar el modelo (requiere historial suficiente). |
| *Su rol no tiene permiso para este módulo* | La opción no corresponde a su rol; consulte al administrador. |
| *La jornada está … ; operación no permitida* | La jornada no está en el estado necesario (por ejemplo, ya fue cerrada). |
