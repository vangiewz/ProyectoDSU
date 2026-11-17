"""Genera el proyecto de Power BI (formato .pbip) conectado a las vistas bi_* de PostgreSQL (RD8, RI14).

Uso:  python powerbi/generar.py
Crea DSU-Residuos.pbip con su modelo semántico (tablas, relaciones y medidas) y una página en blanco.
Los gráficos se arman en Power BI Desktop; ver powerbi/README.md.
"""

import json
import uuid
from pathlib import Path

AQUI = Path(__file__).parent
NOMBRE = "DSU-Residuos"

# Columnas de cada vista (ver analytics/0003_vistas_bi y prediction/0003_vistas_bi) con su tipo en Power BI.
# Las cantidades y coordenadas van como double: el "decimal" de Power BI es fijo a 4 decimales.
S, E, D, F, B = "string", "int64", "double", "dateTime", "boolean"  # E = entero
VISTAS = {
    "bi_hechos_residuos": {
        "id": E,
        "fecha": F,
        "fecha_hora": F,
        "anio": E,
        "mes": E,
        "semana_anio": E,
        "dia_semana": E,
        "sector_codigo": S,
        "sector": S,
        "punto_codigo": S,
        "punto": S,
        "latitud": D,
        "longitud": D,
        "tipo_residuo": S,
        "clasificacion": S,
        "aprovechable": B,
        "magnitud": S,
        "cantidad_base": D,
        "cantidad_original": D,
        "unidad_original": S,
        "periodo_academico": S,
        "atipico": B,
        "jornada_id": E,
    },
    "bi_jornadas": {
        "id": E,
        "fecha": F,
        "turno": S,
        "estado": S,
        "sector_codigo": S,
        "sector": S,
        "puntos_planificados": E,
        "puntos_atendidos": E,
        "puntos_omitidos": E,
        "hora_inicio": F,
        "hora_fin": F,
    },
    "bi_incidencias": {
        "id": E,
        "fecha_hora": F,
        "tipo": S,
        "gravedad": S,
        "estado": S,
        "punto_codigo": S,
        "sector": S,
        "atendida_en": F,
    },
    "bi_puntos": {
        "id": E,
        "codigo": S,
        "nombre": S,
        "sector_codigo": S,
        "sector": S,
        "latitud": D,
        "longitud": D,
        "capacidad_kg": D,
        "estado": S,
        "is_active": B,
    },
    "bi_predicciones": {
        "id": E,
        "fecha": F,
        "sector_codigo": S,
        "sector": S,
        "punto_codigo": S,
        "punto": S,
        "tipo_residuo": S,
        "clasificacion": S,
        "cantidad_kg": D,
        "margen_kg": D,
        "modelo_version": E,
        "generada_en": F,
    },
    "bi_recomendaciones": {
        "id": E,
        "creada_en": F,
        "sector_codigo": S,
        "sector": S,
        "punto_codigo": S,
        "tipo": S,
        "urgencia": S,
        "estado": S,
        "resuelta_en": F,
    },
}

KG = "#,0.00"
MEDIDAS = {
    "bi_hechos_residuos": [
        ("Total kg", 'CALCULATE(SUM(bi_hechos_residuos[cantidad_base]), bi_hechos_residuos[magnitud] = "PESO")', KG),
        ("Total L", 'CALCULATE(SUM(bi_hechos_residuos[cantidad_base]), bi_hechos_residuos[magnitud] = "VOLUMEN")', KG),
        ("Registros", "COUNTROWS(bi_hechos_residuos)", "#,0"),
        ("Puntos con datos", "DISTINCTCOUNT(bi_hechos_residuos[punto_codigo])", "#,0"),
        ("Promedio kg por punto", "DIVIDE([Total kg], [Puntos con datos])", KG),
        ("Total kg año anterior", "CALCULATE([Total kg], SAMEPERIODLASTYEAR(Calendario[Fecha]))", KG),
        ("Variación vs año anterior", "DIVIDE([Total kg] - [Total kg año anterior], [Total kg año anterior])", "0.0%"),
        (
            "Participación aprovechable",
            "DIVIDE(CALCULATE([Total kg], bi_hechos_residuos[aprovechable] = TRUE()), [Total kg])",
            "0.0%",
        ),
    ],
    "bi_jornadas": [
        ("Jornadas cerradas", 'CALCULATE(COUNTROWS(bi_jornadas), bi_jornadas[estado] = "CERRADA")', "#,0"),
        ("Cobertura", "DIVIDE(SUM(bi_jornadas[puntos_atendidos]), SUM(bi_jornadas[puntos_planificados]))", "0.0%"),
    ],
    "bi_incidencias": [
        ("Incidencias", "COUNTROWS(bi_incidencias)", "#,0"),
        ("Incidencias pendientes", 'CALCULATE(COUNTROWS(bi_incidencias), bi_incidencias[estado] = "PENDIENTE")', "#,0"),
    ],
    "bi_predicciones": [
        ("Generación proyectada kg", "SUM(bi_predicciones[cantidad_kg])", KG),
        # Margen de una suma de estimaciones: raíz de la suma de cuadrados (igual que en el sistema).
        ("Margen proyectado kg", "SQRT(SUMX(bi_predicciones, bi_predicciones[margen_kg] ^ 2))", KG),
    ],
    "bi_recomendaciones": [
        (
            "Recomendaciones pendientes",
            'CALCULATE(COUNTROWS(bi_recomendaciones), bi_recomendaciones[estado] = "PENDIENTE")',
            "#,0",
        ),
        (
            "Recomendaciones aceptadas",
            'CALCULATE(COUNTROWS(bi_recomendaciones), bi_recomendaciones[estado] = "ACEPTADA")',
            "#,0",
        ),
    ],
}

