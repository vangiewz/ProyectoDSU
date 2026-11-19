from rest_framework import serializers

from ..models import EjecucionETL


class EjecucionETLSerializer(serializers.ModelSerializer):
    estado_display = serializers.CharField(source="get_estado_display", read_only=True)
    disparada_por_nombre = serializers.SerializerMethodField()
    duracion_segundos = serializers.FloatField(read_only=True)

    class Meta:
        model = EjecucionETL
        fields = "__all__"

    def get_disparada_por_nombre(self, obj):
        return (
            obj.disparada_por.get_full_name() or obj.disparada_por.username
            if obj.disparada_por
            else "Programación automática"
        )
