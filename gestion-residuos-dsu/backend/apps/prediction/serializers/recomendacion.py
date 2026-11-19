from rest_framework import serializers

from ..models import Recomendacion


class RecomendacionSerializer(serializers.ModelSerializer):
    punto_codigo = serializers.CharField(source="punto.codigo", read_only=True)
    punto_nombre = serializers.CharField(source="punto.nombre", read_only=True)
    sector_nombre = serializers.CharField(source="sector.nombre", read_only=True)
    tipo_display = serializers.CharField(source="get_tipo_display", read_only=True)
    urgencia_display = serializers.CharField(source="get_urgencia_display", read_only=True)
    estado_display = serializers.CharField(source="get_estado_display", read_only=True)
    es_alerta = serializers.SerializerMethodField()
    resuelta_por_nombre = serializers.SerializerMethodField()
    jornada_fecha = serializers.DateField(source="jornada.fecha", read_only=True, default=None)

    class Meta:
        model = Recomendacion
        fields = "__all__"

    def get_es_alerta(self, obj):
        return obj.tipo == Recomendacion.Tipo.PRIORIZAR

    def get_resuelta_por_nombre(self, obj):
        u = obj.resuelta_por
        return (u.get_full_name() or u.username) if u else None
