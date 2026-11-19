import pytest
from django.db import DatabaseError, transaction
from rest_framework.test import APIClient

from apps.audit.models import AuditLog


def test_login_emite_tokens_y_registra_bitacora(usuarios):
    r = APIClient().post("/api/auth/login/", {"username": "oper_t", "password": "Clave.Segura.2026"})
    assert r.status_code == 200 and "access" in r.data and "refresh" in r.data
    assert AuditLog.objects.filter(operacion="LOGIN", usuario=usuarios["operario"]).exists()

    r = APIClient().post("/api/auth/login/", {"username": "oper_t", "password": "mala"})
    assert r.status_code == 401
    assert AuditLog.objects.filter(operacion="LOGIN_FALLIDO").exists()


def test_cuenta_desactivada_no_ingresa(usuarios, cliente):
    admin = cliente(usuarios["admin"])
    assert admin.post(f"/api/usuarios/{usuarios['operario'].id}/desactivar/").status_code == 200
    r = APIClient().post("/api/auth/login/", {"username": "oper_t", "password": "Clave.Segura.2026"})
    assert r.status_code == 401


def test_operativo_no_administra_usuarios(usuarios, cliente):
    r = cliente(usuarios["operario"]).get("/api/usuarios/")
    assert r.status_code == 403
    assert AuditLog.objects.filter(operacion="ACCESO_DENEGADO", usuario=usuarios["operario"]).exists()
    assert cliente(usuarios["admin"]).get("/api/usuarios/").status_code == 200


def test_crear_usuario_valida_politica_de_contrasena(usuarios, cliente):
    admin = cliente(usuarios["admin"])
    datos = {"username": "nuevo", "first_name": "N", "last_name": "U", "roles": ["Operativo"], "password": "123"}
    assert admin.post("/api/usuarios/", datos, format="json").status_code == 400
    datos["password"] = "Otra.Clave.Larga.9"
    r = admin.post("/api/usuarios/", datos, format="json")
    assert r.status_code == 201 and r.data["roles"] == ["Operativo"] and "password" not in r.data


def test_bitacora_es_inalterable(usuarios):
    log = AuditLog.objects.create(modulo="test", operacion="CREAR", entidad="x")
    with pytest.raises(DatabaseError), transaction.atomic():
        AuditLog.objects.filter(pk=log.pk).update(detalle="alterado")
    with pytest.raises(DatabaseError), transaction.atomic():
        AuditLog.objects.filter(pk=log.pk).delete()
