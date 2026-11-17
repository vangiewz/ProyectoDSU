"""Indicadores, comparación de periodos y datos espaciales sobre el plano analítico (RF16, RF18–RF21)."""

from dataclasses import dataclass
from datetime import date, timedelta
from decimal import Decimal

from django.db.models import Count, Max, Q, Sum
from django.db.models.functions import TruncMonth
from rest_framework.exceptions import ValidationError

from apps.accounts.permissions import filtrar_por_sector
from apps.campus.models import PuntoRecoleccion
from apps.catalogs.models import ParametrosSistema, PeriodoAcademico
from apps.operations.models import Jornada, JornadaPunto

from ..models import EjecucionETL, HechoResiduo

CERO = Decimal(0)


@dataclass
class Alcance:
    """Periodo y filtros de un análisis; el usuario restringe por sus sectores."""

    desde: date
    hasta: date
    sector: int | None = None
    punto: int | None = None
    tipo_residuo: int | None = None

    @property
    def dias(self) -> int:
        return (self.hasta - self.desde).days + 1

    def anterior(self) -> "Alcance":
        return Alcance(
            self.desde - timedelta(days=self.dias),
            self.desde - timedelta(days=1),
            self.sector,
            self.punto,
            self.tipo_residuo,
        )


def leer_alcance(params, *, por_defecto_dias=30) -> Alcance:
    """Construye el alcance desde la query string; acepta un periodo académico en lugar de fechas."""

    def entero(k):
        v = params.get(k)
        return int(v) if v not in (None, "") else None

    try:
        if params.get("periodo"):
            p = PeriodoAcademico.objects.get(pk=int(params["periodo"]))
            desde, hasta = p.fecha_inicio, p.fecha_fin
        else:
            hasta = date.fromisoformat(params["hasta"]) if params.get("hasta") else date.today()
            desde = (
                date.fromisoformat(params["desde"])
                if params.get("desde")
                else hasta - timedelta(days=por_defecto_dias - 1)
            )
        alcance = Alcance(desde, hasta, entero("sector"), entero("punto"), entero("tipo_residuo"))
    except (ValueError, PeriodoAcademico.DoesNotExist) as err:
        raise ValidationError("Parámetros de consulta inválidos.") from err
    if alcance.desde > alcance.hasta:
        raise ValidationError("El rango de fechas es inválido: 'desde' es posterior a 'hasta'.")
    return alcance


def exigir_etl():
    """RF16 precondición: el ETL debe haberse ejecutado correctamente al menos una vez."""
    if not EjecucionETL.objects.filter(estado__in=["EXITOSA", "CON_ALERTA", "SIN_CAMBIOS"]).exists():
        raise ValidationError("Aún no hay información analítica: ejecute el proceso ETL al menos una vez.")


def hechos(user, a: Alcance):
    qs = HechoResiduo.objects.filter(fecha__range=(a.desde, a.hasta))
    if a.sector:
        qs = qs.filter(sector_id=a.sector)
    if a.punto:
        qs = qs.filter(punto_id=a.punto)
    if a.tipo_residuo:
        qs = qs.filter(tipo_residuo_id=a.tipo_residuo)
    return filtrar_por_sector(qs, user, "sector")


def _totales(qs) -> dict:
    t = qs.aggregate(
        kg=Sum("cantidad_base", filter=Q(magnitud="PESO")), litros=Sum("cantidad_base", filter=Q(magnitud="VOLUMEN"))
    )
    return {"kg": t["kg"] or CERO, "litros": t["litros"] or CERO}


def _variacion(actual: Decimal, previo: Decimal) -> float | None:
    return None if not previo else round(float((actual - previo) * 100 / previo), 1)


def puntos_criticos(user, a: Alcance) -> list[dict]:
    """Puntos cuya generación promedio diaria (kg) supera el umbral configurado (RF16 2.4)."""
    umbral = ParametrosSistema.actual().umbral_critico_kg_dia
    filas = (
        hechos(user, a)
        .filter(magnitud="PESO")
        .values("punto_id", "punto__codigo", "punto__nombre", "sector__nombre")
        .annotate(total=Sum("cantidad_base"))
        .order_by("-total")
    )
    return [{**f, "promedio_dia": round(f["total"] / a.dias, 2)} for f in filas if f["total"] / a.dias > umbral]


