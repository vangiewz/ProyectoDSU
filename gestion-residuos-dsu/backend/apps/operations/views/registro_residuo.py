from django.db.models import Count, DecimalField, ExpressionWrapper, F, Q, Sum
from rest_framework import viewsets

from apps.accounts.permissions import filtrar_por_sector

from ..filters.registro_residuo import RegistroFilter
from ..models import RegistroResiduo
from ..serializers import (
    RegistroResiduoSerializer,
)


class RegistroResiduoViewSet(viewsets.ReadOnlyModelViewSet):
    """RF9: histórico de residuos con filtros, paginación y totales por tipo.

    El alta se hace en /jornadas/{id}/visitas/ (RF8); no hay edición ni borrado (RNF11).
    """

    serializer_class = RegistroResiduoSerializer
    filterset_class = RegistroFilter
    search_fields = ["punto__codigo", "punto__nombre", "observaciones"]
    ordering_fields = ["fecha_hora", "cantidad"]

    def get_queryset(self):
        user = self.request.user
        qs = RegistroResiduo.objects.select_related(
            "punto__sector", "tipo_residuo", "unidad", "registrado_por", "jornada__sector"
        )
        return filtrar_por_sector(qs, user, "punto__sector", Q(registrado_por=user))

    def list(self, request, *args, **kwargs):
        qs = self.filter_queryset(self.get_queryset())
        normalizada = ExpressionWrapper(F("cantidad") * F("unidad__factor_conversion"), output_field=DecimalField())
        totales = list(
            qs.order_by()
            .values("tipo_residuo__nombre", "unidad__magnitud")
            .annotate(total=Sum(normalizada), registros=Count("id"))
            .order_by("tipo_residuo__nombre")
        )
        page = self.paginate_queryset(qs)
        response = self.get_paginated_response(self.get_serializer(page, many=True).data)
        response.data["totales"] = totales
        return response
