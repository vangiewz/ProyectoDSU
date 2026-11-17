"""Completa la página Tablero del informe PBIR sin regenerar el proyecto.

Uso:  python powerbi/tablero.py
Conserva el modelo y el gráfico guardados por Power BI Desktop; agrega la
columna calculada Calendario[Año-Mes] (serie mensual) y los visuales de la
sección 4 del README con nombres fijos, de modo que repetirlo no duplica nada.
Medidas y filtros auditados en docs/auditoria-fase-final/powerbi_medidas.json.
"""

import json
from pathlib import Path

from generar import guid

AQUI = Path(__file__).parent
MODELO = AQUI / "DSU-Residuos.SemanticModel/model.bim"
VISUALES = AQUI / "DSU-Residuos.Report/definition/pages/ReportSection/visuals"
ESQUEMA = (
    "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.14.0/schema.json"
)
EXISTENTE = "1e63c0dc0b2c8e1fcb8d"  # gráfico guardado por Desktop: generación por punto
AZUL, GRIS = "#1F3FA8", "#55606C"


def literal(valor):
    return {"expr": {"Literal": {"Value": valor}}}


def texto(valor):
    return literal("'" + valor.replace("'", "''") + "'")


def medida(tabla, nombre):
    return {
        "field": {"Measure": {"Expression": {"SourceRef": {"Entity": tabla}}, "Property": nombre}},
        "queryRef": f"{tabla}.{nombre}",
    }


def columna(tabla, nombre):
    return {
        "field": {"Column": {"Expression": {"SourceRef": {"Entity": tabla}}, "Property": nombre}},
        "queryRef": f"{tabla}.{nombre}",
        "nativeQueryRef": nombre,
        "active": True,
    }


def visual(nombre, tipo, x, y, w, h, roles, titulo, objetos=None, orden=None):
    v = {
        "visualType": tipo,
        "query": {"queryState": {r: {"projections": p} for r, p in roles.items()}},
        "visualContainerObjects": {"title": [{"properties": {"show": literal("true"), "text": texto(titulo)}}]},
    }
    if orden:
        orden_campo = {"field": orden[0]["field"], "direction": orden[1]}
        v["query"]["sortDefinition"] = {"sort": [orden_campo], "isDefaultSort": True}
    if objetos:
        v["objects"] = objetos
    return {
        "$schema": ESQUEMA,
        "name": nombre,
        "position": {"x": x, "y": y, "z": 0, "height": h, "width": w},
        "visual": v,
    }


def color(c):
    return {"dataPoint": [{"properties": {"fill": {"solid": {"color": literal(f"'{c}'")}}}}]}


def columna_ano_mes():
    m = json.loads(MODELO.read_text(encoding="utf-8"))
    cal = next(t for t in m["model"]["tables"] if t["name"] == "Calendario")
    if not any(c["name"] == "Año-Mes" for c in cal["columns"]):
        cal["columns"].append(
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
        MODELO.write_text(json.dumps(m, ensure_ascii=False, indent=2), encoding="utf-8")


def main():
    columna_ano_mes()
    kg = medida("bi_hechos_residuos", "Total kg")
    tarjetas = [
        ("Total kg", "bi_hechos_residuos", "Generación registrada (kg)"),
        ("Cobertura", "bi_jornadas", "Cobertura de puntos planificados"),
        ("Incidencias pendientes", "bi_incidencias", "Incidencias pendientes (estado actual)"),
        ("Recomendaciones pendientes", "bi_recomendaciones", "Recomendaciones pendientes (estado actual)"),
    ]
    vs = [
        visual(f"dsuTarjeta{i}", "card", 10 + i * 215, 10, 205, 100, {"Values": [medida(t, m)]}, titulo)
        for i, (m, t, titulo) in enumerate(tarjetas)
    ]
    vs += [
        visual("dsuFiltroFecha", "slicer", 870, 10, 200, 100, {"Values": [columna("Calendario", "Fecha")]}, "Periodo"),
        visual(
            "dsuFiltroSector",
            "slicer",
            1080,
            10,
            190,
            100,
            {"Values": [columna("bi_puntos", "sector")]},
            "Sector",
            objetos={"data": [{"properties": {"mode": texto("Dropdown")}}]},
        ),
        visual(
            "dsuSector",
            "clusteredBarChart",
            10,
            120,
            415,
            290,
            {"Category": [columna("bi_puntos", "sector")], "Y": [kg]},
            "Generación por sector (kg)",
            objetos=color(AZUL),
            orden=(kg, "Descending"),
        ),
        visual(
            "dsuTipo",
            "clusteredBarChart",
            435,
            120,
            415,
            290,
            {"Category": [columna("bi_hechos_residuos", "tipo_residuo")], "Y": [kg]},
            "Generación por tipo de residuo (kg)",
            objetos=color(AZUL),
            orden=(kg, "Descending"),
        ),
        visual(
            "dsuMensual",
            "lineChart",
            10,
            420,
            630,
            290,
            {"Category": [columna("Calendario", "Año-Mes")], "Y": [kg]},
            "Evolución mensual (kg)",
            objetos=color(AZUL),
        ),
        visual(
            "dsuPeriodos",
            "pivotTable",
            650,
            420,
            620,
            290,
            {
                "Rows": [columna("bi_puntos", "sector")],
                "Columns": [columna("bi_hechos_residuos", "periodo_academico")],
                "Values": [kg],
            },
            "Comparación entre periodos académicos (kg)",
        ),
    ]
    for v in vs:
        carpeta = VISUALES / v["name"]
        carpeta.mkdir(parents=True, exist_ok=True)
        (carpeta / "visual.json").write_text(json.dumps(v, ensure_ascii=False, indent=2), encoding="utf-8")
    # Gráfico existente: se conserva su consulta; solo se reubica y titula.
    ruta = VISUALES / EXISTENTE / "visual.json"
    e = json.loads(ruta.read_text(encoding="utf-8"))
    e["position"].update(x=860, y=120, width=410, height=290)
    e["visual"]["visualContainerObjects"] = {
        "title": [{"properties": {"show": literal("true"), "text": texto("Generación por punto (kg)")}}]
    }
    e["visual"]["objects"] = color(AZUL)
    ruta.write_text(json.dumps(e, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{len(vs) + 1} visuales en la página Tablero")


if __name__ == "__main__":
    main()
