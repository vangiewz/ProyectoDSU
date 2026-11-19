# Validación funcional gráfica DSU / Residata

Fecha: 2026-11-19T01:08:30.849835. Chrome visible y perfiles efímeros. PostgreSQL 18 propio en loopback, datos sintéticos. No se escribieron datos en Neon ni producción. Sin commits ni publicación.

Se recorrieron por interfaz 34 de 34 CU. 28 tienen su flujo principal aprobado y 6 quedan parciales. Esto no acredita cobertura exhaustiva del 100 %. La fuente documental contiene 75 combinaciones CU/rol; 71 tienen al menos un recorrido con aserciones aprobado (94.7%). Esta cifra mide combinaciones con evidencia, no todas sus excepciones.

Último resultado por identificador y usuario: 242 recorridos, 240 aprobados, 2 no aprobados. Los errores del instrumento y expectativas corregidas se conservan en resultados; no deben contarse como defectos del producto. Residata: 33/33 recorridos a 1440, 820 y 390 px.

## Casos de uso

| CU | Nombre | Estado |
|---|---|---|
| CU01 | Iniciar sesión | FLUJO_PRINCIPAL_APROBADO |
| CU02 | Cerrar sesión | FLUJO_PRINCIPAL_APROBADO |
| CU03 | Gestionar usuarios | FLUJO_PRINCIPAL_APROBADO |
| CU04 | Gestionar roles y permisos | FLUJO_PRINCIPAL_APROBADO |
| CU05 | Gestionar sectores y facultades | PARCIAL |
| CU06 | Gestionar puntos de recolección | FLUJO_PRINCIPAL_APROBADO |
| CU07 | Gestionar contenedores | FLUJO_PRINCIPAL_APROBADO |
| CU08 | Gestionar tipos de residuo y unidades de medida | FLUJO_PRINCIPAL_APROBADO |
| CU09 | Registrar vaciado de residuos | FLUJO_PRINCIPAL_APROBADO |
| CU10 | Registrar incidencia operativa | FLUJO_PRINCIPAL_APROBADO |
| CU11 | Atender incidencia | FLUJO_PRINCIPAL_APROBADO |
| CU12 | Consultar histórico de residuos | FLUJO_PRINCIPAL_APROBADO |
| CU13 | Gestionar vehículos | FLUJO_PRINCIPAL_APROBADO |
| CU14 | Planificar jornada y ruta de recolección | FLUJO_PRINCIPAL_APROBADO |
| CU15 | Asignar personal y vehículos a la jornada | FLUJO_PRINCIPAL_APROBADO |
| CU16 | Ejecutar jornada de recolección | FLUJO_PRINCIPAL_APROBADO |
| CU17 | Omitir punto de la ruta | FLUJO_PRINCIPAL_APROBADO |
| CU18 | Cerrar jornada de recolección | FLUJO_PRINCIPAL_APROBADO |
| CU19 | Consultar historial de recolecciones | FLUJO_PRINCIPAL_APROBADO |
| CU20 | Ejecutar proceso ETL | PARCIAL |
| CU21 | Visualizar tablero interactivo | PARCIAL |
| CU22 | Comparar periodos e identificar tendencias | FLUJO_PRINCIPAL_APROBADO |
| CU23 | Visualizar puntos en el mapa interactivo | FLUJO_PRINCIPAL_APROBADO |
| CU24 | Generar mapa de calor | FLUJO_PRINCIPAL_APROBADO |
| CU25 | Filtrar mapa por periodo, sector y tipo de residuo | FLUJO_PRINCIPAL_APROBADO |
| CU26 | Entrenar y evaluar el modelo Random Forest Regressor | FLUJO_PRINCIPAL_APROBADO |
| CU27 | Publicar o revertir versión del modelo | FLUJO_PRINCIPAL_APROBADO |
| CU28 | Predecir generación futura y emitir alertas | FLUJO_PRINCIPAL_APROBADO |
| CU29 | Consultar alertas y recomendaciones logísticas | FLUJO_PRINCIPAL_APROBADO |
| CU30 | Atender recomendación logística | PARCIAL |
| CU31 | Configurar periodos académicos y parámetros | PARCIAL |
| CU32 | Consultar bitácora de auditoría | FLUJO_PRINCIPAL_APROBADO |
| CU33 | Generar reporte | PARCIAL |
| CU34 | Exportar reporte a Excel o PDF | FLUJO_PRINCIPAL_APROBADO |

## Correcciones verificadas

