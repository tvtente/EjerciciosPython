"""Ejecuta el ejercicio completo de la cuenta bancaria."""

from pathlib import Path
import runpy


archivo_principal = Path(__file__).with_name("cuentabancaria 1.py")
runpy.run_path(archivo_principal, run_name="__main__")
