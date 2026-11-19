"""Caminos de rechazo de RF13: no debe persistir asignaciones parciales."""

from types import SimpleNamespace

import pytest
from rest_framework.exceptions import ValidationError

from apps.operations.models import Jornada, Vehiculo
from apps.operations.services.jornada import asignar


@pytest.mark.parametrize(
    "caso",
    [
        "estado",
        "sin_responsable",
        "fuera_personal",
        "inactivo",
        "vehiculo_fuera",
        "personal_ocupado",
        "vehiculo_ocupado",
        "valido",
    ],
)
def test_caminos_asignacion(usuarios, campus, hoy, caso):
    sup, op = usuarios["supervisor"], usuarios["operario"]
    j = Jornada.objects.create(fecha=hoy, turno="MANANA", sector=campus["sector"], planificada_por=sup)
    v = Vehiculo.objects.create(placa="AUD-001", descripcion="Camioneta de prueba", capacidad_kg=100)
    responsable = op
    if caso == "estado":
        j.estado = Jornada.Estado.CERRADA
        j.save()
    elif caso == "sin_responsable":
        responsable = None
    elif caso == "fuera_personal":
        responsable = sup
    elif caso == "inactivo":
        op.is_active = False
        op.save()
    elif caso == "vehiculo_fuera":
        v.estado = Vehiculo.Estado.FUERA_SERVICIO
        v.save()
    elif caso in ("personal_ocupado", "vehiculo_ocupado"):
        from apps.campus.models import Sector

        otro = Sector.objects.create(codigo="AUD2", nombre="Segundo sector", supervisor=sup)
        j2 = Jornada.objects.create(fecha=hoy, turno="MANANA", sector=otro, planificada_por=sup)
        (j2.personal if caso == "personal_ocupado" else j2.vehiculos).add(op if caso == "personal_ocupado" else v)
    if caso == "valido":
        asignar(SimpleNamespace(user=sup, META={}), j, [op], [v], responsable)
        j.refresh_from_db()
        assert j.responsable == op and list(j.personal.all()) == [op] and list(j.vehiculos.all()) == [v]
    else:
        with pytest.raises(ValidationError):
            asignar(SimpleNamespace(user=sup, META={}), j, [op], [v], responsable)
        j.refresh_from_db()
        assert j.responsable is None and not j.personal.exists() and not j.vehiculos.exists()