def indicadores(user, a: Alcance) -> dict:
    exigir_etl()
    qs = hechos(user, a)
    actual, previo = _totales(qs), _totales(hechos(user, a.anterior()))
    puntos_con_datos = qs.values("punto_id").distinct().count()
    sectores_con_datos = qs.values("sector_id").distinct().count()

    por_sector = list(
        qs.filter(magnitud="PESO")
        .values("sector_id", "sector__codigo", "sector__nombre")
        .annotate(total=Sum("cantidad_base"))
        .order_by("-total")
    )
    # Detalle por punto (RF17 paso 3): los de mayor generación dentro de los filtros aplicados.
    por_punto = list(
        qs.filter(magnitud="PESO")
        .values("punto_id", "punto__codigo", "punto__nombre", "sector__nombre")
        .annotate(total=Sum("cantidad_base"))
        .order_by("-total")[:15]
    )
    por_tipo = list(
        qs.values("tipo_residuo_id", "tipo_residuo__nombre", "magnitud")
        .annotate(total=Sum("cantidad_base"))
        .order_by("-total")
    )
    agrupar_semana = a.dias > 62
    serie = list(
        qs.filter(magnitud="PESO")
        .values("anio", "semana_anio" if agrupar_semana else "fecha")
        .annotate(total=Sum("cantidad_base"))
        .order_by("anio", "semana_anio" if agrupar_semana else "fecha")
    )

    jornadas = filtrar_por_sector(Jornada.objects.filter(fecha__range=(a.desde, a.hasta)), user, "sector")
    paradas = filtrar_por_sector(
        JornadaPunto.objects.filter(jornada__fecha__range=(a.desde, a.hasta)), user, "jornada__sector"
    )
    if a.sector:
        jornadas, paradas = jornadas.filter(sector_id=a.sector), paradas.filter(jornada__sector_id=a.sector)
    if a.punto:
        paradas = paradas.filter(punto_id=a.punto)
    planificadas = paradas.count()
    atendidas = paradas.filter(atendido=True).count()
    puntos_activos = filtrar_por_sector(PuntoRecoleccion.objects.filter(is_active=True), user, "sector")
    if a.sector:
        puntos_activos = puntos_activos.filter(sector_id=a.sector)
    semanas = max(a.dias / 7, 1)
    n_puntos = puntos_activos.count() if not a.punto else 1

    return {
        "alcance": {"desde": a.desde, "hasta": a.hasta, "dias": a.dias},
        "total_kg": actual["kg"],
        "total_litros": actual["litros"],
        "variacion_kg_pct": _variacion(actual["kg"], previo["kg"]),
        "periodo_anterior": {"desde": a.anterior().desde, "hasta": a.anterior().hasta, "total_kg": previo["kg"]},
        "promedio_kg_por_punto": round(actual["kg"] / puntos_con_datos, 2) if puntos_con_datos else CERO,
        "promedio_kg_por_sector": round(actual["kg"] / sectores_con_datos, 2) if sectores_con_datos else CERO,
        "sector_mayor_generacion": por_sector[0] if por_sector else None,
        "tipo_predominante": por_tipo[0] if por_tipo else None,
        "recolecciones_realizadas": jornadas.filter(estado=Jornada.Estado.CERRADA).count(),
        "frecuencia_semanal_por_punto": round(atendidas / (n_puntos * semanas), 2) if n_puntos else 0,
        "cobertura_pct": round(atendidas * 100 / planificadas, 1) if planificadas else None,
        "puntos_criticos": puntos_criticos(user, a),
        "umbral_critico_kg_dia": ParametrosSistema.actual().umbral_critico_kg_dia,
        "registros": qs.count(),
        "atipicos": qs.filter(atipico=True).count(),
        "por_sector": por_sector,
        "por_tipo": por_tipo,
        "por_punto": por_punto,
        "serie": [
            {
                "etiqueta": f"S{f['semana_anio']}-{f['anio']}" if agrupar_semana else f["fecha"].isoformat(),
                "total": f["total"],
            }
            for f in serie
        ],
        "serie_por": "semana" if agrupar_semana else "dia",
    }


