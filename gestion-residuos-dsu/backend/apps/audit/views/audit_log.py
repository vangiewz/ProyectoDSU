from rest_framework import viewsets

from ..filters.audit_log import AuditLogFilter
from ..models import AuditLog
from ..serializers import AuditLogSerializer


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    """RF26: consulta de la bitácora. Solo lectura; la BD rechaza cualquier modificación."""

    queryset = AuditLog.objects.select_related("usuario")
    serializer_class = AuditLogSerializer
    filterset_class = AuditLogFilter
    search_fields = ["detalle", "entidad_id"]
