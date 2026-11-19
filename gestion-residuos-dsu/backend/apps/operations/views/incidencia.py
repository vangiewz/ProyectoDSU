from django.db.models import Q
from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from apps.accounts.permissions import filtrar_por_sector
from apps.audit.models import AuditLog
from apps.audit.services import registrar
from apps.audit.views import AuditedViewSet

from ..models import Incidencia
from ..serializers import (
    IncidenciaSerializer,
)


class IncidenciaViewSet(AuditedViewSet):
    """RF10: registro y atención de incidencias. No se editan; se atienden."""

    serializer_class = IncidenciaSerializer
    filterset_fields = ["estado", "gravedad", "tipo", "punto", "punto__sector", "jornada"]
    search_fields = ["descripcion", "punto__codigo"]
    http_method_names = ["get", "post", "head", "options"]
    action_perms = {"atender": ["operations.atender_incidencia"]}

    def get_queryset(self):
        user = self.request.user
        qs = Incidencia.objects.select_related("punto__sector", "reportada_por", "atendida_por")
        return filtrar_por_sector(qs, user, "punto__sector", Q(reportada_por=user))

    def perform_create(self, serializer):
        serializer.validated_data["reportada_por"] = self.request.user
        super().perform_create(serializer)

    @action(detail=True, methods=["post"])
    def atender(self, request, pk=None):
        inc = self.get_object()
        if inc.estado == Incidencia.Estado.ATENDIDA:
            raise ValidationError("La incidencia ya fue atendida.")
        accion = str(request.data.get("accion_adoptada", "")).strip()
        if not accion:
            raise ValidationError({"accion_adoptada": "Registre la acción adoptada."})
        inc.estado, inc.accion_adoptada = Incidencia.Estado.ATENDIDA, accion
        inc.atendida_por, inc.atendida_en = request.user, timezone.now()
        inc.save()
        registrar(request, AuditLog.Operacion.TRANSICION, inc, despues={"estado": inc.estado, "accion": accion})
        return Response(self.get_serializer(inc).data)
