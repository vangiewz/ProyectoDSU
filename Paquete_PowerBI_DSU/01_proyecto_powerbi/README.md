# Tablero en Power BI (RD8, RI14, RNF26)

`DSU-Residuos.pbip` contiene el modelo de las vistas del sistema, relaciones, calendario y medidas. El 16/11/2026 se configuró el servidor real de Neon y se verificó la conexión directa cifrada con el usuario `powerbi`: lectura de las seis vistas, 15.430 hechos, 1.046 jornadas, 12 puntos, 1 incidencia y 8 recomendaciones. La vista de predicciones devolvió cero filas. El titular autenticó Power BI Desktop y se verificó visualmente la carga de las seis vistas: los recuentos coinciden con SQL. Calendario muestra 1.374 filas. El gráfico existente presenta datos. No se ha publicado. Sigue pendiente completar los gráficos y revisar sus filtros; no hay roles RLS definidos.

No ejecutar `python powerbi/generar.py` sobre el proyecto actual: sobrescribe el modelo y los gráficos editados manualmente. Si cambian las vistas `bi_*`, comparar primero las diferencias, conservar una copia y adaptar el proyecto existente.

## 1. Acceso preparado

El rol `powerbi` ya existe, tiene lectura sobre las seis vistas `bi_*`, sin permisos de escritura sobre ellas y sin atributos administrativos. El 16/11/2026, por autorización del usuario, se renovó únicamente su contraseña y se guardó en `backend/.env`; la contraseña del backend no se modificó. No ejecutar otra vez `CREATE ROLE` ni renovar contraseñas al abrir el informe.

La configuración está en `POWERBI_HOST`, `POWERBI_DATABASE`, `POWERBI_USER` y `POWERBI_PASSWORD`, exclusivamente dentro de `backend/.env`. No copiar la clave al modelo, documentación, capturas ni al paquete de traspaso. La excepción de versionado de este archivo se limita al repositorio privado; antes de hacerlo público se aplica la rotación y limpieza del historial indicadas en `AGENTS.md`.

## 2. Abrir y conectar

1. Abrir `DSU-Residuos.pbip` en Power BI Desktop. Los parámetros `Servidor` y `BaseDatos` ya apuntan a Neon; si cambia la infraestructura, contrastarlos con `POWERBI_HOST` y `POWERBI_DATABASE`.
2. Pulsar **Actualizar**. En la ventana PostgreSQL, seleccionar **Base de datos**, usar el usuario `powerbi` y la clave `POWERBI_PASSWORD` de `.env`. Usar conexión cifrada.
3. Power BI conserva sus credenciales mediante su propia administración de orígenes en el perfil de Windows. **No lee `.env` automáticamente**; se introduce la clave una vez por perfil/origen y se actualiza si se rota.
4. Comprobar las seis vistas y el calendario. La cuenta Microsoft de Power BI es un acceso distinto, necesario para el servicio y la publicación.

La comprobación SQL del 16/11/2026 no modificó registros, no ejecutó ETL y no entrenó el modelo. Evidencia: `docs/auditoria-fase-final/powerbi_conexion.json` desde la raíz del repositorio.

## 3. Qué trae el modelo

| Tabla | Contenido |
|---|---|
| `bi_hechos_residuos` | Registros depurados por el ETL (kg o L según `magnitud`) |
| `bi_jornadas` | Jornadas con puntos planificados, atendidos y omitidos |
| `bi_incidencias` | Incidencias por punto, tipo, gravedad y estado |
| `bi_puntos` | Puntos con sector, coordenadas (categoría Latitud/Longitud) y capacidad |
| `bi_predicciones` | Predicciones vigentes por punto, tipo y fecha, con margen de error y versión del modelo |
| `bi_recomendaciones` | Alertas y recomendaciones con urgencia y decisión |
| `Calendario` | Fecha, año, mes, semestre y semana (marcada como tabla de fechas) |

Relaciones: `Calendario[Fecha]` filtra hechos, jornadas y predicciones; `bi_puntos[codigo]` filtra hechos, incidencias, predicciones y recomendaciones.

