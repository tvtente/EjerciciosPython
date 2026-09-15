"""Consultas puras sobre el catálogo de frutas."""

from unicodedata import combining, normalize

from ..Ejercicio63RaimonConstantes import FRUTAS


def normalizar_texto(texto):
    """Normaliza texto para búsquedas sin acentos y sin distinguir mayúsculas."""
    texto_normalizado = normalize("NFKD", texto.lower())
    return "".join(
        caracter
        for caracter in texto_normalizado
        if not combining(caracter)
    )


def buscar_fruta(fruta):
    """Devuelve las claves del catálogo que empiezan por la búsqueda."""
    clave_entrada = normalizar_texto(fruta)
    if not clave_entrada:
        return []
    return [
        clave
        for clave in FRUTAS
        if clave.startswith(clave_entrada)
    ]
