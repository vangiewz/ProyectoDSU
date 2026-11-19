# Estado del proyecto

Última actualización de contexto: 2026-11-16. Este archivo vive en la carpeta backend del repositorio unificado ProyectoDSU y cubre todo el sistema (backend y frontend). Las verificaciones anteriores conservan sus fechas; las comprobaciones nuevas se detallan a continuación.

## Cierre local de Software II (18–19/11/2026)

Se trabaja en rama cierre-software2-20261118, con respaldo privado verificable de los cambios anteriores y sin commits/push. Bitácora y auditoría: ../../../auditoria_cierre/04_bitacora_cambios.md y 09_auditoria_final.md. La hoja del examen era de otro grupo, no es nota de DSU.

- Regresión nueva: 58 pruebas aprobadas en PostgreSQL 18 local aislado, incluyendo cambio de sector/ruta, concurrencia real de ETL/modelo y asignación de personal/vehículo, reenvíos entre tandas, precisión Decimal y reversión ante fallo de bitácora. Se preservaron las reproducciones fallidas anteriores.
- Demo aislada: 16 pantallas y flujo API completo con persistencia; carga 12 hilos por 60 s, 531 peticiones sin errores, 156 vaciados confirmados y guardados. No es una prueba de doce personas ni de la VM productiva.
- Medición local con más de 500 puntos y 100.000 registros cumplió límites medidos, con rollback comprobado; no incluye red Azure–Neon. Dump/restauración exclusivamente sintéticos con recuentos, claves y trigger comprobados.
- Sitio local: 16 recorridos responsive, salud sin falsos positivos 404/500 y oferta comercial marcada propuesta. La URL pública devolvió inicialmente 404 y luego 200 en once rutas/recursos, sin despliegue del agente; aún publica cifras/oferta anteriores. El titular decidió publicar personalmente.
- Se leyeron por API nativa los tres modelos EA, sin guardarlos. Word/PDF de Software II integra trece capítulos, matrices, evidencias y financiamiento; Taller no se regeneró ni se modificó.
- Proyección revisada: mezcla mitad anual (diez meses), mitad mensual. Capital propuesto Bs 200.000, VAN operativo Bs 120.674, TIR operativa 42,7 %. No son inversión conseguida ni rendimiento garantizado.
- Permanecen internos: hilos web sin cola durable, verificación productiva completa y revisión de obligaciones de terceros. Pendientes externos: publicación por titular, Power BI publicado, trámites/firmas y validación institucional. No se escribió en Neon ni se desplegó esta rama.

## Arranque y comprobaciones locales (18/11/2026)

- Se guardó `backend/.env` con los valores proporcionados expresamente por el titular, sin reproducirlos en documentación. Se preparó `.venv` local con Python 3.13 disponible en este equipo (el stack documentado usa Python 3.12), se instalaron dependencias y se recopilaron estáticos. Backend en `127.0.0.1:8000` y frontend en `127.0.0.1:5173`.
- Django `check`, `migrate --check` (solo comprobación, sin aplicar migraciones) y `pip check` terminaron correctamente. Neon respondió a consultas; el usuario Power BI leyó 15.430 hechos. El modelo vigente v2 cargó sin advertencias y ejecutó una inferencia local sin persistir predicciones.
- Comprobaciones por HTTP a través del proxy Vite: login y perfil de los cinco usuarios demo, consulta de jornadas por rol, 23 consultas de módulos con Administrador, seis vistas previas de reportes, exportaciones PDF/XLSX válidas y comparación con fechas explícitas. Respuestas esperadas: 403 para Usuarios con Directivo y 401 sin autenticación. Los accesos y exportaciones generan su auditoría normal; no se ejecutaron seed, ETL, entrenamiento ni cambios de datos operativos.
- `npm audit fix` actualizó el lockfile, incluido Vite de 8.3.2 a 8.3.8. Build y lint finalizaron correctamente y npm audit informó cero vulnerabilidades. Persisten nueve advertencias de lint y el aviso de tamaño del bundle; Node 22.16.0 local es anterior al mínimo 22.22.0 declarado por React Router, aunque el arranque y build comprobados funcionaron.
- Chrome abrió la aplicación y mostró el formulario de acceso. La automatización no pudo completar el clic por `coordinate input geometry is unavailable`; no se acredita una revisión visual de todos los módulos ni de los flujos de escritura. Las comprobaciones funcionales anteriores son de API y lectura.
- Power BI: credenciales SQL verificadas, pero el enlace del informe publicado en Parámetros está vacío; sigue pendiente publicar/configurar el informe insertado.
- Azure CLI autenticado en Azure for Students; consulta de la VM `dsu-api` en `residata-dsu-rg`, México Central, con aprovisionamiento `Succeeded`. No se realizaron commits ni despliegues en esta sesión.

