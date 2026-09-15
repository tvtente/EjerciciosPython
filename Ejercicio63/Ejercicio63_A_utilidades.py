"""Utilidades independientes de la lógica de compra."""

import platform
import subprocess
import unicodedata


def limpiar_pantalla():
    """Limpia la consola según el sistema operativo."""
    comando = ["cls"] if platform.system() == "Windows" else ["clear"]
    subprocess.run(comando, shell=platform.system() == "Windows")


def calcular_ancho_visual(texto):
    """Calcula el ancho visible de un texto, incluidos los emojis."""
    return sum(
        2 if unicodedata.east_asian_width(caracter) in ("F", "W") or ord(caracter) > 0x1F600 else 1
        for caracter in texto
    )


def formatear_linea(texto, ancho, alineacion="<"):
    """Alinea texto considerando su ancho visual."""
    espacios = max(0, ancho - calcular_ancho_visual(texto))
    if alineacion == "^":
        izquierda = espacios // 2
        return " " * izquierda + texto + " " * (espacios - izquierda)
    if alineacion == ">":
        return " " * espacios + texto
    return texto + " " * espacios
