"""Predicción de la generación futura por punto, sector y tipo de residuo (RF23).

Margen de error: el RMSE de prueba del modelo para cada estimación diaria de un punto y tipo. Al sumar
estimaciones se combina como raíz de la suma de cuadrados (errores supuestos independientes).
"""

import math
from datetime import timedelta
from decimal import Decimal

import pandas as pd
from django.db import transaction
from django.db.models import Count, F, Max, Min, OuterRef, Subquery, Sum
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from apps.accounts.permissions import exigir_sector, filtrar_por_sector
from apps.audit.models import AuditLog
from apps.audit.services import registrar
from apps.campus.models import PuntoRecoleccion
from apps.catalogs.models import ParametrosSistema

from ..models import LotePrediccion, Prediccion
from . import datos, entrenamiento, recomendaciones


def generar(request, horizonte: int, sector=None, punto=None) -> LotePrediccion:
    user = request.user
    maximo = ParametrosSistema.actual().horizonte_max_dias
    if not 1 <= horizonte <= maximo:
        raise ValidationError({"horizonte": f"El horizonte debe estar entre 1 y {maximo} días."})
    modelo = entrenamiento.vigente()
    puntos = filtrar_por_sector(PuntoRecoleccion.objects.filter(is_active=True), user, "sector")
    for alcance in (sector, punto.sector if punto else None):
        if alcance:
            exigir_sector(user, alcance)
    if sector:
        puntos = puntos.filter(sector=sector)
    if punto:
        puntos = puntos.filter(pk=punto.pk)
    ids = list(puntos.values_list("pk", flat=True))
    if not ids:
        raise ValidationError("No hay puntos activos en el alcance indicado.")

    # Paso 2: estado histórico de cada punto y variables temporales de las fechas futuras.
    hoy = timezone.localdate()
    estado = datos.estado_actual(hoy, ids)
    if estado.empty:
        raise ValidationError("Los puntos del alcance carecen de historial reciente suficiente para predecir.")
    habituales = datos.dias_habituales(hoy, ids)
    fechas = pd.date_range(hoy + timedelta(days=1), periods=horizonte)
    filas = estado.merge(pd.DataFrame({"fecha": fechas}), how="cross")
    filas = filas[
        [d in habituales.get(p, ()) for p, d in zip(filas["punto_id"], filas["fecha"].dt.dayofweek, strict=True)]
    ]
    if filas.empty:
        raise ValidationError("En el horizonte solicitado no hay días de recolección habitual para estos puntos.")
    filas = datos.con_temporales(filas.reset_index(drop=True))

    # Paso 3: inferencia con el modelo publicado.
    estimado = entrenamiento.cargar(modelo.pk).predict(filas[modelo.variables]).clip(min=0)
    margen = Decimal(str(round(modelo.rmse, 3)))
    filas["cantidad_kg"] = estimado.round(3)
    filas["margen_kg"] = float(margen)
    filas["fecha"] = filas["fecha"].dt.date
    omitidos = list(puntos.exclude(pk__in=set(estado["punto_id"])).values_list("codigo", flat=True))

    # Paso 4: almacenamiento con la versión del modelo y entrega a las recomendaciones.
    with transaction.atomic():
        lote = LotePrediccion.objects.create(
            modelo=modelo,
            solicitado_por=user,
            desde=fechas[0].date(),
            hasta=fechas[-1].date(),
            sector=sector,
            punto=punto,
            puntos_omitidos=omitidos,
        )
        Prediccion.objects.bulk_create(
            (
                Prediccion(
                    lote=lote,
                    punto_id=int(f.punto_id),
                    sector_id=int(f.sector_id),
                    tipo_residuo_id=int(f.tipo_residuo_id),
                    fecha=f.fecha,
                    cantidad_kg=Decimal(str(f.cantidad_kg)),
                    margen_kg=margen,
                )
                for f in filas.itertuples()
            ),
            batch_size=2000,
        )
        emitidas = recomendaciones.evaluar(
            lote, filas[["punto_id", "tipo_residuo_id", "fecha", "cantidad_kg", "margen_kg"]]
        )
    registrar(
        request,
        AuditLog.Operacion.PROCESO,
        lote,
        detalle=f"Predicción {lote.desde:%d/%m}–{lote.hasta:%d/%m} con el modelo v{modelo.version}: "
        f"{len(ids) - len(omitidos)} punto(s), {len(emitidas)} recomendación(es)",
    )
    return lote


def _agrupar(qs, *campos) -> list[dict]:
    filas = (
        qs.values(*campos).annotate(kg=Sum("cantidad_kg"), m2=Sum(F("margen_kg") * F("margen_kg"))).order_by(*campos)
    )
    return [
        {
            **{k: v for k, v in f.items() if k not in ("kg", "m2")},
            "cantidad_kg": round(f["kg"], 2),
            "margen_kg": round(Decimal(math.sqrt(f["m2"])), 2),
        }
        for f in filas
    ]


def resumen(lote: LotePrediccion, user) -> dict:
    """RF23 paso 4.1: consolidado por punto, sector, tipo y fecha, siempre con su margen."""
    qs = filtrar_por_sector(lote.predicciones.all(), user, "sector")
    return {
        "por_punto": _agrupar(
            qs, "punto_id", "punto__codigo", "punto__nombre", "sector__nombre", "punto__capacidad_kg"
        ),
        "por_sector": _agrupar(qs, "sector_id", "sector__codigo", "sector__nombre"),
        "por_tipo": _agrupar(qs, "tipo_residuo_id", "tipo_residuo__nombre"),
        "serie": _agrupar(qs, "fecha"),
    }


def vigentes(user):
    """Predicciones futuras del lote más reciente que incluyó a cada punto."""
    ultimo = Prediccion.objects.filter(punto=OuterRef("punto")).order_by("-lote_id").values("lote_id")[:1]
    qs = Prediccion.objects.filter(fecha__gt=timezone.localdate(), lote_id=Subquery(ultimo))
    return filtrar_por_sector(qs, user, "sector")


def mapa(user, sector: int | None = None) -> dict:
    """Capa proyectada del mapa de calor (RF20): generación estimada de cada punto en su horizonte vigente."""
    qs = vigentes(user)
    if sector:
        qs = qs.filter(sector_id=sector)
    filas = (
        qs.values("punto_id", "punto__codigo", "punto__nombre", "sector__nombre", "punto__latitud", "punto__longitud")
        .annotate(
            kg=Sum("cantidad_kg"),
            m2=Sum(F("margen_kg") * F("margen_kg")),
            dias=Count("fecha", distinct=True),
            desde=Min("fecha"),
            hasta=Max("fecha"),
            version=Max("lote__modelo__version"),
        )
        .order_by("punto__codigo")
    )
    maximo = max((f["kg"] for f in filas), default=Decimal(0))
    return {
        "maximo_kg": maximo,
        "puntos": [
            {
                "id": f["punto_id"],
                "codigo": f["punto__codigo"],
                "nombre": f["punto__nombre"],
                "sector": f["sector__nombre"],
                "latitud": f["punto__latitud"],
                "longitud": f["punto__longitud"],
                "total_kg": round(f["kg"], 2),
                "margen_kg": round(Decimal(math.sqrt(f["m2"])), 2),
                "promedio_dia_kg": round(f["kg"] / f["dias"], 2),
                "peso": round(float(f["kg"] / maximo), 4) if maximo else 0.0,
                "desde": f["desde"],
                "hasta": f["hasta"],
                "version": f["version"],
            }
            for f in filas
        ],
    }
