from django.db.models import Count, Q
from rest_framework.exceptions import ValidationError

from apps.accounts.permissions import filtrar_por_sector
from apps.audit.views import DeactivatableViewSet

from ..models import Sector
from ..serializers import SectorSerializer


class SectorViewSet(DeactivatableViewSet):
    """RF4: sectores y facultades."""

    serializer_class = SectorSerializer
    filterset_fields = ["is_active", "tipo", "supervisor"]
    search_fields = ["codigo", "nombre"]

    def get_queryset(self):
        user = self.request.user
        qs = (
            Sector.objects.select_related("supervisor")
            .annotate(puntos_activos=Count("puntos", filter=Q(puntos__is_active=True)))
            .order_by("codigo")
        )
        return filtrar_por_sector(qs, user, "", Q(jornadas__personal=user))

    def validar_desactivacion(self, obj, data):
        if obj.puntos.filter(is_active=True).exists():
            raise ValidationError("El sector tiene puntos de recolección activos; desactívelos primero.")
