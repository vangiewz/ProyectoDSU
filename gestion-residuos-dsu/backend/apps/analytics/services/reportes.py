"""Reportes operativos y gerenciales (RF27): datos tabulares y su exportación a Excel y PDF."""

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from io import BytesIO

from django.db.models import Count, Q, Sum
from django.utils import timezone
from fpdf import FPDF
from fpdf.fonts import FontFace
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from rest_framework.exceptions import ValidationError

from apps.accounts.permissions import filtrar_por_sector
from apps.operations.models import Incidencia, Jornada
from apps.prediction.services.prediccion import mapa as mapa_proyectado

from .indicadores import Alcance, exigir_etl, hechos, indicadores

USUARIO_REPORTE = ("responsable__username", "responsable__first_name", "responsable__last_name")
MAX_FILAS = 5000  # RF27 exc. 2: volumen máximo admitido para la exportación.
INSTITUCION = "Universidad Autónoma Gabriel René Moreno"
DIRECCION = "Dirección de Servicios Universitarios (DSU)"
ROJO_DSU = (196, 18, 47)


@dataclass
class Reporte:
    titulo: str
    columnas: list[str]
    filas: list[list] = field(default_factory=list)
    numericas: set[int] = field(default_factory=set)  # índices de columnas numéricas (alineadas a la derecha)
    solicitado_por: object = None  # usuario que pidió el reporte (RF27 paso 3.2)
    emitido_en: datetime | None = None

    def encabezado(self, a: Alcance) -> list[str]:
        """Encabezado institucional con el periodo, la fecha de emisión y quien lo solicitó."""
        emision = timezone.localtime(self.emitido_en).strftime("%d/%m/%Y %H:%M")
        usuario = self.solicitado_por
        return [
            INSTITUCION,
            DIRECCION,
            self.titulo,
            f"Periodo: {a.desde:%d/%m/%Y} al {a.hasta:%d/%m/%Y}",
            f"Emitido el {emision} por {usuario.get_full_name() or usuario.username}",
        ]


def _generacion(user, a: Alcance, campo: str, etiqueta: str, titulo: str) -> Reporte:
    exigir_etl()
    filas = (
        hechos(user, a)
        .values(etiqueta)
        .annotate(
            kg=Sum("cantidad_base", filter=Q(magnitud="PESO")),
            litros=Sum("cantidad_base", filter=Q(magnitud="VOLUMEN")),
            registros=Count("id"),
            puntos=Count("punto_id", distinct=True),
        )
        .order_by("-kg")
    )
    r = Reporte(titulo, [campo, "Total (kg)", "Total (L)", "Registros", "Puntos"], numericas={1, 2, 3, 4})
    r.filas = [[f[etiqueta], f["kg"] or 0, f["litros"] or 0, f["registros"], f["puntos"]] for f in filas]
    return r


def _jornadas(user, a: Alcance) -> Reporte:
    qs = filtrar_por_sector(Jornada.objects.filter(fecha__range=(a.desde, a.hasta)), user, "sector")
    if a.sector:
        qs = qs.filter(sector_id=a.sector)
    qs = (
        qs.select_related("sector", "responsable")
        .only(*("fecha", "turno", "estado", "sector__nombre"), *USUARIO_REPORTE)
        .annotate(
            plan=Count("ruta", distinct=True),
            aten=Count("ruta", filter=Q(ruta__atendido=True), distinct=True),
            omit=Count("ruta", filter=Q(ruta__atendido=False), distinct=True),
        )
        .order_by("fecha", "turno")
    )
    r = Reporte(
        "Cumplimiento de jornadas",
        ["Fecha", "Turno", "Sector", "Responsable", "Estado", "Planificados", "Atendidos", "Omitidos", "Cobertura %"],
        numericas={5, 6, 7, 8},
    )
    r.filas = [
        [
            j.fecha,
            j.get_turno_display(),
            j.sector.nombre,
            j.responsable.get_full_name() if j.responsable else "Sin asignar",
            j.get_estado_display(),
            j.plan,
            j.aten,
            j.omit,
            round(j.aten * 100 / j.plan, 1) if j.plan else 0,
        ]
        for j in qs
    ]
    return r


