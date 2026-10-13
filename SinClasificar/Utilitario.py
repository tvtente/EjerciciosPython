import platform
import re
import subprocess


def borro():
    borrardenuevo(platform.system() == "Windows")

def borrardenuevo(shell):
    """Limpia la consola en Windows, Linux y macOS."""
    if platform.system() == "Windows":
        subprocess.run(["cls"], shell=shell)
    else:
        subprocess.run(["clear"])