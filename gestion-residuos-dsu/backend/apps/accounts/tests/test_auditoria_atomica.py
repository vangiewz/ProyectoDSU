from unittest.mock import patch

import pytest

from apps.campus.models import Sector


def test_fallo_bitacora_revierte_alta(usuarios, cliente):
    with patch("apps.audit.views.base.registrar", side_effect=RuntimeError("fallo simulado de auditoría")):
        with pytest.raises(RuntimeError):
            cliente(usuarios["admin"]).post("/api/sectores/", {"codigo": "NUEVO", "nombre": "Sector nuevo"})
    assert not Sector.objects.filter(codigo="NUEVO").exists()
