from django.contrib.auth.models import Group
from rest_framework.test import APIClient

from apps.accounts.models import Rol, User
from apps.audit.models import AuditLog


def test_logout_revoca_refresh_y_conserva_evidencia(usuarios):
    c = APIClient()
    login = c.post("/api/auth/login/", {"username": "oper_t", "password": "Clave.Segura.2026"})
    assert login.status_code == 200
    c.credentials(HTTP_AUTHORIZATION="Bearer " + login.data["access"])
    assert c.post("/api/auth/logout/", {"refresh": login.data["refresh"]}).status_code == 205
    assert AuditLog.objects.filter(operacion="LOGOUT", usuario=usuarios["operario"]).exists()
    assert c.post("/api/auth/refresh/", {"refresh": login.data["refresh"]}).status_code == 401


def test_directivo_consulta_sin_escribir_y_admin_no_registra_campo(usuarios, campus, hoy, cliente):
    d = User.objects.create_user(username="directivo_t", password="Clave.Segura.2026")
    d.groups.add(Group.objects.get(name=Rol.DIRECTIVO))
    directivo = cliente(d)
    assert directivo.get("/api/puntos/").status_code == 200
    assert directivo.get("/api/predicciones/").status_code == 200
    # CU28 y RF23 permiten solicitar predicciones al Directivo. El permiso
    # no autoriza modificar maestros ni registrar operaciones de campo.
    assert d.has_perm("prediction.generar_prediccion")
    assert directivo.post("/api/predicciones/", {"horizonte": 0}, format="json").status_code == 400
    assert (
        directivo.post("/api/sectores/", {"codigo": "NO", "nombre": "No permitido"}, format="json").status_code == 403
    )
    admin = cliente(usuarios["admin"])
    assert admin.post("/api/incidencias/", {}, format="json").status_code == 403
