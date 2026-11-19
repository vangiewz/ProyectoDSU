from datetime import date, datetime
from decimal import Decimal
from zoneinfo import ZoneInfo

import pytest

from apps.analytics.models import EjecucionETL, HechoResiduo
from apps.analytics.services import etl
from apps.catalogs.models import ParametrosSistema, PeriodoAcademico, UnidadMedida
from apps.operations.models import Jornada, JornadaPunto, RegistroResiduo

LP = ZoneInfo("America/La_Paz")


@pytest.fixture
def datos(usuarios, campus):
    """Una jornada cerrada con registros en kg y en gramos, más un doble envío."""
    p1, p2 = campus["puntos"]
    g = UnidadMedida.objects.create(nombre="Gramo", simbolo="g", magnitud="PESO", factor_conversion=Decimal("0.001"))
    j = Jornada.objects.create(
        fecha=date(2026, 9, 1),
        turno="MANANA",
        sector=campus["sector"],
        planificada_por=usuarios["supervisor"],
        estado="CERRADA",
    )
    JornadaPunto.objects.create(
        jornada=j, punto=p1, orden=1, atendido=True, atendido_en=datetime(2026, 9, 1, 9, tzinfo=LP)
    )
    JornadaPunto.objects.create(jornada=j, punto=p2, orden=2, atendido=False, motivo_omision="Acceso bloqueado")
    op, tipo = usuarios["operario"], campus["tipo"]
    hora = datetime(2026, 9, 1, 9, 0, 10, tzinfo=LP)
    comunes = {"jornada": j, "tipo_residuo": tipo, "registrado_por": op}
    RegistroResiduo.objects.create(punto=p1, unidad=campus["kg"], cantidad=Decimal("40"), fecha_hora=hora, **comunes)
    RegistroResiduo.objects.create(punto=p1, unidad=campus["kg"], cantidad=Decimal("40"), fecha_hora=hora, **comunes)
    RegistroResiduo.objects.create(punto=p2, unidad=g, cantidad=Decimal("2500"), fecha_hora=hora, **comunes)
    PeriodoAcademico.objects.create(nombre="2-2026", fecha_inicio=date(2026, 8, 1), fecha_fin=date(2026, 12, 15))
    return {"jornada": j, "p1": p1, "p2": p2}


def correr_etl():
    return etl.ejecutar(etl.iniciar())


def test_etl_estandariza_deriva_variables_y_excluye_duplicados(datos):
    ej = correr_etl()
    assert ej.estado in (EjecucionETL.Estado.EXITOSA, EjecucionETL.Estado.CON_ALERTA)
    assert (ej.procesados, ej.duplicados, ej.aceptados) == (3, 1, 2)
    gramos = HechoResiduo.objects.get(punto=datos["p2"])
    assert gramos.cantidad_base == Decimal("2.500") and gramos.magnitud == "PESO"
    assert gramos.dia_semana == 1 and gramos.mes == 9 and gramos.periodo.nombre == "2-2026"
    # Incremental: una segunda ejecución no vuelve a cargar lo mismo.
    assert correr_etl().estado == EjecucionETL.Estado.SIN_CAMBIOS
    assert HechoResiduo.objects.count() == 2


def test_etl_no_permite_ejecuciones_simultaneas(datos):
    assert etl.iniciar() is not None
    assert etl.iniciar() is None


def test_etl_detecta_reenvio_en_tanda_posterior(datos):
    correr_etl()
    original = RegistroResiduo.objects.filter(punto=datos["p1"]).first()
    RegistroResiduo.objects.create(
        jornada=original.jornada,
        punto=original.punto,
        tipo_residuo=original.tipo_residuo,
        unidad=original.unidad,
        cantidad=original.cantidad,
        fecha_hora=original.fecha_hora,
        registrado_por=original.registrado_por,
    )
    ejecucion = correr_etl()
    assert ejecucion.duplicados == 1
    assert HechoResiduo.objects.count() == 2


def test_etl_convierte_cantidades_sin_error_binario(datos):
    original = RegistroResiduo.objects.filter(punto=datos["p1"]).first()
    unidad = UnidadMedida.objects.create(
        nombre="Unidad de peso QA", simbolo="qa", magnitud="PESO", factor_conversion=Decimal("0.7")
    )
    nuevo = RegistroResiduo.objects.create(
        jornada=original.jornada,
        punto=original.punto,
        tipo_residuo=original.tipo_residuo,
        unidad=unidad,
        cantidad=Decimal("0.005"),
        fecha_hora=original.fecha_hora,
        registrado_por=original.registrado_por,
    )
    correr_etl()
    assert HechoResiduo.objects.get(registro=nuevo).cantidad_base == Decimal("0.004")


