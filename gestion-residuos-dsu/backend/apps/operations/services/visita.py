from decimal import Decimal

from django.db import transaction
from django.db.models import Sum
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from apps.audit.models import AuditLog
from apps.audit.services import registrar
from apps.campus.models import Contenedor
from apps.catalogs.models import ParametrosSistema, UnidadMedida

from ..models import Jornada, JornadaPunto, RegistroResiduo
from .jornada import exigir_estado, exigir_personal

E = Jornada.Estado


Op = AuditLog.Operacion


def _parada(jornada, punto, bloquear=False):
    qs = jornada.ruta.select_related("punto")
    if bloquear:
        # RCM2: dos registros simultáneos del mismo punto se aplican uno tras otro, sin pisarse.
        qs = qs.select_for_update(of=("self",))
    try:
        return qs.get(punto=punto)
    except JornadaPunto.DoesNotExist as err:
        raise ValidationError({"punto": "El punto no pertenece a la ruta de esta jornada."}) from err


def _validar_capacidad(punto, detalles):
    """RF8 4.1: la cantidad debe ser coherente con la capacidad del punto."""
    tolerancia = ParametrosSistema.actual().tolerancia_capacidad
    kg = sum(
        (
            d["cantidad"] * d["unidad"].factor_conversion
            for d in detalles
            if d["unidad"].magnitud == UnidadMedida.Magnitud.PESO
        ),
        Decimal(0),
    )
    litros = sum(
        (
            d["cantidad"] * d["unidad"].factor_conversion
            for d in detalles
            if d["unidad"].magnitud == UnidadMedida.Magnitud.VOLUMEN
        ),
        Decimal(0),
    )
    if kg > punto.capacidad_kg * tolerancia:
        raise ValidationError(
            {"detalles": f"{kg:.2f} kg excede de forma manifiesta la capacidad del punto ({punto.capacidad_kg} kg)."}
        )
    cap_litros = punto.contenedores.exclude(
        estado__in=[Contenedor.Estado.BAJA, Contenedor.Estado.REEMPLAZADO]
    ).aggregate(t=Sum("capacidad_litros"))["t"]
    if cap_litros and litros > cap_litros * tolerancia:
        raise ValidationError({"detalles": f"{litros:.2f} L excede la capacidad instalada del punto ({cap_litros} L)."})


@transaction.atomic
def registrar_visita(request, jornada, punto, detalles, observaciones="", sin_generacion=False):
    """RF8: registra el vaciado de un punto (uno o varios tipos de residuo) o la visita sin generación."""
    exigir_personal(request.user, jornada)
    exigir_estado(jornada, E.EN_EJECUCION)
    parada = _parada(jornada, punto, bloquear=True)
    if sin_generacion and detalles:
        raise ValidationError("Una visita sin generación no lleva detalle de residuos.")
    if not sin_generacion and not detalles:
        raise ValidationError({"detalles": "Ingrese al menos un tipo de residuo con su cantidad."})
    _validar_capacidad(punto, detalles)

    ahora = timezone.now()
    registros = RegistroResiduo.objects.bulk_create(
        RegistroResiduo(
            jornada=jornada,
            punto=punto,
            tipo_residuo=d["tipo_residuo"],
            unidad=d["unidad"],
            cantidad=d["cantidad"],
            observaciones=observaciones,
            registrado_por=request.user,
            fecha_hora=ahora,
        )
        for d in detalles
    )
    parada.atendido, parada.sin_generacion, parada.motivo_omision, parada.atendido_en = True, sin_generacion, "", ahora
    parada.save()
    registrar(
        request,
        Op.CREAR,
        parada,
        entidad="visita",
        detalle=f"Punto {punto.codigo}: {'sin generación' if sin_generacion else f'{len(registros)} registro(s)'}",
        despues={"registros": [r.pk for r in registros]},
    )
    return registros


def omitir_punto(request, jornada, punto, motivo):
    """RF12 2.2: deja constancia del punto no atendido y su motivo."""
    exigir_personal(request.user, jornada)
    exigir_estado(jornada, E.EN_EJECUCION)
    if not motivo.strip():
        raise ValidationError({"motivo": "Indique el motivo por el que no se atendió el punto."})
    parada = _parada(jornada, punto)
    if parada.atendido:
        raise ValidationError("El punto ya fue atendido.")
    parada.atendido, parada.motivo_omision, parada.atendido_en = False, motivo, timezone.now()
    parada.save()
    registrar(request, Op.ACTUALIZAR, parada, detalle=f"Punto {punto.codigo} omitido: {motivo}")
