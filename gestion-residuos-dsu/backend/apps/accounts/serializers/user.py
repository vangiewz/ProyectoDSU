from django.contrib.auth.models import Group
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from ..models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, style={"input_type": "password"})
    roles = serializers.SlugRelatedField(
        source="groups", many=True, slug_field="name", queryset=Group.objects.all(), required=False
    )

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "ci",
            "telefono",
            "roles",
            "is_active",
            "last_login",
            "date_joined",
            "password",
        ]
        read_only_fields = ["is_active", "last_login", "date_joined"]
        extra_kwargs = {"first_name": {"required": True}, "last_name": {"required": True}}

    def validate(self, attrs):
        if self.instance is None and not attrs.get("password"):
            raise serializers.ValidationError({"password": "La contraseña es obligatoria."})
        if attrs.get("password"):
            candidato = User(**{k: v for k, v in attrs.items() if k not in ("password", "groups")})
            validate_password(attrs["password"], candidato)
        return attrs

    def create(self, validated_data):
        password = validated_data.pop("password")
        groups = validated_data.pop("groups", [])
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        user.groups.set(groups)
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class MeSerializer(serializers.ModelSerializer):
    roles = serializers.SerializerMethodField()
    permisos = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email", "is_superuser", "roles", "permisos"]

    def get_roles(self, user):
        return sorted(user.roles)

    def get_permisos(self, user):
        return sorted(user.get_all_permissions())