# Muchos a uno; los filtros fluyen de la dimensión (derecha) a los hechos (izquierda).
RELACIONES = [
    ("bi_hechos_residuos", "fecha", "Calendario", "Fecha"),
    ("bi_jornadas", "fecha", "Calendario", "Fecha"),
    ("bi_predicciones", "fecha", "Calendario", "Fecha"),
    ("bi_hechos_residuos", "punto_codigo", "bi_puntos", "codigo"),
    ("bi_incidencias", "punto_codigo", "bi_puntos", "codigo"),
    ("bi_predicciones", "punto_codigo", "bi_puntos", "codigo"),
    ("bi_recomendaciones", "punto_codigo", "bi_puntos", "codigo"),
]

GEO = {"latitud": "Latitude", "longitud": "Longitude"}


def guid(*partes: str) -> str:
    """Identificador estable: regenerar el proyecto no cambia los lineageTag (diffs limpios en git)."""
    return str(uuid.uuid5(uuid.NAMESPACE_URL, "dsu-residuos/" + "/".join(partes)))


def columna(tabla: str, nombre: str, tipo: str) -> dict:
    c = {
        "name": nombre,
        "dataType": tipo,
        "sourceColumn": nombre,
        "lineageTag": guid(tabla, nombre),
        "summarizeBy": "none",
    }
    if tipo == F:
        c["formatString"] = "General Date"
    if nombre in GEO:
        c["dataCategory"] = GEO[nombre]
    if nombre in ("cantidad_base", "cantidad_original", "cantidad_kg", "margen_kg", "capacidad_kg"):
        c["summarizeBy"] = "sum"
        c["formatString"] = KG
    return c


def tabla_vista(vista: str, columnas: dict) -> dict:
    m = [
        "let",
        "    Origen = PostgreSQL.Database(Servidor, BaseDatos),",
        f'    Vista = Origen{{[Schema="public", Item="{vista}"]}}[Data]',
        "in",
        "    Vista",
    ]
    return {
        "name": vista,
        "lineageTag": guid(vista),
        "columns": [columna(vista, n, t) for n, t in columnas.items()],
        "measures": [
            {"name": n, "expression": e, "formatString": f, "lineageTag": guid(vista, "medida", n)}
            for n, e, f in MEDIDAS.get(vista, [])
        ],
        "partitions": [{"name": vista, "mode": "import", "source": {"type": "m", "expression": m}}],
    }


