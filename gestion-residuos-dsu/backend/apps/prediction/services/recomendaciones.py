"""Alertas tempranas y recomendaciones logísticas a partir de las predicciones (RF24).

Son apoyo a la decisión (RNF13): el sistema las emite con su evidencia y el supervisor las acepta o descarta.
"""

import math
from datetime import timedelta

import pandas as pd
from django.db import transaction
from django.db.models import Count, Min
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from apps.accounts.permissions import exigir_sector
from apps.audit.models import AuditLog
from apps.audit.services import registrar
from apps.campus.models import PuntoRecoleccion
from apps.catalogs.models import ParametrosSistema, TipoResiduo
from apps.operations.models import Incidencia, Jornada, JornadaPunto

from ..models import LotePrediccion, Recomendacion
from . import datos

R = Recomendacion
PLANIFICABLES = [Jornada.Estado.PLANIFICADA, Jornada.Estado.CONFIRMADA]


def _num(x: float) -> str:
    return f"{x:,.1f}".replace(",", "X").replace(".", ",").replace("X", ".")


def evaluar(lote: LotePrediccion, preds: pd.DataFrame) -> list[Recomendacion]:
    """Pasos 1 a 3 de RF24 para cada punto del lote; reemplaza las recomendaciones pendientes anteriores.

    `preds` trae las predicciones recién guardadas (punto_id, tipo_residuo_id, fecha, cantidad_kg, margen_kg):
    se reciben en memoria para no volver a leerlas de la base (RTR11).
    """
    p = ParametrosSistema.actual()
    alerta_pct, crecimiento_pct, no_aprov_pct = (
        float(p.alerta_capacidad_pct),
        float(p.crecimiento_alerta_pct),
        float(p.no_aprovechable_max_pct),
    )
    if preds.empty:
        return []
    no_aprovechables = set(
        TipoResiduo.objects.filter(clasificacion=TipoResiduo.Clasificacion.NO_APROVECHABLE).values_list("pk", flat=True)
    )
    preds = preds.assign(m2=preds["margen_kg"] ** 2)
    preds["no_aprov"] = preds["cantidad_kg"].where(preds["tipo_residuo_id"].isin(no_aprovechables), 0.0)
    diario = preds.groupby(["punto_id", "fecha"])[["cantidad_kg", "m2", "no_aprov"]].sum().reset_index()
    ids = [int(i) for i in diario["punto_id"].unique()]

    # Paso 1: historia reciente, próxima atención prevista e incidencias de segregación.
    hoy = timezone.localdate()
    reciente = datos.serie_diaria(hoy - timedelta(days=datos.VENTANA_DIAS - 1), ids)
    promedio_reciente = reciente.groupby(["punto_id", "fecha"])["kg"].sum().groupby("punto_id").mean().to_dict()
    proxima = dict(
        JornadaPunto.objects.filter(
            punto_id__in=ids, atendido__isnull=True, jornada__fecha__gt=hoy, jornada__estado__in=PLANIFICABLES
        )
        .values("punto_id")
        .annotate(f=Min("jornada__fecha"))
        .values_list("punto_id", "f")
    )
    mal_segregado = dict(
        Incidencia.objects.filter(
            punto_id__in=ids, tipo=Incidencia.Tipo.MAL_SEGREGADO, fecha_hora__date__gte=hoy - timedelta(days=90)
        )
        .values("punto_id")
        .annotate(n=Count("id"))
        .values_list("punto_id", "n")
    )
    puntos = PuntoRecoleccion.objects.in_bulk(ids)

    Recomendacion.objects.filter(punto_id__in=ids, estado=R.Estado.PENDIENTE).update(estado=R.Estado.REEMPLAZADA)
    nuevas = []
    for punto_id, d in diario.groupby("punto_id"):
        punto = puntos[int(punto_id)]
        capacidad = float(punto.capacidad_kg)
        # Lo que se acumula hasta la próxima atención planificada o, sin planificación, el próximo día habitual.
        fin = proxima.get(punto_id)
        ventana = d[d["fecha"] <= fin] if fin else d.head(1)
        if ventana.empty:
            ventana = d.head(1)
        # Redondeadas una vez: el mensaje y la evidencia muestran la misma cifra.
        acumulado, margen = round(ventana["cantidad_kg"].sum(), 1), round(math.sqrt(ventana["m2"].sum()), 1)
        proyectado_dia, maximo_dia = d["cantidad_kg"].mean(), d["cantidad_kg"].max()
        reciente_dia = promedio_reciente.get(punto_id)
        crecimiento = (proyectado_dia / reciente_dia - 1) * 100 if reciente_dia else None
        no_aprov = d["no_aprov"].sum() * 100 / d["cantidad_kg"].sum() if d["cantidad_kg"].sum() else 0.0
        evidencia = {
            "capacidad_kg": capacidad,
            "proxima_atencion": fin.isoformat() if fin else None,
            "dias_hasta_atencion": len(ventana),
            "acumulado_proyectado_kg": round(acumulado, 2),
            "margen_kg": round(margen, 2),
            "ocupacion_proyectada_pct": round(acumulado * 100 / capacidad, 1),
            "promedio_proyectado_dia_kg": round(proyectado_dia, 2),
            "maximo_proyectado_dia_kg": round(maximo_dia, 2),
            "promedio_reciente_dia_kg": round(reciente_dia, 2) if reciente_dia else None,
            "crecimiento_pct": round(crecimiento, 1) if crecimiento is not None else None,
            "no_aprovechable_pct": round(no_aprov, 1),
            "incidencias_mal_segregado_90d": mal_segregado.get(punto_id, 0),
            "modelo_version": lote.modelo.version,
            "horizonte": {"desde": lote.desde.isoformat(), "hasta": lote.hasta.isoformat()},
        }

        def emitir(tipo, urgencia, mensaje, punto=punto, evidencia=evidencia):
            nuevas.append(
                R(
                    lote=lote,
                    punto=punto,
                    sector_id=punto.sector_id,
                    tipo=tipo,
                    urgencia=urgencia,
                    mensaje=mensaje,
                    evidencia=evidencia,
                )
            )

        # Paso 2: alerta temprana de desborde antes de la siguiente atención.
        if acumulado >= capacidad:
            urgencia = R.Urgencia.ALTA
        elif acumulado + margen >= capacidad:
            urgencia = R.Urgencia.MEDIA
        elif acumulado >= capacidad * alerta_pct / 100:
            urgencia = R.Urgencia.BAJA
        else:
            urgencia = None
        cuando = f"antes de la atención del {fin:%d/%m}" if fin else "en el próximo día de recolección"
        if urgencia:
            emitir(
                R.Tipo.PRIORIZAR,
                urgencia,
                f"Riesgo de desborde {cuando}: se proyectan {_num(acumulado)} ± {_num(margen)} kg para una "
                f"capacidad de {_num(capacidad)} kg. Priorizar el punto en la siguiente jornada.",
            )
        # Paso 3: acciones según el patrón detectado.
        if maximo_dia >= capacidad:
            emitir(
                R.Tipo.REDISTRIBUIR_CONTENEDORES,
                R.Urgencia.ALTA if proyectado_dia >= capacidad else R.Urgencia.MEDIA,
                f"La generación diaria proyectada llega a {_num(maximo_dia)} kg y supera la capacidad instalada de "
                f"{_num(capacidad)} kg aun con recolección diaria. Redistribuir o incorporar contenedores.",
            )
        if crecimiento is not None and crecimiento >= crecimiento_pct:
            emitir(
                R.Tipo.INCREMENTAR_FRECUENCIA,
                R.Urgencia.MEDIA if urgencia else R.Urgencia.BAJA,
                f"Se proyecta un promedio de {_num(proyectado_dia)} kg por día de recolección, "
                f"{_num(crecimiento)} % más que en los últimos {datos.VENTANA_DIAS} días. "
                "Incrementar la frecuencia de recolección.",
            )
        if no_aprov >= no_aprov_pct:
            emitir(
                R.Tipo.REFORZAR_SEPARACION,
                R.Urgencia.BAJA,
                f"El {_num(no_aprov)} % de lo proyectado es residuo no aprovechable "
                f"(tolerado: {_num(no_aprov_pct)} %). Reforzar la separación en origen.",
            )
    return Recomendacion.objects.bulk_create(nuevas)


