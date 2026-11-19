from django.contrib.auth.models import Group, Permission
from rest_framework import serializers

APPS_DEL_SISTEMA = ["accounts", "auth", "audit", "catalogs", "campus", "operations", "analytics", "prediction"]


class PermissionSerializer(serializers.ModelSerializer):
    modulo = serializers.CharField(source="content_type.app_label", read_only=True)
    entidad = serializers.CharField(source="content_type.model", read_only=True)

    class Meta:
        model = Permission
        fields = ["id", "codename", "name", "modulo", "entidad"]


class RoleSerializer(serializers.ModelSerializer):
    permissions = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Permission.objects.filter(content_type__app_label__in=APPS_DEL_SISTEMA)
    )
    usuarios = serializers.IntegerField(source="user_set.count", read_only=True)

    class Meta:
        model = Group
        fields = ["id", "name", "permissions", "usuarios"]

    def validate_permissions(self, value):
        if not value:
            raise serializers.ValidationError("El rol debe tener al menos un permiso.")
        return value
