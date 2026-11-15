from django.db.models import Case, Value, When
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.accounts.permissions import filtrar_por_sector

from ..models import Recomendacion
from ..serializers import RecomendacionSerializer
from ..services import recomendaciones

RESOLVER = ["prediction.resolver_recomendacion"]


class RecomendacionViewSet(viewsets.ReadOnlyModelViewSet):
    """RF24: panel de alertas y recomendaciones con su evidencia; el supervisor las acepta o descarta (RI7)."""

    serializer_class = RecomendacionSerializer
    filterset_fields = ["estado", "urgencia", "tipo", "sector", "punto", "lote"]
    action_perms = {"aceptar": RESOLVER, "descartar": RESOLVER}

    def get_queryset(self):
        U = Recomendacion.Urgencia
        rango = Case(When(urgencia=U.ALTA, then=Value(0)), When(urgencia=U.MEDIA, then=Value(1)), default=Value(2))
        qs = Recomendacion.objects.select_related("punto", "sector", "resuelta_por", "jornada").order_by(
            rango, "-creada_en"
        )
        return filtrar_por_sector(qs, self.request.user, "sector")

    def _resolver(self, request, aceptar):
        rec = recomendaciones.resolver(request, self.get_object(), aceptar, request.data.get("motivo", ""))
        return Response(self.get_serializer(rec).data)

    @action(detail=True, methods=["post"])
    def aceptar(self, request, pk=None):
        return self._resolver(request, True)

    @action(detail=True, methods=["post"])
    def descartar(self, request, pk=None):
        return self._resolver(request, False)
