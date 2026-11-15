# Tablero en Power BI (RD8, RI14, RNF26)

`DSU-Residuos.pbip` es un proyecto de Power BI Desktop ya conectado a las vistas depuradas del sistema, con el modelo armado: tablas, relaciones, una tabla calendario y las medidas principales. Falta solo dibujar los gráficos y publicarlo.

Si cambian las vistas `bi_*`, regenerarlo con `python powerbi/generar.py` (desde la raíz del backend).

## 1. Usuario de solo lectura en Neon (una vez)

En la consola de Neon → *SQL Editor*:

```sql
CREATE ROLE powerbi LOGIN PASSWORD '<una-clave-fuerte>';
GRANT USAGE ON SCHEMA public TO powerbi;
GRANT SELECT ON bi_hechos_residuos, bi_jornadas, bi_incidencias, bi_puntos,
                bi_predicciones, bi_recomendaciones TO powerbi;
```

Nunca usar el usuario dueño de la base en Power BI.

## 2. Abrir y conectar

1. Abrir `DSU-Residuos.pbip` con Power BI Desktop (versión de 2024 o posterior).
2. *Inicio → Transformar datos → Editar parámetros*:
   - **Servidor**: el host de Neon **sin** `-pooler` (por ejemplo `ep-xxxx.sa-east-1.aws.neon.tech`).
   - **BaseDatos**: `neondb`.
3. *Aplicar cambios*. Cuando pida credenciales: pestaña **Base de datos**, usuario `powerbi` y su clave; conexión cifrada.
4. *Actualizar*. Se cargan las 6 vistas y el calendario.

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
- `DSU-Residuos.pbip`, `*.SemanticModel/`, `*.Report/`: el proyecto. Power BI Desktop guarda ahí también `.pbi/localSettings.json` y `cache.abf`, que no se versionan.
