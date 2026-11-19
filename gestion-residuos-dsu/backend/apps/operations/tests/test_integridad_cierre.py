from apps.campus.models import Sector
from apps.operations.models import Jornada, JornadaPunto


def test_cambio_sector_revalida_ruta_existente(usuarios, campus, hoy, cliente):
    sector = Sector.objects.create(codigo="NUEVO", nombre="Nuevo", supervisor=usuarios["supervisor"])
    jornada = Jornada.objects.create(
        fecha=hoy, turno="MANANA", sector=campus["sector"], planificada_por=usuarios["supervisor"]
    )
    JornadaPunto.objects.create(jornada=jornada, punto=campus["puntos"][0], orden=1)
    r = cliente(usuarios["supervisor"]).patch(f"/api/jornadas/{jornada.pk}/", {"sector": sector.pk}, format="json")
    assert r.status_code == 400
    jornada.refresh_from_db()
    assert jornada.sector_id == campus["sector"].pk
