from rest_framework import serializers

from ..models import AuditLog


class AuditLogSerializer(serializers.ModelSerializer):
    usuario = serializers.StringRelatedField()
    operacion_display = serializers.CharField(source="get_operacion_display", read_only=True)

    class Meta:
        model = AuditLog
        fields = "__all__"
