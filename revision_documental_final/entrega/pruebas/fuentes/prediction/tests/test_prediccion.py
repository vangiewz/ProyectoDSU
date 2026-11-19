from datetime import datetime, time, timedelta
from decimal import Decimal

import numpy as np
import pytest
from django.db import connection
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from apps.analytics.services import etl
from apps.campus.models import PuntoRecoleccion
from apps.catalogs.models import ParametrosSistema
from apps.operations.models import Jornada, JornadaPunto, RegistroResiduo
from apps.prediction.models import ModeloEntrenado, Recomendacion
from apps.prediction.services import datos, entrenamiento

E = ModeloEntrenado.Estado
RAPIDO = {"n_estimators": 20, "max_depth": 8, "min_samples_leaf": 2}


@pytest.fixture(autouse=True)
def modelos_dir(settings, tmp_path):
    settings.MODELOS_DIR = tmp_path


@pytest.fixture
def historico(usuarios, campus):
    """Unos 120 días hábiles de vaciados: P1 genera ~30 kg y P2 ~60 kg, con lunes más cargados."""
    hoy = timezone.localdate()
    rng = np.random.default_rng(1)
    fechas = [hoy - timedelta(days=i) for i in range(170, 0, -1) if (hoy - timedelta(days=i)).weekday() < 5]
    jornadas = Jornada.objects.bulk_create(
        Jornada(
            fecha=f, turno="MANANA", sector=campus["sector"], planificada_por=usuarios["supervisor"], estado="CERRADA"
        )
        for f in fechas
    )
    RegistroResiduo.objects.bulk_create(
        RegistroResiduo(
            jornada=j,
            punto=punto,
            tipo_residuo=campus["tipo"],
            unidad=campus["kg"],
            cantidad=Decimal(f"{base * (1.15 if j.fecha.weekday() == 0 else 1) * rng.uniform(0.92, 1.08):.3f}"),
            registrado_por=usuarios["operario"],
            fecha_hora=timezone.make_aware(datetime.combine(j.fecha, time(9))),
        )
        for j in jornadas
        for base, punto in zip((30, 60), campus["puntos"], strict=True)
    )
    etl.ejecutar(etl.iniciar())
    ParametrosSistema.objects.update_or_create(
        pk=1, defaults={"min_registros_entrenamiento": 50, "umbral_r2_modelo": Decimal("0.3")}
    )
    return fechas


def entrenar(usuario=None):
    return entrenamiento.entrenar(entrenamiento.iniciar(usuario, RAPIDO))


def test_entrenamiento_sin_volumen_minimo_no_publica(db):
    modelo = entrenar()
    assert modelo.estado == E.RECHAZADO and not modelo.vigente
    assert "se necesitan al menos" in modelo.mensaje
    with pytest.raises(ValidationError):
        entrenamiento.vigente()


def test_entrena_publica_predice_y_revierte(usuarios, historico, cliente):
    admin, sup = cliente(usuarios["admin"]), cliente(usuarios["supervisor"])
    assert sup.post("/api/modelos/entrenar/").status_code == 403
    assert sup.post("/api/predicciones/", {"horizonte": 7}, format="json").status_code == 400  # sin modelo

    v1 = entrenar(usuarios["admin"])
    assert v1.estado == E.APROBADO and v1.vigente, v1.mensaje
    assert v1.r2 >= 0.3 and v1.rmse > 0 and set(v1.importancias) <= set(datos.VARIABLES)
    # Partición cronológica: la prueba son las fechas más recientes.
    assert historico[0] < v1.corte <= historico[-1]

    assert sup.post("/api/predicciones/", {"horizonte": 31}, format="json").status_code == 400
    r = sup.post("/api/predicciones/", {"horizonte": 7}, format="json")
    assert r.status_code == 201, r.data
    assert r.data["version"] == 1
    p1, p2 = sorted(r.data["por_punto"], key=lambda p: p["punto__codigo"])
    assert p2["cantidad_kg"] > p1["cantidad_kg"] and p1["margen_kg"] > 0
    # Capa proyectada del mapa (RF20) y reporte con predicciones (RF27).
    assert len(sup.get("/api/predicciones/mapa/").data["puntos"]) == 2
    assert len(sup.get("/api/reportes/prediccion/").data["filas"]) == 2
    assert sup.get("/api/reportes/prediccion/", {"formato": "pdf"}).content.startswith(b"%PDF")
    # RD8: Power BI lee las predicciones vigentes desde la vista bi_predicciones.
    with connection.cursor() as c:
        c.execute("SELECT COUNT(DISTINCT punto_codigo) FROM bi_predicciones")
        assert c.fetchone()[0] == 2

    # Reversión (RD13): la v2 queda vigente al aprobarse y se vuelve a la v1.
    v2 = entrenar(usuarios["admin"])
    assert v2.vigente
    assert sup.post(f"/api/modelos/{v1.pk}/publicar/").status_code == 403
    assert admin.post(f"/api/modelos/{v1.pk}/publicar/").status_code == 200
    v1.refresh_from_db()
    v2.refresh_from_db()
    assert v1.vigente and not v2.vigente


def test_alerta_de_desborde_se_resuelve_y_entra_en_la_jornada(usuarios, campus, historico, cliente):
    entrenar()
    p1, p2 = campus["puntos"]
    PuntoRecoleccion.objects.filter(pk=p2.pk).update(capacidad_kg=Decimal("40"))  # P2 genera ~60 kg por día
    jornada = Jornada.objects.create(
        fecha=timezone.localdate() + timedelta(days=1),
        turno="MANANA",
        sector=campus["sector"],
        planificada_por=usuarios["supervisor"],
    )
    JornadaPunto.objects.create(jornada=jornada, punto=p1, orden=1)
    sup = cliente(usuarios["supervisor"])
    assert sup.post("/api/predicciones/", {"horizonte": 7}, format="json").status_code == 201

    alerta = Recomendacion.objects.get(punto=p2, tipo=Recomendacion.Tipo.PRIORIZAR)
    assert alerta.urgencia == Recomendacion.Urgencia.ALTA and alerta.evidencia["capacidad_kg"] == 40.0
    assert Recomendacion.objects.filter(punto=p2, tipo=Recomendacion.Tipo.REDISTRIBUIR_CONTENEDORES).exists()
    assert not Recomendacion.objects.filter(punto=p1, tipo=Recomendacion.Tipo.PRIORIZAR).exists()

    url = f"/api/recomendaciones/{alerta.pk}/"
    assert cliente(usuarios["otro_supervisor"]).post(url + "aceptar/", {"motivo": "x"}).status_code == 404
    assert sup.post(url + "aceptar/", {}, format="json").status_code == 400  # falta el motivo
    r = sup.post(url + "aceptar/", {"motivo": "Coincide con lo observado"}, format="json")
    assert r.status_code == 200 and r.data["jornada"] == jornada.pk
    assert list(jornada.ruta.order_by("orden").values_list("punto__codigo", flat=True)) == ["P2", "P1"]
    assert sup.post(url + "descartar/", {"motivo": "x"}, format="json").status_code == 400  # ya resuelta
    assert cliente(usuarios["operario"]).get("/api/recomendaciones/").status_code == 403
