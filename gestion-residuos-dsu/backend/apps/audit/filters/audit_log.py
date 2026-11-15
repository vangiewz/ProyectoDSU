import django_filters

from ..models import AuditLog


class AuditLogFilter(django_filters.FilterSet):
    desde = django_filters.DateFilter(field_name="fecha", lookup_expr="date__gte")
    hasta = django_filters.DateFilter(field_name="fecha", lookup_expr="date__lte")

    class Meta:
        model = AuditLog
        fields = ["usuario", "modulo", "operacion", "entidad"]
