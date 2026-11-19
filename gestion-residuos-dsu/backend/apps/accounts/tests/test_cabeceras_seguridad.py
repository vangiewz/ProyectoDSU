from rest_framework.test import APIClient


def test_respuestas_rechazadas_y_no_encontradas_tienen_cabeceras():
    client = APIClient()
    for path, status in [("/api/auth/me/", 401), ("/ruta-inexistente/", 404)]:
        r = client.get(path)
        assert r.status_code == status
        assert "default-src 'none'" in r["Content-Security-Policy"]
        assert "frame-ancestors 'none'" in r["Content-Security-Policy"]
        assert r["X-Content-Type-Options"] == "nosniff"
        assert r["X-Frame-Options"] == "DENY"
        assert r["Permissions-Policy"] == "geolocation=(), camera=(), microphone=()"
        assert r["Cross-Origin-Resource-Policy"] == "cross-origin"


def test_cors_del_cliente_autorizado_no_se_rompe(settings, usuarios, cliente):
    settings.CORS_ALLOWED_ORIGINS = ["https://dsu-ejemplo.vercel.app"]
    c = cliente(usuarios["supervisor"])
    r = c.get("/api/auth/me/", HTTP_ORIGIN="https://dsu-ejemplo.vercel.app")
    assert r.status_code == 200
    assert r["Access-Control-Allow-Origin"] == "https://dsu-ejemplo.vercel.app"
    r = c.get("/api/auth/me/", HTTP_ORIGIN="https://no-autorizado.example")
    assert "Access-Control-Allow-Origin" not in r
