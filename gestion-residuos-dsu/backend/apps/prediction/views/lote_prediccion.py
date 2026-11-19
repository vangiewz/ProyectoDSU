from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from ..models import LotePrediccion
from ..serializers import LotePrediccionSerializer, SolicitudPrediccionSerializer
from ..services import prediccion as svc

VER = ["prediction.view_prediccion"]


class LotePrediccionViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """RF23: solicitar predicciones, consultarlas consolidadas y alimentar la capa proyectada del mapa (RF20)."""

    serializer_class = LotePrediccionSerializer
    action_perms = {"list": VER, "retrieve": VER, "mapa": VER, "create": ["prediction.generar_prediccion"]}

    def get_queryset(self):
        qs = LotePrediccion.objects.select_related("modelo", "solicitado_por", "sector", "punto").defer(
            "modelo__artefacto", "solicitado_por__password"
        )
        user = self.request.user
        return qs if user.acceso_global else qs.filter(solicitado_por=user)

    def create(self, request):
        s = SolicitudPrediccionSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        lote = svc.generar(request, **s.validated_data)
        return Response(self._detalle(lote), status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        return Response(self._detalle(self.get_object()))

    def _detalle(self, lote):
        return {**self.get_serializer(lote).data, **svc.resumen(lote, self.request.user)}

    @action(detail=False)
    def mapa(self, request):
        sector = request.query_params.get("sector")
        return Response(svc.mapa(request.user, int(sector) if sector and sector.isdigit() else None))
