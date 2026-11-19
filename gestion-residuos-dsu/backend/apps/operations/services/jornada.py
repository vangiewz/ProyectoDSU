from django.db import transaction
from django.db.models import DecimalField, ExpressionWrapper, F, Sum
from django.utils import timezone
from rest_framework.exceptions import PermissionDenied, ValidationError

from apps.accounts.models import Rol
from apps.audit.models import AuditLog
from apps.audit.services import registrar
from config.concurrencia import bloquear_proceso

from ..models import Jornada, Vehiculo

E = Jornada.Estado


Op = AuditLog.Operacion


def exigir_estado(jornada, *estados):
    if jornada.estado not in estados:
        raise ValidationError(f"La jornada está {jornada.get_estado_display().lower()}; operación no permitida.")


def exigir_personal(user, jornada):
    """El operativo solo actúa sobre jornadas en las que está asignado (RF12 exc. 3)."""
    if Rol.OPERATIVO in user.roles and not user.acceso_global and not jornada.personal.filter(pk=user.pk).exists():
        raise PermissionDenied("No forma parte del personal asignado a esta jornada.")


def _transicion(request, jornada, nuevo_estado, **campos):
    anterior = jornada.estado
    jornada.estado = nuevo_estado
    for k, v in campos.items():
        setattr(jornada, k, v)
    jornada.save()
    registrar(request, Op.TRANSICION, jornada, antes={"estado": anterior}, despues={"estado": nuevo_estado})


@transaction.atomic
def asignar(request, jornada, personal, vehiculos, responsable):
    """RF13: asigna personal y vehículos validando superposición en el mismo turno."""
    bloquear_proceso(3)  # Recursos compartidos por jornadas de distintos sectores y workers.
    jornada = Jornada.objects.select_for_update().get(pk=jornada.pk)
    exigir_estado(jornada, E.PLANIFICADA, E.CONFIRMADA)
    if responsable is None:
        raise ValidationError({"responsable": "Debe designar un responsable de la jornada."})
    if responsable not in personal:
        raise ValidationError({"responsable": "El responsable debe formar parte del personal asignado."})
    no_operativos = [u.username for u in personal if not u.is_active or Rol.OPERATIVO not in u.roles]
    if no_operativos:
        raise ValidationError({"personal": f"No son personal operativo activo: {', '.join(no_operativos)}."})
    fuera = [v.placa for v in vehiculos if v.estado == Vehiculo.Estado.FUERA_SERVICIO or not v.is_active]
    if fuera:
        raise ValidationError({"vehiculos": f"Vehículos fuera de servicio: {', '.join(fuera)}."})

    mismo_turno = Jornada.objects.filter(fecha=jornada.fecha, turno=jornada.turno).exclude(pk=jornada.pk)
    ocupados = set(mismo_turno.filter(personal__in=personal).values_list("personal__username", flat=True))
    if ocupados:
        raise ValidationError(
            {"personal": f"Ya asignados a otra jornada en este turno: {', '.join(sorted(ocupados))}."}
        )
    v_ocupados = set(mismo_turno.filter(vehiculos__in=vehiculos).values_list("vehiculos__placa", flat=True))
    if v_ocupados:
        raise ValidationError({"vehiculos": f"Ya asignados en este turno: {', '.join(sorted(v_ocupados))}."})

    jornada.personal.set(personal)
    jornada.vehiculos.set(vehiculos)
    jornada.responsable = responsable
    jornada.save(update_fields=["responsable"])
    registrar(
        request,
        Op.ACTUALIZAR,
        jornada,
        detalle="Asignación de personal y vehículos",
        despues={
            "personal": [u.pk for u in personal],
            "vehiculos": [v.pk for v in vehiculos],
            "responsable": responsable.pk,
        },
    )


def confirmar(request, jornada):
    """RF11 paso 3: publica la jornada para el personal asignado."""
    exigir_estado(jornada, E.PLANIFICADA)
    if not jornada.ruta.exists():
        raise ValidationError("La ruta no tiene puntos.")
    if jornada.ruta.filter(punto__is_active=False).exists():
        raise ValidationError("La ruta incluye puntos desactivados.")
    if jornada.responsable_id is None:
        raise ValidationError("Asigne personal y un responsable antes de confirmar.")
    _transicion(request, jornada, E.CONFIRMADA)


def abrir(request, jornada):
    """RF12 paso 1: inicia la ejecución el día planificado."""
    exigir_personal(request.user, jornada)
    exigir_estado(jornada, E.CONFIRMADA)
    if jornada.fecha != timezone.localdate():
        raise ValidationError("Solo puede abrirse una jornada en la fecha planificada.")
    _transicion(request, jornada, E.EN_EJECUCION, hora_inicio=timezone.now())


def cerrar(request, jornada, observaciones=""):
    """RF12 paso 4: cierra la jornada; desde aquí es inmutable."""
    exigir_estado(jornada, E.EN_EJECUCION)
    pendientes = list(jornada.ruta.filter(atendido__isnull=True).values_list("punto__codigo", flat=True))
    if pendientes:
        raise ValidationError(f"Puntos sin registro ni motivo de omisión: {', '.join(pendientes)}.")
    _transicion(request, jornada, E.CERRADA, hora_fin=timezone.now(), observaciones_cierre=observaciones)


def resumen(jornada):
    """RF12 paso 3: consolidado por tipo de residuo y contraste planificado vs. ejecutado."""
    normalizada = ExpressionWrapper(F("cantidad") * F("unidad__factor_conversion"), output_field=DecimalField())
    por_tipo = list(
        jornada.registros.values("tipo_residuo__nombre", "unidad__magnitud")
        .annotate(total=Sum(normalizada))
        .order_by("tipo_residuo__nombre")
    )
    ruta = jornada.ruta.all()
    planificados = ruta.count()
    atendidos = ruta.filter(atendido=True).count()
    return {
        "planificados": planificados,
        "atendidos": atendidos,
        "omitidos": list(ruta.filter(atendido=False).values("punto__codigo", "motivo_omision")),
        "pendientes": ruta.filter(atendido__isnull=True).count(),
        "cobertura": round(atendidos * 100 / planificados, 1) if planificados else 0,
        "total_kg": jornada.registros.filter(unidad__magnitud="PESO").aggregate(t=Sum(normalizada))["t"] or 0,
        "total_litros": jornada.registros.filter(unidad__magnitud="VOLUMEN").aggregate(t=Sum(normalizada))["t"] or 0,
        "por_tipo": por_tipo,
        "incidencias": jornada.incidencias.count(),
        "incidencias_pendientes": jornada.incidencias.filter(estado="PENDIENTE").count(),
    }
