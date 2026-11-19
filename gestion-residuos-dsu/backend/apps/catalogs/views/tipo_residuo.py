from apps.audit.views import DeactivatableViewSet

from ..models import TipoResiduo
from ..serializers import TipoResiduoSerializer


class TipoResiduoViewSet(DeactivatableViewSet):
    queryset = TipoResiduo.objects.select_related("unidad")
    serializer_class = TipoResiduoSerializer
    filterset_fields = ["is_active", "clasificacion", "aprovechable"]
    search_fields = ["nombre"]
