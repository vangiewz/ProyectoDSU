"""Acceso al modelo financiero canónico incluido en la entrega."""
from pathlib import Path
import runpy
if __name__ == '__main__':
    runpy.run_path(str(Path(__file__).resolve().parents[1]/'finanzas/finanzas.py'),run_name='__main__')
