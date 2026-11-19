"""Mide los tiempos de respuesta (RTR1–RTR12) y la capacidad (RCM3, RCM5, RCM7) con volumen sintético.

Crea 500 puntos y ~100 000 observaciones dentro de una transacción, mide cada operación por la API (en el
mismo proceso, sin la red entre navegador y servidor) y al final **deshace todo**: la base queda como estaba.
"""

import statistics
import tempfile
import time
from datetime import datetime, timedelta
from decimal import Decimal

import numpy as np
from django.conf import settings
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.test import override_settings
from django.utils import timezone
from rest_framework.test import APIClient

from apps.accounts.models import Rol, User
from apps.analytics.services import etl
from apps.campus.models import PuntoRecoleccion, Sector
from apps.catalogs.models import TipoResiduo, UnidadMedida
from apps.operations.models import Jornada, JornadaPunto, RegistroResiduo
from apps.prediction.services import entrenamiento

CLAVE = "Medicion.Rendimiento.2026"


class Deshacer(Exception):
    """Fuerza el rollback de todo lo creado para la medición."""


class Command(BaseCommand):
    help = "Mide RTR1–RTR12 y RCM3/5/7 con 500 puntos y ~100 000 observaciones sintéticas; deshace todo al final."

    def add_arguments(self, parser):
        parser.add_argument("--puntos", type=int, default=500)
        parser.add_argument("--sectores", type=int, default=10)
        parser.add_argument("--dias", type=int, default=100, help="Días hábiles de historial.")

    def handle(self, *args, puntos, sectores, dias, **opts):
        self.filas = []
        # El cliente de pruebas de DRF se presenta como "testserver".
        hosts = [*settings.ALLOWED_HOSTS, "testserver"]
        with tempfile.TemporaryDirectory() as tmp, override_settings(MODELOS_DIR=tmp, ALLOWED_HOSTS=hosts):
            try:
                with transaction.atomic():
                    self._medir(puntos, sectores, dias)
                    raise Deshacer
            except Deshacer:
                pass
        self.stdout.write("\n| Requisito | Operación | Límite | Medido | Cumple |\n|---|---|---|---|---|")
        for req, nombre, limite, medido, extra in self.filas:
            cumple = "—" if limite is None else ("✅" if medido <= limite else "❌")
            lim = "—" if limite is None else f"≤ {limite:g} s"
            self.stdout.write(f"| {req} | {nombre}{extra} | {lim} | {medido:.2f} s | {cumple} |")
        self.stdout.write("\nTodo lo creado para la medición se deshizo (rollback).")

    def _tiempo(self, req, nombre, limite, fn, veces=3, extra=""):
        tiempos = []
        for _ in range(veces):
            t = time.perf_counter()
            r = fn()
            tiempos.append(time.perf_counter() - t)
            codigo = getattr(r, "status_code", 200)
            if codigo >= 400:
                raise CommandError(f"{nombre}: respuesta {codigo} {getattr(r, 'data', '')}")
        medido = statistics.median(tiempos)
        self.filas.append((req, nombre, limite, medido, extra))
        self.stdout.write(f"  {req} {nombre}: {medido:.2f} s")
        return r

    def _medir(self, n_puntos, n_sectores, n_dias):
        rng = np.random.default_rng(7)
        hoy = timezone.localdate()
        kg = UnidadMedida.objects.filter(simbolo="kg").first()
        tipos = list(TipoResiduo.objects.filter(is_active=True, unidad=kg)[:2])
        if kg is None or len(tipos) < 2:
            raise CommandError("Faltan los catálogos base: ejecute primero `python manage.py seed`.")

        admin = User.objects.create_user("medicion_admin", password=CLAVE, is_superuser=True)
        admin.groups.add(Group.objects.get(name=Rol.ADMINISTRADOR))
        operario = User.objects.create_user("medicion_operario", password=CLAVE)
        operario.groups.add(Group.objects.get(name=Rol.OPERATIVO))

        self.stdout.write(f"Creando {n_puntos} puntos y {n_puntos * len(tipos) * n_dias} vaciados sintéticos…")
        t = time.perf_counter()
        sectores = Sector.objects.bulk_create(
            Sector(codigo=f"MED{i:02d}", nombre=f"Sector de medición {i}", supervisor=admin) for i in range(n_sectores)
        )
        por_sector = n_puntos // n_sectores
        puntos = PuntoRecoleccion.objects.bulk_create(
            PuntoRecoleccion(
                sector=s,
                codigo=f"MED-P{i * por_sector + j:04d}",
                nombre=f"Punto de medición {i * por_sector + j}",
                latitud=Decimal(str(round(-17.7790 + 0.006 * rng.random(), 6))),
                longitud=Decimal(str(round(-63.1980 + 0.006 * rng.random(), 6))),
                capacidad_kg=Decimal("150"),
            )
            for i, s in enumerate(sectores)
            for j in range(por_sector)
        )
        base = {p.pk: rng.uniform(5, 40) for p in puntos}
        fechas = []
        f = hoy - timedelta(days=1)
        while len(fechas) < n_dias:
            if f.weekday() < 5:
                fechas.append(f)
            f -= timedelta(days=1)
        jornadas = Jornada.objects.bulk_create(
            (
                Jornada(
                    fecha=fecha,
                    turno=Jornada.Turno.MANANA,
                    sector=s,
                    estado=Jornada.Estado.CERRADA,
                    planificada_por=admin,
                    responsable=operario,
                )
                for fecha in fechas
                for s in sectores
            ),
            batch_size=1000,
        )
        rutas, registros = [], []
        puntos_de = {s.pk: [p for p in puntos if p.sector_id == s.pk] for s in sectores}
        for j in jornadas:
            hora = timezone.make_aware(datetime.combine(j.fecha, datetime.min.time().replace(hour=9)))
            factor = 1.25 if j.fecha.weekday() == 0 else 1.0
            for orden, p in enumerate(puntos_de[j.sector_id], start=1):
                rutas.append(JornadaPunto(jornada=j, punto=p, orden=orden, atendido=True, atendido_en=hora))
                for k, tipo in enumerate(tipos):
                    cantidad = base[p.pk] * factor * (0.6 if k else 1) * rng.lognormal(0, 0.15)
                    registros.append(
                        RegistroResiduo(
                            jornada=j,
                            punto=p,
                            tipo_residuo=tipo,
                            unidad=kg,
                            cantidad=Decimal(f"{cantidad:.3f}"),
                            registrado_por=operario,
                            fecha_hora=hora,
                        )
                    )
        JornadaPunto.objects.bulk_create(rutas, batch_size=5000)
        RegistroResiduo.objects.bulk_create(registros, batch_size=5000)
        self.stdout.write(f"  datos creados en {time.perf_counter() - t:.0f} s")

        # Jornada de hoy en ejecución, para medir la captura en campo.
        hoy_j = Jornada.objects.create(
            fecha=hoy,
            turno=Jornada.Turno.TARDE,
            sector=sectores[0],
            estado=Jornada.Estado.EN_EJECUCION,
            planificada_por=admin,
            responsable=operario,
        )
        hoy_j.personal.add(operario)
        JornadaPunto.objects.bulk_create(
            JornadaPunto(jornada=hoy_j, punto=p, orden=i) for i, p in enumerate(puntos_de[sectores[0].pk], start=1)
        )

        api, campo = APIClient(), APIClient()
        api.force_authenticate(admin)
        campo.force_authenticate(operario)
        desde_anio = (hoy - timedelta(days=364)).isoformat()
        mes = {"desde": (hoy - timedelta(days=29)).isoformat(), "hasta": hoy.isoformat()}
        anio = {"desde": desde_anio, "hasta": hoy.isoformat()}

        self.stdout.write("Midiendo…")
        # RCM5: el ETL procesa el histórico acumulado.
        t = time.perf_counter()
        ejecucion = etl.ejecutar(etl.iniciar(admin))
        self.filas.append(
            (
                "RCM5",
                "ETL sobre el histórico nuevo",
                None,
                time.perf_counter() - t,
                f" ({ejecucion.procesados} registros)",
            )
        )
        self.stdout.write(f"  ETL: {ejecucion.get_estado_display()}, {ejecucion.procesados} registros")

        self._tiempo(
            "RTR1",
            "Autenticación",
            2,
            lambda: APIClient().post(
                "/api/auth/login/", {"username": "medicion_admin", "password": CLAVE}, format="json"
            ),
        )
        self._tiempo(
            "RTR2",
            "Datos de la interfaz principal (sesión + jornadas)",
            3,
            lambda: (api.get("/api/auth/me/"), api.get("/api/jornadas/"))[1],
        )
        self._tiempo("RTR3", "Búsqueda de un punto", 2, lambda: api.get("/api/puntos/", {"search": "MED-P0420"}))
        self._tiempo("RTR3", "Búsqueda de un sector", 2, lambda: api.get("/api/sectores/", {"search": "MED05"}))
        paradas = iter(puntos_de[sectores[0].pk])
        self._tiempo(
            "RTR4",
            "Registro de un vaciado",
            3,
            lambda: campo.post(
                f"/api/jornadas/{hoy_j.pk}/visitas/",
                {"punto": next(paradas).pk, "detalles": [{"tipo_residuo": tipos[0].pk, "cantidad": "12.5"}]},
                format="json",
            ),
        )
        self._tiempo(
            "RTR5",
            "Registro de una incidencia",
            3,
            lambda: campo.post(
                "/api/incidencias/",
                {
                    "jornada": hoy_j.pk,
                    "punto": puntos_de[sectores[0].pk][0].pk,
                    "tipo": "DESBORDE",
                    "gravedad": "MEDIA",
                    "descripcion": "Medición de rendimiento",
                },
                format="json",
            ),
        )
        self._tiempo(
            "RTR6",
            "Histórico con filtros (12 meses, un sector)",
            4,
            lambda: api.get("/api/registros/", {**anio, "sector": sectores[3].pk}),
        )
        self._tiempo(
            "RTR7",
            f"Mapa con los {len(puntos)}+ puntos activos (30 días)",
            4,
            lambda: api.get("/api/analitica/mapa/", mes),
        )
        self._tiempo("RTR8", "Capa de calor de 12 meses", 6, lambda: api.get("/api/analitica/mapa/", anio))
        self._tiempo(
            "RTR9", "Indicadores del periodo (30 días)", 5, lambda: api.get("/api/analitica/indicadores/", mes)
        )
        self._tiempo(
            "RTR9", "Indicadores del periodo (12 meses)", 5, lambda: api.get("/api/analitica/indicadores/", anio)
        )
        self._tiempo(
            "RTR10",
            "Reporte exportable PDF (12 meses)",
            8,
            lambda: api.get("/api/reportes/generacion-sector/", {**anio, "formato": "pdf"}),
        )
        self._tiempo(
            "RTR10",
            "Reporte exportable Excel (12 meses)",
            8,
            lambda: api.get("/api/reportes/cumplimiento-jornadas/", {**anio, "formato": "xlsx"}),
        )

        # RCM7 / RTR12: entrenamiento completo sobre el histórico ampliado.
        t = time.perf_counter()
        modelo = entrenamiento.entrenar(entrenamiento.iniciar(admin, dict(entrenamiento.PROPUESTOS)))
        obs = modelo.observaciones_entrenamiento + modelo.observaciones_prueba
        self.filas.append(
            (
                "RTR12 / RCM7",
                "Entrenamiento completo",
                600,
                time.perf_counter() - t,
                f" ({obs} observaciones, R² {modelo.r2:.3f}, {modelo.get_estado_display().lower()})"
                if modelo.r2 is not None
                else f" ({modelo.mensaje})",
            )
        )
        self.stdout.write(f"  entrenamiento: {modelo.mensaje}")
        r = self._tiempo(
            "RTR11 / RCM8",
            "Predicción a 30 días de todos los puntos",
            15,
            lambda: api.post("/api/predicciones/", {"horizonte": 30}, format="json"),
            veces=1,
        )
        self.filas[-1] = (*self.filas[-1][:4], f" ({len(r.data['por_punto'])} puntos)")
        activos = PuntoRecoleccion.objects.filter(is_active=True).count()
        self.stdout.write(f"RCM3: {activos} puntos activos durante la medición.")
