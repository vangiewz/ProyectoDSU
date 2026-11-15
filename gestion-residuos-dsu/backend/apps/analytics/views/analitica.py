from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.catalogs.models import ParametrosSistema

from ..services import indicadores as svc

VER = ["analytics.view_hechoresiduo"]


class AnaliticaViewSet(viewsets.ViewSet):
    """RF16–RF21: indicadores, comparación de periodos y datos del mapa sobre el plano analítico."""

    action_perms = {"indicadores": VER, "comparacion": VER, "mapa": VER, "powerbi": VER}

    @action(detail=False)
    def indicadores(self, request):
        return Response(svc.indicadores(request.user, svc.leer_alcance(request.query_params)))

    @action(detail=False)
    def comparacion(self, request):
        p = request.query_params

        def alcance(prefijo):
            return svc.leer_alcance(
                {
                    "desde": p.get(f"{prefijo}_desde"),
                    "hasta": p.get(f"{prefijo}_hasta"),
                    "sector": p.get("sector"),
                    "tipo_residuo": p.get("tipo_residuo"),
                }
            )

        return Response(svc.comparar(request.user, alcance("base"), alcance("comp")))

    @action(detail=False)
    def mapa(self, request):
        return Response(svc.mapa(request.user, svc.leer_alcance(request.query_params)))

    @action(detail=False)
    def powerbi(self, request):
        """RD8: enlace del informe publicado en Power BI que el Tablero inserta, si ya fue configurado."""
        return Response({"url": ParametrosSistema.actual().url_powerbi})
