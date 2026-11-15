from decimal import Decimal

from rest_framework import serializers

from apps.campus.models import PuntoRecoleccion
from apps.catalogs.models import TipoResiduo, UnidadMedida


class DetalleVisitaSerializer(serializers.Serializer):
    tipo_residuo = serializers.PrimaryKeyRelatedField(queryset=TipoResiduo.objects.filter(is_active=True))
    cantidad = serializers.DecimalField(max_digits=10, decimal_places=3, min_value=Decimal("0.001"))
    unidad = serializers.PrimaryKeyRelatedField(queryset=UnidadMedida.objects.filter(is_active=True), required=False)

    def validate(self, attrs):
        attrs.setdefault("unidad", attrs["tipo_residuo"].unidad)  # RF8 3.2: unidad propuesta por el tipo
        return attrs


class VisitaSerializer(serializers.Serializer):
    punto = serializers.PrimaryKeyRelatedField(queryset=PuntoRecoleccion.objects.all())
    sin_generacion = serializers.BooleanField(default=False)
    detalles = DetalleVisitaSerializer(many=True, required=False, default=list)
    observaciones = serializers.CharField(required=False, allow_blank=True, default="")


class OmisionSerializer(serializers.Serializer):
    punto = serializers.PrimaryKeyRelatedField(queryset=PuntoRecoleccion.objects.all())
    motivo = serializers.CharField()
