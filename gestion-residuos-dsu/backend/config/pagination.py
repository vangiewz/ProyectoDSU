from rest_framework.pagination import PageNumberPagination


class Paginacion(PageNumberPagination):
    """25 por página; el cliente puede pedir hasta 500 (selects y mapa de puntos)."""

    page_size = 25
    page_size_query_param = "page_size"
    max_page_size = 500
