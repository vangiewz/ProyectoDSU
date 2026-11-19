"""Bloqueos transaccionales entre procesos, sin tablas ni migraciones adicionales."""

from django.db import connection


def bloquear_proceso(clave: int) -> None:
    """Serializa una sección crítica en PostgreSQL hasta terminar su transaction.atomic.

    El espacio de claves DSU evita bloquear aplicaciones ajenas. No depende de que ya exista
    una fila activa, ni de memoria compartida entre workers de Gunicorn.
    """
    if not connection.in_atomic_block:
        raise RuntimeError("El bloqueo requiere una transacción activa")
    with connection.cursor() as cursor:
        cursor.execute("SELECT pg_advisory_xact_lock(%s, %s)", [1146311936, clave])
