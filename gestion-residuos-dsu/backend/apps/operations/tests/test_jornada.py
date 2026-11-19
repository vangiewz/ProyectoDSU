from apps.operations.models import Jornada, RegistroResiduo


def test_flujo_completo_de_jornada(usuarios, campus, hoy, cliente):
    sup, op = cliente(usuarios["supervisor"]), cliente(usuarios["operario"])
    p1, p2 = campus["puntos"]

    # RF11: planificar
    r = sup.post(
        "/api/jornadas/",
        {"fecha": hoy, "turno": "MANANA", "sector": campus["sector"].id, "puntos": [p1.id, p2.id]},
        format="json",
    )
    assert r.status_code == 201, r.data
    jid = r.data["id"]
    assert [p["codigo"] for p in r.data["ruta"]] == ["P1", "P2"]

    # RF11 exc. 1: misma fecha, turno y sector
    r = sup.post(
        "/api/jornadas/",
        {"fecha": hoy, "turno": "MANANA", "sector": campus["sector"].id, "puntos": [p1.id]},
        format="json",
    )
    assert r.status_code == 400

    # RF13 exc. 2: sin responsable no se asigna; luego asignación válida
    oper = usuarios["operario"].id
    r = sup.post(f"/api/jornadas/{jid}/asignar/", {"personal": [oper], "responsable": None}, format="json")
    assert r.status_code == 400
    r = sup.post(f"/api/jornadas/{jid}/asignar/", {"personal": [oper], "responsable": oper}, format="json")
    assert r.status_code == 200, r.data

    assert sup.post(f"/api/jornadas/{jid}/confirmar/").status_code == 200
    assert op.post(f"/api/jornadas/{jid}/abrir/").status_code == 200

    # RF8: cantidad inválida y exceso manifiesto de capacidad (100 kg * 1.5)
    visita = {"punto": p1.id, "detalles": [{"tipo_residuo": campus["tipo"].id, "cantidad": "0"}]}
    assert op.post(f"/api/jornadas/{jid}/visitas/", visita, format="json").status_code == 400
    visita["detalles"][0]["cantidad"] = "151"
    assert op.post(f"/api/jornadas/{jid}/visitas/", visita, format="json").status_code == 400

    visita["detalles"][0]["cantidad"] = "35.5"
    r = op.post(f"/api/jornadas/{jid}/visitas/", visita, format="json")
    assert r.status_code == 201, r.data
    reg = RegistroResiduo.objects.get()
    assert reg.registrado_por == usuarios["operario"] and reg.unidad == campus["kg"]

    # RF12 exc. 2: no cierra con puntos pendientes
    assert sup.post(f"/api/jornadas/{jid}/cerrar/").status_code == 400
    r = op.post(f"/api/jornadas/{jid}/omitir/", {"punto": p2.id, "motivo": "Acceso bloqueado"}, format="json")
    assert r.status_code == 200

    r = sup.get(f"/api/jornadas/{jid}/resumen/")
    assert r.data["cobertura"] == 50.0 and r.data["omitidos"][0]["punto__codigo"] == "P2"

    assert sup.post(f"/api/jornadas/{jid}/cerrar/", {"observaciones": "OK"}).status_code == 200
    assert Jornada.objects.get(pk=jid).estado == Jornada.Estado.CERRADA

    # Jornada cerrada: inmutable
    assert op.post(f"/api/jornadas/{jid}/visitas/", visita, format="json").status_code == 400
    assert sup.patch(f"/api/jornadas/{jid}/", {"descripcion": "x"}, format="json").status_code == 400


def test_supervisor_no_opera_sectores_ajenos(usuarios, campus, hoy, cliente):
    otro = cliente(usuarios["otro_supervisor"])
    r = otro.post(
        "/api/jornadas/",
        {"fecha": hoy, "turno": "TARDE", "sector": campus["sector"].id, "puntos": [campus["puntos"][0].id]},
        format="json",
    )
    assert r.status_code == 403
    assert otro.get("/api/puntos/").data["count"] == 0


def test_operario_solo_ve_jornadas_asignadas(usuarios, campus, hoy, cliente):
    sup = cliente(usuarios["supervisor"])
    sup.post(
        "/api/jornadas/",
        {"fecha": hoy, "turno": "NOCHE", "sector": campus["sector"].id, "puntos": [campus["puntos"][0].id]},
        format="json",
    )
    assert cliente(usuarios["operario"]).get("/api/jornadas/").data["count"] == 0


def test_administrador_no_opera_en_campo(usuarios):
    admin = usuarios["admin"]
    assert admin.has_perm("operations.add_jornada")
    for p in ("add_registroresiduo", "ejecutar_jornada", "cerrar_jornada", "add_incidencia", "atender_incidencia"):
        assert not admin.has_perm(f"operations.{p}")