def calendario() -> dict:
    """Tabla de fechas en M (marcada como tabla de fechas) para filtrar por día, mes, semestre o año."""
    m = [
        "let",
        "    Inicio = #date(2024, 1, 1),",
        "    Fin = Date.AddYears(Date.From(DateTime.LocalNow()), 1),",
        "    Fechas = List.Dates(Inicio, Duration.Days(Fin - Inicio) + 1, #duration(1, 0, 0, 0)),",
        '    Tabla = Table.FromList(Fechas, Splitter.SplitByNothing(), {"Fecha"}),',
        '    ConTipo = Table.TransformColumnTypes(Tabla, {{"Fecha", type datetime}}),',
        '    Anio = Table.AddColumn(ConTipo, "Año", each Date.Year([Fecha]), Int64.Type),',
        '    Mes = Table.AddColumn(Anio, "Mes", each Date.Month([Fecha]), Int64.Type),',
        '    NombreMes = Table.AddColumn(Mes, "Nombre del mes",'
        ' each Date.ToText(Date.From([Fecha]), "MMMM", "es-BO"), type text),',
        '    Semestre = Table.AddColumn(NombreMes, "Semestre",'
        " each if Date.Month([Fecha]) <= 6 then 1 else 2, Int64.Type),",
        '    Semana = Table.AddColumn(Semestre, "Semana", each Date.WeekOfYear([Fecha], Day.Monday), Int64.Type)',
        "in",
        "    Semana",
    ]
    cols = [("Fecha", F), ("Año", E), ("Mes", E), ("Nombre del mes", S), ("Semestre", E), ("Semana", E)]
    columnas = [columna("Calendario", n, t) for n, t in cols]
    columnas[0].update(isKey=True, formatString="Short Date")
    columnas[3]["sortByColumn"] = "Mes"
    # Serie mensual ordenable (la agrega también tablero.py al proyecto existente).
    columnas.append(
        {
            "type": "calculated",
            "name": "Año-Mes",
            "dataType": "string",
            "isDataTypeInferred": True,
            "expression": 'FORMAT(Calendario[Fecha], "yyyy-MM")',
            "lineageTag": guid("Calendario", "Año-Mes"),
            "summarizeBy": "none",
        }
    )
    return {
        "name": "Calendario",
        "dataCategory": "Time",
        "lineageTag": guid("Calendario"),
        "columns": columnas,
        "partitions": [{"name": "Calendario", "mode": "import", "source": {"type": "m", "expression": m}}],
    }


def parametro(nombre: str, valor: str) -> dict:
    return {
        "name": nombre,
        "kind": "m",
        "expression": f'"{valor}" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]',
        "lineageTag": guid("parametro", nombre),
    }


def modelo() -> dict:
    tablas = [calendario()] + [tabla_vista(v, c) for v, c in VISTAS.items()]
    return {
        "compatibilityLevel": 1550,
        "model": {
            "culture": "es-ES",
            "defaultPowerBIDataSourceVersion": "powerBI_V3",
            "sourceQueryCulture": "es-BO",
            "dataAccessOptions": {"legacyRedirects": True, "returnErrorValuesAsNull": True},
            "tables": tablas,
            "relationships": [
                {"name": guid(a, b, c, d), "fromTable": a, "fromColumn": b, "toTable": c, "toColumn": d}
                for a, b, c, d in RELACIONES
            ],
            # Se editan en Power BI Desktop: Transformar datos → Editar parámetros.
            "expressions": [
                parametro("Servidor", "EDITAR-host-de-neon.neon.tech"),
                parametro("BaseDatos", "neondb"),
            ],
            "annotations": [
                {
                    "name": "PBI_QueryOrder",
                    "value": json.dumps(["Servidor", "BaseDatos", *[t["name"] for t in tablas]]),
                },
                {"name": "__PBI_TimeIntelligenceEnabled", "value": "0"},
            ],
        },
    }


def reporte() -> dict:
    """Una página en blanco: los gráficos se agregan en Desktop (ver README)."""
    return {
        "config": json.dumps({"version": "5.43", "themeCollection": {}, "activeSectionIndex": 0}),
        "layoutOptimization": 0,
        "resourcePackages": [],
        "sections": [
            {
                "config": "{}",
                "displayName": "Tablero",
                "displayOption": 1,
                "filters": "[]",
                "height": 720.0,
                "name": "ReportSection",
                "ordinal": 0,
                "visualContainers": [],
                "width": 1280.0,
            }
        ],
    }


def escribir(ruta: Path, datos) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    texto = datos if isinstance(datos, str) else json.dumps(datos, ensure_ascii=False, indent=2)
    ruta.write_text(texto + "\n", encoding="utf-8")


def main():
    escribir(
        AQUI / f"{NOMBRE}.pbip",
        {
            "version": "1.0",
            "artifacts": [{"report": {"path": f"{NOMBRE}.Report"}}],
            "settings": {"enableAutoRecovery": True},
        },
    )
    escribir(AQUI / f"{NOMBRE}.SemanticModel" / "definition.pbism", {"version": "1.0", "settings": {}})
    escribir(AQUI / f"{NOMBRE}.SemanticModel" / "model.bim", modelo())
    escribir(
        AQUI / f"{NOMBRE}.Report" / "definition.pbir",
        {"version": "1.0", "datasetReference": {"byPath": {"path": f"../{NOMBRE}.SemanticModel"}}},
    )
    escribir(AQUI / f"{NOMBRE}.Report" / "report.json", reporte())
    print(f"Proyecto generado en {AQUI / NOMBRE}.pbip")


if __name__ == "__main__":
    main()
