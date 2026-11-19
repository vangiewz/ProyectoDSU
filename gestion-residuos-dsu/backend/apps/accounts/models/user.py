from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.functional import cached_property


class Rol:
    """Nombres de los grupos (roles) sembrados por la migración de roles (Tablas 12–15 del documento)."""

    ADMINISTRADOR = "Administrador"
    SUPERVISOR = "Supervisor"
    OPERATIVO = "Operativo"
    DIRECTIVO = "Directivo"

    # Roles que consultan todos los sectores sin restricción territorial.
    GLOBALES = {ADMINISTRADOR, DIRECTIVO}


class User(AbstractUser):
    ci = models.CharField("carnet de identidad", max_length=20, blank=True)
    telefono = models.CharField(max_length=20, blank=True)

    class Meta:
        ordering = ["username"]

    @cached_property
    def roles(self) -> set[str]:
        return set(self.groups.values_list("name", flat=True))

    @property
    def acceso_global(self) -> bool:
        return self.is_superuser or bool(self.roles & Rol.GLOBALES)
