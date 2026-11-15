from rest_framework import serializers

from ..models import ModeloEntrenado


class ModeloEntrenadoSerializer(serializers.ModelSerializer):
    estado_display = serializers.CharField(source="get_estado_display", read_only=True)
    entrenado_por_nombre = serializers.SerializerMethodField()

    class Meta:
        model = ModeloEntrenado
        exclude = ["artefacto"]

    def get_entrenado_por_nombre(self, obj):
        u = obj.entrenado_por
        return (u.get_full_name() or u.username) if u else "Línea de comandos"
