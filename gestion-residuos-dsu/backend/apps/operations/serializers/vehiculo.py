from decimal import Decimal

from rest_framework import serializers

from ..models import Vehiculo


class VehiculoSerializer(serializers.ModelSerializer):
    estado_display = serializers.CharField(source="get_estado_display", read_only=True)

    class Meta:
        model = Vehiculo
        fields = "__all__"
        read_only_fields = ["is_active"]
        extra_kwargs = {"capacidad_kg": {"min_value": Decimal("0.01")}}
