from apps.audit.views import DeactivatableViewSet

from ..models import Vehiculo
from ..serializers import (
    VehiculoSerializer,
)


class VehiculoViewSet(DeactivatableViewSet):
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer
    filterset_fields = ["is_active", "estado"]
    search_fields = ["placa", "descripcion"]
