from rest_framework import serializers

from apps.campus.models import PuntoRecoleccion, Sector

from ..models import LotePrediccion


class LotePrediccionSerializer(serializers.ModelSerializer):
    version = serializers.IntegerField(source="modelo.version", read_only=True)
    sector_nombre = serializers.CharField(source="sector.nombre", read_only=True, default=None)
    punto_codigo = serializers.CharField(source="punto.codigo", read_only=True, default=None)
    solicitado_por_nombre = serializers.SerializerMethodField()

    class Meta:
        model = LotePrediccion
        fields = "__all__"

    def get_solicitado_por_nombre(self, obj):
        return obj.solicitado_por.get_full_name() or obj.solicitado_por.username


class SolicitudPrediccionSerializer(serializers.Serializer):
    """RF23 paso 1.2: horizonte en días y alcance opcional por sector o por punto."""

    horizonte = serializers.IntegerField()
    sector = serializers.PrimaryKeyRelatedField(queryset=Sector.objects.all(), required=False, allow_null=True)
    punto = serializers.PrimaryKeyRelatedField(
        queryset=PuntoRecoleccion.objects.select_related("sector"), required=False, allow_null=True
    )