def _incidencias(user, a: Alcance) -> Reporte:
    qs = filtrar_por_sector(
        Incidencia.objects.filter(fecha_hora__date__range=(a.desde, a.hasta)), user, "punto__sector"
    ).select_related("punto__sector", "reportada_por")
    qs = qs.only(
        *("fecha_hora", "tipo", "gravedad", "estado", "accion_adoptada", "punto__codigo", "punto__sector__nombre"),
        *(f"reportada_por__{c}" for c in ("username", "first_name", "last_name")),
    )
    if a.sector:
        qs = qs.filter(punto__sector_id=a.sector)
    if a.punto:
        qs = qs.filter(punto_id=a.punto)
    r = Reporte(
        "Incidencias registradas",
        ["Fecha", "Punto", "Sector", "Tipo", "Gravedad", "Estado", "Reportó", "Acción adoptada"],
    )
    r.filas = [
        [
            timezone.localtime(i.fecha_hora).strftime("%d/%m/%Y %H:%M"),
            i.punto.codigo,
            i.punto.sector.nombre,
            i.get_tipo_display(),
            i.get_gravedad_display(),
            i.get_estado_display(),
            i.reportada_por.get_full_name() or i.reportada_por.username,
            i.accion_adoptada,
        ]
        for i in qs.order_by("fecha_hora")
    ]
    return r


def _indicadores(user, a: Alcance) -> Reporte:
    k = indicadores(user, a)
    sector = k["sector_mayor_generacion"]
    tipo = k["tipo_predominante"]
    r = Reporte("Indicadores del periodo", ["Indicador", "Valor"])
    r.filas = [
        ["Total recolectado (kg)", k["total_kg"]],
        ["Total recolectado (L)", k["total_litros"]],
        [
            "Variación respecto del periodo anterior (%)",
            "Sin datos previos" if k["variacion_kg_pct"] is None else k["variacion_kg_pct"],
        ],
        ["Generación promedio por punto (kg)", k["promedio_kg_por_punto"]],
        ["Generación promedio por sector (kg)", k["promedio_kg_por_sector"]],
        ["Sector de mayor generación", f"{sector['sector__nombre']} ({_texto(sector['total'])} kg)" if sector else "—"],
        ["Tipo de residuo predominante", tipo["tipo_residuo__nombre"] if tipo else "—"],
        ["Recolecciones realizadas (jornadas cerradas)", k["recolecciones_realizadas"]],
        ["Frecuencia de atención por punto (veces/semana)", k["frecuencia_semanal_por_punto"]],
        ["Cobertura de las jornadas (%)", "—" if k["cobertura_pct"] is None else k["cobertura_pct"]],
        [f"Puntos críticos (> {_texto(k['umbral_critico_kg_dia'])} kg/día)", len(k["puntos_criticos"])],
    ]
    return r


def _prediccion(user, a: Alcance) -> Reporte:
    """Predicciones vigentes por punto, siempre con su margen (RF23, RNF13). El horizonte lo fija cada lote."""
    filas = mapa_proyectado(user, a.sector)["puntos"]
    if a.punto:
        filas = [f for f in filas if f["id"] == a.punto]
    r = Reporte(
        "Generación proyectada por punto",
        [
            "Punto",
            "Nombre",
            "Sector",
            "Desde",
            "Hasta",
            "Estimado (kg)",
            "Margen ± (kg)",
            "Prom. diario (kg)",
            "Modelo",
        ],
        numericas={5, 6, 7},
    )
    r.filas = [
        [
            f["codigo"],
            f["nombre"],
            f["sector"],
            f["desde"],
            f["hasta"],
            f["total_kg"],
            f["margen_kg"],
            f["promedio_dia_kg"],
            f"v{f['version']}",
        ]
        for f in filas
    ]
    return r


TIPOS = {
    "generacion-sector": (
        "Generación por sector",
        lambda u, a: _generacion(u, a, "Sector", "sector__nombre", "Generación por sector"),
    ),
    "generacion-tipo": (
        "Generación por tipo de residuo",
        lambda u, a: _generacion(u, a, "Tipo de residuo", "tipo_residuo__nombre", "Generación por tipo de residuo"),
    ),
    "cumplimiento-jornadas": ("Cumplimiento de jornadas", _jornadas),
    "incidencias": ("Incidencias registradas", _incidencias),
    "indicadores": ("Indicadores del periodo", _indicadores),
    "prediccion": ("Generación proyectada por punto", _prediccion),
}


def generar(tipo: str, user, a: Alcance) -> Reporte:
    if tipo not in TIPOS:
        raise ValidationError("Tipo de reporte desconocido.")
    r = TIPOS[tipo][1](user, a)
    r.solicitado_por, r.emitido_en = user, timezone.now()
    if len(r.filas) > MAX_FILAS:
        raise ValidationError(
            f"El reporte tiene {len(r.filas)} filas y supera el máximo de {MAX_FILAS}; acote el periodo."
        )
    return r


def _texto(v) -> str:
    if isinstance(v, Decimal):
        return f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    if isinstance(v, float):
        return f"{v:,.1f}".replace(",", "X").replace(".", ",").replace("X", ".")
    if hasattr(v, "strftime"):
        return v.strftime("%d/%m/%Y")
    return "" if v is None else str(v)


