"""Arma dist/ con recursos públicos, sin fuentes internas ni credenciales de herramientas."""
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
subprocess.run([sys.executable, str(ROOT / "construir.py")], check=True)
out = ROOT / "dist"
out.mkdir(exist_ok=True)
for filename in [*ROOT.glob("*.html"), ROOT / "feed.xml", ROOT / "vercel.json"]:
    shutil.copy2(filename, out / filename.name)
for dirname in ["css", "fonts", "img", "js", "marketing", "pitch"]:
    shutil.copytree(ROOT / dirname, out / dirname, dirs_exist_ok=True)
print("Publicación preparada en", out)
if "--solo-publico" in sys.argv:
    sys.exit(0)

# El proyecto Vercel existente tiene Root Directory = sitio-residata.
# La raíz del envío debe conservar esa estructura, aun al publicar solo recursos públicos.
project = out / "proyecto"
public = project / "sitio-residata"
public.mkdir(parents=True, exist_ok=True)
for filename in [*ROOT.glob("*.html"), ROOT / "feed.xml", ROOT / "vercel.json"]:
    shutil.copy2(filename, public / filename.name)
for dirname in ["css", "fonts", "img", "js", "marketing", "pitch"]:
    shutil.copytree(ROOT / dirname, public / dirname, dirs_exist_ok=True)
link = ROOT / ".vercel" / "project.json"
if link.exists():
    import json
    config = json.loads(link.read_text(encoding="utf-8"))
    if config.get("projectName") != "residata":
        raise ValueError("El vínculo local debe apuntar al proyecto existente residata")
    (project / ".vercel").mkdir(exist_ok=True)
    shutil.copy2(link, project / ".vercel" / "project.json")
print("Raíz para Vercel (conserva Root Directory):", project)
