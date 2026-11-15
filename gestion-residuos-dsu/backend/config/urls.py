from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from apps.accounts import views as accounts
from apps.analytics import views as analytics
from apps.audit.views import AuditLogViewSet
from apps.campus import views as campus
from apps.catalogs import views as catalogs
from apps.operations import views as operations
from apps.prediction import views as prediction

router = DefaultRouter()
router.register("usuarios", accounts.UserViewSet, basename="usuario")
router.register("roles", accounts.RoleViewSet, basename="rol")
router.register("permisos", accounts.PermissionViewSet, basename="permiso")
router.register("unidades", catalogs.UnidadMedidaViewSet, basename="unidad")
router.register("tipos-residuo", catalogs.TipoResiduoViewSet, basename="tipo-residuo")
router.register("periodos", catalogs.PeriodoAcademicoViewSet, basename="periodo")
router.register("sectores", campus.SectorViewSet, basename="sector")
router.register("puntos", campus.PuntoRecoleccionViewSet, basename="punto")
router.register("contenedores", campus.ContenedorViewSet, basename="contenedor")
router.register("vehiculos", operations.VehiculoViewSet, basename="vehiculo")
router.register("jornadas", operations.JornadaViewSet, basename="jornada")
router.register("registros", operations.RegistroResiduoViewSet, basename="registro")
router.register("incidencias", operations.IncidenciaViewSet, basename="incidencia")
router.register("bitacora", AuditLogViewSet, basename="bitacora")
router.register("etl", analytics.EjecucionETLViewSet, basename="etl")
router.register("analitica", analytics.AnaliticaViewSet, basename="analitica")
router.register("modelos", prediction.ModeloEntrenadoViewSet, basename="modelo")
router.register("predicciones", prediction.LotePrediccionViewSet, basename="prediccion")
router.register("recomendaciones", prediction.RecomendacionViewSet, basename="recomendacion")

api = [
    path("auth/login/", accounts.LoginView.as_view(), name="login"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("auth/logout/", accounts.LogoutView.as_view(), name="logout"),
    path("auth/me/", accounts.MeView.as_view(), name="me"),
    path("parametros/", catalogs.ParametrosView.as_view(), name="parametros"),
    path("reportes/<slug:tipo>/", analytics.ReportesView.as_view(), name="reportes"),
    path("", include(router.urls)),
]

urlpatterns = [
    path("api/", include(api)),
]
