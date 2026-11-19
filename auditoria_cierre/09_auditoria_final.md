# Auditoría final del cierre local DSU y Residata

## Veredicto

Se ejecutaron correcciones de código, pruebas, finanzas, documentación y preparación de publicación. No es otra auditoría sin implementación. El piloto funciona en el recorrido aislado probado; no se declara 100 % de los trece puntos ni lanzamiento comercial completo. Resultado académico/local: 8 CUMPLE, 5 PARCIAL y 0 NO CUMPLE, según 02_matriz_13_requisitos.md.

La hoja con 68 puntos era de otro grupo. No se usa como nota del proyecto. La autoría individual de Carlos previa a la unificación sigue NO VERIFICABLE con el Git disponible. Las responsabilidades declaradas en PAPS no se convierten en autoría de cada función.

## Evidencia nueva

- Regresión PostgreSQL aislado: 58 pruebas, 0 fallos, 0 errores, 172.475 segundos; regresion_final.xml/json/txt.
- Antes de corregir: cinco fallos en reproduccion_controlada.xml y un fallo de precisión en reproduccion_precision.xml. Se conservan los errores del primer arnés como tales, no se ocultan.
- Demo: 16 pantallas de cuatro roles, login UI real y flujo integrado por API en el navegador de prueba; demo_ui/resultados.json. No se dice que cada formulario se haya rellenado manualmente.
- Carga: 12 hilos HTTP, 60 s, 531 peticiones, 0 errores y 156 vaciados confirmados/persistidos; carga_12_usuarios.txt. Son clientes virtuales con identidades compartidas, no doce participantes reales.
- Rendimiento: 500 puntos añadidos y más de 100.000 registros; todas las filas con límite del comando cumplieron localmente. Ver valores exactos y recuentos de rollback en rendimiento_local.txt/json. API en proceso local, sin red Azure–Neon; no certifica RNF productivos.
- Restauración: dump sintético restaurado en otra base local, coincidencia de todas las tablas, claves foráneas validadas y trigger activo; restauracion.json. No restaura producción ni mide RTO institucional.
- Sitio: 16 recorridos a 1440 y 390 px y seis escenarios de función de salud. No se enviaron formularios reales.
- Caja blanca: matrices, aristas, E−N+2, P+1 e independencia verificados para CU9, CU15 y CU28; caja_blanca_verificada.json. Es el modelo de mensajes, no cobertura total del código Python.
- EA: tres archivos abiertos por API, sin guardar cambios; enterprise_architect_todos.json.
- Finanzas: siete comprobaciones y conciliación de web/pitch/documento; finanzas.json. Déficit Bs 162.817, capital propuesto Bs 200.000, VAN operativo Bs 120.674 y TIR operativa 42,7 %. Son proyecciones.
- Documento: 298 páginas, trece carátulas, cero páginas vacías, campos rotos o elementos fuera de página detectados. Exportación Word nativa y muestreo visual de PNG; revisión.json vincula hashes de Word y PDF. El renderer empaquetado falló por LibreOffice ausente; no se afirma que ese método funcionó.

## Fases y criterios de aceptación

