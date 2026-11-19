# -*- coding: utf-8 -*-
"""Fuente unica de la Fase 2: actores, paquetes y casos de uso.

De aqui salen el modelo de Enterprise Architect (ea_modelo.py) y el texto de
los capitulos 5 y 6 (cap5.py, cap6.py), de modo que los numeros y nombres de
los casos de uso coinciden en todos los diagramas y tablas. Los actores, la
prioridad y los procesos se derivan del capitulo 4 (RF1-RF27) y de los
permisos por rol implementados en el backend.
"""

SISTEMA = ("Sistema web de gestión de residuos sólidos para la DSU-UAGRM "
           "con predicción mediante Random Forest Regressor")

# ----------------------------------------------------------------------
# actores
# ----------------------------------------------------------------------
POL, SUP, CDD, ADM = "POL", "SUP", "CDD", "ADM"

# Actores = los cuatro roles (grupos) del sistema, independientes entre si: no
# hay actor abstracto ni actores no humanos. El antiguo rol Administrativo se
# integro al Administrador (backend: operations/0003_fusionar_administrativo).
ACTORES = {
    POL: dict(nombre="Personal Operativo de Limpieza",
              desc="Ejecuta la recolección en campo. Desde el teléfono registra "
                   "el vaciado de cada punto de su jornada, las cantidades por "
                   "tipo de residuo y las incidencias que encuentra, y consulta "
                   "sus propias jornadas y registros."),
    SUP: dict(nombre="Supervisor de Recolección",
              desc="Planifica las jornadas y rutas de sus sectores, asigna "
                   "personal y vehículos, controla la ejecución, atiende las "
                   "incidencias y resuelve las recomendaciones del sistema."),
    CDD: dict(nombre="Cuerpo Directivo de la DSU",
              desc="Consume la información analítica, cartográfica y predictiva "
                   "(tableros, mapas, predicciones y reportes) para la toma de "
                   "decisiones institucionales, sin registrar datos operativos."),
    ADM: dict(nombre="Administrador del Sistema",
              desc="Administra usuarios, roles, catálogos y parámetros; ejecuta "
                   "el proceso ETL, entrena, publica y revierte el modelo "
                   "predictivo, revisa la bitácora de auditoría y elabora los "
                   "reportes. No registra la operación de campo."),
}
TODOS = [POL, SUP, CDD, ADM]

# ----------------------------------------------------------------------
# paquetes = los ocho modulos del capitulo 4
# ----------------------------------------------------------------------
PAQUETES = [
    dict(n=1, nombre="Gestión de Usuarios y Control de Acceso", rf="RF1–RF3",
         desc="agrupa la autenticación de los usuarios, el cierre de sesión y la "
              "administración de cuentas, roles y permisos. Determina quién "
              "ingresa al sistema y qué operaciones puede realizar cada rol, por "
              "lo que es utilizado por todos los demás paquetes."),
    dict(n=2, nombre="Gestión Topológica y Puntos de Recolección", rf="RF4–RF7",
         desc="digitaliza la estructura del campus: sectores y facultades, "
              "puntos de recolección georreferenciados, contenedores instalados "
              "y el catálogo de tipos de residuo y unidades de medida. Es la "
              "base territorial y de clasificación que usan la operación, la "
              "analítica y la predicción."),
    dict(n=3, nombre="Gestión de Residuos", rf="RF8–RF10",
         desc="contiene el núcleo transaccional: el registro en campo del "
              "vaciado de cada punto, el registro y la atención de incidencias "
              "operativas y la consulta del histórico de residuos."),
    dict(n=4, nombre="Gestión de Recolecciones y Logística", rf="RF11–RF14",
         desc="organiza el trabajo de recolección: vehículos, planificación de "
              "jornadas y rutas, asignación de personal y vehículos, ejecución "
              "punto por punto, cierre con resumen y consulta del historial."),
    dict(n=5, nombre="Inteligencia de Negocios y Analítica Visual", rf="RF15–RF18",
         desc="consolida y depura la información mediante el proceso ETL, "
              "calcula los indicadores clave, los presenta en tableros "
              "interactivos (incluido Power BI) y compara periodos para "
              "identificar tendencias."),
    dict(n=6, nombre="Componente Cartográfico y Análisis Espacial", rf="RF19–RF21",
         desc="representa los puntos de recolección sobre el mapa del campus, "
              "genera el mapa de calor de generación observada o proyectada y "
              "aplica los filtros de periodo, sector y tipo de residuo."),
    dict(n=7, nombre="Predicción mediante Random Forest Regressor", rf="RF22–RF24",
         desc="entrena, evalúa, publica y revierte el modelo Random Forest "
              "Regressor, genera las predicciones de generación futura con su "
              "margen de error y emite y resuelve las alertas y "
              "recomendaciones logísticas."),
    dict(n=8, nombre="Administración de la Plataforma y Auditoría", rf="RF25–RF27",
         desc="configura los periodos académicos y los parámetros globales, "
              "registra y consulta la bitácora de auditoría inalterable y genera, "
              "exporta e imprime los reportes. Es transversal: la bitácora la "
              "invocan las operaciones críticas de todos los paquetes."),
]

# ----------------------------------------------------------------------
# casos de uso
# Claves: n, nombre, rf, paq, actores, pri (prioridad), riesgo, ini
# (actor iniciador), proposito, desc, pre, proceso, post, exc,
# incluye [n], extiende (n, condicion), especializa n.
# ----------------------------------------------------------------------

