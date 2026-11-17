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


def cabeceras_seguridad(get_response):
    """API separada del SPA: no necesita ejecutar scripts ni ser enmarcada.

    CORP permite recursos entre orígenes; las lecturas de datos siguen sujetas
    a CORS, JWT y permisos. No usar COEP restrictivo en el cliente Power BI.
    """

    def middleware(request):
        response = get_response(request)
        response.setdefault(
            "Content-Security-Policy", "default-src 'none'; frame-ancestors 'none'; base-uri 'none'; form-action 'none'"
        )
        response.setdefault("Permissions-Policy", "geolocation=(), camera=(), microphone=()")
        response.setdefault("Cross-Origin-Resource-Policy", "cross-origin")
        response.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
        return response

    return middleware
