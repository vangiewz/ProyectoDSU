from apps.accounts.permissions import filtrar_por_sector
from apps.audit.views import AuditedViewSet

from ..models import Contenedor
from ..serializers import ContenedorSerializer


class ContenedorViewSet(AuditedViewSet):
    """RF7: contenedores por punto. Los cambios de estado quedan en la bitácora."""

    serializer_class = ContenedorSerializer
    filterset_fields = ["punto", "punto__sector", "estado"]
    search_fields = ["codigo", "tipo", "punto__codigo"]

    def get_queryset(self):
        return filtrar_por_sector(Contenedor.objects.select_related("punto"), self.request.user, "punto__sector")
