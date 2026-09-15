import os
import platform
import subprocess


def Borro():
    """Limpia la consola según el sistema operativo."""
    comando = ["cls"] if platform.system() == "Windows" else ["clear"]
    subprocess.run(comando, shell=platform.system() == "Windows")
