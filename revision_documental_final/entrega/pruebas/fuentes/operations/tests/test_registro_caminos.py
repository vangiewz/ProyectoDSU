"""Caminos básicos de RF8 (CU9 Registrar vaciado): uno por cada decisión del diagrama de secuencia.
Ningún rechazo debe dejar registros ni marcar la parada como atendida."""

from datetime import date
from decimal import Decimal
from types import SimpleNamespace

import pytest
from rest_framework.exceptions import PermissionDenied, ValidationError

from apps.campus.models import Contenedor
from apps.catalogs.models import UnidadMedida
from apps.operations.models import Jornada, JornadaPunto, RegistroResiduo
from apps.operations.services.visita import registrar_visita

CASOS = {
    "no_asignado": PermissionDenied,
    "estado": ValidationError,
    "fuera_ruta": ValidationError,
    "sin_generacion_con_detalle": ValidationError,
    "sin_detalle": ValidationError,
    "excede_kg": ValidationError,
    "excede_litros": ValidationError,
    "valido": None,
}


@pytest.mark.parametrize("caso", CASOS)
def test_caminos_registro(usuarios, campus, hoy, caso):
    sup, op = usuarios["supervisor"], usuarios["operario"]
    p1, p2 = campus["puntos"]
    j = Jornada.objects.create(
        fecha=hoy, turno="MANANA", sector=campus["sector"], planificada_por=sup, estado=Jornada.Estado.EN_EJECUCION
    )
    JornadaPunto.objects.create(jornada=j, punto=p1, orden=1)
    j.personal.add(op)
    punto, sin_generacion = p1, False
    detalles = [{"tipo_residuo": campus["tipo"], "unidad": campus["kg"], "cantidad": Decimal("35.5")}]

    if caso == "no_asignado":
        j.personal.clear()
    elif caso == "estado":
        j.estado = Jornada.Estado.PLANIFICADA
        j.save()
    elif caso == "fuera_ruta":
        punto = p2
    elif caso == "sin_generacion_con_detalle":
        sin_generacion = True
    elif caso == "sin_detalle":
        detalles = []
    elif caso == "excede_kg":
        detalles[0]["cantidad"] = Decimal("151")  # capacidad 100 kg x tolerancia 1,5
    elif caso == "excede_litros":
        litro = UnidadMedida.objects.create(nombre="Litro", simbolo="L", magnitud="VOLUMEN", factor_conversion=1)
        Contenedor.objects.create(
            punto=p1, codigo="C-1", tipo="Turril", capacidad_litros=200, fecha_instalacion=date(2026, 1, 5)
        )
        detalles = [{"tipo_residuo": campus["tipo"], "unidad": litro, "cantidad": Decimal("301")}]  # 200 L x 1,5

    request = SimpleNamespace(user=op, META={})
    if CASOS[caso] is None:
        registros = registrar_visita(request, j, punto, detalles, sin_generacion=sin_generacion)
        assert len(registros) == 1 and registros[0].registrado_por == op
        assert JornadaPunto.objects.get(jornada=j, punto=p1).atendido is True
    else:
        with pytest.raises(CASOS[caso]):
            registrar_visita(request, j, punto, detalles, sin_generacion=sin_generacion)
        assert not RegistroResiduo.objects.exists()
        assert JornadaPunto.objects.get(jornada=j, punto=p1).atendido is None