def comparar(user, base: Alcance, comp: Alcance) -> dict:
    """RF18: variación absoluta y porcentual por sector, punto y tipo entre dos periodos que no se superponen."""
    exigir_etl()
    if base.desde <= comp.hasta and comp.desde <= base.hasta:
        raise ValidationError("Los periodos seleccionados se superponen.")
    claves = {
        "sector": ("sector_id", "sector__nombre"),
        "punto": ("punto_id", "punto__codigo"),
        "tipo": ("tipo_residuo_id", "tipo_residuo__nombre"),
    }
    crecientes = tendencia_creciente(user, base, comp)

    def totales(a: Alcance, id_: str, etiqueta: str) -> dict:
        filas = hechos(user, a).filter(magnitud="PESO").values(id_, etiqueta).annotate(total=Sum("cantidad_base"))
        return {f[id_]: (f[etiqueta], f["total"]) for f in filas}

    resultado = {}
    for nombre, (id_, etiqueta) in claves.items():
        b, c = totales(base, id_, etiqueta), totales(comp, id_, etiqueta)
        filas = []
        for k in b.keys() | c.keys():
            tb = b[k][1] if k in b else CERO
            tc = c[k][1] if k in c else CERO
            filas.append(
                {
                    "id": k,
                    "nombre": (b.get(k) or c[k])[0],
                    "base_kg": tb,
                    "comparacion_kg": tc,
                    "variacion_kg": tc - tb,
                    "variacion_pct": _variacion(tc, tb),
                    "tendencia_creciente": (nombre, k) in crecientes,
                }
            )
        resultado[nombre] = sorted(filas, key=lambda f: f["variacion_kg"], reverse=True)
    if not any(resultado.values()):
        raise ValidationError("Ninguno de los periodos tiene datos suficientes para comparar.")
    return {
        "base": {"desde": base.desde, "hasta": base.hasta},
        "comparacion": {"desde": comp.desde, "hasta": comp.hasta},
        **resultado,
    }


def tendencia_creciente(user, base: Alcance, comp: Alcance) -> set[tuple[str, int]]:
    """Elementos con crecimiento mensual sostenido (3 meses consecutivos al alza) en el histórico disponible."""
    desde, hasta = min(base.desde, comp.desde), max(base.hasta, comp.hasta)
    qs = filtrar_por_sector(HechoResiduo.objects.filter(magnitud="PESO", fecha__range=(desde, hasta)), user, "sector")
    marcados = set()
    for nombre, campo in (("sector", "sector_id"), ("punto", "punto_id"), ("tipo", "tipo_residuo_id")):
        series: dict[int, list[Decimal]] = {}
        for f in (
            qs.annotate(mes_=TruncMonth("fecha"))
            .values(campo, "mes_")
            .annotate(t=Sum("cantidad_base"))
            .order_by(campo, "mes_")
        ):
            series.setdefault(f[campo], []).append(f["t"])
        for k, valores in series.items():
            ultimos = valores[-4:]
            if len(ultimos) >= 4 and all(x < y for x, y in zip(ultimos, ultimos[1:], strict=False)):
                marcados.add((nombre, k))
    return marcados


def mapa(user, a: Alcance) -> dict:
    """RF19–RF21: puntos activos con su generación del periodo, peso relativo y condición de crítico."""
    exigir_etl()
    puntos = filtrar_por_sector(PuntoRecoleccion.objects.filter(is_active=True), user, "sector").select_related(
        "sector"
    )
    if a.sector:
        puntos = puntos.filter(sector_id=a.sector)
    if a.punto:
        puntos = puntos.filter(pk=a.punto)
    totales = {
        f["punto_id"]: f["total"]
        for f in hechos(user, a).filter(magnitud="PESO").values("punto_id").annotate(total=Sum("cantidad_base"))
    }
    ultima = dict(
        JornadaPunto.objects.filter(atendido=True, punto__in=puntos)
        .values("punto_id")
        .annotate(u=Max("atendido_en"))
        .values_list("punto_id", "u")
    )
    maximo = max(totales.values(), default=CERO)
    umbral = ParametrosSistema.actual().umbral_critico_kg_dia
    filas = []
    for p in puntos:
        total = totales.get(p.pk, CERO)
        filas.append(
            {
                "id": p.pk,
                "codigo": p.codigo,
                "nombre": p.nombre,
                "sector": p.sector.nombre,
                "latitud": p.latitud,
                "longitud": p.longitud,
                "capacidad_kg": p.capacidad_kg,
                "total_kg": total,
                "promedio_dia_kg": round(total / a.dias, 2),
                "peso": round(float(total / maximo), 4) if maximo else 0.0,
                "critico": total / a.dias > umbral,
                "ultima_atencion": ultima.get(p.pk),
            }
        )
    return {
        "alcance": {"desde": a.desde, "hasta": a.hasta, "dias": a.dias},
        "maximo_kg": maximo,
        "umbral_critico_kg_dia": umbral,
        "puntos": filas,
        "registros": hechos(user, a).aggregate(n=Count("id"))["n"],
    }
