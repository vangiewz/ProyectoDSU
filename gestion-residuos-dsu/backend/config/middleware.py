from django.utils.cache import add_never_cache_headers


def api_sin_cache(get_response):
    """Las respuestas de la API son datos vivos y por usuario: el navegador no debe guardarlas.

    Sin esto, Chrome puede servir una respuesta vieja (p. ej. de antes de una actualización) y la
    interfaz se rompe al leer un campo que esa versión no traía. Tampoco quedan datos en equipos compartidos.
    """

    def middleware(request):
        response = get_response(request)
        if request.path.startswith("/api/"):
            add_never_cache_headers(response)
        return response

    return middleware
