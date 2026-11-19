from django.db.models import Q, Sum
from rest_framework.exceptions import ValidationError

from apps.accounts.permissions import filtrar_por_sector
from apps.audit.views import DeactivatableViewSet

from ..models import Contenedor, PuntoRecoleccion
from ..serializers import PuntoRecoleccionSerializer

ACTIVOS = ~Q(contenedores__estado__in=[Contenedor.Estado.BAJA, Contenedor.Estado.REEMPLAZADO])


class PuntoRecoleccionViewSet(DeactivatableViewSet):
    """RF5: puntos georreferenciados. El operativo solo ve los puntos de sus jornadas."""

    serializer_class = PuntoRecoleccionSerializer
    filterset_fields = ["is_active", "sector", "estado"]
    search_fields = ["codigo", "nombre", "sector__nombre", "sector__codigo"]

    @staticmethod
    def visibles(user):
        return filtrar_por_sector(
            PuntoRecoleccion.objects.all(),
            user,
            "sector",
            Q(en_rutas__jornada__personal=user, en_rutas__jornada__estado__in=["CONFIRMADA", "EN_EJECUCION"]),
        )

    def get_queryset(self):
        return (
            self.visibles(self.request.user)
            .select_related("sector")
            .annotate(capacidad_contenedores_litros=Sum("contenedores__capacidad_litros", filter=ACTIVOS))
            .order_by("codigo")
        )

    def validar_desactivacion(self, obj, data):
        if not str(data.get("motivo", "")).strip():
            raise ValidationError({"motivo": "Indique el motivo de la desactivación."})
        obj.motivo_baja = data["motivo"]
