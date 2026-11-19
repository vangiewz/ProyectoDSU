# Informe de revisión DSU y Residata

Fecha: 19/11/2026. Rama de trabajo: `cierre-software2-20261118`, siguiendo a `origin/cierre-software2-20261118`; commit revisado: `4980f79`.

El proyecto cubre manual de usuario, estándares de codificación, mapa, material de marketing y grabaciones de pruebas. Quedan pendientes la actualización comprobada de producción, funciones propias del celular y la organización del repositorio. Esta revisión no realizó despliegues, modificaciones de datos, limpieza, commits ni publicaciones.

| Solicitud | Estado | Resultado |
|---|---|---|
| Revisar despliegue correcto | Parcial | Servicios accesibles, recursos de app disponibles y CORS correcto; el pitch público conserva cifras anteriores. No se acredita que toda la última rama esté desplegada. |
| Incluir materiales en el repositorio | Cubierto en gran parte | Manual PDF/Markdown, marketing, pitch y 66 videos de pruebas empaquetados. No se identificó un folleto o tríptico independiente. |
| Algo simple para móvil con funciones del celular | Parcial | Interfaz adaptable y mapa existentes; sin integración localizada de GPS, cámara o micrófono. |
| Limpiar repositorio | Pendiente de organización | Exclusiones y paquetes divididos presentes; muchas versiones, respaldos documentales y evidencias repetidas. |
| Manual de usuario en el documento | Sí | Capítulo 12, sección 12.2, con acceso, campo, supervisión, consulta directiva y administración. |
| Estándar de codificación en el documento | Sí | Sección 3.9.3 y anexo I, con reglas generales, backend, frontend, base de datos y API. |

## Despliegue comprobado hoy

Solicitudes HTTPS de solo lectura:

- App: https://dsu-uagrm.vercel.app/ → 200. Sus archivos JavaScript y CSS referenciados también respondieron 200.
- Sitio: https://residata-bolivia.vercel.app/ → 200.
- Marketing: https://residata-bolivia.vercel.app/marketing/ → 200.
- Pitch: https://residata-bolivia.vercel.app/pitch/ → 200, con contenido financiero anterior: VAN aproximado Bs 212 mil, TIR 64,2 % y solicitud Bs 170000 en la descripción.
- API: https://dsu-uagrm-api.mexicocentral.cloudapp.azure.com/api/ y `/api/auth/me/` → 401 sin sesión, respuesta coherente con protección de acceso. La respuesta de `/api/auth/me/` acepta el origen de la app mediante CORS.

El cierre documental vigente registra VAN Bs 117027, TIR operativa 41,8 % y propuesta de capital Bs 200000. La diferencia demuestra que el pitch publicado no está actualizado. No permite identificar por sí sola la versión desplegada del backend o de toda la app.

No se hizo un recorrido autenticado nuevo, escritura en Neon, envío de formularios, comprobación de respaldos remotos ni inspección de Azure/Vercel. Las pruebas históricas no se presentan como pruebas nuevas. La disponibilidad puntual no acredita disponibilidad mensual.

El workflow `.github/workflows/ci.yml` ejecuta CI en pushes a `main`, pull requests y ejecución manual. El despliegue de API requiere push a `main` y secrets configurados. Un push directo a `cierre-software2-20261118` no activa ese CI por la configuración actual. Conviene incorporar esta rama a CI si será la base de trabajo, conservando una decisión explícita para publicar.

## Materiales existentes

- Manual por rol editable: `gestion-residuos-dsu/frontend/docs/MANUAL_USUARIO.md`.
- Manual PDF independiente: `Entregables/Material_Drive/04_Manual_de_Usuario.pdf`; existen además copias en paquetes e históricos.
- Marketing: tres imágenes en `DocumentoSoftware2/recursos/sitio/marketing-*.png` y página en `sitio-residata/marketing/index.html`.
- Pitch: `sitio-residata/pitch/index.html` y `sitio-residata/pitch/Residata_pitch.pdf`.
- Videos: `revision_documental_final/entrega/evidencias/Evidencias_GUI_DSU_Residata.zip.partes/` contiene dos partes, manifiesto e instrucciones de reconstrucción, todos versionados. Se verificaron los SHA-256 de ambas partes y del ZIP completo. Su índice contiene 683 entradas, incluidas 66 grabaciones `.webm`.

Los videos están guardados como evidencia de recorridos. Su presencia no acredita un video comercial editado, narrado o preparado para la defensa. No se encontraron archivos identificados por nombre como folleto, brochure o tríptico: el material confirmado son banners y publicaciones digitales. Se necesita decidir si ese formato satisface el pedido o preparar un folleto específico.

El acceso del docente al repositorio privado y a Drive sigue siendo un asunto separado de la existencia local de los archivos.

## Móvil

Existen la pantalla de operación `Campo.tsx`, mapas Leaflet/OpenStreetMap en `MapaCampus.tsx` y componentes compartidos, además de pruebas históricas de pantallas pequeñas. Un mapa navegable no implica acceso a la ubicación física del teléfono.

La búsqueda en `frontend/src` y `frontend/public` no localizó llamadas a geolocalización, captura de cámara/micrófono, grabación o reconocimiento de voz, ni registro de service worker. No se identificó una PWA instalable con trabajo sin conexión. La documentación de estado indica que campo conserva el formulario ante errores, pero no encola registros offline.

Como propuesta de alcance pequeño, se puede ampliar la misma aplicación con un botón «Mi ubicación» en el mapa y validarlo en un teléfono real, incluyendo permiso denegado y ubicación fuera del campus. Si se desea evidencia fotográfica para incidencias, habría que revisar primero almacenamiento, API y requisitos compartidos. Estas son propuestas; no están implementadas ni probadas en esta revisión.

