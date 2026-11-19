from rest_framework import serializers

from ..models import RegistroResiduo


class RegistroResiduoSerializer(serializers.ModelSerializer):
    punto_codigo = serializers.CharField(source="punto.codigo", read_only=True)
    sector = serializers.CharField(source="punto.sector.nombre", read_only=True)
    tipo_residuo_nombre = serializers.CharField(source="tipo_residuo.nombre", read_only=True)
    unidad_simbolo = serializers.CharField(source="unidad.simbolo", read_only=True)
    registrado_por_nombre = serializers.CharField(source="registrado_por.get_full_name", read_only=True)
    jornada_detalle = serializers.CharField(source="jornada.__str__", read_only=True)

    class Meta:
        model = RegistroResiduo
        fields = "__all__"