CU = [
    # ======================= Paquete 1 =======================
    dict(n=1, nombre="Iniciar sesión", rf="RF3", paq=1, actores=TODOS,
         pri="Alta", riesgo="Alto", ini="Cualquiera de los actores",
         proposito="Autenticar al usuario y abrir una sesión con acceso "
                   "únicamente a las funciones de su rol.",
         desc="El usuario ingresa su nombre de usuario y contraseña; el sistema "
              "verifica las credenciales, emite el token de acceso con tiempo de "
              "expiración y muestra solo los módulos habilitados para su rol.",
         pre="El usuario cuenta con una cuenta activa registrada en el sistema.",
         proceso=["1. El usuario accede al formulario de inicio de sesión.",
                  "2. El usuario ingresa su nombre de usuario y contraseña.",
                  "3. El sistema verifica las credenciales contra la información "
                  "almacenada (contraseña cifrada).",
                  "4. El sistema verifica que la cuenta esté activa.",
                  "5. El sistema emite el token de acceso y el de renovación.",
                  "6. El sistema registra el evento en la bitácora de auditoría "
                  "(inicio de sesión).",
                  "7. El sistema presenta el menú con los módulos habilitados "
                  "para el rol del usuario."],
         post="La sesión queda abierta y el usuario accede solo a las funciones "
              "autorizadas para su rol.",
         exc=["1. Las credenciales son incorrectas: el sistema registra el "
              "intento fallido en la bitácora, muestra un mensaje y permite "
              "reintentar (con límite de intentos por minuto).",
              "2. La cuenta está desactivada: el sistema rechaza el acceso.",
              "3. Faltan datos obligatorios en el formulario."]),
    dict(n=2, nombre="Cerrar sesión", rf="RF3", paq=1, actores=TODOS,
         pri="Media", riesgo="Medio", ini="Cualquiera de los actores",
         proposito="Terminar la sesión del usuario e invalidar sus credenciales "
                   "de acceso.",
         desc="El usuario cierra su sesión o esta expira por inactividad; el "
              "sistema invalida el token de renovación y retorna al formulario "
              "de acceso.",
         pre="El usuario tiene una sesión abierta.",
         proceso=["1. El usuario selecciona la opción Cerrar sesión.",
                  "2. El sistema invalida el token de renovación (lista negra).",
                  "3. El sistema registra el evento en la bitácora de auditoría.",
                  "4. El sistema elimina las credenciales guardadas en el navegador.",
                  "5. El sistema retorna al formulario de inicio de sesión.",
                  "5.a. Si la sesión expira por inactividad, el sistema ejecuta "
                  "los pasos 4 y 5 sin intervención del usuario."],
         post="La sesión queda cerrada, registrada en la bitácora, y el token ya "
              "no permite el acceso.",
         exc=["1. El token ya había expirado: el sistema retorna igualmente al "
              "formulario de acceso."]),
    dict(n=3, nombre="Gestionar usuarios", rf="RF1", paq=1, actores=[ADM],
         pri="Alta", riesgo="Alto", ini="Administrador del Sistema",
         proposito="Administrar las cuentas del personal que accede al sistema.",
         desc="El administrador registra, consulta, actualiza, desactiva y "
              "reactiva las cuentas de usuario y les asigna sus roles.",
         pre="El administrador inició sesión con permisos de administración.",
         proceso=["1. El administrador accede al módulo de usuarios.",
                  "2. El sistema muestra la lista de usuarios registrados.",
                  "3. Registrar: el administrador ingresa los datos personales, "
                  "el nombre de usuario, la contraseña y los roles.",
                  "3.1. El sistema valida los datos, la unicidad del nombre de "
                  "usuario y la política de contraseñas.",
                  "3.2. El sistema almacena la cuenta con la contraseña cifrada.",
                  "4. Actualizar: el administrador selecciona un usuario, "
                  "modifica sus datos o roles y el sistema los guarda.",
                  "5. Desactivar o reactivar: el administrador cambia el estado "
                  "de la cuenta; el sistema impide nuevos accesos y conserva el "
                  "historial del usuario.",
                  "6. El sistema registra el evento en la bitácora de auditoría."],
         post="La cuenta queda registrada o actualizada con sus roles.",
         exc=["1. El nombre de usuario ya se encuentra registrado.",
              "2. Existen datos obligatorios incompletos.",
              "3. La contraseña no cumple la política de seguridad.",
              "4. El usuario no cuenta con permisos suficientes."]),
    dict(n=4, nombre="Gestionar roles y permisos", rf="RF2", paq=1, actores=[ADM],
         pri="Alta", riesgo="Alto", ini="Administrador del Sistema",
         proposito="Definir los niveles de acceso a los módulos del sistema.",
         desc="El administrador consulta los roles, registra nuevos roles y "
              "agrega o quita los permisos de cada uno.",
         pre="El administrador inició sesión con permisos de administración.",
         proceso=["1. El administrador accede al módulo de roles.",
                  "2. El sistema muestra los roles y sus permisos.",
                  "3. Registrar: el administrador ingresa el nombre del rol y "
                  "selecciona sus permisos; el sistema lo almacena.",
                  "4. Modificar: el administrador selecciona un rol y agrega o "
                  "quita permisos; el sistema guarda la configuración.",
                  "5. El sistema registra el evento en la bitácora de auditoría."],
         post="Los roles quedan definidos con sus permisos y se aplican a los "
              "usuarios que los tienen asignados.",
         exc=["1. El rol ya existe.",
              "2. No se seleccionó ningún permiso.",
              "3. El usuario no cuenta con permisos suficientes."]),

    # ======================= Paquete 2 =======================
    dict(n=5, nombre="Gestionar sectores y facultades", rf="RF4", paq=2,
         actores=[ADM, SUP], pri="Alta", riesgo="Medio",
         ini="Administrador del Sistema",
         proposito="Mantener la estructura territorial del campus sobre la que se "
                   "agregan los indicadores y las predicciones.",
         desc="El administrador registra los sectores y facultades con su código "
              "y supervisor responsable; el supervisor puede actualizar los "
              "datos de sus sectores.",
         pre="El usuario inició sesión con permisos sobre sectores.",
         proceso=["1. El usuario accede al módulo de sectores (Maestros).",
                  "2. El sistema muestra los sectores con sus puntos asociados.",
                  "3. Registrar: el usuario ingresa código, nombre, descripción y "
                  "supervisor; el sistema valida que el código no esté duplicado "
                  "y lo almacena.",
                  "4. Actualizar: el usuario modifica los datos y el sistema los "
                  "guarda.",
                  "5. Desactivar: el sistema cambia el estado y excluye el sector "
                  "de nuevas planificaciones, conservando su historial.",
                  "6. El sistema registra el evento en la bitácora de auditoría."],
         post="La estructura de sectores queda actualizada.",
         exc=["1. El código del sector ya existe.",
              "2. Existen datos obligatorios incompletos.",
              "3. Se intenta desactivar un sector con puntos activos.",
              "4. El supervisor intenta modificar un sector que no tiene asignado."]),
    dict(n=6, nombre="Gestionar puntos de recolección", rf="RF5", paq=2,
         actores=[ADM, SUP], pri="Alta", riesgo="Alto",
         ini="Supervisor de Recolección",
         proposito="Registrar los puntos de recolección georreferenciados que "
                   "alimentan la operación, el mapa y el modelo.",
         desc="El usuario registra, consulta, actualiza y desactiva puntos de "
              "recolección con su sector, coordenadas, capacidad y estado, "
              "ubicándolos sobre el mapa del campus.",
         pre="Existe al menos un sector activo.",
         proceso=["1. El usuario accede al módulo de puntos de recolección.",
                  "2. El sistema muestra los puntos filtrables por sector, "
                  "código o estado.",
                  "3. Registrar: el usuario selecciona el sector e ingresa el "
                  "código, la referencia y la capacidad.",
                  "4. El usuario ubica el punto haciendo clic en el mapa o "
                  "ingresa la latitud y longitud.",
                  "5. El sistema valida que las coordenadas estén dentro del "
                  "área del campus y que el código sea único, y almacena el punto.",
                  "6. Desactivar: el usuario indica el motivo; el sistema excluye "
                  "el punto de nuevas jornadas y conserva su historial.",
                  "7. El sistema registra el evento en la bitácora de auditoría."],
         post="El punto queda registrado y visible en el mapa.",
         exc=["1. El código del punto ya existe.",
              "2. Las coordenadas están fuera del área del campus.",
              "3. El sector está desactivado.",
              "4. Falta el motivo de desactivación."]),
    dict(n=7, nombre="Gestionar contenedores", rf="RF7", paq=2,
         actores=[ADM, SUP], pri="Media", riesgo="Bajo",
         ini="Supervisor de Recolección",
         proposito="Registrar la capacidad instalada de cada punto.",
         desc="El usuario registra los contenedores de cada punto con su tipo, "
              "capacidad, fecha de instalación y estado, y actualiza su estado "
              "por deterioro, reemplazo o reubicación.",
         pre="Existe al menos un punto de recolección activo.",
         proceso=["1. El usuario selecciona el punto de recolección.",
                  "2. El sistema muestra sus contenedores y la capacidad total.",
                  "3. Registrar: el usuario ingresa código, tipo, capacidad en "
                  "litros y fecha de instalación; el sistema valida y almacena.",
                  "4. Actualizar estado: el usuario registra el cambio y el "
                  "sistema lo guarda.",
                  "5. El sistema registra el evento en la bitácora de auditoría."],
         post="La capacidad instalada del punto queda actualizada.",
         exc=["1. El punto está desactivado.",
              "2. La capacidad ingresada no es válida."]),
    dict(n=8, nombre="Gestionar tipos de residuo y unidades de medida", rf="RF6",
         paq=2, actores=[ADM], pri="Alta", riesgo="Medio",
         ini="Administrador del Sistema",
         proposito="Homogeneizar la clasificación y la cuantificación de los "
                   "residuos.",
         desc="El usuario administra el catálogo de tipos de residuo (clase, "
              "aprovechable, unidad) y de unidades de medida con su magnitud "
              "(masa o volumen) y su factor de conversión.",
         pre="El usuario inició sesión con permisos sobre catálogos.",
         proceso=["1. El usuario accede al módulo de catálogos.",
                  "2. El sistema muestra los tipos de residuo y las unidades.",
                  "3. Registrar tipo: el usuario ingresa nombre, clasificación, "
                  "condición de aprovechable y unidad; el sistema valida que no "
                  "esté duplicado y lo almacena.",
                  "4. Registrar unidad: el usuario ingresa nombre, símbolo, "
                  "magnitud y factor de conversión; el sistema valida el factor.",
                  "5. Actualizar: el sistema bloquea el cambio de factor si la "
                  "unidad ya tiene registros históricos.",
                  "6. El sistema registra el evento en la bitácora de auditoría."],
         post="El catálogo queda disponible para el registro y la analítica.",
         exc=["1. El tipo de residuo o la unidad ya existe.",
              "2. Se intenta cambiar el factor de una unidad con registros.",
              "3. El factor de conversión no es positivo."]),

    # ======================= Paquete 3 =======================
    dict(n=9, nombre="Registrar vaciado de residuos", rf="RF8", paq=3,
         actores=[POL, SUP], pri="Alta", riesgo="Alto",
         ini="Personal Operativo de Limpieza",
         proposito="Capturar en campo la unidad básica de información del "
                   "sistema: cuánto residuo, de qué tipo y de qué punto.",
         desc="Desde el teléfono, el operario registra el vaciado del punto que "
              "está atendiendo con los tipos de residuo, las cantidades y las "
              "observaciones, o indica que el punto no tenía residuos.",
         pre="El operario inició sesión y su jornada está abierta (en ejecución).",
         proceso=["1. El sistema muestra el siguiente punto de la ruta de la "
                  "jornada.",
                  "2. El operario indica si el punto presenta residuos.",
                  "2.a. Si no presenta, el sistema registra la visita sin "
                  "generación y pasa al siguiente punto.",
                  "3. El operario selecciona el tipo de residuo; el sistema "
                  "propone la unidad asociada.",
                  "4. El operario ingresa la cantidad y, si corresponde, agrega "
                  "otros tipos a la misma visita y observaciones.",
                  "5. El sistema valida que la cantidad sea positiva y coherente "
                  "con la capacidad del punto.",
                  "6. El sistema almacena el registro con fecha, hora, usuario y "
                  "jornada, y actualiza el avance de la ruta.",
                  "7. Si el operario detecta un problema, extiende con CU10 "
                  "Registrar incidencia operativa."],
         post="El vaciado queda vinculado al punto, sector, jornada y operario, "
              "disponible para el ETL.",
         exc=["1. El punto no pertenece a la jornada.",
              "2. La cantidad es nula, negativa o excede la capacidad del punto.",
              "3. No hay conexión: el sistema informa el error y conserva el "
              "formulario.",
              "4. La jornada no está en ejecución."]),
    dict(n=10, nombre="Registrar incidencia operativa", rf="RF10", paq=3,
         actores=[POL, SUP], pri="Media", riesgo="Medio",
         ini="Personal Operativo de Limpieza",
         proposito="Documentar las situaciones que afectan la recolección.",
         desc="El usuario registra una incidencia (contenedor dañado, acceso "
              "bloqueado, residuos mal segregados o peligrosos, desborde) con su "
              "gravedad; queda pendiente para el supervisor del sector.",
         pre="El usuario inició sesión; si es operario, está dentro de una "
             "jornada en ejecución.",
         proceso=["1. El usuario selecciona el punto afectado.",
                  "2. El sistema solicita tipo, descripción y gravedad.",
                  "3. El usuario registra la información.",
                  "4. El sistema almacena la incidencia como pendiente y la "
                  "muestra en el panel del supervisor del sector."],
         post="La incidencia queda registrada y pendiente de atención.",
         exc=["1. El punto indicado no existe.",
              "2. Existen datos obligatorios incompletos."],
         extiende=(9, "el operario detecta un problema en el punto")),
    dict(n=11, nombre="Atender incidencia", rf="RF10", paq=3, actores=[SUP],
         pri="Media", riesgo="Bajo", ini="Supervisor de Recolección",
         proposito="Cerrar las incidencias con la acción adoptada.",
         desc="El supervisor revisa las incidencias pendientes de sus sectores, "
              "registra la acción adoptada y la cierra.",
         pre="Existe al menos una incidencia pendiente en un sector del "
             "supervisor.",
         proceso=["1. El supervisor accede a las incidencias pendientes.",
                  "2. El sistema muestra las incidencias de sus sectores.",
                  "3. El supervisor selecciona una y registra la acción adoptada.",
                  "4. El sistema la marca como atendida con fecha y usuario.",
                  "5. El sistema registra el evento en la bitácora de auditoría."],
         post="La incidencia queda atendida y conserva su trazabilidad.",
         exc=["1. La incidencia ya está atendida.",
              "2. El sector no está asignado al supervisor."]),
    dict(n=12, nombre="Consultar histórico de residuos", rf="RF9", paq=3,
         actores=[SUP, ADM, CDD, POL], pri="Alta", riesgo="Medio",
         ini="Supervisor de Recolección",
         proposito="Recuperar los registros históricos con filtros y totales.",
         desc="El usuario consulta los registros de residuos por sector, punto, "
              "tipo, rango de fechas y usuario, con totales por tipo de residuo. "
              "El supervisor ve sus sectores y el operario solo los registros de "
              "sus jornadas.",
         pre="Existen registros de residuos almacenados.",
         proceso=["1. El usuario accede al módulo de registros.",
                  "2. El usuario define el rango de fechas y los filtros.",
                  "3. El sistema recupera los registros (el supervisor solo ve "
                  "sus sectores).",
                  "4. El sistema muestra los resultados paginados y los totales "
                  "por tipo de residuo.",
                  "5. El usuario puede consultar el detalle de un registro."],
         post="El usuario obtiene el histórico solicitado.",
         exc=["1. No existen registros para los filtros.",
              "2. El rango de fechas es inválido."]),

    # ======================= Paquete 4 =======================
    dict(n=13, nombre="Gestionar vehículos", rf="RF13", paq=4,
         actores=[ADM, SUP], pri="Media", riesgo="Bajo",
         ini="Supervisor de Recolección",
         proposito="Mantener el registro de los vehículos disponibles para las "
                   "jornadas.",
         desc="El usuario registra, actualiza y da de baja los vehículos con su "
              "placa, descripción, capacidad y estado.",
         pre="El usuario inició sesión con permisos sobre vehículos.",
         proceso=["1. El usuario accede al módulo de vehículos.",
                  "2. El sistema muestra los vehículos registrados.",
                  "3. Registrar o actualizar: el usuario ingresa placa, "
                  "descripción, capacidad y estado; el sistema valida que la "
                  "placa sea única y guarda.",
                  "4. El sistema registra el evento en la bitácora de auditoría."],
         post="El vehículo queda disponible (o fuera de servicio) para asignar.",
         exc=["1. La placa ya está registrada.",
              "2. Existen datos obligatorios incompletos."]),
    dict(n=14, nombre="Planificar jornada y ruta de recolección", rf="RF11",
         paq=4, actores=[SUP, ADM], pri="Alta", riesgo="Alto",
         ini="Supervisor de Recolección",
         proposito="Definir cuándo, dónde y en qué orden se recolecta.",
         desc="El supervisor crea la jornada con fecha, turno y sector, define "
              "la secuencia de puntos (con los puntos priorizados por las "
              "recomendaciones aceptadas) y la confirma.",
         pre="Existen sectores y puntos activos.",
         proceso=["1. El supervisor accede al módulo de jornadas y elige Nueva "
                  "jornada.",
                  "2. El sistema solicita fecha, turno y sector.",
                  "3. El sistema propone los puntos priorizados por las "
                  "recomendaciones aceptadas.",
                  "4. El supervisor agrega, quita y ordena los puntos de la ruta.",
                  "5. El sistema ejecuta CU15 Asignar personal y vehículos a la "
                  "jornada.",
                  "6. El supervisor confirma la jornada; el sistema la publica "
                  "para el personal asignado.",
                  "7. El sistema registra el evento en la bitácora de auditoría."],
         post="La jornada queda planificada y confirmada con su ruta.",
         exc=["1. Ya existe una jornada para la misma fecha, turno y sector.",
              "2. La ruta no tiene puntos.",
              "3. Un punto de la ruta está desactivado.",
              "4. El sector no está asignado al supervisor."],
         incluye=[15]),
    dict(n=15, nombre="Asignar personal y vehículos a la jornada", rf="RF13",
         paq=4, actores=[SUP, ADM], pri="Alta", riesgo="Medio",
         ini="Supervisor de Recolección",
         proposito="Dotar a la jornada de responsable, personal y vehículos sin "
                   "superposiciones.",
         desc="El supervisor selecciona el personal operativo, los vehículos y "
              "el responsable; el sistema verifica que no estén asignados a otra "
              "jornada del mismo turno.",
         pre="Existe una jornada planificada y personal registrado.",
         proceso=["1. El sistema muestra el personal y los vehículos disponibles "
                  "para el turno.",
                  "2. El supervisor selecciona los recursos y designa al "
                  "responsable.",
                  "3. El sistema valida que no exista superposición de turno y "
                  "que los vehículos estén en servicio.",
                  "4. El sistema registra la asignación."],
         post="La jornada queda con personal, vehículos y responsable.",
         exc=["1. Una persona ya está asignada a otra jornada en el mismo turno.",
              "2. No se designó responsable.",
              "3. Un vehículo está fuera de servicio."]),
    dict(n=16, nombre="Ejecutar jornada de recolección", rf="RF12", paq=4,
         actores=[SUP, POL], pri="Alta", riesgo="Alto",
         ini="Supervisor de Recolección",
         proposito="Controlar la ejecución real de la jornada punto por punto.",
         desc="El responsable abre la jornada confirmada y el personal recorre "
              "la ruta registrando el vaciado de cada punto; el sistema muestra "
              "el avance.",
         pre="Existe una jornada confirmada para la fecha, con personal "
             "asignado.",
         proceso=["1. El supervisor u operario responsable abre la jornada.",
                  "2. El sistema registra la hora de inicio y habilita la captura.",
                  "3. Para cada punto de la ruta, el sistema ejecuta CU9 "
                  "Registrar vaciado de residuos.",
                  "4. Si un punto no puede atenderse, extiende con CU17 Omitir "
                  "punto de la ruta.",
                  "5. El sistema actualiza el avance hasta agotar la ruta."],
         post="Todos los puntos quedan visitados u omitidos con motivo.",
         exc=["1. La fecha de la jornada no corresponde.",
              "2. El usuario no forma parte del personal asignado.",
              "3. La jornada no está confirmada."],
         incluye=[9]),
    dict(n=17, nombre="Omitir punto de la ruta", rf="RF12", paq=4,
         actores=[POL, SUP], pri="Media", riesgo="Bajo",
         ini="Personal Operativo de Limpieza",
         proposito="Dejar constancia de los puntos planificados que no se "
                   "atendieron y por qué.",
         desc="Cuando un punto no puede atenderse, el usuario indica el motivo; "
              "el sistema lo marca como omitido y continúa con la ruta.",
         pre="La jornada está en ejecución y el punto está pendiente.",
         proceso=["1. El usuario selecciona Omitir en el punto actual.",
                  "2. El sistema solicita el motivo.",
                  "3. El sistema marca el punto como omitido y presenta el "
                  "siguiente."],
         post="El punto queda omitido con su motivo y cuenta en la desviación "
              "de la jornada.",
         exc=["1. No se indicó el motivo.",
              "2. El punto ya fue visitado."],
         extiende=(16, "el punto no puede ser atendido")),
    dict(n=18, nombre="Cerrar jornada de recolección", rf="RF12", paq=4,
         actores=[SUP], pri="Alta", riesgo="Medio",
         ini="Supervisor de Recolección",
         proposito="Consolidar la jornada y bloquear cambios posteriores.",
         desc="El supervisor revisa el resumen (totales por tipo, puntos "
              "ejecutados frente a planificados), registra observaciones y "
              "cierra la jornada.",
         pre="La jornada está en ejecución y todos sus puntos fueron visitados "
             "u omitidos.",
         proceso=["1. El supervisor solicita el cierre de la jornada.",
                  "2. El sistema totaliza las cantidades por tipo de residuo y "
                  "contrasta lo ejecutado con lo planificado.",
                  "3. El supervisor revisa el resumen y registra observaciones.",
                  "4. El sistema cierra la jornada con la hora de finalización e "
                  "impide nuevas modificaciones.",
                  "5. El sistema registra el evento en la bitácora de auditoría."],
         post="La jornada queda cerrada con su resumen consolidado.",
         exc=["1. La jornada ya está cerrada.",
              "2. Existen puntos sin registro ni motivo de omisión."]),
    dict(n=19, nombre="Consultar historial de recolecciones", rf="RF14", paq=4,
         actores=[SUP, ADM, CDD, POL], pri="Media", riesgo="Bajo",
         ini="Supervisor de Recolección",
         proposito="Revisar las jornadas ejecutadas y su cobertura.",
         desc="El usuario consulta las jornadas por sector, fechas, responsable "
              "y estado, con su cobertura, cantidades e incidencias. El "
              "supervisor ve sus sectores y el operario solo las jornadas en las "
              "que fue asignado.",
         pre="Existen jornadas registradas.",
         proceso=["1. El usuario accede al historial de jornadas.",
                  "2. El usuario aplica los filtros.",
                  "3. El sistema muestra las jornadas con su porcentaje de "
                  "cobertura y totales.",
                  "4. El usuario selecciona una jornada y el sistema despliega "
                  "su recorrido, registros e incidencias."],
         post="El usuario obtiene el historial solicitado.",
         exc=["1. No existen jornadas para los filtros.",
              "2. El rango de fechas es inválido."]),

    # ======================= Paquete 5 =======================
    dict(n=20, nombre="Ejecutar proceso ETL", rf="RF15", paq=5,
         actores=[ADM], pri="Alta", riesgo="Alto",
         ini="Administrador del Sistema",
         proposito="Consolidar y depurar la información transaccional para la "
                   "analítica y el modelo.",
         desc="El administrador lo ejecuta a pedido y el servidor lo repite con la "
              "periodicidad de los parámetros (tarea programada con el comando "
              "etl --programado); el sistema extrae los registros "
              "nuevos, elimina duplicados, estandariza unidades a kg, deriva las "
              "variables temporales, marca atípicos y carga la tabla de hechos.",
         pre="Existen registros transaccionales nuevos desde la última ejecución.",
         proceso=["1. El administrador selecciona Ejecutar ETL (o la tarea "
                  "programada del servidor lo inicia al cumplirse la periodicidad).",
                  "2. El sistema crea la ejecución y extrae los registros "
                  "pendientes.",
                  "3. El sistema elimina duplicados, corrige formatos y "
                  "estandariza las cantidades a kilogramos.",
                  "4. El sistema deriva día, semana, mes y periodo académico y "
                  "marca los valores atípicos.",
                  "5. El sistema carga los hechos depurados y guarda los "
                  "descartados con su motivo.",
                  "6. El sistema registra el resultado (procesados, aceptados, "
                  "observados, duración).",
                  "7. El sistema registra el evento en la bitácora de auditoría."],
         post="La tabla de hechos queda actualizada para indicadores, mapas y "
              "modelo.",
         exc=["1. No hay registros nuevos.",
              "2. Ya hay una ejecución en curso.",
              "3. Falla la conexión con la base de datos: la ejecución queda "
              "como fallida."]),
    dict(n=21, nombre="Visualizar tablero interactivo", rf="RF16, RF17", paq=5,
         actores=[CDD, SUP, ADM], pri="Alta", riesgo="Medio",
         ini="Cuerpo Directivo de la DSU",
         proposito="Calcular los indicadores clave y presentarlos con sus series "
                   "de forma interactiva.",
         desc="El usuario explora el tablero con filtros por fecha, sector, "
              "punto, tipo y periodo académico. El sistema calcula sobre los "
              "hechos depurados los indicadores clave (total recolectado, "
              "promedios por punto y sector, sector y tipo predominantes, "
              "frecuencia, cobertura, variación y puntos críticos); un clic en un "
              "sector o tipo filtra todo. Incluye la pestaña de Power BI.",
         pre="El usuario inició sesión con permisos de consulta analítica y el "
             "proceso ETL se ejecutó al menos una vez.",
         proceso=["1. El usuario accede al tablero.",
                  "2. El sistema recupera los hechos del periodo con los filtros "
                  "por defecto.",
                  "3. El sistema calcula totales, promedios y frecuencias, la "
                  "variación respecto del periodo anterior y los puntos que "
                  "superan el umbral crítico configurado.",
                  "4. El sistema presenta indicadores, series y gráficos.",
                  "5. El usuario modifica los filtros o hace clic en un elemento.",
                  "6. El sistema recalcula y actualiza todas las visualizaciones.",
                  "7. Opcionalmente, el usuario abre la pestaña Power BI.",
                  "8. Si desea comparar periodos, extiende con CU22."],
         post="El usuario interpreta el comportamiento histórico de los residuos.",
         exc=["1. No hay datos para la combinación de filtros.",
              "2. El periodo anterior no tiene datos para la variación.",
              "3. El informe de Power BI no está configurado."]),
    dict(n=22, nombre="Comparar periodos e identificar tendencias", rf="RF18",
         paq=5, actores=[CDD, SUP, ADM], pri="Media", riesgo="Bajo",
         ini="Cuerpo Directivo de la DSU",
         proposito="Medir la variación entre dos periodos y detectar crecimiento "
                   "sostenido.",
         desc="El usuario elige un periodo base y uno de comparación; el sistema "
              "calcula la variación absoluta y porcentual por sector, punto y "
              "tipo y marca las tendencias crecientes sostenidas.",
         pre="Existen hechos en ambos periodos.",
         proceso=["1. El usuario selecciona el periodo base y el de comparación.",
                  "2. El sistema calcula la variación absoluta y porcentual.",
                  "3. El sistema evalúa la tendencia (cuatro meses consecutivos "
                  "al alza).",
                  "4. El sistema muestra la comparación y destaca las tendencias "
                  "crecientes."],
         post="La comparación y las tendencias quedan visibles en el tablero.",
         exc=["1. Un periodo no tiene datos.",
              "2. Los periodos se superponen."],
         extiende=(21, "el usuario solicita la comparación entre periodos")),

    # ======================= Paquete 6 =======================
    dict(n=23, nombre="Visualizar puntos en el mapa interactivo", rf="RF19",
         paq=6, actores=[CDD, SUP, ADM], pri="Alta", riesgo="Medio",
         ini="Supervisor de Recolección",
         proposito="Mostrar la distribución geográfica de los puntos.",
         desc="El sistema carga la cartografía del campus y posiciona los "
              "marcadores de los puntos activos; al seleccionar uno muestra su "
              "detalle.",
         pre="Existen puntos con coordenadas válidas.",
         proceso=["1. El usuario accede al mapa del campus.",
                  "2. El sistema carga la cartografía base (OpenStreetMap).",
                  "3. El sistema posiciona los marcadores según latitud y "
                  "longitud, diferenciados por nivel de generación.",
                  "4. El usuario selecciona un marcador y el sistema muestra "
                  "código, sector, capacidad, generación y última atención.",
                  "5. El usuario puede extender con CU24 o CU25."],
         post="El usuario visualiza la distribución de los puntos.",
         exc=["1. No hay puntos con coordenadas.",
              "2. El servicio de cartografía no está disponible."]),
    dict(n=24, nombre="Generar mapa de calor", rf="RF20", paq=6, actores=[CDD, SUP, ADM],
         pri="Alta", riesgo="Medio",
         ini="Supervisor de Recolección",
         proposito="Identificar visualmente las zonas críticas del campus.",
         desc="El usuario activa la capa de calor observada o proyectada; el "
              "sistema pondera cada punto por su generación y dibuja el "
              "gradiente con su leyenda.",
         pre="Existen hechos (o predicciones vigentes, para la capa proyectada) "
             "en el alcance.",
         proceso=["1. El usuario activa la capa de calor y elige observada o "
                  "proyectada.",
                  "2. El sistema recupera las cantidades por punto del alcance.",
                  "3. El sistema normaliza las cantidades y asigna el peso "
                  "relativo.",
                  "4. El sistema dibuja el gradiente y la leyenda.",
                  "5. El sistema resalta los puntos que superan el umbral "
                  "crítico."],
         post="El mapa de calor queda dibujado con las zonas críticas.",
         exc=["1. No hay datos para el alcance.",
              "2. Se pide la capa proyectada sin predicciones vigentes."],
         extiende=(23, "el usuario activa la capa de calor")),
    dict(n=25, nombre="Filtrar mapa por periodo, sector y tipo de residuo",
         rf="RF21", paq=6, actores=[CDD, SUP, ADM], pri="Media", riesgo="Bajo",
         ini="Supervisor de Recolección",
         proposito="Acotar la vista cartográfica.",
         desc="El usuario modifica los filtros y el sistema actualiza los "
              "marcadores y recalcula la capa de calor.",
         pre="El mapa está cargado.",
         proceso=["1. El usuario modifica fechas, periodo, sector, punto o tipo.",
                  "2. El sistema recupera la información del nuevo alcance.",
                  "3. El sistema actualiza marcadores y capa de calor.",
                  "4. El usuario puede restablecer los filtros."],
         post="El mapa refleja solo la información filtrada.",
         exc=["1. La combinación no arroja resultados.",
              "2. El rango de fechas es inválido."],
         extiende=(23, "el usuario modifica los filtros")),

    # ======================= Paquete 7 =======================
    dict(n=26, nombre="Entrenar y evaluar el modelo Random Forest Regressor",
         rf="RF22", paq=7, actores=[ADM], pri="Alta", riesgo="Alto",
         ini="Administrador del Sistema",
         proposito="Obtener una nueva versión del modelo y medir su desempeño.",
         desc="El administrador lanza el entrenamiento con los hiperparámetros "
              "propuestos o propios; el sistema arma el conjunto, lo divide en "
              "orden cronológico, entrena, evalúa (MAE, RMSE, R²) y calcula la "
              "importancia de variables.",
         pre="Existe el volumen mínimo de hechos depurados configurado.",
         proceso=["1. El administrador accede al módulo del modelo.",
                  "2. El sistema propone hiperparámetros (árboles, profundidad, "
                  "muestras por hoja).",
                  "3. El administrador acepta o ajusta y selecciona Entrenar.",
                  "4. El sistema construye las variables y el objetivo, y "
                  "codifica las categóricas.",
                  "5. El sistema separa entrenamiento y prueba respetando el "
                  "orden cronológico.",
                  "6. El sistema entrena el Random Forest Regressor.",
                  "7. El sistema evalúa MAE, RMSE y R² e importancias.",
                  "8. El sistema guarda la versión como candidata si supera el "
                  "umbral.",
                  "9. El sistema registra el evento en la bitácora de auditoría."],
         post="Queda una nueva versión entrenada y evaluada.",
         exc=["1. Volumen de datos insuficiente.",
              "2. Las métricas no alcanzan el umbral: la versión queda "
              "rechazada.",
              "3. Hiperparámetros fuera de rango.",
              "4. Ya hay un entrenamiento en curso."]),
    dict(n=27, nombre="Publicar o revertir versión del modelo", rf="RF22",
         paq=7, actores=[ADM], pri="Media", riesgo="Alto",
         ini="Administrador del Sistema",
         proposito="Decidir qué versión del modelo usan las predicciones.",
         desc="El administrador publica una versión candidata o vuelve a una "
              "versión anterior; solo una versión queda vigente.",
         pre="Existe al menos una versión entrenada que superó el umbral.",
         proceso=["1. El sistema lista las versiones con sus métricas.",
                  "2. El administrador elige una versión y selecciona Publicar.",
                  "3. El sistema la marca vigente y retira la anterior.",
                  "4. El sistema registra el evento en la bitácora de auditoría."],
         post="La versión elegida queda vigente para las predicciones.",
         exc=["1. La versión no superó el umbral.",
              "2. La versión ya es la vigente."]),
    dict(n=28, nombre="Predecir generación futura y emitir alertas",
         rf="RF23, RF24", paq=7, actores=[SUP, CDD, ADM], pri="Alta",
         riesgo="Alto", ini="Supervisor de Recolección",
         proposito="Estimar cuánto residuo se generará por punto y sector, con "
                   "su margen de error, y traducir la estimación en alertas y "
                   "recomendaciones logísticas.",
         desc="El usuario define el horizonte y el alcance y ejecuta la "
              "predicción. El sistema aplica el modelo vigente, guarda el lote "
              "con su margen de error y evalúa cada punto con su predicción, "
              "capacidad y tendencia para emitir alertas de desborde y "
              "recomendaciones (priorizar, frecuencia, contenedores, separación) "
              "con su evidencia.",
         pre="Existe un modelo publicado vigente.",
         proceso=["1. El usuario accede al módulo de predicción.",
                  "2. El usuario define el horizonte (días) y el sector o punto "
                  "y ejecuta la predicción.",
                  "3. El sistema construye las variables con el estado histórico "
                  "y las fechas futuras.",
                  "4. El sistema aplica el modelo vigente.",
                  "5. El sistema agrega por sector y tipo y calcula el margen "
                  "de error.",
                  "6. El sistema guarda el lote con la versión del modelo.",
                  "7. El sistema evalúa cada punto: si se desbordaría antes de la "
                  "próxima atención emite una alerta de priorización; si el "
                  "máximo diario alcanza la capacidad recomienda contenedores; si "
                  "el crecimiento supera el umbral recomienda aumentar la "
                  "frecuencia; si el porcentaje no aprovechable supera el umbral "
                  "recomienda reforzar la separación.",
                  "8. El sistema guarda cada recomendación con su evidencia, "
                  "pendiente de resolución.",
                  "9. El sistema muestra las estimaciones siempre con su margen."],
         post="El lote de predicciones queda guardado y las recomendaciones, "
              "pendientes de resolución.",
         exc=["1. No hay modelo vigente.",
              "2. El horizonte excede el máximo configurado.",
              "3. Un punto carece de historial suficiente.",
              "4. Un punto no tiene capacidad instalada registrada: no se "
              "evalúa el desborde."]),
    dict(n=29, nombre="Consultar alertas y recomendaciones logísticas",
         rf="RF24", paq=7, actores=[SUP, CDD, ADM], pri="Alta", riesgo="Medio",
         ini="Supervisor de Recolección",
         proposito="Revisar las alertas tempranas y las recomendaciones emitidas "
                   "con su evidencia.",
         desc="El usuario consulta las alertas y recomendaciones de los "
              "sectores a su alcance, con su urgencia, su evidencia y su estado: "
              "el supervisor ve las de sus sectores; el directivo y el "
              "administrador, todas.",
         pre="El usuario inició sesión con permiso para ver las "
             "recomendaciones.",
         proceso=["1. El usuario accede a Alertas y recomendaciones.",
                  "2. El sistema muestra las alertas y recomendaciones de su "
                  "alcance ordenadas por urgencia.",
                  "3. El usuario filtra por estado, sector o tipo.",
                  "4. El usuario abre una recomendación y el sistema muestra su "
                  "evidencia (predicción, capacidad y tendencia).",
                  "5. Si tiene permiso para resolverla, puede extender con CU30."],
         post="El usuario conoce las alertas y recomendaciones vigentes.",
         exc=["1. No hay recomendaciones para los filtros."]),
    dict(n=30, nombre="Atender recomendación logística", rf="RF24", paq=7,
         actores=[SUP, ADM], pri="Alta", riesgo="Medio",
         ini="Supervisor de Recolección",
         proposito="Aceptar o descartar cada recomendación dejando constancia.",
         desc="El supervisor revisa las recomendaciones de sus sectores con su "
              "evidencia y las acepta o descarta con motivo; las aceptadas se "
              "incorporan a la próxima jornada.",
         pre="Existen recomendaciones pendientes en sectores del supervisor.",
         proceso=["1. Desde CU29, el supervisor selecciona una recomendación "
                  "pendiente.",
                  "2. El sistema muestra su evidencia.",
                  "3. El supervisor acepta o descarta e indica el motivo.",
                  "4. Si acepta, el sistema incorpora el punto a la próxima "
                  "jornada planificada del sector.",
                  "5. El sistema registra el evento en la bitácora de auditoría."],
         post="La recomendación queda resuelta y, si se aceptó, incorporada.",
         exc=["1. La recomendación ya fue resuelta.",
              "2. Falta el motivo.",
              "3. El sector no está asignado al supervisor."],
         extiende=(29, "el supervisor resuelve una recomendación pendiente")),

    # ======================= Paquete 8 =======================
    dict(n=31, nombre="Configurar periodos académicos y parámetros", rf="RF25",
         paq=8, actores=[ADM], pri="Media", riesgo="Medio",
         ini="Administrador del Sistema",
         proposito="Ajustar el comportamiento analítico y predictivo sin tocar "
                   "el código.",
         desc="El administrador define los periodos académicos y modifica los "
              "parámetros globales: umbral crítico, mínimo para entrenar, umbral "
              "de desempeño, horizonte máximo, periodicidad del ETL y enlace de "
              "Power BI.",
         pre="El administrador inició sesión con permisos de administración.",
         proceso=["1. El administrador accede a Parámetros.",
                  "2. El sistema muestra los valores vigentes.",
                  "3. El administrador modifica un parámetro; el sistema valida "
                  "el rango y lo aplica.",
                  "4. El administrador registra un periodo académico con sus "
                  "fechas; el sistema valida que no se superponga.",
                  "5. El sistema registra el evento en la bitácora de auditoría."],
         post="Los parámetros y periodos quedan aplicados a las siguientes "
              "ejecuciones.",
         exc=["1. Valor fuera de rango.",
              "2. Periodos superpuestos."]),
    dict(n=32, nombre="Consultar bitácora de auditoría", rf="RF26", paq=8,
         actores=[ADM], pri="Media", riesgo="Bajo",
         ini="Administrador del Sistema",
         proposito="Revisar quién hizo qué y cuándo.",
         desc="El sistema registra de forma automática e inalterable cada "
              "operación que modifica datos, cada acceso y cada denegación, con "
              "usuario, fecha, operación, entidad y valores antes y después. El "
              "usuario filtra la bitácora por usuario, fecha, módulo y tipo de "
              "operación y consulta el detalle de cada registro.",
         pre="El usuario tiene permiso de auditoría.",
         proceso=["1. El usuario accede a la bitácora.",
                  "2. El usuario aplica los filtros.",
                  "3. El sistema muestra los registros.",
                  "4. El usuario selecciona uno y el sistema muestra los valores "
                  "anteriores y nuevos."],
         post="El usuario obtiene la traza solicitada.",
         exc=["1. No hay registros para los filtros.",
              "2. Se intenta modificar o borrar un registro: la base de datos "
              "lo rechaza (disparador)."]),
    dict(n=33, nombre="Generar reporte", rf="RF27", paq=8,
         actores=[ADM, SUP, CDD], pri="Media", riesgo="Medio",
         ini="Administrador del Sistema",
         proposito="Emitir reportes operativos y gerenciales.",
         desc="El usuario elige el tipo de reporte (generación por sector, por "
              "tipo, cumplimiento de jornadas, incidencias, indicadores, "
              "generación proyectada) y los filtros; el sistema lo presenta en "
              "pantalla para imprimir o exportar.",
         pre="Existe información para el periodo y filtros.",
         proceso=["1. El usuario accede a Reportes y elige el tipo.",
                  "2. El usuario define fechas y filtros.",
                  "3. El sistema consolida la información (el supervisor solo "
                  "sus sectores).",
                  "4. El sistema presenta el reporte en pantalla.",
                  "5. El usuario puede imprimirlo o extender con CU34 Exportar "
                  "reporte a Excel o PDF."],
         post="El reporte queda generado en pantalla.",
         exc=["1. No hay información para el periodo.",
              "2. El rango de fechas es inválido."]),
    dict(n=34, nombre="Exportar reporte a Excel o PDF", rf="RF27", paq=8,
         actores=[ADM, SUP, CDD], pri="Media", riesgo="Bajo",
         ini="Administrador del Sistema",
         proposito="Obtener el reporte como archivo con encabezado institucional "
                   "para archivarlo, compartirlo o imprimirlo.",
         desc="El usuario elige el formato: Excel (.xlsx), con encabezado y "
              "tabla con formato, o PDF, con encabezado, tabla y pie de página "
              "numerado. El archivo lleva el encabezado de la DSU, la fecha de "
              "emisión y el usuario, y la emisión queda registrada.",
         pre="El reporte está generado en pantalla.",
         proceso=["1. El usuario selecciona el formato (Excel o PDF).",
                  "2. El sistema escribe el encabezado institucional y la tabla "
                  "con sus totales.",
                  "3. En PDF, el sistema numera las páginas.",
                  "4. El sistema registra la emisión en la bitácora de auditoría.",
                  "5. El navegador descarga el archivo."],
         post="El archivo queda descargado y la emisión registrada.",
         exc=["1. El volumen excede el máximo admitido para exportar.",
              "2. Error al generar el archivo."],
         extiende=(33, "el usuario solicita exportar")),
]

