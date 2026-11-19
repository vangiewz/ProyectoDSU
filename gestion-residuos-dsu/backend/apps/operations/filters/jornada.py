import django_filters

from ..models import Jornada
from .rango import validar_rango


class JornadaFilter(django_filters.FilterSet):
    desde = django_filters.DateFilter(field_name="fecha", lookup_expr="gte")
    hasta = django_filters.DateFilter(field_name="fecha", lookup_expr="lte")

    class Meta:
        model = Jornada
        fields = ["sector", "estado", "turno", "responsable", "fecha"]

    def filter_queryset(self, queryset):
        validar_rango(self.form.cleaned_data.get("desde"), self.form.cleaned_data.get("hasta"))
        return super().filter_queryset(queryset)
