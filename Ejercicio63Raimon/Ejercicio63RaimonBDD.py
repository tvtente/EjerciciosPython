"""Catálogo de frutas almacenado en un archivo JSON."""

import json
from pathlib import Path


RUTA_FRUTAS = Path(__file__).with_name("Ejercicio63RaimonBDD.json")


_FRUTAS_QUEMADAS = {
    "cereza": ("🍒", "Cereza", 4.50),
    "datil": ("🌴", "Dátil", 6.20),
    "fresa": ("🍓", "Fresa", 3.80),
    "kiwi": ("🥝", "Kiwi", 3.20),
    "limon": ("🍋", "Limón", 1.60),
    "mango": ("🥭", "Mango", 3.50),
    "manzana": ("🍎", "Manzana", 1.95),
    "melocoton": ("🍑", "Melocotón", 2.40),
    "melon": ("🍈", "Melón", 1.20),
    "naranja": ("🍊", "Naranja", 1.50),
    "pera": ("🍐", "Pera", 2.15),
    "pina": ("🍍", "Piña", 1.80),
    "platano": ("🍌", "Plátano", 2.10),
    "sandia": ("🍉", "Sandía", 0.95),
    "uva": ("🍇", "Uva", 2.90),
}


def cargar_frutas():
    if RUTA_FRUTAS.exists():
        with RUTA_FRUTAS.open("r", encoding="utf-8") as archivo:
            frutas = json.load(archivo)
    else:
        frutas = _FRUTAS_QUEMADAS
        with RUTA_FRUTAS.open("w", encoding="utf-8") as archivo:
            json.dump(frutas, archivo, ensure_ascii=False, indent=4)
            archivo.write("\n")

    return {
        clave: tuple(datos)
        for clave, datos in frutas.items()
    }


FRUTAS = cargar_frutas()