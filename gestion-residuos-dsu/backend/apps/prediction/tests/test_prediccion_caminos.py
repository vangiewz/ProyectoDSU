"""Rechazos tempranos de CU28 sin crear lotes ni predicciones parciales."""

from types import SimpleNamespace
from unittest.mock import patch

import pandas as pd
import pytest
from rest_framework.exceptions import PermissionDenied, ValidationError

from apps.prediction.models import LotePrediccion
from apps.prediction.services import prediccion

from .test_prediccion import entrenar
from .test_prediccion import historico as historico


@pytest.mark.parametrize(
    "caso", ["horizonte_cero", "horizonte_excesivo", "sin_puntos", "sin_historia", "sin_dias", "sector_ajeno"]
)
def test_rechazos_prediccion(usuarios, campus, caso):
    p = campus["puntos"][0]
    model = SimpleNamespace(pk=1)
    horizonte = {"horizonte_cero": 0, "horizonte_excesivo": 999}.get(caso, 7)
    historia = pd.DataFrame() if caso == "sin_historia" else pd.DataFrame({"punto_id": [p.pk]})
    if caso == "sin_puntos":
        for punto in campus["puntos"]:
            punto.is_active = False
            punto.save()
    user = usuarios["otro_supervisor"] if caso == "sector_ajeno" else usuarios["supervisor"]
    antes = LotePrediccion.objects.count()
    with (
        patch.object(prediccion.entrenamiento, "vigente", return_value=model),
        patch.object(prediccion.datos, "estado_actual", return_value=historia),
        patch.object(prediccion.datos, "dias_habituales", return_value={}),
    ):
        error = PermissionDenied if caso == "sector_ajeno" else ValidationError
        with pytest.raises(error):
            prediccion.generar(
                SimpleNamespace(user=user), horizonte, sector=campus["sector"] if caso == "sector_ajeno" else None
            )
    assert LotePrediccion.objects.count() == antes


@pytest.mark.parametrize("alcance", ["sector", "punto", "ambos"])
def test_prediccion_con_filtros(usuarios, campus, historico, alcance):
    modelo = entrenar(usuarios["admin"])
    assert modelo.vigente
    kwargs = {}
    if alcance in ("sector", "ambos"):
        kwargs["sector"] = campus["sector"]
    if alcance in ("punto", "ambos"):
        kwargs["punto"] = campus["puntos"][0]
    lote = prediccion.generar(SimpleNamespace(user=usuarios["supervisor"], META={}), 7, **kwargs)
    from apps.prediction.models import Prediccion

    qs = Prediccion.objects.filter(lote=lote)
    assert qs.exists()
    assert set(qs.values_list("sector_id", flat=True)) == {campus["sector"].pk}
    if "punto" in kwargs:
        assert set(qs.values_list("punto_id", flat=True)) == {campus["puntos"][0].pk}
