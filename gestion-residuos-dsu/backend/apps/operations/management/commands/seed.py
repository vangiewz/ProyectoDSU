from datetime import date, datetime, time, timedelta
from decimal import Decimal

import numpy as np
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from apps.accounts.models import Rol, User
from apps.campus.models import Contenedor, PuntoRecoleccion, Sector
from apps.catalogs.models import PeriodoAcademico, TipoResiduo, UnidadMedida
from apps.operations.models import Jornada, JornadaPunto, RegistroResiduo, Vehiculo

UNIDADES = [
    ("Kilogramo", "kg", "PESO", "1"),
    ("Gramo", "g", "PESO", "0.001"),
    ("Litro", "L", "VOLUMEN", "1"),
    ("Metro cúbico", "m3", "VOLUMEN", "1000"),
]
TIPOS = [
    ("Orgánico", "ORGANICO", True, "kg"),
    ("Papel y cartón", "RECICLABLE", True, "kg"),
    ("Plástico PET", "RECICLABLE", True, "kg"),
    ("Vidrio", "RECICLABLE", True, "kg"),
    ("Residuo común", "NO_APROVECHABLE", False, "kg"),
    ("Residuo peligroso", "PELIGROSO", False, "kg"),
]

# Datos de demostración: coordenadas aproximadas de la Ciudad Universitaria UAGRM (no oficiales).
SECTORES_DEMO = [
    ("FICCT", "Facultad de Ciencias de la Computación y Telecomunicaciones", "FACULTAD", -17.77570, -63.19560),
    ("FCET", "Facultad de Ciencias Exactas y Tecnología", "FACULTAD", -17.77440, -63.19390),
    ("FCEE", "Facultad de Ciencias Económicas y Empresariales", "FACULTAD", -17.77720, -63.19720),
    ("BIBLIO", "Biblioteca central y áreas comunes", "AREA_COMUN", -17.77610, -63.19280),
]
USUARIOS_DEMO = [
    ("supervisor", "Sara", "Supervisora", Rol.SUPERVISOR),
    ("operario1", "Óscar", "Operario", Rol.OPERATIVO),
    ("operario2", "Olga", "Operaria", Rol.OPERATIVO),
    ("directivo", "Diego", "Director", Rol.DIRECTIVO),
]

# Histórico sintético para entrenar el modelo en demostración (no son datos reales de la DSU).
DIAS_HISTORICO = 365
PERIODOS_DEMO = [
    ("2-2025", date(2025, 8, 4), date(2025, 12, 13)),
    ("1-2026", date(2026, 3, 2), date(2026, 7, 11)),
    ("2-2026", date(2026, 8, 3), date(2026, 12, 12)),
]
MEZCLA = {  # proporción de cada tipo en lo que genera un punto
    "Orgánico": 0.38,
    "Papel y cartón": 0.20,
    "Plástico PET": 0.16,
    "Vidrio": 0.05,
    "Residuo común": 0.19,
    "Residuo peligroso": 0.02,
}
FACTOR_DIA = [1.25, 1.0, 1.0, 0.95, 0.85]  # el lunes recoge lo acumulado el fin de semana
FACTOR_VACACIONES = 0.4


