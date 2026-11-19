from decimal import Decimal

from django.conf import settings
from rest_framework import serializers

from apps.accounts.permissions import exigir_sector

from ..models import PuntoRecoleccion


class PuntoRecoleccionSerializer(serializers.ModelSerializer):
    sector_nombre = serializers.CharField(source="sector.nombre", read_only=True)
    estado_display = serializers.CharField(source="get_estado_display", read_only=True)
    capacidad_contenedores_litros = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = PuntoRecoleccion
        fields = "__all__"
        read_only_fields = ["is_active", "motivo_baja"]
        extra_kwargs = {"capacidad_kg": {"min_value": Decimal("0.01")}}

    def validate_sector(self, sector):
        if not sector.is_active:
            raise serializers.ValidationError("El sector está desactivado.")
        exigir_sector(self.context["request"].user, sector)
        return sector

    def validate(self, attrs):
        lat = attrs.get("latitud", getattr(self.instance, "latitud", None))
        lon = attrs.get("longitud", getattr(self.instance, "longitud", None))
        # Comparar Decimal con float puede excluir una coordenada sobre el borde.
        lat_min, lon_min, lat_max, lon_max = (Decimal(str(v)) for v in settings.CAMPUS_BBOX)
        if not (lat_min <= lat <= lat_max and lon_min <= lon <= lon_max):
            raise serializers.ValidationError({"latitud": "Las coordenadas están fuera del área atendida por la DSU."})
        return attrs
