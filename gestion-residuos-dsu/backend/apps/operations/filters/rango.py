from rest_framework.exceptions import ValidationError


def validar_rango(desde, hasta):
    if desde and hasta and desde > hasta:
        raise ValidationError("El rango de fechas es inválido: 'desde' es posterior a 'hasta'.")
