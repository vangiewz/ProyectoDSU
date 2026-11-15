from rest_framework import serializers

from ..models import TipoResiduo


class TipoResiduoSerializer(serializers.ModelSerializer):
    unidad_simbolo = serializers.CharField(source="unidad.simbolo", read_only=True)
    clasificacion_display = serializers.CharField(source="get_clasificacion_display", read_only=True)

    class Meta:
        model = TipoResiduo
        fields = "__all__"
        read_only_fields = ["is_active"]

    def validate_unidad(self, unidad):
        if not unidad.is_active:
            raise serializers.ValidationError("La unidad de medida está desactivada.")
        return unidad
