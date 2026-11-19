from rest_framework import serializers

from apps.accounts.models import Rol
from apps.accounts.permissions import exigir_sector

from ..models import Incidencia, Jornada


class IncidenciaSerializer(serializers.ModelSerializer):
    punto_codigo = serializers.CharField(source="punto.codigo", read_only=True)
    sector = serializers.CharField(source="punto.sector.nombre", read_only=True)
    tipo_display = serializers.CharField(source="get_tipo_display", read_only=True)
    gravedad_display = serializers.CharField(source="get_gravedad_display", read_only=True)
    reportada_por_nombre = serializers.CharField(source="reportada_por.get_full_name", read_only=True)

    class Meta:
        model = Incidencia
        fields = "__all__"
        read_only_fields = ["estado", "reportada_por", "fecha_hora", "atendida_por", "accion_adoptada", "atendida_en"]

    def validate(self, attrs):
        user = self.context["request"].user
        jornada, punto = attrs.get("jornada"), attrs["punto"]
        exigir_sector(user, punto.sector)
        if jornada is None:
            if not user.acceso_global and Rol.SUPERVISOR not in user.roles:
                raise serializers.ValidationError({"jornada": "Registre la incidencia dentro de una jornada activa."})
            return attrs
        if jornada.estado != Jornada.Estado.EN_EJECUCION:
            raise serializers.ValidationError({"jornada": "La jornada no está en ejecución."})
        if not jornada.ruta.filter(punto=punto).exists():
            raise serializers.ValidationError({"punto": "El punto no pertenece a la ruta de la jornada."})
        if Rol.OPERATIVO in user.roles and not jornada.personal.filter(pk=user.pk).exists():
            raise serializers.ValidationError({"jornada": "No forma parte del personal de esta jornada."})
        return attrs