1. Capacidad no positiva de puntos: antes 500; ahora validación 400.
2. Capacidad no positiva de contenedores: antes 500; ahora 400.
3. Factor de conversión no positivo: antes 500; ahora 400.
4. Vehículos aceptaban capacidad cero/negativa: ahora 400; null sigue permitido.
5. Crear rol con permisos fallaba al auditar objetos Permission: relaciones ahora se auditan por ID.
6. Borde BBOX rechazado por comparar Decimal con float: comparación decimal consistente.
7. Usuarios solo ofrecía cuatro roles fijos: ahora carga los roles existentes y permite asignar roles sintéticos.
8. Editor de roles omitía prediction: permisos predictivos incorporados.
9. 404 de jornadas mostraba mensaje interno en inglés: respuesta clara en español.
10. Planificación carecía de edición gráfica: ruta protegida para editar fechas, sector y ruta antes de ejecución.
11. Respuesta atrasada sobrescribía reporte/filtros actuales: carga descarta respuestas anteriores; exportación espera la vista actual.

## Pendientes y límites

- Power BI: informe publicado, autenticación institucional y actualización real.
- Contacto: recepción real de correos; envío bloqueado por instrucción del usuario.
- Imprimir: diálogo nativo y resultado de impresión.
- Caída de PostgreSQL en medio de ETL.
- Todos los límites de cada parámetro y longitud de cada formulario.
- Doble clic/reenvío de todas las operaciones de escritura.
- Navegación con cambios sin guardar: no se verificó cada pantalla.
- Todos los enlaces y controles del pitch y material de marketing (se verificó carga, no cada interacción).
- Combinaciones CU/rol sin recorrido completo registrado en matriz_permisos_y_roles.json.
- Administrador resolviendo recomendaciones: documentación y permisos vigentes difieren; no se alteraron roles originales.

## Persistencia y evidencias

Altas, ediciones, estados, asignaciones, visitas, omisiones, incidencias, cierres, parámetros, versiones y decisiones se comprobaron tras recarga. Hay pruebas de logout/login y sesión renovada/expirada. Las cinco cuentas se usaron individualmente; las modificaciones de cuentas y roles se hicieron sobre usuarios sintéticos.

ETL: 2.000 entradas duplicadas preparadas como fixture por ORM local; ejecución por botón mostró 1.999 duplicados y bloqueó otro inicio concurrente. Entrenamiento: se comprobaron rechazo por volumen, rechazo por R², límites, entrenamiento concurrente, publicación y reversión. El fixture sin modelo vigente fue reversible y no se cuenta como operación de negocio por interfaz.

Reportes: nueve parejas Excel/PDF descargadas por botones, contrastadas contra 169 filas de los seis tipos iniciales y los reportes proyectados posteriores; consultar descargas/verificacion.json para los recuentos exactos, celdas y títulos. Las capturas y videos están en capturas/, videos/ y corporativo/. Inventario de controles observado en inventario_dom/, fuente estática en controles_fuente.json.

## Demostración académica

Están demostrados los ingresos por rol, CRUD autorizado, planificación y edición, asignación, operación de ambos operativos, incidencias, cierre, ETL, tableros, comparación, mapas, entrenamiento, predicción, recomendaciones del supervisor y descargas. Usar datos sintéticos y explicar que métricas del modelo no validan rendimiento con datos reales. La publicación sigue a cargo del titular.

## Reproducción

entorno.py levanta PostgreSQL y servidores propios. DSU_GUI_PASSWORD se suministra solo mediante variable de entorno. recorridos.py ejecuta fases en Chrome visible; corporativo.py bloquea tráfico externo. runtime/ contiene estado privado y se excluye de la entrega. No ejecutar contra la base compartida.

## Validación técnica complementaria

Build TypeScript/Vite aprobado; lint sin errores y nueve advertencias previas. Ruff aprobado en archivos de backend modificados. Regresión específica: 15 pruebas aprobadas antes de agregar la comprobación de 404 en español. La suite completa se registra en `auditoria_cierre/05_ejecuciones_pruebas/gui-completa.*`; su resultado no sustituye la evidencia GUI.


Resultado final de regresión completa: **74 pruebas aprobadas en 236,50 segundos**, PostgreSQL aislado. Evidencia copiada a `regresion/`. Build aprobado; lint con nueve advertencias previas; Ruff aprobado.

Los dos resultados gráficos no aprobados del consolidado son: intento de alta de sector por Supervisor (botón ausente por permisos; la consulta autorizada sí pasó) y resolución de recomendación por Administrador (documento la incluye, permisos vigentes no la habilitan). Se mantuvieron los roles originales. Los demás fallos anteriores del instrumento y los defectos corregidos están en los archivos históricos de resultados.