Medidas: `Total kg`, `Total L`, `Registros`, `Puntos con datos`, `Promedio kg por punto`, `Total kg año anterior`, `Variación vs año anterior`, `Participación aprovechable`, `Jornadas cerradas`, `Cobertura`, `Incidencias`, `Incidencias pendientes`, `Generación proyectada kg`, `Margen proyectado kg`, `Recomendaciones pendientes`, `Recomendaciones aceptadas`.

> `cantidad_base` está en kg o en litros según `magnitud`: usar siempre las medidas `Total kg` / `Total L`, nunca sumar la columna directamente.

## 4. Gráficos que pide el documento (RF17, sección 2.6)

`python powerbi/tablero.py` (16/11/2026) arma en la página *Tablero*: cuatro tarjetas (Total kg, Cobertura, Incidencias pendientes, Recomendaciones pendientes), segmentadores de fecha y sector, barras por sector, por tipo y por punto, la evolución mensual (columna calculada `Calendario[Año-Mes]`) y la matriz sector × periodo académico. Conserva el modelo y el gráfico guardados por Desktop y puede repetirse sin duplicar visuales. Antes se auditaron las medidas contra SQL (`docs/auditoria-fase-final/powerbi_medidas.json`): coinciden. Límites declarados: el segmentador de fecha no filtra incidencias ni recomendaciones (sin relación con Calendario: se muestran como estado actual) y el de sector no filtra jornadas; *Participación aprovechable* se calcula sobre kg. Abrir en Desktop, **Actualizar** y revisar los filtros antes de capturar o publicar.

Referencia de visuales:

En la página *Tablero*:

| Visual | Campos |
|---|---|
| Tarjetas | `Total kg`, `Variación vs año anterior`, `Cobertura`, `Incidencias pendientes`, `Recomendaciones pendientes` |
| Barras: generación por sector | Eje `bi_puntos[sector]`, valor `Total kg` |
| Barras: generación por tipo | Eje `bi_hechos_residuos[tipo_residuo]`, valor `Total kg` |
| Líneas: evolución histórica | Eje `Calendario[Fecha]` (o Año/Mes), valor `Total kg` |
| Matriz: comparación entre periodos | Filas `bi_puntos[sector]`, columnas `bi_hechos_residuos[periodo_academico]`, valor `Total kg` |
| Barras: frecuencia de recolección | Eje `bi_puntos[codigo]`, valor `Jornadas cerradas` o `Cobertura` |
| Mapa | Latitud/Longitud de `bi_puntos`, tamaño `Total kg` |
| Predicción | Columnas por `Calendario[Fecha]` con `Generación proyectada kg`; mostrar siempre `Margen proyectado kg` en la información sobre herramientas (RNF13) |

**Segmentaciones (filtros):** `Calendario[Fecha]`, `bi_puntos[sector]`, `bi_puntos[codigo]`, `bi_hechos_residuos[tipo_residuo]`, `bi_hechos_residuos[periodo_academico]`.

Usar los colores del sistema: rojo DSU `#C4122F`, grafito `#1E2328`, azul `#1F3FA8` para lo medido y gris `#55606C` para lo estimado.

## 5. Publicar y mostrarlo en el sistema

1. *Inicio → Publicar* en un área de trabajo de la institución (requiere Power BI Pro; el documento presupuesta 2 licencias).
2. En el servicio, configurar la **actualización programada** diaria, después del horario del ETL. Si el servicio pide una *puerta de enlace* para PostgreSQL, instalar el *on-premises data gateway* en un equipo siempre encendido.
3. En el informe publicado: *Archivo → Insertar informe → Sitio web o portal* y copiar el enlace.
4. En el sistema, como administrador: *Parámetros → Power BI* → pegar el enlace. El informe aparece en *Tablero → Power BI* (cada usuario entra con su cuenta de Power BI).

## Archivos

- `generar.py`: genera el proyecto a partir de la lista de vistas y medidas.
- `tablero.py`: agrega los visuales de la página Tablero al proyecto existente sin regenerarlo.
- `DSU-Residuos.pbip`, `*.SemanticModel/`, `*.Report/`: el proyecto. Power BI Desktop guarda ahí también `.pbi/localSettings.json` y `cache.abf`, que no se versionan.
