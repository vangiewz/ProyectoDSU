"""Mensajes de API en español sin exponer nombres internos del modelo."""

from django.http import Http404
from rest_framework.exceptions import NotFound
from rest_framework.views import exception_handler


def manejar_excepcion(exc, context):
    if isinstance(exc, Http404):
        exc = NotFound("No se encontró el registro solicitado.")
    return exception_handler(exc, context)