def _incorporar(rec: Recomendacion) -> Jornada | None:
    """RF24 paso 4.3: lleva el punto a la siguiente jornada planificada de su sector."""
    jornada = (
        Jornada.objects.filter(sector_id=rec.sector_id, fecha__gte=timezone.localdate(), estado__in=PLANIFICABLES)
        .order_by("fecha", "turno")
        .first()
    )
    if jornada is None:
        return None
    resto = list(jornada.ruta.exclude(punto_id=rec.punto_id).order_by("orden"))
    if rec.tipo == R.Tipo.PRIORIZAR:
        JornadaPunto.objects.update_or_create(jornada=jornada, punto_id=rec.punto_id, defaults={"orden": 1})
        for i, parada in enumerate(resto, start=2):
            parada.orden = i
        JornadaPunto.objects.bulk_update(resto, ["orden"])
    else:
        JornadaPunto.objects.get_or_create(jornada=jornada, punto_id=rec.punto_id, defaults={"orden": len(resto) + 1})
    return jornada


def resolver(request, rec: Recomendacion, aceptar: bool, motivo: str) -> Recomendacion:
    """RF24 paso 4.2: el supervisor acepta o descarta con motivo; queda constancia en la bitácora."""
    motivo = (motivo or "").strip()
    if not motivo:
        raise ValidationError({"motivo": "Indique el motivo de la decisión."})
    exigir_sector(request.user, rec.sector)
    with transaction.atomic():
        rec = Recomendacion.objects.select_for_update().get(pk=rec.pk)
        if rec.estado != R.Estado.PENDIENTE:
            raise ValidationError(f"La recomendación ya fue resuelta ({rec.get_estado_display().lower()}).")
        rec.estado = R.Estado.ACEPTADA if aceptar else R.Estado.DESCARTADA
        if aceptar and rec.tipo in (R.Tipo.PRIORIZAR, R.Tipo.INCREMENTAR_FRECUENCIA):
            rec.jornada = _incorporar(rec)
        rec.motivo_decision, rec.resuelta_por, rec.resuelta_en = motivo, request.user, timezone.now()
        rec.save()
    registrar(
        request,
        AuditLog.Operacion.TRANSICION,
        rec,
        antes={"estado": R.Estado.PENDIENTE},
        despues={"estado": rec.estado, "motivo": motivo, "jornada": rec.jornada_id},
        detalle=f"{rec.get_tipo_display()} en {rec.punto.codigo}: {rec.get_estado_display().lower()}",
    )
    return rec
