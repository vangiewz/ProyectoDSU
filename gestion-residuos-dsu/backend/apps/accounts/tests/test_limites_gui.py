"""Regresión de valores no positivos reproducidos desde los formularios GUI."""

import pytest

from apps.audit.models import AuditLog


@pytest.mark.django_db
@pytest.mark.parametrize(
    "recurso,campo",
    [
        ("puntos", "capacidad_kg"),
        ("contenedores", "capacidad_litros"),
        ("unidades", "factor_conversion"),
        ("vehiculos", "capacidad_kg"),
    ],
)
@pytest.mark.parametrize("valor", ["0", "-1"])
def test_valor_no_positivo_rechazado_sin_escritura(cliente, usuarios, campus, recurso, campo, valor):
    payloads = {
        "puntos": {
            "codigo": "GUI-P",
            "nombre": "Punto QA",
            "sector": campus["sector"].pk,
            "latitud": "-17.775700",
            "longitud": "-63.195600",
        },
        "contenedores": {
            "codigo": "GUI-C",
            "tipo": "Turril QA",
            "punto": campus["puntos"][0].pk,
            "fecha_instalacion": "2026-11-19",
        },
        "unidades": {"nombre": "Unidad QA", "simbolo": "qa", "magnitud": "PESO"},
        "vehiculos": {"placa": "GUI-V", "descripcion": "Vehículo QA"},
    }
    auditados = AuditLog.objects.count()
    response = cliente(usuarios["admin"]).post(f"/api/{recurso}/", {**payloads[recurso], campo: valor}, format="json")
    assert response.status_code == 400
    assert campo in response.data
    assert AuditLog.objects.count() == auditados


@pytest.mark.django_db
def test_capacidad_vehiculo_opcional_y_minima(cliente, usuarios):
    c = cliente(usuarios["admin"])
    response = c.post(
        "/api/vehiculos/", {"placa": "GUI-NULL", "descripcion": "Sin medición", "capacidad_kg": None}, format="json"
    )
    assert response.status_code == 201
    assert response.data["capacidad_kg"] is None
    response = c.patch(f"/api/vehiculos/{response.data['id']}/", {"capacidad_kg": "0.01"}, format="json")
    assert response.status_code == 200
    assert response.data["capacidad_kg"] == "0.01"


@pytest.mark.django_db
def test_rol_con_permisos_se_guarda_y_audita(cliente, usuarios):
    from django.contrib.auth.models import Group, Permission

    permiso = Permission.objects.get(content_type__app_label="campus", codename="view_sector")
    c = cliente(usuarios["admin"])
    response = c.post("/api/roles/", {"name": "Rol GUI", "permissions": [permiso.pk]}, format="json")
    assert response.status_code == 201
    rol = Group.objects.get(pk=response.data["id"])
    assert list(rol.permissions.values_list("pk", flat=True)) == [permiso.pk]
    evento = AuditLog.objects.get(entidad="group", entidad_id=str(rol.pk), operacion="CREAR")
    assert evento.datos_nuevos["permissions"] == [permiso.pk]
    otro = Permission.objects.get(content_type__app_label="campus", codename="view_puntorecoleccion")
    response = c.patch(f"/api/roles/{rol.pk}/", {"name": "Rol GUI editado", "permissions": [otro.pk]}, format="json")
    assert response.status_code == 200
    evento = AuditLog.objects.get(entidad="group", entidad_id=str(rol.pk), operacion="ACTUALIZAR")
    assert evento.datos_anteriores["permissions"] == [permiso.pk]
    assert evento.datos_nuevos["permissions"] == [otro.pk]


@pytest.mark.django_db
@pytest.mark.parametrize(
    "lat,lon", [("-17.95", "-63.35"), ("-17.95", "-63.05"), ("-17.65", "-63.35"), ("-17.65", "-63.05")]
)
def test_coordenadas_en_borde_inclusivo(cliente, usuarios, campus, settings, lat, lon):
    settings.CAMPUS_BBOX = [-17.95, -63.35, -17.65, -63.05]
    response = cliente(usuarios["admin"]).patch(
        f"/api/puntos/{campus['puntos'][0].pk}/", {"latitud": lat, "longitud": lon}, format="json"
    )
    assert response.status_code == 200
    assert float(response.data["latitud"]) == float(lat)
    assert float(response.data["longitud"]) == float(lon)


@pytest.mark.django_db
def test_permisos_predictivos_disponibles_para_roles(cliente, usuarios):
    from django.contrib.auth.models import Permission

    c = cliente(usuarios["admin"])
    response = c.get("/api/permisos/")
    assert response.status_code == 200
    assert any(p["modulo"] == "prediction" and p["codename"] == "entrenar_modelo" for p in response.data)
    permiso = Permission.objects.get(content_type__app_label="prediction", codename="entrenar_modelo")
    response = c.post("/api/roles/", {"name": "Predictivo QA", "permissions": [permiso.pk]}, format="json")
    assert response.status_code == 201


@pytest.mark.django_db
def test_no_encontrado_en_espanol_sin_detalles_internos(cliente, usuarios):
    response = cliente(usuarios["admin"]).get("/api/jornadas/999999999/")
    assert response.status_code == 404
    assert response.data["detail"] == "No se encontró el registro solicitado."
