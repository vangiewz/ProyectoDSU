from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from ..models import EjecucionETL
from ..serializers import EjecucionETLSerializer
from ..services import etl


class EjecucionETLViewSet(viewsets.ReadOnlyModelViewSet):
    """RF15: bitácora de ejecuciones del ETL y disparo bajo demanda (corre en segundo plano)."""

    queryset = EjecucionETL.objects.select_related("disparada_por")
    serializer_class = EjecucionETLSerializer
    filterset_fields = ["estado"]
    action_perms = {"ejecutar": ["analytics.ejecutar_etl"]}

    @action(detail=False, methods=["post"])
    def ejecutar(self, request):
        ejecucion = etl.iniciar(request.user)
        if ejecucion is None:
            return Response({"detail": "Ya hay una ejecución del ETL en curso."}, status=status.HTTP_409_CONFLICT)
        etl.ejecutar_en_segundo_plano(ejecucion)
        return Response(self.get_serializer(ejecucion).data, status=status.HTTP_202_ACCEPTED)