|Fase|Estado|Criterios aprobados y evidencia|Criterios pendientes / siguiente acción|
|---|---|---|---|
|0 Inventario y recuperación|COMPLETA|Rama, commit base, respaldo privado con SHA256; matrices 27 RF y 46 RNF/RTR/RCM.|No usar el patch privado como entregable; contiene configuración privada.|
|1 Calidad del producto|PARCIAL|Seis defectos reproducidos corregidos, transacción de auditoría y concurrencia de personal/vehículo; regresión y demo aprobadas.|Hilos web no durables; recorrido de todos los formularios/variantes y producción institucional no cerrado. Riesgo interno explícito.|
|2 Sitio y marketing|PARCIAL|Versión local, rutas, responsive, salud, pitch y material preparados.|Publicación a cargo del titular; URL corporativa recuperada a 200, pero aún con contenido anterior a corregir.|
|3 Pruebas y seguridad|PARCIAL|Suite, caja blanca, errores negativos, carga, precisión, restauración y navegador aprobados en entorno aislado.|ZAP disponible es histórico y pasivo; no se repitió pentest ni toda la matriz de navegadores/RNF productivos.|
|4 Infraestructura y puesta en marcha|PARCIAL|Runbook Azure, CI revisado, rollback preparado, restauración sintética y salud de solo lectura.|No se desplegó la rama; copia independiente y recuperación productiva sin evidencia nueva.|
|5 Legal|PARCIAL|Capítulo coherente, inventario de licencias y borradores/matriz listos.|Formalización, revisión competente, convenio y firmas reales: PENDIENTE EXTERNO.|
|6 Mercado y financiamiento|PARCIAL|Cálculos, descuento anual, escenarios, capital, valoración y pitch conciliados.|Demanda, precios aceptados y capacidad por cliente no validados; no inventar entrevistas.|
|7 PAPS/PUDS/SQAP/CASE|COMPLETA|Documentación preservada y actualizada, normas sin certificación ficticia y modelos nativos comprobados.|No acredita ejecución de todas las revisiones previstas ni autoría individual completa.|
|8 Entrega unificada|PARCIAL|Word/PDF de 13 capítulos, manuales, pitch, código sin .env real y manifiesto del paquete.|Los QR/URLs responden, pero enlazan una versión pública anterior; revisión final humana de consigna original aconsejada.|
|9 Defensa y aceptación|PARCIAL|Guion, preguntas difíciles, demo reproducible, matrices y formatos preparados.|Ensayo oral de los integrantes y aceptación/firma institucional no realizados.|

Cada fase conserva rollback en el commit base y respaldo privado descritos en 00_inventario_y_linea_base.md; no hay commits ni push del cierre. Los nuevos archivos son identificables en esta rama. No se ejecutó restauración, seed, entrenamiento ni pruebas con escritura contra Neon.

## Cambios principales y archivos

- config/concurrencia.py: bloqueos transaccionales PostgreSQL entre workers sin nuevas tablas.
- operations/serializers/jornada.py: sector y ruta existente coherentes; services/jornada.py: asignación serializada.
- analytics/services/etl.py: reenvíos entre tandas y normalización Decimal; tests de error binario.
- prediction/services/entrenamiento.py: arranque y numeración de versiones serializados.
- audit/views/base.py: alta/edición y bitácora en la misma transacción; prueba de reversión.
- scripts/carga.py: HTTP 4xx ya no se cuentan como éxito y el script devuelve error si incumple criterios.
- sitio-residata/js/site.js: respuestas 404/500 y opacas no se declaran servicio sano; propuesta comercial sin factura habilitada ficticia.
- sitio-residata/preparar_publicacion.py y publicar.sh: solo recursos públicos y proyecto previamente vinculado, sin cambio automático de alias.
- DocumentoSoftware2/finanzas.py y ensamblar.py: descuento anual, escenarios, financiación y trece capítulos con matrices y QR.
- .github/workflows/ci.yml: CD espera tres jobs, exige dos secretos y reintenta salud; no se ejecutó un despliegue.

Las rutas de código anteriores son relativas a gestion-residuos-dsu/backend salvo las que nombran otra carpeta. El paquete incluye código actualizado sin historial ni configuración privada. backend/.env sigue siendo la excepción autorizada en el repositorio privado; no debe publicarse el repositorio sin aplicar la rotación/limpieza acordadas.

## Bloqueos y trabajo que no se oculta

Solo los trámites, cuentas, autorizaciones y firmas de terceros se listan en 07_pendientes_externos.md. Internamente siguen pendientes una solución durable para tareas largas, comprobación productiva de capacidad/latencia, automatización de todos los formularios y revisión completa de obligaciones de licencias. El proyecto se entrega como piloto funcional con estas limitaciones, no como SaaS multiempresa terminado.

La actualización pública la realizará el titular por instrucción explícita. El sitio pasó de 404 a HTTP 200 en una reverificación de once rutas/recursos, sin despliegue del agente; siguen públicas la oferta no corregida y la ronda anterior. No se le pide otra autorización para el mismo trabajo local. No se han enviado mensajes, celebrado contratos, registrado entidades, comprado suscripciones ni atribuido resultados del otro grupo.