def test_indicadores_exigen_etl_y_calculan_kpis(usuarios, datos, cliente):
    sup = cliente(usuarios["supervisor"])
    q = {"desde": "2026-09-01", "hasta": "2026-09-30"}
    assert sup.get("/api/analitica/indicadores/", q).status_code == 400  # sin ETL todavía
    correr_etl()
    r = sup.get("/api/analitica/indicadores/", q)
    assert r.status_code == 200, r.data
    assert r.data["total_kg"] == Decimal("42.500")
    assert r.data["cobertura_pct"] == 50.0
    assert r.data["recolecciones_realizadas"] == 1
    # 40 kg en 30 días = 1,33 kg/día < umbral por defecto (20 kg/día): sin críticos.
    assert r.data["puntos_criticos"] == []
    # RF17 paso 3: detalle por punto, de mayor a menor.
    assert [p["punto__codigo"] for p in r.data["por_punto"]] == ["P1", "P2"]
    assert sup.get("/api/analitica/indicadores/", {"desde": "2026-09-30", "hasta": "2026-09-01"}).status_code == 400


def test_punto_critico_segun_umbral_configurable(usuarios, datos, cliente):
    correr_etl()
    admin = cliente(usuarios["admin"])
    assert admin.patch("/api/parametros/", {"umbral_critico_kg_dia": "0"}, format="json").status_code == 400
    assert admin.patch("/api/parametros/", {"umbral_critico_kg_dia": "1"}, format="json").status_code == 200
    assert ParametrosSistema.actual().actualizado_por == usuarios["admin"]
    r = admin.get("/api/analitica/mapa/", {"desde": "2026-09-01", "hasta": "2026-09-30"})
    criticos = {p["codigo"] for p in r.data["puntos"] if p["critico"]}
    assert criticos == {"P1"}
    assert cliente(usuarios["supervisor"]).patch("/api/parametros/", {"umbral_critico_kg_dia": "5"}).status_code == 403


def test_comparacion_rechaza_periodos_superpuestos(usuarios, datos, cliente):
    correr_etl()
    sup = cliente(usuarios["supervisor"])
    q = {"base_desde": "2026-08-01", "base_hasta": "2026-09-15", "comp_desde": "2026-09-01", "comp_hasta": "2026-09-30"}
    assert sup.get("/api/analitica/comparacion/", q).status_code == 400
    q.update(base_hasta="2026-08-31")
    r = sup.get("/api/analitica/comparacion/", q)
    assert r.status_code == 200
    assert r.data["sector"][0]["variacion_kg"] == Decimal("42.500") and r.data["sector"][0]["variacion_pct"] is None


@pytest.mark.parametrize("formato,firma", [("xlsx", b"PK"), ("pdf", b"%PDF")])
def test_reportes_exportan_y_quedan_en_bitacora(usuarios, datos, cliente, formato, firma):
    correr_etl()
    directivo = cliente(usuarios["admin"])
    q = {"desde": "2026-09-01", "hasta": "2026-09-30", "formato": formato}
    for tipo in ("generacion-sector", "generacion-tipo", "cumplimiento-jornadas", "incidencias", "indicadores"):
        r = directivo.get(f"/api/reportes/{tipo}/", q)
        assert r.status_code == 200, (tipo, getattr(r, "data", None))
        assert r.content.startswith(firma)
    from apps.audit.models import AuditLog

    assert AuditLog.objects.filter(operacion="EXPORTAR").count() == 5
    assert cliente(usuarios["operario"]).get("/api/reportes/indicadores/", q).status_code == 403


def test_etl_bajo_demanda_requiere_permiso(usuarios, datos, cliente):
    assert cliente(usuarios["supervisor"]).post("/api/etl/ejecutar/").status_code == 403
    etl.iniciar()  # deja una ejecución en curso
    assert cliente(usuarios["admin"]).post("/api/etl/ejecutar/").status_code == 409


def test_enlace_powerbi_solo_de_app_powerbi(usuarios, cliente):
    admin, sup = cliente(usuarios["admin"]), cliente(usuarios["supervisor"])
    ajena = {"url_powerbi": "https://otro.sitio/informe"}
    assert admin.patch("/api/parametros/", ajena, format="json").status_code == 400
    url = "https://app.powerbi.com/reportEmbed?reportId=abc&autoAuth=true"
    assert admin.patch("/api/parametros/", {"url_powerbi": url}, format="json").status_code == 200
    r = sup.get("/api/analitica/powerbi/")
    assert r.data == {"url": url}
    assert "no-store" in r["Cache-Control"]  # el navegador nunca reutiliza respuestas viejas de la API
    assert cliente(usuarios["operario"]).get("/api/analitica/powerbi/").status_code == 403