## Documento y estándares

Se inspeccionó el contenido XML del Word canónico `revision_documental_final/entrega/Documento_Software_2_DSU_Entrega.docx`, además del informe de validación final. Se confirmó la existencia del manual por rol y de los estándares, no solo su mención en los apuntes de sesión.

El estándar incluye PEP 8, Ruff, longitud de línea de 120 caracteres, convenciones de nombres, TypeScript/React y oxlint, así como reglas de datos y API. Esto confirma documentación del estándar; no sustituye ejecutar los analizadores para comprobar cumplimiento actual.

La validación previa registra 74 pruebas aprobadas en PostgreSQL aislado y 34 casos de uso recorridos: 28 flujos principales aprobados y seis parciales. No se repitió esa suite hoy y no se declara cobertura funcional exhaustiva.

No se regeneró ni modificó Word/PDF. Para entregar o imprimir debe usarse la pareja con sufijo `Entrega` de esa carpeta; hay versiones anteriores con nombres similares.

## Organización y limpieza

El índice Git contiene 4909 archivos. `Entregables/versiones` reúne 1016 archivos y aproximadamente 399,5 MiB; `revision_documental_final`, 1343 archivos y 506,2 MiB; `auditoria_gui`, 622 archivos y 260,0 MiB. Estas cifras corresponden a archivos versionados del árbol actual, no al tamaño del historial Git.

Hay exclusiones para dependencias, cachés y temporales, y división de ZIP grandes para transporte. La limpieza queda parcial porque coexisten múltiples entregas, capturas y documentos históricos, y algunas instrucciones antiguas describen estados superados. Por ejemplo, `DocumentoSoftware2/CONTEXTO.md` conserva la descripción de un avance de 53 páginas; `CONTINUAR_SESION.md` ya señala la entrega final canónica y advierte sobre apuntes históricos.

Se propone crear un índice único de entrega y materiales; separar fuentes, entrega vigente, evidencias e históricos; detectar duplicados por hash antes de retirar copias; y actualizar los apuntes desfasados. No se eliminó ningún archivo durante la revisión.

La excepción autorizada de `backend/.env` se mantiene en el repositorio privado. La organización de materiales no debe trasladar esa configuración a paquetes públicos. No se imprimieron sus valores ni se efectuó una auditoría completa de secretos.

## Orden recomendado

1. Actualizar y verificar el contenido publicado desde la rama vigente, incluyendo sitio, pitch, app y API según los cambios correspondientes.
2. Habilitar CI para la rama de trabajo o establecer el flujo mediante pull requests.
3. Preparar un índice de materiales que explique cómo reconstruir y consultar los videos; confirmar si se necesita folleto y video de presentación independientes.
4. Implementar y probar una función móvil pequeña, comenzando por ubicación en el mapa.
5. Organizar duplicados e históricos preservando trazabilidad y el documento canónico.

Fuentes internas: `revision_documental_final/entrega/Informe_validacion_final.md`, `auditoria_gui/INFORME_FINAL.md`, `gestion-residuos-dsu/backend/docs/ESTADO.md`, Word canónico, archivos de frontend, manifiesto de evidencias y workflow CI/CD. Las comprobaciones en línea se detallan arriba con su alcance.


## Actualización posterior a la implementación y publicación

Se creó Flutter Android en gestion-residuos-dsu/movil sin cambiar los hashes del Word/PDF canónicos. GPS y orden por cercanía sobre puntos permitidos, confirmación del código, dictado y envío de incidencias a Azure. En Samsung Galaxy S23 se verificaron login, restauración de sesión, mapa, GPS/sugerencia y el usuario confirmó el dictado. La incidencia controlada 11 se comprobó por GET y quedó ATENDIDA. Ocho pruebas automáticas aprobadas y análisis Flutter sin incidencias. Sin cámara, fotos, cola offline ni prueba exhaustiva de dispositivos/roles.

Se publicaron frontend y sitio; el pitch público ahora contiene VAN Bs 117027, TIR operativa 41,8 % y capital propuesto Bs 200000. Azure ya ejecutaba el código base 4980f79; este cierre no requirió cambios de esquema ni de lógica backend. Los HTTP puntuales y los identificadores de despliegue están en auditoria_movil/publicacion_y_drive.json.

La carpeta del QR de Drive se reorganizó en carpetas específicas numeradas: documento, PAPS, calidad, manual, capturas, UML, pruebas/videos, código fuente, Android, marketing/pitch, defensa y respaldo documental. El PDF y Word de 01_Documento se reemplazaron conservando sus enlaces/permisos. La carpeta mezclada de entrega actualizada y los tres PDF antiguos sueltos se enviaron a la papelera; sus versiones vigentes están en cada carpeta correspondiente. Cartas y carátulas firmadas se preservaron en 12_Respaldo_Documental.

La limpieza de Git retiró 980 copias idénticas de Entregables/versiones, con índice SHA-256 y script de reconstrucción. Se añadió folleto PDF complementario y APK demo ARM64 firmado para pruebas. El repositorio continúa privado, con la excepción .env autorizada, sin trasladarla a Drive.

El CI de GitHub aprobó backend, frontend y sitio. El análisis y los ocho tests Flutter también pasaron en el primer job; la compilación remota encontró un fallo al instalar NDK. Se corrigió la preparación de Android/Java y la reserva de disco del runner. El estado vigente se comprueba en GitHub Actions; los resultados locales no sustituyen el chequeo del último commit.