## Despliegue en producción (18/11/2026)

- API desplegada en **Azure VM** `dsu-api` (Standard_B2als_v2, Ubuntu 24.04, Mexico Central): `deploy/compose.azure.yml` (app Gunicorn, Caddy con Let's Encrypt, respaldo pg_dump diario 14 días), `.env` de producción solo en la VM (`~/dsu/backend/.env`), cron horario del ETL. URL: https://dsu-uagrm-api.mexicocentral.cloudapp.azure.com. AWS quedó descartado (la suscripción disponible es Azure for Students; regiones permitidas: EE. UU., Canadá, México).
- Frontend en Vercel (`dsu-uagrm`, `VITE_API_URL` configurada): https://dsu-uagrm.vercel.app. CORS de la API: solo ese origen.
- Monitoreo: Application Insights `residata-monitor` (prueba de disponibilidad de la API cada 15 min) y alertas de CPU, memoria y disponibilidad por correo.
- Suite: 50 pruebas sin fallos (nuevo `operations/tests/test_registro_caminos.py`, caminos de RF8); CI en `.github/workflows/ci.yml`.
- Latencia observada: login 4,8–6,9 s y carga de pantallas 3,4–7,3 s desde el navegador (VM en México, Neon en São Paulo).

## Auditoría de fase final (16/11/2026)

- La arquitectura productiva prevista es frontend Vercel, API en AWS EC2 Linux/Docker en São Paulo y PostgreSQL gestionado por Neon. Hay configuración revisable en `deploy/compose.aws.yml` y `deploy/Caddyfile`; no se ha acreditado despliegue remoto. El compose local publica el puerto de API solo en loopback.
- Regresión: **42 pruebas aprobadas** contra PostgreSQL 18 desechable desde Windows y repetidas desde la imagen Linux construida. No se sembró, entrenó ni alteró Neon para estas comprobaciones. Se añadieron escenarios de asignación, predicción, alcance, revocación JWT, cabeceras y CORS. Evidencias sanitizadas: `../../../docs/auditoria-fase-final/pruebas/` y `pruebas_linux/`.
- Seguridad: ZAP baseline pasivo en un entorno aislado, con acceso autenticado comprobado. Se añadieron cabeceras en la API y en `frontend/vercel.json`, y exclusiones `.env.*` en la imagen. La imagen inspeccionada no contiene `.env`. Persisten advertencias documentadas; no se declara pentest completo ni ausencia de vulnerabilidades.
- Pantallas: 25 combinaciones de rol/ruta en 1440 y 390 px (50 capturas), datos sintéticos aislados y cabeceras de Vercel reproducidas localmente. Sin errores JS, violaciones CSP ni desbordamiento general. El directivo recibe «Sin acceso» en Usuarios. Se conservaron las cancelaciones `ERR_ABORTED` de teselas durante el ajuste del mapa; las capturas muestran cartografía cargada. Esta revisión de carga/lectura no sustituye todos los flujos interactivos ni el despliegue real.
- Power BI: servidor real configurado y conexión TLS verificada por SQL con el rol `powerbi`: lectura de seis vistas, 15.430 hechos; predicciones actuales vacías. Su contraseña se renovó por autorización del usuario y quedó exclusivamente en `backend/.env` (`POWERBI_*`), sin cambiar la del backend. Desktop pudo capturarse y abrirse; El titular autenticó Desktop y se verificaron las seis vistas cargadas: sus recuentos coinciden con SQL; se conservan capturas en `../../../Paquete_PowerBI_DSU/02_capturas/`. Se amplió el gráfico existente y se alinearon las siete tarjetas del diagrama; 16/11/2026 (tarde): las 16 medidas se auditaron contra SQL de solo lectura y coinciden (`../../../docs/auditoria-fase-final/powerbi_medidas.json`); `powerbi/tablero.py` agregó a la página Tablero cuatro tarjetas, segmentadores de fecha y sector, barras por sector/tipo/punto, evolución mensual (columna calculada `Calendario[Año-Mes]`) y la matriz sector × periodo. El titular lo abrió en Desktop y capturó la página completa (119,25 mil kg, igual al SQL); esa captura es la figura de CU21 del documento. Faltan RLS y publicar. El guardado de Desktop convirtió el informe al formato PBIR, conservando el gráfico existente y el modelo BIM. No regenerar con `powerbi/generar.py`. Evidencia: `../../../docs/auditoria-fase-final/powerbi_conexion.json`.
- Documento 1–10 en revisión y matriz de pendientes: `../../../docs/auditoria-fase-final/AUDITORIA.md`. El vigente contiene los capítulos 1–10; la copia anterior 1–7 se conserva como respaldo. Sin commits ni publicaciones.

## Contexto compartido y repositorio (15/11/2026)

- Proyecto único para Taller de Grado I y Software 2; PUDS confirmado para Software 2. Entregables propios de Software 2 pendientes, incluido SQAP. Ver [contexto raíz](../../../AGENTS.md) y [Software 2](../../../DocumentoSoftware2/CONTEXTO.md).
- Código, documentación, ejemplos, generadores y modelo UML reunidos en **vangiewz/ProyectoDSU**, privado. Backend y frontend son carpetas normales. Los remotos antiguos se conservan sin modificaciones; sus metadatos Git locales se respaldaron fuera del proyecto.
- Se mantiene **Neon**; la propuesta de migrar a PostgreSQL local fue descartada. Ambos integrantes comparten los datos demo existentes. No ejecutar seed, limpieza, restauración o entrenamiento para preparar un clon.
- El usuario solicitó incluir `backend/.env` en el repositorio privado. Antes de hacerlo público, rotar credenciales, retirar el archivo y limpiar el historial; eliminar solo la nota o el archivo no basta. Ver AGENTS.md.
- Esta unificación no cambia requisitos, lógica de negocio, documentos Word, diagramas ni datos de Neon.

## Resumen

Implementados **RF1–RF27**, incluido el componente predictivo (Random Forest con scikit-learn, app `prediction`). Backend con 20 tests en verde contra Neon; frontend compila y pasa el detector de impeccable. Las pantallas del módulo predictivo se revisaron en navegador (escritorio y 390 px); el resto del sistema aún no tiene revisión visual completa.

## Trazabilidad de requisitos funcionales

| RF | Requisito | Estado | Dónde |
|---|---|---|---|
| RF1 | Gestionar usuarios | ✅ | `accounts/views/user.py`, `pages/Admin.tsx` (Usuarios) |
| RF2 | Roles y permisos | ✅ | `accounts/views/role.py`, `pages/Admin.tsx` (Roles); roles sembrados en `operations/migrations/0002_roles.py` |
| RF3 | Autenticación y control de acceso | ✅ | `accounts/views/auth.py`, `accounts/permissions/` (rechazos a bitácora) |
| RF4 | Sectores y facultades | ✅ | `campus/views/sector.py`, `pages/Maestros.tsx` |
| RF5 | Puntos georreferenciados | ✅ | `campus/views/punto_recoleccion.py` (valida `CAMPUS_BBOX`), selector en mapa |
| RF6 | Tipos de residuo y unidades | ✅ | `catalogs/` (factor bloqueado si la unidad ya tiene registros) |
| RF7 | Contenedores | ✅ | `campus/views/contenedor.py` |
| RF8 | Registrar vaciado | ✅ | `operations/services/visita.py`, `pages/Campo.tsx` (≤4 interacciones) |
| RF9 | Histórico de residuos | ✅ | `operations/views/registro_residuo.py` (totales por tipo), `pages/Registros.tsx` |
| RF10 | Incidencias | ✅ | `operations/views/incidencia.py` (registrar y atender) |
| RF11 | Planificar jornadas y rutas | ✅ | `operations/serializers/jornada.py`, `pages/Jornadas.tsx` (NuevaJornada) |
| RF12 | Ejecución de la recolección | ✅ | `operations/services/jornada.py` (abrir, omitir, cerrar, resumen), eje 08:00–15:00 |
| RF13 | Asignar personal y vehículos | ✅ | `services.jornada.asignar` (valida superposición por turno) |
| RF14 | Historial de recolecciones | ✅ | `JornadaViewSet` con filtros y cobertura |
| RF15 | ETL | ✅ | `analytics/services/etl.py`, comando `etl`, `pages/Sistema.tsx` (ProcesoETL) |
| RF16 | Indicadores (KPI) | ✅ | `analytics/services/indicadores.py`, `pages/Tablero.tsx` |
| RF17 | Tableros interactivos | ✅ | `pages/Tablero.tsx` (clic en sector/tipo filtra todo; clic en punto abre su detalle) + Power BI: vistas `bi_*` y proyecto `powerbi/DSU-Residuos.pbip` (RD8), insertado en la pestaña Power BI |
| RF18 | Comparar periodos y tendencias | ✅ | `indicadores.comparar` / `tendencia_creciente` |
| RF19 | Puntos en mapa interactivo | ✅ | `pages/MapaCampus.tsx` (marcadores) |
| RF20 | Mapa de calor | ✅ | `pages/MapaCampus.tsx`: capa observada y proyectada (`/api/predicciones/mapa/`) |
| RF21 | Filtros del mapa | ✅ | `components/FiltrosAnalisis.tsx` |
| RF22 | Entrenar y evaluar Random Forest | ✅ | `prediction/services/entrenamiento.py`, comando `entrenar`, `pages/Modelo.tsx` (versiones, métricas, importancias, publicar/revertir) |
| RF23 | Predecir generación futura | ✅ | `prediction/services/prediccion.py`, `pages/Prediccion.tsx` (siempre con margen de error) |
| RF24 | Alertas y recomendaciones | ✅ | `prediction/services/recomendaciones.py`, `pages/Recomendaciones.tsx` (aceptar/descartar con motivo; la aceptada entra en la próxima jornada) |
| RF25 | Catálogos y parámetros | ✅ | `catalogs/models/parametros.py`, `pages/Sistema.tsx` (ParametrosPage) |
| RF26 | Bitácora de auditoría | ✅ | `audit/` (trigger PostgreSQL inalterable) |
| RF27 | Reportes exportables | ✅ | `analytics/services/reportes.py`: Excel, PDF e impresión; incluye *Generación proyectada* |

Tests: `backend/apps/accounts/tests/`, `backend/apps/operations/tests/`, `backend/apps/analytics/tests/`, `backend/apps/prediction/tests/`.

## Decisiones tomadas (con el usuario)

| Fecha | Decisión | Motivo |
|---|---|---|
| 2026-10-04 | Patrón **MVC** (el documento no fija uno) con capas de la Figura de arquitectura | Pedido del usuario |
| 2026-10-04 | **Tailwind** para estilos | El documento no nombra framework CSS; pedido del usuario |
| 2026-10-04 | Base de datos en **Neon** (URL solo en `backend/.env`) | Provista por el usuario |
| 2026-10-04 | Backend con **paquetes por entidad** en cada app | Pedido explícito del usuario para orden |
| 2026-10-04 | Mundo visual **"Planilla de control sellada"**, rojo DSU como marca | Elegido por el usuario en la ronda de impeccable |
| 2026-10-05 | Tableros **en el sistema y además** vistas SQL para Power BI | Elección del usuario |
| 2026-10-05 | ETL **sin infraestructura extra**: comando + cron + hilo a pedido | Elección del usuario |
| 2026-10-05 | Reportes en **Excel + PDF** | Elección del usuario |
| 2026-10-04 | Una jornada cubre **un sector**; turnos Mañana/Tarde/Noche | Interpretación propia (RF11 dice "sectores"; la DSU trabaja en turno único 08:00–15:00). Revisar con el usuario si se necesita multisector |
| 2026-10-05 | Punto crítico = promedio diario en kg > `umbral_critico_kg_dia` | Definición propia para RF16/RF20; configurable |
| 2026-10-05 | Tendencia creciente = 4 meses consecutivos al alza | Definición propia para RF18 |
| 2026-10-05 | **Sin LLM/Ollama en el sistema**: la IA es solo el Random Forest; recomendaciones por reglas y plantillas | Elección del usuario (no exige GPU en producción, auditable, RNF13) |
| 2026-10-05 | Datos de entrenamiento de demo: `seed --historico` (un año sintético en la BD demo de Neon) | Elección del usuario; borrar con el resto de datos demo antes de producción |
| 2026-10-05 | Observación del modelo = kg por punto × tipo × día; variables: sector, punto, tipo (OrdinalEncoder), promedio 28 días previos, visitas/semana, día semana, día mes, mes, semana, en periodo académico | Interpretación de RF22 |
| 2026-10-05 | Margen de error = RMSE de prueba por estimación diaria; agregados por raíz de suma de cuadrados | Definición propia para RF23/RNF13 |
| 2026-10-05 | Entrenamiento en hilo + comando (igual que el ETL), sin Celery/Redis | Coherente con la decisión del ETL; Celery no corre en Windows |
| 2026-10-05 | Reglas RF24: desborde antes de la próxima atención → priorizar; máx. diario ≥ capacidad → contenedores; crecimiento ≥ umbral → frecuencia; % no aprovechable ≥ umbral → separación. Umbrales en `ParametrosSistema` | Definición propia |
| 2026-10-05 | Estimaciones se muestran "a lápiz" (token `--color-lapiz`, `components/Estimado.tsx`), nunca en azul bolígrafo | Distinguir lo estimado de lo medido (RNF13) dentro del mundo visual |
| 2026-10-30 | Rol **Administrativo integrado al Administrador** (`operations/0003`); el Administrador **pierde las acciones de campo** (registrar vaciados, abrir/cerrar jornadas, reportar/atender incidencias: `operations/0004`), como dice su tabla de características en el cap. 4. Quedan 4 roles = 4 actores del documento | Revisión de actores de la Fase 2 (usuario) |
| 2026-10-30 | `ParametrosSistema.actualizado_por` (FK a User, `catalogs/0005`): el registro de configuración guarda quién lo cambió por última vez, además de la bitácora. `Reporte` guarda `solicitado_por` y `emitido_en`, y el encabezado institucional es su método `encabezado(alcance)` | Diagramas del documento sin elementos sueltos y diseño igual al código |

## Limitaciones conocidas (marcadas con `ponytail:` en el código)

- `frontend/src/lib/api.ts`: tokens JWT en localStorage. Pasar a cookie httpOnly si se endurece la seguridad.
- `analytics/services/etl.py`: duplicados detectados solo dentro de la misma tanda del ETL.
- `analytics/services/etl.py` y `prediction/services/entrenamiento.py`: ETL y entrenamiento a pedido corren en un hilo del proceso web (RD10). Pasar a una cola de tareas si compiten por CPU con la operación.
- `prediction/models/modelo_entrenado.py`: el artefacto (~3,6 MB por versión con el histórico demo) vive en la BD; copia local en `MODELOS_DIR`.
- `prediction/services/datos.py`: al predecir a varios días se usa la historia de 28 días a hoy para todo el horizonte (el modelo se entrena como si fuera a 1 día); puede ser algo optimista a 30 días.
- Las predicciones solo cubren los días de la semana en que el punto tuvo registros en las últimas 8 semanas.
- Desactivar un punto pide el motivo con `window.prompt` (`components/Crud.tsx`); se puede cambiar por un campo en línea.
- La captura en campo no guarda registros sin conexión: informa el error y conserva el formulario (RI17), pero no encola.

## Próximos pasos sugeridos (en orden)

1. **Power BI:** abrir `powerbi/DSU-Residuos.pbip` en Power BI Desktop, *Actualizar* y revisar los visuales que dejó `powerbi/tablero.py`; luego definir RLS si corresponde, publicar y pegar el enlace en *Parámetros → Power BI*.
2. **Rendimiento:** ver [RENDIMIENTO.md](RENDIMIENTO.md). Cumplen RTR1–RTR10 y RTR12/RCM7; **RTR11 (500 puntos) no cumple desde la PC de desarrollo** (30–40 s). Repetir desde el servidor en `sa-east-1` y correr `scripts/carga.py` (RNF4/RCM1/RCM2) allí o en una rama de prueba de Neon.
3. **Revisión visual** del resto de pantallas (las del módulo predictivo y el Tablero ya se revisaron) y *finish review* de impeccable. `DESIGN.md` ya existe en el frontend.
4. **Repositorio unificado ProyectoDSU** (decisión del 15/11/2026): reemplaza el plan anterior de compartir dos repositorios. El despliegue continúa separado: raíz `gestion-residuos-dsu/backend` para Docker y `gestion-residuos-dsu/frontend` para Vercel. La prueba de Docker documentada es del 07/10/2026; configurar `CORS_ALLOWED_ORIGINS` y `VITE_API_URL` al desplegar.
5. **Validar el modelo con datos reales** de la DSU: las métricas actuales son sobre histórico sintético.
6. **Antes de producción:** limpiar datos demo e histórico sintético, rotar la credencial de Neon, servidor en la misma región que Neon, `DEBUG=False`, TLS, cron del ETL, `RESPALDO_DATABASE_URL` directo y copia externa de `respaldos/`.

## Datos de demostración en Neon

`python manage.py seed --demo` creó: usuarios `supervisor`, `operario1`, `operario2`, `administrativo` (desde el 30/10/2026 con rol Administrador), `directivo` (contraseña demo documentada en el README), 4 sectores con 3 puntos cada uno y coordenadas **aproximadas no oficiales**, 2 vehículos y la jornada 1 (FICCT, 05/10/2026) en ejecución con un vaciado registrado. El usuario `admin` tiene contraseña propia (no versionada).

`python manage.py seed --historico` agregó (05/10/2026) un año **sintético**: 1040 jornadas cerradas, 15 428 vaciados, periodos académicos 2-2025, 1-2026 y 2-2026, y una jornada PLANIFICADA por sector para el 06/10/2026. Luego `etl` y `entrenar` dejaron las versiones v1 y v2 del modelo (v2 vigente) y se generaron dos lotes de predicción del supervisor (alerta de desborde en FCEE-P1, el "comedor" que el histórico hace crecer).


## Validación gráfica local — 19/11/2026

Chrome visible, cinco cuentas y PostgreSQL 18 propio: evidencias independientes en `../../../auditoria_gui/INFORME_FINAL.md`. Se recorrieron 34 CU; 28 flujos principales aprobados y 6 parciales. No se acredita cobertura exhaustiva. Se corrigieron validaciones de cantidades, auditoría M2M, límites BBOX, roles dinámicos y predictivos, mensajes 404, edición gráfica de planificación y respuestas asíncronas atrasadas. `npm run build` pasa; lint conserva nueve advertencias previas. No se modificó Neon ni se publicó. Consultar matrices y pendientes antes de sostener un 100 %.

Regresión final de esta validación: 74 pruebas aprobadas en PostgreSQL aislado (236,50 s). Evidencias: `auditoria_gui/regresion/`.


## Complemento móvil y cierre de materiales — 19/11/2026

Por pedido del usuario, se añadió `../movil/` (Flutter Android) sin alterar el Word/PDF académico. Usa la misma API HTTPS de Azure, cuenta y permisos. GPS puntual para sugerir y ordenar puntos permitidos por cercanía, confirmación del código, mapa e indicaciones y reporte de incidencias con dictado en español. No implementa fotos ni cola offline; no guarda coordenadas personales en Azure.

Ocho pruebas automáticas aprobadas y análisis Flutter sin incidencias. En Samsung Galaxy S23 por ADB se verificaron login supervisor, sesión restaurada, mapa y puntos, GPS/sugerencia; el usuario confirmó el dictado real. El botón de la app creó una única incidencia de prueba (ID 11, marca DSU-MOVIL-20261119-01), contrastada por GET y dejada ATENDIDA mediante la API. No se ejecutaron seed, ETL, entrenamiento ni migraciones. Evidencia sanitizada: `../../../auditoria_movil/resultado_dispositivo.json`.

CI ampliado a la rama `cierre-software2-20261118`, con análisis, pruebas y APK demo ARM64. El CD de API continúa limitado a main. Azure se inspeccionó por SSH: contenedor en ejecución identificado como 4980f79. La revisión de Residata aún requiere publicar los cambios desde la cuenta propietaria; no confundir un despliegue intentado con uno aprobado.

Se retiraron 980 copias idénticas solo de Entregables/versiones (109,9 MiB del árbol actual), preservando cada contenido único y el documento vigente. Índice SHA-256 y reconstrucción en esa carpeta. No se reescribió Git ni se retiraron las credenciales autorizadas del repositorio privado. Se preparó folleto PDF complementario y guía de Android. Las pruebas de frontend pasan con nueve advertencias previas de lint; no equivalen a una nueva prueba exhaustiva de producción.
