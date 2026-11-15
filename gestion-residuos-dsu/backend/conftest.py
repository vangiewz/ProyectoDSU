from decimal import Decimal

import pytest
from django.contrib.auth.models import Group
from django.utils import timezone
from rest_framework.test import APIClient

from apps.accounts.models import Rol, User
from apps.campus.models import PuntoRecoleccion, Sector
from apps.catalogs.models import TipoResiduo, UnidadMedida


def crear_usuario(username, rol):
    user = User.objects.create_user(username=username, password="Clave.Segura.2026", first_name=username)
    user.groups.add(Group.objects.get(name=rol))
    return user


@pytest.fixture
def cliente():
    """Devuelve un APIClient autenticado como el usuario indicado."""

    def _cliente(user):
        c = APIClient()
        c.force_authenticate(user)
        return c

    return _cliente


@pytest.fixture
def usuarios(db):
    return {
        "admin": crear_usuario("admin_t", Rol.ADMINISTRADOR),
        "supervisor": crear_usuario("super_t", Rol.SUPERVISOR),
        "otro_supervisor": crear_usuario("super2_t", Rol.SUPERVISOR),
        "operario": crear_usuario("oper_t", Rol.OPERATIVO),
    }


@pytest.fixture
def campus(usuarios):
    kg = UnidadMedida.objects.create(nombre="Kilogramo", simbolo="kg", magnitud="PESO", factor_conversion=1)
    tipo = TipoResiduo.objects.create(nombre="Orgánico", clasificacion="ORGANICO", aprovechable=True, unidad=kg)
    sector = Sector.objects.create(codigo="S1", nombre="Sector 1", supervisor=usuarios["supervisor"])
    puntos = [
        PuntoRecoleccion.objects.create(
            sector=sector,
            codigo=f"P{i}",
            nombre=f"Punto {i}",
            latitud=Decimal("-17.775700"),
            longitud=Decimal("-63.195600"),
            capacidad_kg=Decimal("100"),
        )
        for i in (1, 2)
    ]
    return {"kg": kg, "tipo": tipo, "sector": sector, "puntos": puntos}


@pytest.fixture
def hoy():
    return timezone.localdate().isoformat()
