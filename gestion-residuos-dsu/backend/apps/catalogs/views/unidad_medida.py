from apps.audit.views import DeactivatableViewSet

from ..models import UnidadMedida
from ..serializers import UnidadMedidaSerializer


class UnidadMedidaViewSet(DeactivatableViewSet):
    queryset = UnidadMedida.objects.all()
    serializer_class = UnidadMedidaSerializer
    filterset_fields = ["is_active", "magnitud"]
    search_fields = ["nombre", "simbolo"]
