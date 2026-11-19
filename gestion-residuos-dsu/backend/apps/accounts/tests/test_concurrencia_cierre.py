from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
from types import SimpleNamespace
from unittest.mock import patch

import pytest
from django.db import close_old_connections, connection, connections
from django.db.backends.postgresql.operations import DatabaseOperations
from rest_framework.exceptions import ValidationError

from apps.accounts.models import User
from apps.analytics.models import EjecucionETL
from apps.analytics.services import etl
from apps.campus.models import Sector
from apps.operations.models import Jornada, Vehiculo
from apps.operations.services.jornada import asignar
from apps.prediction.models import ModeloEntrenado
from apps.prediction.services import entrenamiento

pytestmark = pytest.mark.django_db(transaction=True, serialized_rollback=True)


@pytest.fixture(scope="module", autouse=True)
def limpieza_exclusiva_base_de_pruebas():
    """Django necesita TRUNCATE entre TransactionTestCase; el producto lo prohíbe deliberadamente.

    Solo el flush de test_* suspende el trigger durante su limpieza. La aplicación y sus pruebas
    de inmutabilidad conservan el trigger habilitado. No ejecutar este módulo contra datos reales.
    """
    original = DatabaseOperations.sql_flush

    def sql_flush(self, *args, **kwargs):
        if not self.connection.settings_dict["NAME"].startswith("test_"):
            raise RuntimeError("La limpieza solo admite la base test_* aislada")
        return (
            ["ALTER TABLE audit_auditlog DISABLE TRIGGER USER;"]
            + original(self, *args, **kwargs)
            + ["ALTER TABLE audit_auditlog ENABLE TRIGGER USER;"]
        )

    with patch.object(DatabaseOperations, "sql_flush", sql_flush):
        yield


def simultaneas(funciones):
    barrera = Barrier(len(funciones))

    def correr(fn):
        close_old_connections()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT pg_backend_pid()")
                pid = cursor.fetchone()[0]
            barrera.wait(timeout=15)
            return pid, fn()
        finally:
            connections.close_all()

    with ThreadPoolExecutor(max_workers=len(funciones)) as pool:
        resultados = list(pool.map(correr, funciones))
    assert len({pid for pid, _ in resultados}) == len(funciones)
    return [valor for _, valor in resultados]


@pytest.mark.parametrize("servicio,modelo", [(etl, EjecucionETL), (entrenamiento, ModeloEntrenado)])
def test_inicio_realmente_concurrente(servicio, modelo):
    resultados = simultaneas([lambda: servicio.iniciar() is not None] * 6)
    assert sum(resultados) == 1
    assert modelo.objects.count() == 1


@pytest.mark.parametrize("recurso", ["personal", "vehiculo"])
def test_asignacion_concurrente_no_duplica_recurso(usuarios, campus, hoy, recurso):
    sector2 = Sector.objects.create(codigo="S2", nombre="Segundo", supervisor=usuarios["supervisor"])
    jornadas = [
        Jornada.objects.create(fecha=hoy, turno="MANANA", sector=s, planificada_por=usuarios["supervisor"])
        for s in [campus["sector"], sector2]
    ]
    segundo = User.objects.create_user(username="segundo_qa", password="Solo.Pruebas.2026")
    segundo.groups.set(usuarios["operario"].groups.all())
    vehiculo = Vehiculo.objects.create(placa="QA-123", descripcion="Vehículo sintético")

    def intentar(j):
        operario = segundo if recurso == "vehiculo" and j.pk == jornadas[1].pk else usuarios["operario"]
        try:
            asignar(
                SimpleNamespace(user=usuarios["supervisor"], META={}),
                j,
                [operario],
                [vehiculo] if recurso == "vehiculo" else [],
                operario,
            )
            return True
        except ValidationError:
            return False

    assert sum(simultaneas([lambda j=j: intentar(j) for j in jornadas])) == 1
