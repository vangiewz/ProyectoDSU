# -*- coding: utf-8 -*-
"""Catalogo de los 27 requisitos funcionales del sistema.

Cada requisito de prioridad Alta incluye la definicion de su diagrama de
actividad en la clave 'pasos'; figuras.py los renderiza a PNG y cap4.py los
inserta inmediatamente despues de la tabla de detalle correspondiente.
"""

ADM = "Administrador del Sistema"
OPE = "Personal Operativo de Limpieza"
SUP = "Supervisor de Recolección"
DIR = "Cuerpo Directivo de la DSU"
APO = "Personal Administrativo de la DSU"

RF = [
    # ---------------- Modulo 1: usuarios y acceso ----------------
    dict(
        id="RF1", nombre="Gestionar Usuarios", prioridad="Esencial",
        modulo="Gestión de usuarios y control de acceso",
        resumen="Administración de las cuentas de usuario del sistema, incluyendo "
                "el registro, la consulta, la actualización y la desactivación.",
        descripcion="El sistema deberá permitir la administración de los usuarios "
                    "de la plataforma, incluyendo su registro, consulta, "
                    "actualización y desactivación, con el fin de controlar el "
                    "acceso y mantener organizada la información de las cuentas "
                    "habilitadas del personal de la DSU.",
        usuarios=ADM, iniciador=ADM,
        precondicion="El administrador debe haber iniciado sesión en el sistema "
                     "con permisos de administración.",
        proceso=[
            "1. Consultar usuarios",
            "1.1. El administrador accede al módulo de usuarios.",
            "1.2. El sistema muestra la lista de usuarios registrados.",
            "2. Registrar usuario",
            "2.1. El administrador selecciona la opción de nuevo usuario.",
            "2.2. El sistema solicita los datos personales y de cuenta.",
            "2.3. El administrador registra la información requerida.",
            "2.4. El sistema valida los datos y la unicidad del nombre de usuario.",
            "2.5. El sistema almacena la nueva cuenta con la contraseña cifrada.",
            "3. Actualizar usuario",
            "3.1. El administrador selecciona un usuario existente.",
            "3.2. El sistema muestra los datos registrados.",
            "3.3. El administrador modifica la información necesaria.",
            "3.4. El sistema actualiza los datos.",
            "4. Desactivar usuario",
            "4.1. El administrador selecciona la opción de desactivar cuenta.",
            "4.2. El sistema cambia el estado e impide nuevos accesos, "
            "conservando el historial de operaciones del usuario.",
        ],
        postcondicion="La información de los usuarios queda registrada y "
                      "actualizada en el sistema.",
        excepciones=["1. El nombre de usuario ya se encuentra registrado.",
                     "2. Existen datos obligatorios incompletos.",
                     "3. La contraseña no cumple la política de seguridad.",
                     "4. El administrador no cuenta con permisos suficientes."],
    ),
    dict(
        id="RF2", nombre="Gestionar Roles y Permisos", prioridad="Esencial",
        modulo="Gestión de usuarios y control de acceso",
        resumen="Administración de los roles del sistema, definición de permisos y "
                "asignación de niveles de acceso a los usuarios.",
        descripcion="El sistema deberá permitir la administración de roles y "
                    "permisos, definiendo los niveles de acceso a los distintos "
                    "módulos de la plataforma y asociándolos a los usuarios "
                    "correspondientes, de modo que la información operativa, "
                    "administrativa y gerencial resulte accesible únicamente al "
                    "personal autorizado.",
        usuarios=ADM, iniciador=ADM,
        precondicion="El administrador debe haber iniciado sesión y debe existir "
                     "al menos un usuario registrado.",
        proceso=[
            "1. Consultar roles",
            "1.1. El administrador accede al módulo de roles y permisos.",
            "1.2. El sistema muestra los roles existentes y sus permisos asociados.",
            "2. Registrar rol",
            "2.1. El administrador selecciona la opción de nuevo rol.",
            "2.2. El sistema solicita el nombre y la descripción del rol.",
            "2.3. El administrador define los permisos correspondientes.",
            "2.4. El sistema registra el nuevo rol.",
            "3. Asignar rol a usuario",
            "3.1. El administrador selecciona un usuario existente.",
            "3.2. El sistema muestra los roles disponibles.",
            "3.3. El administrador asigna el rol correspondiente.",
            "3.4. El sistema actualiza el nivel de acceso del usuario.",
            "4. Modificar permisos",
            "4.1. El administrador selecciona un rol existente.",
            "4.2. El sistema muestra los permisos configurados.",
            "4.3. El administrador agrega o elimina permisos.",
            "4.4. El sistema guarda la nueva configuración.",
        ],
        postcondicion="Los roles y permisos quedan definidos y correctamente "
                      "asociados a los usuarios del sistema.",
        excepciones=["1. El rol ya existe.",
                     "2. No se define ningún permiso para el rol.",
                     "3. El usuario seleccionado no existe.",
                     "4. El administrador no cuenta con permisos suficientes."],
    ),
    dict(
        id="RF3", nombre="Autenticar y Controlar el Acceso", prioridad="Esencial",
        modulo="Gestión de usuarios y control de acceso",
        resumen="Autenticación de los usuarios mediante credenciales cifradas y "
                "restricción de las funciones según el rol asignado.",
        descripcion="El sistema deberá autenticar a los usuarios mediante nombre de "
                    "usuario y contraseña, establecer una sesión con tiempo de "
                    "expiración y restringir el acceso a cada módulo según los "
                    "permisos del rol asignado, tanto en la interfaz como en los "
                    "servicios del servidor.",
        usuarios="Todos los usuarios del sistema", iniciador="Usuario del sistema",
        precondicion="El usuario debe contar con una cuenta activa registrada en "
                     "el sistema.",
        proceso=[
            "1. Iniciar sesión",
            "1.1. El usuario ingresa sus credenciales en el formulario de acceso.",
            "1.2. El sistema verifica las credenciales contra la información "
            "almacenada.",
            "1.3. El sistema establece la sesión y emite el token de acceso.",
            "1.4. El sistema presenta únicamente los módulos habilitados para el "
            "rol del usuario.",
            "2. Validar permisos",
            "2.1. El sistema verifica, ante cada operación solicitada, que el rol "
            "del usuario la tenga autorizada.",
            "2.2. El sistema rechaza y registra los intentos no autorizados.",
            "3. Cerrar sesión",
            "3.1. El usuario selecciona la opción de cerrar sesión o la sesión "
            "expira por inactividad.",
            "3.2. El sistema invalida el token y retorna al formulario de acceso.",
        ],
        postcondicion="El usuario accede únicamente a las funciones autorizadas "
                      "para su rol y la sesión queda registrada en la bitácora.",
        excepciones=["1. Las credenciales son incorrectas.",
                     "2. La cuenta se encuentra desactivada.",
                     "3. La sesión ha expirado por inactividad.",
                     "4. El usuario intenta acceder a un módulo no autorizado."],
    ),

    # ---------------- Modulo 2: topologia ----------------
    dict(
        id="RF4", nombre="Gestionar Sectores y Facultades", prioridad="Esencial",
        modulo="Gestión topológica y puntos de recolección",
        resumen="Registro, consulta, actualización y desactivación de los sectores "
                "y facultades que componen el campus atendido por la DSU.",
        descripcion="El sistema deberá permitir registrar, consultar, actualizar y "
                    "desactivar los sectores y facultades del campus, codificando "
                    "cada uno y asociándolo al supervisor responsable, con el fin "
                    "de disponer de la estructura territorial sobre la que se "
                    "agregarán los indicadores y las predicciones.",
        usuarios=ADM + ", " + SUP, iniciador=ADM,
        precondicion="El usuario autorizado debe haber iniciado sesión en el "
                     "sistema.",
        proceso=[
            "1. Registrar sector",
            "1.1. El usuario accede al módulo de sectores.",
            "1.2. El sistema solicita el código, el nombre y la descripción.",
            "1.3. El usuario registra la información requerida.",
            "1.4. El sistema valida que el código no se encuentre duplicado.",
            "1.5. El sistema almacena el sector.",
            "2. Consultar sector",
            "2.1. El usuario busca por código o nombre.",
            "2.2. El sistema muestra la información registrada y los puntos "
            "asociados.",
            "3. Actualizar sector",
            "3.1. El usuario selecciona un sector existente y modifica sus datos.",
            "3.2. El sistema valida y actualiza la información.",
            "4. Desactivar sector",
            "4.1. El usuario selecciona la opción de desactivar.",
            "4.2. El sistema cambia el estado y lo excluye de las nuevas "
            "planificaciones, conservando su historial.",
        ],
        postcondicion="La estructura de sectores queda actualizada y disponible "
                      "para el registro de puntos de recolección.",
        excepciones=["1. El código del sector ya existe.",
                     "2. Existen datos obligatorios incompletos.",
                     "3. Se intenta desactivar un sector con puntos activos "
                     "asociados.",
                     "4. El usuario no cuenta con permisos suficientes."],
    ),
    dict(
        id="RF5", nombre="Gestionar Puntos de Recolección Georreferenciados",
        prioridad="Esencial",
        modulo="Gestión topológica y puntos de recolección",
        resumen="Registro y mantenimiento de los puntos de recolección con sus "
                "coordenadas geográficas, capacidad y estado operativo.",
        descripcion="El sistema deberá permitir registrar, consultar, actualizar y "
                    "desactivar los puntos de recolección, asociando cada uno a un "
                    "sector y almacenando su latitud, longitud, descripción de "
                    "referencia, capacidad estimada y estado operativo. La "
                    "georreferenciación es indispensable para la representación "
                    "cartográfica y para el análisis espacial.",
        usuarios=ADM + ", " + SUP, iniciador=SUP,
        precondicion="Debe existir al menos un sector activo registrado en el "
                     "sistema.",
        proceso=[
            "1. Registrar punto de recolección",
            "1.1. El usuario accede al módulo de puntos de recolección.",
            "1.2. El usuario selecciona el sector al que pertenece el punto.",
            "1.3. El sistema solicita el código, la descripción de referencia, la "
            "capacidad y las coordenadas.",
            "1.4. El usuario ubica el punto sobre el mapa o ingresa la latitud y "
            "la longitud manualmente.",
            "1.5. El sistema valida el rango de las coordenadas y la unicidad del "
            "código.",
            "1.6. El sistema almacena el punto y lo muestra sobre el mapa.",
            "2. Consultar punto",
            "2.1. El usuario filtra por sector, código o estado.",
            "2.2. El sistema muestra los puntos y su ubicación.",
            "3. Actualizar punto",
            "3.1. El usuario selecciona un punto y modifica sus datos o su "
            "ubicación.",
            "3.2. El sistema valida y actualiza la información.",
            "4. Desactivar punto",
            "4.1. El usuario indica el motivo de la desactivación.",
            "4.2. El sistema excluye el punto de las nuevas jornadas y conserva "
            "su historial de registros.",
        ],
        postcondicion="Los puntos de recolección quedan registrados, "
                      "georreferenciados y disponibles para el registro de "
                      "residuos y para la representación cartográfica.",
        excepciones=["1. El código del punto ya existe.",
                     "2. Las coordenadas están fuera del rango válido o fuera del "
                     "área del campus.",
                     "3. El sector seleccionado no existe o está desactivado.",
                     "4. El usuario no cuenta con permisos suficientes."],
    ),
    dict(
        id="RF6", nombre="Gestionar Tipos de Residuo y Unidades de Medida",
        prioridad="Esencial",
        modulo="Gestión topológica y puntos de recolección",
        resumen="Administración del catálogo de tipos de residuo y de las unidades "
                "de medida empleadas para cuantificarlos.",
        descripcion="El sistema deberá permitir administrar el catálogo de tipos de "
                    "residuo, indicando su clasificación, si es aprovechable y la "
                    "unidad de medida utilizada para cuantificarlo, con el fin de "
                    "que la información capturada en campo resulte homogénea y "
                    "comparable entre sectores y periodos.",
        usuarios=ADM + ", " + APO, iniciador=ADM,
        precondicion="El usuario autorizado debe haber iniciado sesión en el "
                     "sistema.",
        proceso=[
            "1. Registrar tipo de residuo",
            "1.1. El usuario accede al módulo de catálogos.",
            "1.2. El sistema solicita el nombre, la clasificación, la condición de "
            "aprovechable y la unidad de medida.",
            "1.3. El usuario registra la información requerida.",
            "1.4. El sistema valida que el tipo no se encuentre duplicado y lo "
            "almacena.",
            "2. Gestionar unidades de medida",
            "2.1. El usuario registra o actualiza las unidades disponibles y su "
            "factor de conversión.",
            "2.2. El sistema valida la consistencia de los factores.",
            "3. Consultar y actualizar",
            "3.1. El usuario consulta el catálogo y modifica los registros "
            "necesarios.",
            "3.2. El sistema actualiza la información conservando la "
            "compatibilidad con los registros históricos.",
        ],
        postcondicion="El catálogo de tipos de residuo y unidades queda disponible "
                      "para el registro operativo y para la analítica.",
        excepciones=["1. El tipo de residuo ya existe.",
                     "2. La unidad de medida indicada no está registrada.",
                     "3. Se intenta modificar una unidad utilizada en registros "
                     "históricos sin factor de conversión.",
                     "4. El usuario no cuenta con permisos suficientes."],
    ),
    dict(
        id="RF7", nombre="Gestionar Contenedores", prioridad="Media",
        modulo="Gestión topológica y puntos de recolección",
        resumen="Registro de los contenedores instalados en cada punto de "
                "recolección, con su tipo, capacidad y estado.",
        descripcion="El sistema deberá permitir registrar los contenedores "
                    "asignados a cada punto de recolección, indicando su tipo, "
                    "capacidad nominal, fecha de instalación y estado, de modo que "
                    "sea posible evaluar si la capacidad instalada resulta "
                    "suficiente frente a la generación observada y prevista.",
        usuarios=ADM + ", " + SUP, iniciador=SUP,
        precondicion="Debe existir al menos un punto de recolección activo.",
        proceso=[
            "1. Registrar contenedor",
            "1.1. El usuario selecciona el punto de recolección.",
            "1.2. El sistema solicita el tipo, la capacidad y la fecha de "
            "instalación.",
            "1.3. El usuario registra la información y el sistema la almacena.",
            "2. Consultar contenedores",
            "2.1. El usuario consulta los contenedores por punto o por sector.",
            "2.2. El sistema muestra la capacidad instalada agregada.",
            "3. Actualizar estado",
            "3.1. El usuario registra el cambio de estado del contenedor por "
            "deterioro, reemplazo o reubicación.",
            "3.2. El sistema actualiza la información y deja constancia del "
            "cambio.",
        ],
        postcondicion="La capacidad instalada de cada punto queda registrada y "
                      "disponible para el análisis de suficiencia.",
        excepciones=["1. El punto de recolección no existe o está desactivado.",
                     "2. La capacidad ingresada no es válida.",
                     "3. El usuario no cuenta con permisos suficientes."],
    ),

    # ---------------- Modulo 3: gestion de residuos ----------------
    dict(
        id="RF8", nombre="Registrar Generación y Vaciado de Residuos",
        prioridad="Alta",
        modulo="Gestión de residuos",
        resumen="Núcleo transaccional del sistema. Registro en campo del vaciado de "
                "cada punto, capturando tipo de residuo, cantidad, fecha, hora y "
                "observaciones.",
        descripcion="El sistema deberá permitir al personal operativo registrar, "
                    "desde una interfaz responsiva utilizable en campo, el vaciado "
                    "de cada punto de recolección, capturando el punto atendido, el "
                    "tipo de residuo, la cantidad expresada en peso o volumen, la "
                    "unidad de medida, la fecha y hora de la operación y las "
                    "observaciones pertinentes. Cada registro constituye la unidad "
                    "básica de información que alimenta el repositorio histórico, "
                    "los indicadores, los mapas de calor y el modelo predictivo, "
                    "por lo que debe validarse antes de su almacenamiento.",
        usuarios=OPE + ", " + SUP, iniciador=OPE,
        precondicion="El operario debe haber iniciado sesión y debe existir una "
                     "jornada de recolección abierta con puntos asignados.",
        proceso=[
            "1. Seleccionar el punto atendido",
            "1.1. El operario accede al módulo de registro de residuos.",
            "1.2. El sistema muestra los puntos asignados a su jornada.",
            "1.3. El operario selecciona el punto que está atendiendo.",
            "2. Verificar el estado del contenedor",
            "2.1. El operario indica si el punto presenta residuos para retirar.",
            "2.2. Si no los presenta, el sistema registra la visita sin "
            "generación y finaliza el flujo.",
            "3. Capturar el detalle del residuo",
            "3.1. El operario selecciona el tipo de residuo retirado.",
            "3.2. El sistema propone la unidad de medida asociada al tipo.",
            "3.3. El operario ingresa la cantidad y, de ser necesario, agrega "
            "otros tipos de residuo a la misma visita.",
            "3.4. El operario registra las observaciones que correspondan.",
            "4. Validar y almacenar",
            "4.1. El sistema valida que la cantidad sea positiva y coherente con "
            "la capacidad del punto.",
            "4.2. El sistema registra la estampa de tiempo, el usuario y la "
            "jornada asociada.",
            "4.3. El sistema almacena el registro y confirma la operación.",
            "4.4. El sistema deja el registro disponible para el histórico, los "
            "indicadores y el modelo predictivo.",
        ],
        postcondicion="El vaciado queda registrado, vinculado al punto, al sector, "
                      "a la jornada y al operario responsable, y disponible para "
                      "el procesamiento analítico.",
        excepciones=["1. El punto seleccionado no pertenece a la jornada asignada.",
                     "2. La cantidad ingresada es negativa, nula o excede de forma "
                     "manifiesta la capacidad del punto.",
                     "3. El tipo de residuo no se encuentra registrado.",
                     "4. El dispositivo no dispone de conexión al momento del "
                     "registro.",
                     "5. Existen datos obligatorios incompletos."],
        pasos=[
            ("inicio",),
            ("accion", "El operario accede al modulo de registro de residuos"),
            ("accion", "El sistema muestra los puntos asignados a la jornada"),
            ("accion", "El operario selecciona el punto atendido"),
            ("decision", "El punto presenta residuos para retirar?",
             "No", ["El sistema registra la visita sin generacion"],
             "Si", ["El operario selecciona el tipo de residuo",
                    "El operario ingresa la cantidad y la unidad",
                    "El operario registra las observaciones"]),
            ("accion", "El sistema valida la cantidad y la coherencia del registro"),
            ("decision", "La validacion es correcta?",
             "No", ["El sistema muestra el mensaje de error", "El operario corrige los datos"],
             "Si", ["El sistema registra fecha, hora, usuario y jornada"]),
            ("accion", "El sistema almacena el registro y confirma la operacion"),
            ("fin",),
        ],
    ),
    dict(
        id="RF9", nombre="Consultar el Histórico de Residuos", prioridad="Esencial",
        modulo="Gestión de residuos",
        resumen="Consulta y filtrado de los registros históricos de generación de "
                "residuos por sector, punto, tipo y periodo.",
        descripcion="El sistema deberá permitir consultar el histórico de registros "
                    "de residuos aplicando filtros por sector, punto de "
                    "recolección, tipo de residuo, rango de fechas y usuario "
                    "responsable, y mostrar los resultados paginados junto con sus "
                    "totales agregados.",
        usuarios=SUP + ", " + APO + ", " + DIR, iniciador=SUP,
        precondicion="Deben existir registros de residuos almacenados en el "
                     "sistema.",
        proceso=[
            "1. Definir los criterios de consulta",
            "1.1. El usuario accede al módulo de consultas históricas.",
            "1.2. El usuario define el rango de fechas y los filtros deseados.",
            "2. Ejecutar la consulta",
            "2.1. El sistema recupera los registros que cumplen los criterios.",
            "2.2. El sistema muestra los resultados paginados y los totales por "
            "tipo de residuo.",
            "3. Consultar el detalle",
            "3.1. El usuario selecciona un registro específico.",
            "3.2. El sistema despliega su detalle completo, incluido el operario "
            "y la jornada asociada.",
        ],
        postcondicion="El usuario obtiene la información histórica solicitada con "
                      "sus totales agregados.",
        excepciones=["1. No existen registros que cumplan los criterios "
                     "indicados.",
                     "2. El rango de fechas es inválido.",
                     "3. El usuario no cuenta con permisos sobre el sector "
                     "consultado."],
    ),
    dict(
        id="RF10", nombre="Registrar Incidencias Operativas", prioridad="Media",
        modulo="Gestión de residuos",
        resumen="Documentación de las situaciones que afectan la ejecución normal "
                "de la recolección.",
        descripcion="El sistema deberá permitir registrar las incidencias ocurridas "
                    "durante la jornada, tales como contenedores dañados, accesos "
                    "bloqueados, residuos mal segregados, presencia de residuos "
                    "peligrosos o desbordes, indicando el punto afectado, el tipo "
                    "de incidencia, la descripción y su nivel de gravedad.",
        usuarios=OPE + ", " + SUP, iniciador=OPE,
        precondicion="El operario debe haber iniciado sesión y encontrarse dentro "
                     "de una jornada activa.",
        proceso=[
            "1. Registrar la incidencia",
            "1.1. El operario selecciona el punto afectado.",
            "1.2. El sistema solicita el tipo de incidencia, la descripción y la "
            "gravedad.",
            "1.3. El operario registra la información y el sistema la almacena.",
            "2. Notificar al supervisor",
            "2.1. El sistema marca la incidencia como pendiente de atención.",
            "2.2. El sistema la expone en el panel del supervisor del sector.",
            "3. Atender la incidencia",
            "3.1. El supervisor registra la acción adoptada.",
            "3.2. El sistema cierra la incidencia y conserva su trazabilidad.",
        ],
        postcondicion="La incidencia queda registrada, notificada al supervisor y "
                      "con su estado actualizado.",
        excepciones=["1. El punto indicado no existe.",
                     "2. Existen datos obligatorios incompletos.",
                     "3. Se intenta cerrar una incidencia ya cerrada."],
    ),

    # ---------------- Modulo 4: recolecciones ----------------
    dict(
        id="RF11", nombre="Planificar Jornadas y Rutas de Recolección",
        prioridad="Esencial",
        modulo="Gestión de recolecciones y logística",
        resumen="Definición de las jornadas de recolección y de la secuencia de "
                "puntos que serán atendidos en cada una.",
        descripcion="El sistema deberá permitir al supervisor crear jornadas de "
                    "recolección indicando la fecha, el turno y los sectores "
                    "involucrados, y definir para cada jornada la secuencia de "
                    "puntos que será atendida, tomando como insumo las "
                    "recomendaciones emitidas por el subsistema predictivo.",
        usuarios=SUP + ", " + ADM, iniciador=SUP,
        precondicion="Deben existir sectores y puntos de recolección activos "
                     "registrados en el sistema.",
        proceso=[
            "1. Crear la jornada",
            "1.1. El supervisor accede al módulo de jornadas.",
            "1.2. El sistema solicita la fecha, el turno y los sectores.",
            "1.3. El supervisor registra la información general de la jornada.",
            "2. Definir la ruta",
            "2.1. El sistema propone los puntos priorizados según las "
            "recomendaciones vigentes.",
            "2.2. El supervisor agrega, quita u ordena los puntos de la ruta.",
            "3. Confirmar la planificación",
            "3.1. El supervisor confirma la jornada.",
            "3.2. El sistema la publica y la deja visible para el personal "
            "asignado.",
        ],
        postcondicion="La jornada queda planificada, con su ruta definida y "
                      "disponible para la asignación de personal.",
        excepciones=["1. Ya existe una jornada registrada para la misma fecha, "
                     "turno y sector.",
                     "2. No se ha incluido ningún punto en la ruta.",
                     "3. Un punto incluido se encuentra desactivado.",
                     "4. El usuario no cuenta con permisos suficientes."],
    ),
    dict(
        id="RF12", nombre="Registrar la Ejecución de la Recolección",
        prioridad="Alta",
        modulo="Gestión de recolecciones y logística",
        resumen="Seguimiento de la ejecución real de cada jornada: inicio, avance "
                "punto por punto, cantidades recolectadas y cierre.",
        descripcion="El sistema deberá permitir registrar la ejecución efectiva de "
                    "una jornada de recolección, controlando su apertura, el avance "
                    "punto por punto, la consolidación de las cantidades "
                    "recolectadas, el registro de las incidencias ocurridas y el "
                    "cierre con el resumen correspondiente. La ejecución debe "
                    "contrastarse con la planificación, de modo que el sistema "
                    "evidencie los puntos planificados que no fueron atendidos y "
                    "el motivo.",
        usuarios=OPE + ", " + SUP, iniciador=SUP,
        precondicion="Debe existir una jornada planificada y confirmada, con "
                     "personal asignado.",
        proceso=[
            "1. Abrir la jornada",
            "1.1. El supervisor o el operario responsable abre la jornada "
            "planificada.",
            "1.2. El sistema registra la hora de inicio y habilita la captura en "
            "campo.",
            "2. Ejecutar el recorrido",
            "2.1. El sistema presenta el siguiente punto de la ruta.",
            "2.2. El operario registra el vaciado o indica el motivo por el cual "
            "el punto no pudo ser atendido.",
            "2.3. El sistema actualiza el avance de la jornada.",
            "2.4. El proceso se repite hasta agotar los puntos de la ruta.",
            "3. Consolidar la jornada",
            "3.1. El sistema totaliza las cantidades recolectadas por tipo de "
            "residuo y por sector.",
            "3.2. El sistema contrasta los puntos ejecutados frente a los "
            "planificados.",
            "4. Cerrar la jornada",
            "4.1. El supervisor revisa el resumen y registra las observaciones "
            "finales.",
            "4.2. El sistema cierra la jornada, registra la hora de finalización "
            "e impide nuevas modificaciones.",
        ],
        postcondicion="La jornada queda cerrada con su resumen consolidado, sus "
                      "desviaciones respecto de la planificación y sus registros "
                      "disponibles para el análisis.",
        excepciones=["1. La jornada ya se encuentra cerrada.",
                     "2. Existen puntos de la ruta sin registro ni motivo de "
                     "omisión.",
                     "3. El usuario no forma parte del personal asignado a la "
                     "jornada.",
                     "4. Se intenta abrir una jornada cuya fecha no corresponde."],
        pasos=[
            ("inicio",),
            ("accion", "El supervisor abre la jornada planificada"),
            ("accion", "El sistema registra la hora de inicio y habilita la captura"),
            ("accion", "El sistema presenta el siguiente punto de la ruta"),
            ("decision", "El punto pudo ser atendido?",
             "No", ["El operario registra el motivo de la omision"],
             "Si", ["El operario registra el vaciado del punto",
                    "El sistema actualiza el avance de la jornada"]),
            ("decision", "Quedan puntos pendientes en la ruta?",
             "Si", ["El sistema avanza al siguiente punto"],
             "No", ["El sistema totaliza las cantidades recolectadas",
                    "El sistema contrasta lo ejecutado con lo planificado"]),
            ("accion", "El supervisor revisa el resumen y registra observaciones"),
            ("accion", "El sistema cierra la jornada y registra la hora de fin"),
            ("fin",),
        ],
    ),
    dict(
        id="RF13", nombre="Asignar Personal y Vehículos a las Jornadas",
        prioridad="Media",
        modulo="Gestión de recolecciones y logística",
        resumen="Asignación del personal operativo y de los vehículos responsables "
                "de cada jornada de recolección.",
        descripcion="El sistema deberá permitir asignar a cada jornada el personal "
                    "operativo y los vehículos que la ejecutarán, verificando que "
                    "no exista superposición de asignaciones para el mismo turno y "
                    "dejando constancia del responsable de la jornada.",
        usuarios=SUP + ", " + ADM, iniciador=SUP,
        precondicion="Debe existir una jornada planificada y personal registrado "
                     "en el sistema.",
        proceso=[
            "1. Seleccionar la jornada",
            "1.1. El supervisor accede a la jornada planificada.",
            "2. Asignar recursos",
            "2.1. El sistema muestra el personal y los vehículos disponibles para "
            "el turno.",
            "2.2. El supervisor selecciona los recursos y designa al responsable.",
            "2.3. El sistema valida que no exista superposición de asignaciones.",
            "3. Confirmar la asignación",
            "3.1. El sistema registra la asignación y notifica al personal "
            "designado.",
        ],
        postcondicion="La jornada queda con su personal y sus vehículos asignados "
                      "y notificados.",
        excepciones=["1. El personal seleccionado ya está asignado a otra jornada "
                     "en el mismo turno.",
                     "2. No se designa un responsable de jornada.",
                     "3. El vehículo seleccionado se encuentra fuera de servicio."],
    ),
    dict(
        id="RF14", nombre="Consultar el Historial de Recolecciones",
        prioridad="Esencial",
        modulo="Gestión de recolecciones y logística",
        resumen="Consulta del historial de jornadas ejecutadas con filtros por "
                "sector, fecha, responsable y estado.",
        descripcion="El sistema deberá permitir consultar el historial de jornadas "
                    "de recolección, filtrando por sector, rango de fechas, "
                    "responsable y estado, y mostrar para cada jornada su "
                    "cobertura, las cantidades recolectadas y las incidencias "
                    "registradas.",
        usuarios=SUP + ", " + APO + ", " + DIR, iniciador=SUP,
        precondicion="Deben existir jornadas registradas en el sistema.",
        proceso=[
            "1. Definir los criterios",
            "1.1. El usuario accede al historial de recolecciones.",
            "1.2. El usuario aplica los filtros deseados.",
            "2. Consultar los resultados",
            "2.1. El sistema muestra las jornadas que cumplen los criterios.",
            "2.2. El sistema presenta para cada una su porcentaje de cobertura y "
            "sus totales.",
            "3. Consultar el detalle",
            "3.1. El usuario selecciona una jornada.",
            "3.2. El sistema despliega el recorrido efectuado, los registros "
            "capturados y las incidencias.",
        ],
        postcondicion="El usuario obtiene el historial de recolecciones "
                      "solicitado.",
        excepciones=["1. No existen jornadas que cumplan los criterios.",
                     "2. El rango de fechas es inválido.",
                     "3. El usuario no cuenta con permisos sobre el sector "
                     "consultado."],
    ),

    # ---------------- Modulo 5: inteligencia de negocios ----------------
    dict(
        id="RF15", nombre="Ejecutar los Procesos de Extracción, Transformación y "
                          "Carga", prioridad="Alta",
        modulo="Inteligencia de Negocios y analítica visual",
        resumen="Consolidación, depuración y enriquecimiento de la información "
                "transaccional para su consumo analítico y predictivo.",
        descripcion="El sistema deberá ejecutar, de forma programada o bajo "
                    "demanda, un proceso de extracción, transformación y carga que "
                    "consolide la información transaccional de residuos y "
                    "recolecciones, elimine duplicados, corrija formatos, "
                    "estandarice las unidades de medida, detecte valores atípicos y "
                    "derive las variables temporales requeridas por el componente "
                    "analítico y por el modelo predictivo. El proceso debe generar "
                    "una bitácora con el número de registros procesados, aceptados "
                    "y observados.",
        usuarios=ADM + ", " + APO, iniciador=ADM,
        precondicion="Deben existir registros transaccionales de residuos y "
                     "recolecciones almacenados en la base de datos.",
        proceso=[
            "1. Extraer la información",
            "1.1. El proceso se dispara de forma programada o el administrador lo "
            "ejecuta manualmente.",
            "1.2. El sistema extrae los registros de residuos, recolecciones, "
            "sectores, puntos, tipos de residuo e incidencias.",
            "2. Transformar la información",
            "2.1. El sistema elimina los registros duplicados.",
            "2.2. El sistema identifica los valores faltantes y corrige los "
            "formatos.",
            "2.3. El sistema estandariza las unidades de medida mediante los "
            "factores de conversión registrados.",
            "2.4. El sistema deriva el día de la semana, el mes, la semana del "
            "año y el periodo académico de cada registro.",
            "2.5. El sistema marca los valores atípicos para su revisión.",
            "3. Cargar la información",
            "3.1. El sistema carga la información depurada en las estructuras "
            "analíticas.",
            "3.2. El sistema deja los datos disponibles para los indicadores, el "
            "componente cartográfico y el modelo predictivo.",
            "4. Registrar el resultado",
            "4.1. El sistema genera la bitácora del proceso con la fecha, la "
            "duración y el conteo de registros procesados, aceptados y observados.",
        ],
        postcondicion="La información analítica queda actualizada, depurada y "
                      "enriquecida con las variables temporales derivadas.",
        excepciones=["1. No existen registros nuevos desde la última ejecución.",
                     "2. Se detectan registros con unidades de medida sin factor "
                     "de conversión definido.",
                     "3. La proporción de registros observados supera el umbral "
                     "configurado.",
                     "4. Se produce un fallo de conexión con la base de datos "
                     "durante la ejecución."],
        pasos=[
            ("inicio",),
            ("accion", "El proceso se dispara de forma programada o manual"),
            ("accion", "El sistema extrae los registros transaccionales del periodo"),
            ("decision", "Existen registros nuevos por procesar?",
             "No", ["El sistema finaliza y registra la ejecucion sin cambios"],
             "Si", ["El sistema elimina duplicados y corrige formatos",
                    "El sistema estandariza las unidades de medida",
                    "El sistema deriva las variables temporales"]),
            ("accion", "El sistema marca los valores atipicos detectados"),
            ("decision", "Los registros observados superan el umbral?",
             "Si", ["El sistema notifica al administrador", "El sistema suspende la carga"],
             "No", ["El sistema carga los datos en las estructuras analiticas"]),
            ("accion", "El sistema genera la bitacora del proceso"),
            ("fin",),
        ],
    ),
    dict(
        id="RF16", nombre="Calcular los Indicadores Clave de Rendimiento",
        prioridad="Alta",
        modulo="Inteligencia de Negocios y analítica visual",
        resumen="Cálculo de los indicadores que describen el comportamiento "
                "histórico de la generación y la eficiencia de la recolección.",
        descripcion="El sistema deberá calcular, a partir de la información "
                    "depurada, el conjunto de indicadores clave de rendimiento que "
                    "describen la gestión de residuos: total recolectado, "
                    "generación promedio por punto y por sector, sector de mayor "
                    "generación, tipo de residuo predominante, número de "
                    "recolecciones realizadas, frecuencia promedio de recolección, "
                    "porcentaje de cobertura de las jornadas, variación respecto "
                    "del periodo anterior y cantidad de puntos considerados "
                    "críticos. El cálculo debe ejecutarse sobre el periodo y los "
                    "filtros que el usuario seleccione.",
        usuarios=DIR + ", " + SUP + ", " + APO, iniciador=DIR,
        precondicion="El proceso de extracción, transformación y carga debe "
                     "haberse ejecutado correctamente al menos una vez.",
        proceso=[
            "1. Seleccionar el alcance del análisis",
            "1.1. El usuario accede al módulo analítico.",
            "1.2. El usuario define el periodo y los filtros por sector, punto y "
            "tipo de residuo.",
            "2. Calcular los indicadores",
            "2.1. El sistema recupera la información analítica del periodo "
            "seleccionado.",
            "2.2. El sistema calcula los totales, los promedios y las "
            "frecuencias.",
            "2.3. El sistema compara los resultados con el periodo inmediatamente "
            "anterior y determina la variación.",
            "2.4. El sistema identifica los puntos cuyo nivel de generación supera "
            "el umbral configurado y los clasifica como críticos.",
            "3. Presentar los resultados",
            "3.1. El sistema muestra los indicadores calculados.",
            "3.2. El usuario puede profundizar en cualquiera de ellos hasta el "
            "nivel del registro individual.",
        ],
        postcondicion="Los indicadores quedan calculados y disponibles para su "
                      "visualización en los tableros y para su exportación.",
        excepciones=["1. No existe información analítica para el periodo "
                     "seleccionado.",
                     "2. El periodo anterior no dispone de datos suficientes para "
                     "calcular la variación.",
                     "3. El rango de fechas es inválido.",
                     "4. El usuario no cuenta con permisos sobre los sectores "
                     "seleccionados."],
        pasos=[
            ("inicio",),
            ("accion", "El usuario define el periodo y los filtros de analisis"),
            ("accion", "El sistema recupera la informacion analitica del periodo"),
            ("decision", "Existe informacion para el periodo?",
             "No", ["El sistema informa que no hay datos disponibles"],
             "Si", ["El sistema calcula totales, promedios y frecuencias",
                    "El sistema compara con el periodo anterior",
                    "El sistema identifica los puntos criticos"]),
            ("accion", "El sistema presenta los indicadores calculados"),
            ("accion", "El usuario profundiza en el indicador seleccionado"),
            ("fin",),
        ],
    ),
    dict(
        id="RF17", nombre="Visualizar los Tableros Interactivos",
        prioridad="Esencial",
        modulo="Inteligencia de Negocios y analítica visual",
        resumen="Presentación de los indicadores mediante tableros interactivos con "
                "filtros dinámicos.",
        descripcion="El sistema deberá presentar los indicadores y las series "
                    "históricas mediante tableros interactivos que permitan "
                    "aplicar filtros por fecha, sector, punto de recolección, tipo "
                    "de residuo y periodo académico, y que actualicen todas las "
                    "visualizaciones de forma coherente ante cada cambio de filtro.",
        usuarios=DIR + ", " + SUP + ", " + APO, iniciador=DIR,
        precondicion="Los indicadores deben haber sido calculados previamente.",
        proceso=[
            "1. Acceder al tablero",
            "1.1. El usuario accede al módulo de tableros.",
            "1.2. El sistema presenta las visualizaciones con los filtros por "
            "defecto.",
            "2. Explorar la información",
            "2.1. El usuario modifica los filtros disponibles.",
            "2.2. El sistema actualiza de forma coherente todas las "
            "visualizaciones del tablero.",
            "3. Consultar el detalle",
            "3.1. El usuario selecciona un elemento de una visualización.",
            "3.2. El sistema despliega el detalle asociado.",
        ],
        postcondicion="El usuario visualiza e interpreta el comportamiento "
                      "histórico de los residuos según los criterios "
                      "seleccionados.",
        excepciones=["1. No existen datos para la combinación de filtros "
                     "seleccionada.",
                     "2. El servicio de visualización no se encuentra disponible.",
                     "3. El usuario no cuenta con permisos suficientes."],
    ),
    dict(
        id="RF18", nombre="Comparar Periodos e Identificar Tendencias",
        prioridad="Media",
        modulo="Inteligencia de Negocios y analítica visual",
        resumen="Comparación de la generación entre periodos y detección de "
                "tendencias crecientes o decrecientes por sector y punto.",
        descripcion="El sistema deberá permitir comparar la generación de residuos "
                    "entre dos periodos seleccionados por el usuario, calcular la "
                    "variación absoluta y porcentual por sector, punto y tipo de "
                    "residuo, y señalar aquellos elementos que presentan una "
                    "tendencia sostenida de crecimiento a lo largo de los periodos "
                    "analizados.",
        usuarios=DIR + ", " + APO, iniciador=DIR,
        precondicion="Debe existir información analítica correspondiente a ambos "
                     "periodos de comparación.",
        proceso=[
            "1. Definir los periodos",
            "1.1. El usuario selecciona el periodo base y el periodo de "
            "comparación.",
            "2. Calcular las variaciones",
            "2.1. El sistema calcula la variación absoluta y porcentual por "
            "sector, punto y tipo de residuo.",
            "2.2. El sistema evalúa la tendencia sobre la serie histórica "
            "disponible.",
            "3. Presentar el resultado",
            "3.1. El sistema muestra la comparación y destaca los elementos con "
            "tendencia creciente sostenida.",
        ],
        postcondicion="El usuario obtiene la comparación entre periodos y la "
                      "identificación de las tendencias observadas.",
        excepciones=["1. Alguno de los periodos carece de datos suficientes.",
                     "2. Los periodos seleccionados se superponen.",
                     "3. El rango de fechas es inválido."],
    ),

    # ---------------- Modulo 6: GIS ----------------
    dict(
        id="RF19", nombre="Visualizar los Puntos de Recolección en el Mapa "
                          "Interactivo", prioridad="Esencial",
        modulo="Componente cartográfico y análisis espacial",
        resumen="Representación de los puntos de recolección sobre un mapa "
                "interactivo del campus mediante marcadores.",
        descripcion="El sistema deberá representar sobre un mapa interactivo del "
                    "campus todos los puntos de recolección activos, utilizando "
                    "marcadores posicionados según su latitud y longitud y "
                    "diferenciados según su nivel de generación, y deberá permitir "
                    "consultar la información detallada de cada punto al "
                    "seleccionarlo.",
        usuarios=DIR + ", " + SUP + ", " + APO, iniciador=SUP,
        precondicion="Deben existir puntos de recolección registrados con "
                     "coordenadas válidas.",
        proceso=[
            "1. Cargar el mapa",
            "1.1. El usuario accede al módulo cartográfico.",
            "1.2. El sistema carga la cartografía base y posiciona los marcadores "
            "de los puntos activos.",
            "2. Consultar un punto",
            "2.1. El usuario selecciona un marcador.",
            "2.2. El sistema muestra el código del punto, su sector, su capacidad, "
            "su generación acumulada y la fecha de su última atención.",
            "3. Navegar el mapa",
            "3.1. El usuario desplaza y amplía la vista del campus.",
            "3.2. El sistema mantiene la coherencia de los marcadores en cada "
            "nivel de acercamiento.",
        ],
        postcondicion="El usuario visualiza la distribución geográfica de los "
                      "puntos de recolección del campus.",
        excepciones=["1. No existen puntos con coordenadas válidas registradas.",
                     "2. El servicio de cartografía base no se encuentra "
                     "disponible.",
                     "3. Un punto presenta coordenadas fuera del área del campus."],
    ),
    dict(
        id="RF20", nombre="Generar el Mapa de Calor de Zonas Críticas",
        prioridad="Alta",
        modulo="Componente cartográfico y análisis espacial",
        resumen="Representación mediante intensidad visual de las zonas del campus "
                "con mayor concentración de generación de residuos.",
        descripcion="El sistema deberá generar dinámicamente un mapa de calor sobre "
                    "la cartografía del campus, ponderando cada punto de "
                    "recolección según la cantidad de residuos generada en el "
                    "periodo seleccionado, de modo que las zonas de mayor "
                    "concentración resulten identificables de forma inmediata. El "
                    "mapa debe poder alternar entre la generación histórica "
                    "observada y la generación proyectada por el modelo "
                    "predictivo, y debe recalcularse ante cualquier cambio en los "
                    "filtros de periodo, sector o tipo de residuo.",
        usuarios=DIR + ", " + SUP, iniciador=DIR,
        precondicion="Deben existir registros de residuos asociados a puntos "
                     "georreferenciados dentro del periodo seleccionado.",
        proceso=[
            "1. Definir el alcance del mapa",
            "1.1. El usuario accede al módulo cartográfico y activa la capa de "
            "calor.",
            "1.2. El usuario selecciona el periodo, el sector y el tipo de "
            "residuo.",
            "1.3. El usuario indica si desea visualizar la generación observada o "
            "la proyectada.",
            "2. Calcular las ponderaciones",
            "2.1. El sistema recupera las cantidades correspondientes a cada punto "
            "dentro del alcance definido.",
            "2.2. El sistema normaliza las cantidades y asigna a cada punto su "
            "peso relativo.",
            "3. Renderizar la capa de calor",
            "3.1. El sistema genera el gradiente de intensidad sobre la "
            "cartografía.",
            "3.2. El sistema presenta la leyenda con la escala de valores "
            "utilizada.",
            "4. Identificar las zonas críticas",
            "4.1. El sistema resalta los puntos cuyo peso relativo supera el "
            "umbral configurado.",
            "4.2. El usuario consulta el detalle de cada zona crítica "
            "identificada.",
        ],
        postcondicion="El mapa de calor queda renderizado y las zonas críticas del "
                      "campus resultan identificables visualmente.",
        excepciones=["1. No existen registros para el periodo y los filtros "
                     "seleccionados.",
                     "2. Los puntos involucrados carecen de coordenadas válidas.",
                     "3. Se solicita la capa proyectada sin que existan "
                     "predicciones vigentes.",
                     "4. El servicio de cartografía base no se encuentra "
                     "disponible."],
        pasos=[
            ("inicio",),
            ("accion", "El usuario activa la capa de calor sobre el mapa"),
            ("accion", "El usuario selecciona periodo, sector y tipo de residuo"),
            ("decision", "Que capa se desea visualizar?",
             "Observada", ["El sistema recupera las cantidades historicas"],
             "Proyectada", ["El sistema recupera las predicciones vigentes"]),
            ("decision", "Existen datos para el alcance definido?",
             "No", ["El sistema informa que no hay datos disponibles"],
             "Si", ["El sistema normaliza las cantidades por punto",
                    "El sistema asigna el peso relativo a cada punto"]),
            ("accion", "El sistema renderiza el gradiente de intensidad"),
            ("accion", "El sistema resalta los puntos que superan el umbral critico"),
            ("fin",),
        ],
    ),
    dict(
        id="RF21", nombre="Filtrar el Mapa por Periodo, Sector y Tipo de Residuo",
        prioridad="Media",
        modulo="Componente cartográfico y análisis espacial",
        resumen="Aplicación de filtros dinámicos sobre la representación "
                "cartográfica.",
        descripcion="El sistema deberá permitir aplicar filtros por rango de "
                    "fechas, periodo académico, sector, punto de recolección y tipo "
                    "de residuo sobre la representación cartográfica, y actualizar "
                    "de forma coherente tanto los marcadores como la capa de calor "
                    "ante cada cambio.",
        usuarios=DIR + ", " + SUP + ", " + APO, iniciador=SUP,
        precondicion="El mapa interactivo debe encontrarse cargado.",
        proceso=[
            "1. Aplicar los filtros",
            "1.1. El usuario modifica uno o varios de los filtros disponibles.",
            "2. Recalcular la vista",
            "2.1. El sistema recupera la información correspondiente al nuevo "
            "alcance.",
            "2.2. El sistema actualiza los marcadores y recalcula la capa de "
            "calor.",
            "3. Restablecer",
            "3.1. El usuario puede restablecer los filtros a sus valores por "
            "defecto.",
        ],
        postcondicion="La representación cartográfica refleja exclusivamente la "
                      "información correspondiente a los filtros aplicados.",
        excepciones=["1. La combinación de filtros no arroja resultados.",
                     "2. El rango de fechas es inválido.",
                     "3. El sector seleccionado no posee puntos "
                     "georreferenciados."],
    ),

    # ---------------- Modulo 7: machine learning ----------------
    dict(
        id="RF22", nombre="Entrenar y Evaluar el Modelo Random Forest Regressor",
        prioridad="Alta",
        modulo="Predicción mediante Random Forest Regressor",
        resumen="Preparación del conjunto de datos, entrenamiento del modelo "
                "predictivo y evaluación de su desempeño mediante métricas de "
                "error.",
        descripcion="El sistema deberá permitir entrenar el modelo Random Forest "
                    "Regressor sobre el repositorio histórico depurado, utilizando "
                    "como variables predictoras el sector, el punto de recolección, "
                    "el tipo de residuo, la cantidad histórica acumulada, la "
                    "frecuencia de recolección y las variables temporales "
                    "derivadas, y como variable objetivo la cantidad generada. La "
                    "partición entre entrenamiento y prueba deberá respetar el "
                    "orden cronológico de los datos. El modelo solo podrá "
                    "publicarse cuando sus métricas de evaluación superen el umbral "
                    "de desempeño configurado.",
        usuarios=ADM + ", " + APO, iniciador=ADM,
        precondicion="Debe existir un volumen mínimo de registros históricos "
                     "depurados, definido en los parámetros del sistema.",
        proceso=[
            "1. Preparar el conjunto de datos",
            "1.1. El administrador accede al módulo de modelado predictivo.",
            "1.2. El sistema recupera la información analítica depurada.",
            "1.3. El sistema construye la matriz de variables predictoras y el "
            "vector objetivo.",
            "1.4. El sistema codifica las variables categóricas.",
            "2. Dividir el conjunto",
            "2.1. El sistema separa los datos en entrenamiento y prueba "
            "respetando el orden cronológico.",
            "3. Entrenar el modelo",
            "3.1. El administrador define o acepta los hiperparámetros propuestos, "
            "entre ellos el número de árboles y la profundidad máxima.",
            "3.2. El sistema entrena el modelo Random Forest Regressor sobre el "
            "conjunto de entrenamiento.",
            "4. Evaluar el desempeño",
            "4.1. El sistema genera las predicciones sobre el conjunto de prueba.",
            "4.2. El sistema calcula el error absoluto medio, el error cuadrático "
            "medio, su raíz y el coeficiente de determinación.",
            "4.3. El sistema calcula la importancia relativa de cada variable.",
            "5. Publicar el modelo",
            "5.1. El sistema compara las métricas con el umbral configurado.",
            "5.2. Si el desempeño es aceptable, el sistema versiona y publica el "
            "modelo; en caso contrario, conserva la versión anterior.",
            "5.3. El sistema registra la ejecución con sus parámetros, métricas y "
            "fecha.",
        ],
        postcondicion="El modelo queda entrenado, evaluado, versionado y "
                      "disponible para la generación de predicciones, con su "
                      "registro de métricas almacenado.",
        excepciones=["1. El volumen de registros disponibles es insuficiente para "
                     "el entrenamiento.",
                     "2. Las métricas obtenidas no alcanzan el umbral de "
                     "desempeño configurado.",
                     "3. El conjunto de datos presenta variables constantes o "
                     "íntegramente nulas.",
                     "4. Se produce un error durante la ejecución del "
                     "entrenamiento.",
                     "5. El usuario no cuenta con permisos suficientes."],
        pasos=[
            ("inicio",),
            ("accion", "El administrador solicita el entrenamiento del modelo"),
            ("accion", "El sistema recupera la informacion analitica depurada"),
            ("decision", "El volumen de registros es suficiente?",
             "No", ["El sistema informa que no hay datos suficientes"],
             "Si", ["El sistema construye las variables predictoras y el objetivo",
                    "El sistema codifica las variables categoricas",
                    "El sistema divide los datos respetando el orden cronologico"]),
            ("accion", "El sistema entrena el modelo Random Forest Regressor"),
            ("accion", "El sistema calcula MAE, MSE, RMSE y R2 sobre el conjunto de prueba"),
            ("decision", "Las metricas superan el umbral configurado?",
             "No", ["El sistema conserva la version anterior del modelo"],
             "Si", ["El sistema versiona y publica el nuevo modelo"]),
            ("accion", "El sistema registra la ejecucion con sus parametros y metricas"),
            ("fin",),
        ],
    ),
    dict(
        id="RF23", nombre="Predecir la Generación Futura de Residuos",
        prioridad="Alta",
        modulo="Predicción mediante Random Forest Regressor",
        resumen="Generación de las estimaciones de generación futura por punto y "
                "por sector para el horizonte solicitado.",
        descripcion="El sistema deberá generar, a partir del modelo publicado, la "
                    "estimación de la cantidad de residuos que se generará en cada "
                    "punto de recolección y en cada sector durante el horizonte "
                    "temporal solicitado. Cada predicción deberá almacenarse junto "
                    "con la versión del modelo que la produjo, la fecha de "
                    "ejecución y el margen de error asociado, y deberá presentarse "
                    "siempre acompañada de dicho margen, nunca como un valor "
                    "exacto.",
        usuarios=DIR + ", " + SUP + ", " + ADM, iniciador=SUP,
        precondicion="Debe existir un modelo entrenado, evaluado y publicado en el "
                     "sistema.",
        proceso=[
            "1. Solicitar la predicción",
            "1.1. El usuario accede al módulo predictivo.",
            "1.2. El usuario define el horizonte temporal y el alcance por sector "
            "o por punto.",
            "2. Construir las variables de entrada",
            "2.1. El sistema recupera el estado histórico de cada punto incluido "
            "en el alcance.",
            "2.2. El sistema genera las variables temporales correspondientes a "
            "las fechas futuras solicitadas.",
            "3. Ejecutar la inferencia",
            "3.1. El sistema aplica el modelo publicado sobre las variables "
            "construidas.",
            "3.2. El sistema obtiene la cantidad estimada para cada punto y "
            "fecha.",
            "4. Consolidar y almacenar",
            "4.1. El sistema agrega las estimaciones por sector y por tipo de "
            "residuo.",
            "4.2. El sistema almacena las predicciones junto con la versión del "
            "modelo y el margen de error.",
            "4.3. El sistema deja los resultados disponibles para el mapa de "
            "calor proyectado y para el subsistema de recomendaciones.",
        ],
        postcondicion="Las predicciones quedan generadas, almacenadas y "
                      "disponibles para su visualización y para la emisión de "
                      "recomendaciones.",
        excepciones=["1. No existe un modelo publicado vigente.",
                     "2. El horizonte solicitado excede el máximo configurado.",
                     "3. Un punto incluido en el alcance carece de historial "
                     "suficiente.",
                     "4. Se produce un error durante la ejecución de la "
                     "inferencia."],
        pasos=[
            ("inicio",),
            ("accion", "El usuario define el horizonte temporal y el alcance"),
            ("decision", "Existe un modelo publicado vigente?",
             "No", ["El sistema informa que debe entrenarse el modelo"],
             "Si", ["El sistema recupera el estado historico de cada punto",
                    "El sistema genera las variables temporales futuras"]),
            ("accion", "El sistema aplica el modelo sobre las variables construidas"),
            ("accion", "El sistema obtiene la cantidad estimada por punto y fecha"),
            ("accion", "El sistema agrega las estimaciones por sector y tipo de residuo"),
            ("accion", "El sistema almacena las predicciones con su margen de error"),
            ("fin",),
        ],
    ),
    dict(
        id="RF24", nombre="Generar Alertas y Recomendaciones Logísticas",
        prioridad="Alta",
        modulo="Predicción mediante Random Forest Regressor",
        resumen="Traducción de las predicciones y los indicadores en alertas "
                "tempranas y en recomendaciones concretas de planificación.",
        descripcion="El sistema deberá interpretar las predicciones del modelo y "
                    "los indicadores calculados para emitir alertas tempranas sobre "
                    "los puntos con riesgo de desborde y recomendaciones concretas "
                    "sobre la priorización de puntos, el incremento de la "
                    "frecuencia de recolección, la redistribución o incorporación "
                    "de contenedores y el refuerzo de la separación en origen. Cada "
                    "recomendación deberá presentarse acompañada de la evidencia "
                    "que la sustenta y deberá poder ser aceptada o descartada por "
                    "el supervisor, dejando constancia de la decisión.",
        usuarios=DIR + ", " + SUP, iniciador="El sistema",
        precondicion="Deben existir predicciones vigentes e indicadores calculados "
                     "para el periodo de análisis.",
        proceso=[
            "1. Evaluar las condiciones",
            "1.1. El sistema recupera las predicciones vigentes y los indicadores "
            "del periodo.",
            "1.2. El sistema evalúa, para cada punto, la generación histórica, la "
            "tendencia observada, la capacidad instalada y la cantidad proyectada.",
            "2. Emitir las alertas",
            "2.1. El sistema identifica los puntos cuya cantidad proyectada supera "
            "su capacidad instalada antes de la siguiente atención prevista.",
            "2.2. El sistema genera la alerta temprana correspondiente y la "
            "clasifica según su nivel de urgencia.",
            "3. Formular las recomendaciones",
            "3.1. El sistema determina la acción sugerida según el patrón "
            "detectado: priorización, incremento de frecuencia, redistribución de "
            "contenedores o refuerzo de la separación en origen.",
            "3.2. El sistema adjunta a cada recomendación la evidencia histórica y "
            "predictiva que la sustenta.",
            "4. Resolver la recomendación",
            "4.1. El sistema presenta las alertas y recomendaciones al supervisor "
            "y al cuerpo directivo.",
            "4.2. El supervisor acepta o descarta cada recomendación e indica el "
            "motivo.",
            "4.3. El sistema incorpora las recomendaciones aceptadas a la "
            "planificación de la siguiente jornada y registra la decisión adoptada.",
        ],
        postcondicion="Las alertas y recomendaciones quedan emitidas, resueltas "
                      "por el supervisor y, cuando corresponde, incorporadas a la "
                      "planificación.",
        excepciones=["1. No existen predicciones vigentes para el periodo.",
                     "2. Los puntos involucrados carecen de capacidad instalada "
                     "registrada.",
                     "3. La recomendación ya fue resuelta previamente.",
                     "4. El supervisor no cuenta con permisos sobre el sector "
                     "afectado."],
        pasos=[
            ("inicio",),
            ("accion", "El sistema recupera las predicciones vigentes y los indicadores"),
            ("accion", "El sistema evalua tendencia, capacidad y cantidad proyectada"),
            ("decision", "La cantidad proyectada supera la capacidad instalada?",
             "No", ["El sistema mantiene la frecuencia planificada"],
             "Si", ["El sistema emite la alerta temprana",
                    "El sistema clasifica el nivel de urgencia"]),
            ("accion", "El sistema formula la recomendacion y adjunta su evidencia"),
            ("accion", "El sistema presenta la recomendacion al supervisor"),
            ("decision", "El supervisor acepta la recomendacion?",
             "No", ["El supervisor registra el motivo del descarte"],
             "Si", ["El sistema la incorpora a la siguiente jornada"]),
            ("accion", "El sistema registra la decision adoptada"),
            ("fin",),
        ],
    ),

    # ---------------- Modulo 8: administracion ----------------
    dict(
        id="RF25", nombre="Administrar Catálogos y Parámetros del Modelo",
        prioridad="Media",
        modulo="Administración de plataforma y auditoría",
        resumen="Configuración de los catálogos maestros y de los parámetros que "
                "gobiernan el comportamiento analítico y predictivo.",
        descripcion="El sistema deberá permitir al administrador mantener los "
                    "catálogos maestros y configurar los parámetros globales que "
                    "gobiernan el comportamiento del sistema, entre ellos el umbral "
                    "de punto crítico, el volumen mínimo de registros para el "
                    "entrenamiento, el umbral de desempeño aceptable del modelo, el "
                    "horizonte máximo de predicción, la periodicidad del proceso de "
                    "extracción, transformación y carga y la definición de los "
                    "periodos académicos, sin necesidad de intervenir el código "
                    "fuente.",
        usuarios=ADM, iniciador=ADM,
        precondicion="El administrador debe haber iniciado sesión con permisos de "
                     "administración.",
        proceso=[
            "1. Consultar la configuración",
            "1.1. El administrador accede al módulo de administración.",
            "1.2. El sistema muestra los parámetros vigentes y su valor actual.",
            "2. Modificar un parámetro",
            "2.1. El administrador selecciona el parámetro y registra el nuevo "
            "valor.",
            "2.2. El sistema valida que el valor se encuentre dentro del rango "
            "admitido.",
            "2.3. El sistema aplica el cambio y registra la modificación en la "
            "bitácora.",
            "3. Definir los periodos académicos",
            "3.1. El administrador registra las fechas de inicio y fin de cada "
            "periodo del calendario.",
            "3.2. El sistema los incorpora como variable disponible para el "
            "análisis y la predicción.",
        ],
        postcondicion="Los catálogos y parámetros quedan actualizados y aplicados "
                      "a las siguientes ejecuciones analíticas.",
        excepciones=["1. El valor ingresado está fuera del rango admitido.",
                     "2. Los periodos académicos definidos se superponen.",
                     "3. El administrador no cuenta con permisos suficientes."],
    ),
    dict(
        id="RF26", nombre="Registrar y Consultar la Bitácora de Auditoría",
        prioridad="Esencial",
        modulo="Administración de plataforma y auditoría",
        resumen="Trazabilidad de las operaciones críticas realizadas sobre el "
                "sistema.",
        descripcion="El sistema deberá registrar en una bitácora las operaciones "
                    "críticas efectuadas sobre la plataforma, incluyendo el "
                    "usuario responsable, la fecha y hora, el tipo de operación, la "
                    "entidad afectada y los valores modificados, y deberá permitir "
                    "su consulta filtrada por usuario, fecha, módulo y tipo de "
                    "operación. Los registros de la bitácora no podrán ser "
                    "modificados ni eliminados.",
        usuarios=ADM + ", " + APO, iniciador="El sistema",
        precondicion="El usuario debe encontrarse autenticado y la operación debe "
                     "estar clasificada como crítica.",
        proceso=[
            "1. Registrar la operación",
            "1.1. El sistema detecta la ejecución de una operación clasificada "
            "como crítica.",
            "1.2. El sistema almacena el usuario, la fecha y hora, el tipo de "
            "operación, la entidad afectada y los valores anteriores y nuevos.",
            "2. Consultar la bitácora",
            "2.1. El usuario autorizado accede al módulo de auditoría.",
            "2.2. El usuario aplica los filtros por usuario, fecha, módulo o tipo "
            "de operación.",
            "2.3. El sistema muestra los registros que cumplen los criterios.",
            "3. Consultar el detalle",
            "3.1. El usuario selecciona un registro de la bitácora.",
            "3.2. El sistema despliega la información completa de la operación "
            "auditada.",
        ],
        postcondicion="Las operaciones críticas quedan registradas de forma "
                      "inalterable y disponibles para su revisión.",
        excepciones=["1. Se intenta modificar o eliminar un registro de la "
                     "bitácora.",
                     "2. No existen registros que cumplan los criterios "
                     "indicados.",
                     "3. El usuario no cuenta con permisos de auditoría."],
    ),
    dict(
        id="RF27", nombre="Generar, Exportar e Imprimir Reportes",
        prioridad="Media",
        modulo="Administración de plataforma y auditoría",
        resumen="Emisión de reportes operativos y gerenciales y su exportación "
                "para uso administrativo.",
        descripcion="El sistema deberá generar reportes de generación por sector, "
                    "generación por tipo de residuo, cumplimiento de jornadas, "
                    "incidencias registradas, indicadores del periodo y "
                    "predicciones vigentes, aplicando los filtros definidos por el "
                    "usuario, y deberá permitir su exportación a formatos de "
                    "documento y de hoja de cálculo, así como su impresión.",
        usuarios=DIR + ", " + APO + ", " + SUP, iniciador=APO,
        precondicion="Debe existir información correspondiente al periodo y a los "
                     "filtros solicitados.",
        proceso=[
            "1. Seleccionar el reporte",
            "1.1. El usuario accede al módulo de reportes y elige el tipo "
            "deseado.",
            "1.2. El usuario define el rango de fechas y los filtros aplicables.",
            "2. Generar el reporte",
            "2.1. El sistema recupera la información y la consolida.",
            "2.2. El sistema presenta el reporte en pantalla.",
            "3. Exportar o imprimir",
            "3.1. El usuario selecciona el formato de exportación o la opción de "
            "impresión.",
            "3.2. El sistema genera el archivo con el encabezado institucional, la "
            "fecha de emisión y el usuario solicitante.",
            "3.3. El sistema registra la emisión del reporte en la bitácora.",
        ],
        postcondicion="El reporte queda generado, disponible para su descarga o "
                      "impresión, y su emisión registrada.",
        excepciones=["1. No existe información para el periodo y los filtros "
                     "seleccionados.",
                     "2. El volumen de información excede el máximo admitido para "
                     "la exportación.",
                     "3. El usuario no cuenta con permisos sobre los sectores "
                     "solicitados."],
    ),
]


def con_diagrama():
    """Requisitos de prioridad Alta que llevan diagrama de actividad."""
    return [r for r in RF if r.get("pasos")]


def archivo_diagrama(rid):
    return "%s_actividad.png" % rid.lower()
