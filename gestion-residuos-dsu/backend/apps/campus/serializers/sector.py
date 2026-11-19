from rest_framework import serializers

from apps.accounts.models import Rol, User

from ..models import Sector


class SectorSerializer(serializers.ModelSerializer):
    supervisor = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(groups__name=Rol.SUPERVISOR, is_active=True), allow_null=True, required=False
    )
    supervisor_nombre = serializers.CharField(source="supervisor.get_full_name", read_only=True, default=None)
    tipo_display = serializers.CharField(source="get_tipo_display", read_only=True)
    puntos_activos = serializers.IntegerField(read_only=True)

    class Meta:
        model = Sector
        fields = "__all__"
        read_only_fields = ["is_active"]
