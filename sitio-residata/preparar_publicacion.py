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
