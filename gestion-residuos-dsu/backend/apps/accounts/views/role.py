from django.contrib.auth.models import Group, Permission
from rest_framework import viewsets

from apps.audit.views import AuditedViewSet

from ..serializers import APPS_DEL_SISTEMA, PermissionSerializer, RoleSerializer


class RoleViewSet(AuditedViewSet):
    """RF2: roles = grupos de Django con sus permisos."""

    queryset = Group.objects.prefetch_related("permissions").order_by("name")
    serializer_class = RoleSerializer
    search_fields = ["name"]


class PermissionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Permission.objects.filter(content_type__app_label__in=APPS_DEL_SISTEMA).select_related("content_type")
    serializer_class = PermissionSerializer
    pagination_class = None
    action_perms = {"list": ["auth.view_group"], "retrieve": ["auth.view_group"]}
