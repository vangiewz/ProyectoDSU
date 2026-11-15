import django_filters

from ..models import RegistroResiduo
from .rango import validar_rango


class RegistroFilter(django_filters.FilterSet):
    desde = django_filters.DateFilter(field_name="fecha_hora", lookup_expr="date__gte")
    hasta = django_filters.DateFilter(field_name="fecha_hora", lookup_expr="date__lte")
    sector = django_filters.NumberFilter(field_name="punto__sector")

    class Meta:
        model = RegistroResiduo
        fields = ["punto", "tipo_residuo", "registrado_por", "jornada"]

    def filter_queryset(self, queryset):
        validar_rango(self.form.cleaned_data.get("desde"), self.form.cleaned_data.get("hasta"))
        return super().filter_queryset(queryset)