def a_excel(r: Reporte, a: Alcance) -> bytes:
    wb = Workbook()
    ws = wb.active
    ws.title = r.titulo[:31]
    for i, linea in enumerate(r.encabezado(a), start=1):
        ws.cell(row=i, column=1, value=linea).font = Font(bold=i <= 3, size=13 if i == 3 else 11)
    fila_cab = 7
    for j, col in enumerate(r.columnas, start=1):
        c = ws.cell(row=fila_cab, column=j, value=col)
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor="C4122F")
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    for i, fila in enumerate(r.filas, start=fila_cab + 1):
        for j, v in enumerate(fila, start=1):
            ws.cell(row=i, column=j, value=float(v) if isinstance(v, Decimal) else v)
    for j, col in enumerate(r.columnas, start=1):
        largo = max([len(col)] + [len(_texto(f[j - 1])) for f in r.filas[:500]])
        ws.column_dimensions[ws.cell(row=fila_cab, column=j).column_letter].width = min(max(largo + 2, 10), 50)
    ws.freeze_panes = ws.cell(row=fila_cab + 1, column=1)
    buffer = BytesIO()
    wb.save(buffer)
    return buffer.getvalue()


def _latin1(texto: str) -> str:
    """Las fuentes base del PDF son Latin-1; se reemplazan los pocos signos fuera de ese juego."""
    return texto.replace("—", "-").replace("–", "-").replace("…", "...").encode("latin-1", "replace").decode("latin-1")


class _PDF(FPDF):
    pie = ""

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", size=8)
        self.set_text_color(90, 90, 90)
        self.cell(0, 6, _latin1(f"{self.pie}   ·   Página {self.page_no()} de {{nb}}"), align="C")


def a_pdf(r: Reporte, a: Alcance) -> bytes:
    pdf = _PDF(orientation="L" if len(r.columnas) > 5 else "P", unit="mm", format="Letter")
    pdf.pie = f"{DIRECCION} - {r.titulo}"
    pdf.set_auto_page_break(auto=True, margin=16)
    pdf.add_page()
    inst, direc, titulo, periodo, emision = r.encabezado(a)
    # Bloque institucional: sigla DSU en blanco sobre rojo, como el emblema de la dirección.
    pdf.set_fill_color(*ROJO_DSU)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(22, 12, "DSU", fill=True, align="C")
    pdf.set_text_color(30, 35, 40)
    pdf.set_xy(pdf.l_margin + 26, pdf.t_margin)
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(0, 6, _latin1(inst), new_x="LMARGIN", new_y="NEXT")
    pdf.set_x(pdf.l_margin + 26)
    pdf.set_font("Helvetica", size=10)
    pdf.cell(0, 6, _latin1(direc), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    pdf.set_font("Helvetica", "B", 15)
    pdf.cell(0, 8, _latin1(titulo), new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", size=9)
    pdf.set_text_color(74, 85, 96)
    pdf.cell(0, 5, _latin1(f"{periodo}   ·   {emision}"), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)

    pdf.set_text_color(30, 35, 40)
    if not r.filas:
        pdf.set_font("Helvetica", "I", 10)
        pdf.cell(0, 8, "No existe información para el periodo y los filtros seleccionados.")
        return bytes(pdf.output())
    pdf.set_font("Helvetica", size=8.5)
    pdf.set_fill_color(255, 255, 255)
    # Ancho relativo por contenido: las columnas de texto largo reciben más espacio.
    anchos = tuple(
        min(max([len(c)] + [len(_texto(f[i])) for f in r.filas[:200]]), 40) + 4 for i, c in enumerate(r.columnas)
    )
    with pdf.table(
        col_widths=anchos,
        cell_fill_mode="NONE",
        headings_style=_estilo_cabecera(),
        line_height=5.5,
        text_align=tuple("RIGHT" if i in r.numericas else "LEFT" for i in range(len(r.columnas))),
        borders_layout="HORIZONTAL_LINES",
        first_row_as_headings=True,
    ) as tabla:
        tabla.row([_latin1(c) for c in r.columnas])
        for fila in r.filas:
            tabla.row([_latin1(_texto(v)) for v in fila])
    return bytes(pdf.output())


def _estilo_cabecera():
    return FontFace(emphasis="BOLD", color=(255, 255, 255), fill_color=ROJO_DSU)


def nombre_archivo(tipo: str, a: Alcance, extension: str) -> str:
    return f"dsu-{tipo}-{a.desde:%Y%m%d}-{a.hasta:%Y%m%d}.{extension}"