for c in CU:
    c.setdefault("incluye", [])
    c.setdefault("extiende", None)
    c.setdefault("especializa", None)

CU_POR_N = {c["n"]: c for c in CU}


def etiqueta(n):
    return "CU%d. %s" % (n, CU_POR_N[n]["nombre"])


def nombres_actores(c):
    return ", ".join(ACTORES[a]["nombre"] for a in c["actores"]) or "—"


def actores_efectivos(c):
    """Actores de un CU; si no tiene asociacion directa, los del CU que lo
    activa (base del extend, padre de la especializacion o quien lo incluye)."""
    if c["actores"]:
        return c["actores"]
    if c["extiende"]:
        return actores_efectivos(CU_POR_N[c["extiende"][0]])
    if c["especializa"]:
        return actores_efectivos(CU_POR_N[c["especializa"]])
    return []


assert len(CU) == 34 and [c["n"] for c in CU] == list(range(1, 35))
assert all(1 <= c["paq"] <= 8 for c in CU)
# ningun CU aislado: o tiene actor, o lo incluye otro, o extiende/especializa
_incluidos = {i for c in CU for i in c["incluye"]}
assert all(c["actores"] or c["n"] in _incluidos or c["extiende"] or c["especializa"]
           for c in CU), "hay un caso de uso aislado"
assert all(any(a in c["actores"] for c in CU) for a in ACTORES), "hay un actor sin CU"
assert all(c["actores"] for c in CU), "hay un caso de uso sin actor"