class Command(BaseCommand):
    help = "Carga catálogos base (unidades y tipos de residuo) y, con --demo, usuarios y campus de ejemplo."

    def add_arguments(self, parser):
        parser.add_argument("--admin-password", help="Crea o actualiza el usuario 'admin' con esta contraseña.")
        parser.add_argument("--demo", action="store_true", help="Agrega usuarios, sectores y puntos de ejemplo.")
        parser.add_argument("--demo-password", default="Residuos.2026", help="Contraseña de los usuarios demo.")
        parser.add_argument(
            "--historico", action="store_true", help="Agrega un año de jornadas y vaciados sintéticos (demo)."
        )

    @transaction.atomic
    def handle(self, *args, **opts):
        for nombre, simbolo, magnitud, factor in UNIDADES:
            UnidadMedida.objects.get_or_create(
                simbolo=simbolo, defaults={"nombre": nombre, "magnitud": magnitud, "factor_conversion": Decimal(factor)}
            )
        for nombre, clasif, aprovechable, simbolo in TIPOS:
            TipoResiduo.objects.get_or_create(
                nombre=nombre,
                defaults={
                    "clasificacion": clasif,
                    "aprovechable": aprovechable,
                    "unidad": UnidadMedida.objects.get(simbolo=simbolo),
                },
            )
        self.stdout.write("Catálogos base listos.")

        if opts["admin_password"]:
            admin = self._usuario("admin", "Administrador", "del Sistema", Rol.ADMINISTRADOR, opts["admin_password"])
            admin.is_superuser = True
            admin.save()
            self.stdout.write("Usuario 'admin' listo.")

        if opts["demo"]:
            self._demo(opts["demo_password"])

        if opts["historico"]:
            self._historico()

    def _usuario(self, username, nombre, apellido, rol, password):
        user, _ = User.objects.get_or_create(username=username, defaults={"first_name": nombre, "last_name": apellido})
        user.set_password(password)
        user.save()
        user.groups.set([Group.objects.get(name=rol)])
        return user

    def _demo(self, password):
        usuarios = {u: self._usuario(u, n, a, r, password) for u, n, a, r in USUARIOS_DEMO}
        for codigo, nombre, tipo, lat, lon in SECTORES_DEMO:
            sector, _ = Sector.objects.get_or_create(
                codigo=codigo, defaults={"nombre": nombre, "tipo": tipo, "supervisor": usuarios["supervisor"]}
            )
            for j in range(3):
                punto, _ = PuntoRecoleccion.objects.get_or_create(
                    codigo=f"{codigo}-P{j + 1}",
                    defaults={
                        "sector": sector,
                        "nombre": f"Punto {j + 1} {codigo}",
                        "latitud": Decimal(str(round(lat + 0.00025 * j, 6))),
                        "longitud": Decimal(str(round(lon - 0.0002 * j, 6))),
                        "capacidad_kg": Decimal("120"),
                    },
                )
                Contenedor.objects.get_or_create(
                    codigo=f"{punto.codigo}-C1",
                    defaults={
                        "punto": punto,
                        "tipo": "Turril plástico",
                        "capacidad_litros": Decimal("200"),
                        "fecha_instalacion": "2026-03-01",
                    },
                )
        Vehiculo.objects.get_or_create(placa="DSU-001", defaults={"descripcion": "Camioneta de recolección"})
        Vehiculo.objects.get_or_create(placa="DSU-002", defaults={"descripcion": "Carrito eléctrico"})
        self.stdout.write(f"Datos demo listos. Usuarios: {', '.join(usuarios)} (contraseña: {password}).")

    def _historico(self):
        """Un año de jornadas cerradas con vaciados por tipo: patrón semanal, vacaciones, crecimiento y ruido."""
        puntos = list(
            PuntoRecoleccion.objects.filter(sector__codigo__in=[s[0] for s in SECTORES_DEMO], is_active=True)
            .select_related("sector")
            .order_by("codigo")
        )
        if not puntos:
            raise CommandError("Primero cargue el campus de demostración con --demo.")
        for nombre, inicio, fin in PERIODOS_DEMO:
            PeriodoAcademico.objects.get_or_create(nombre=nombre, defaults={"fecha_inicio": inicio, "fecha_fin": fin})
        periodos = list(PeriodoAcademico.objects.values_list("fecha_inicio", "fecha_fin"))
        supervisor = User.objects.get(username="supervisor")
        operarios = list(User.objects.filter(username__in=["operario1", "operario2"]))
        tipos = {t.nombre: t for t in TipoResiduo.objects.filter(nombre__in=MEZCLA)}
        kg = UnidadMedida.objects.get(simbolo="kg")
        rng = np.random.default_rng(2026)
        # Generación base (kg por día hábil) y crecimiento mensual de cada punto. FCEE-P1 (comedor)
        # crece rápido y se acerca a su capacidad: debe disparar alertas en la demostración.
        perfil = {p.pk: (rng.uniform(25, 55), rng.uniform(0, 0.01)) for p in puntos}
        perfil.update({p.pk: (75.0, 0.035) for p in puntos if p.codigo == "FCEE-P1"})
        por_sector: dict[Sector, list[PuntoRecoleccion]] = {}
        for p in puntos:
            por_sector.setdefault(p.sector, []).append(p)

        def hora(f, h, m=0):
            return timezone.make_aware(datetime.combine(f, time(h, m)))

        hoy = timezone.localdate()
        ocupadas = set(Jornada.objects.filter(turno=Jornada.Turno.MANANA).values_list("fecha", "sector_id"))
        plan = []
        for dias in range(DIAS_HISTORICO, 0, -1):
            f = hoy - timedelta(days=dias)
            if f.weekday() > 4:
                continue
            for sector in por_sector:
                if (f, sector.pk) in ocupadas:
                    continue
                op = operarios[int(rng.integers(len(operarios)))]
                jornada = Jornada(
                    fecha=f,
                    turno=Jornada.Turno.MANANA,
                    sector=sector,
                    estado=Jornada.Estado.CERRADA,
                    descripcion="Histórico de demostración",
                    planificada_por=supervisor,
                    responsable=op,
                    hora_inicio=hora(f, 8),
                    hora_fin=hora(f, 14),
                )
                plan.append((jornada, op))
        Jornada.objects.bulk_create([j for j, _ in plan], batch_size=500)
        Jornada.personal.through.objects.bulk_create(
            [Jornada.personal.through(jornada_id=j.pk, user_id=op.pk) for j, op in plan], batch_size=1000
        )

        rutas, registros = [], []
        for jornada, op in plan:
            f = jornada.fecha
            clases = any(a <= f <= b for a, b in periodos)
            meses = (DIAS_HISTORICO - (hoy - f).days) / 30
            for orden, p in enumerate(por_sector[jornada.sector], start=1):
                if rng.random() < 0.03:
                    rutas.append(
                        JornadaPunto(
                            jornada=jornada, punto=p, orden=orden, atendido=False, motivo_omision="Acceso bloqueado"
                        )
                    )
                    continue
                atendido = hora(f, 8, 30) + timedelta(minutes=25 * orden)
                rutas.append(JornadaPunto(jornada=jornada, punto=p, orden=orden, atendido=True, atendido_en=atendido))
                base, crecimiento = perfil[p.pk]
                total = (
                    base
                    * FACTOR_DIA[f.weekday()]
                    * (1 if clases else FACTOR_VACACIONES)
                    * (1 + crecimiento) ** meses
                    * rng.lognormal(0, 0.12)
                )
                for nombre, parte in MEZCLA.items():
                    if nombre == "Residuo peligroso" and rng.random() > 0.1:
                        continue
                    cantidad = total * parte * rng.lognormal(0, 0.2)
                    if cantidad >= 0.2:
                        registros.append(
                            RegistroResiduo(
                                jornada=jornada,
                                punto=p,
                                tipo_residuo=tipos[nombre],
                                unidad=kg,
                                cantidad=Decimal(f"{cantidad:.3f}"),
                                registrado_por=op,
                                fecha_hora=atendido,
                            )
                        )
        JornadaPunto.objects.bulk_create(rutas, batch_size=1000)
        RegistroResiduo.objects.bulk_create(registros, batch_size=1000)

        # Próxima jornada planificada por sector: destino de las recomendaciones aceptadas (RF24 paso 4.3).
        proxima = hoy + timedelta(days=1)
        while proxima.weekday() > 4:
            proxima += timedelta(days=1)
        for sector, pts in por_sector.items():
            if (proxima, sector.pk) in ocupadas:
                continue
            jornada = Jornada.objects.create(
                fecha=proxima,
                turno=Jornada.Turno.MANANA,
                sector=sector,
                descripcion="Planificada (demostración)",
                planificada_por=supervisor,
            )
            JornadaPunto.objects.bulk_create(
                JornadaPunto(jornada=jornada, punto=p, orden=i) for i, p in enumerate(pts, start=1)
            )
        self.stdout.write(
            f"Histórico listo: {len(plan)} jornadas y {len(registros)} vaciados sintéticos. "
            "Siga con `python manage.py etl` y `python manage.py entrenar`."
        )
