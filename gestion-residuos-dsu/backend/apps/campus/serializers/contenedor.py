from rest_framework import serializers

from apps.accounts.permissions import exigir_sector

from ..models import Contenedor


class ContenedorSerializer(serializers.ModelSerializer):
    punto_codigo = serializers.CharField(source="punto.codigo", read_only=True)
    estado_display = serializers.CharField(source="get_estado_display", read_only=True)

    class Meta:
        model = Contenedor
        fields = "__all__"

    def validate_punto(self, punto):
        if not punto.is_active:
            raise serializers.ValidationError("El punto de recolección está desactivado.")
        exigir_sector(self.context["request"].user, punto.sector)
        return punto
