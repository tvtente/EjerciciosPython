"""Persistencia del catálogo de frutas en formato JSON."""

import json
from pathlib import Path

RUTA_BDD = Path(__file__).with_name("Ejercicio63_A_frutas.json")

# Datos de arranque: solo se usan para crear el JSON la primera vez.
FRUTAS_INICIALES = {
    "🍌 Plátano": {"codigo": "01", "tipo": "peso", "precio_kg": 1.35, "stock": 10.0},
    "🍎 Manzana": {"codigo": "02", "tipo": "peso", "precio_kg": 0.80, "stock": 8.0},
    "🍐 Pera": {"codigo": "03", "tipo": "peso", "precio_kg": 0.85, "stock": 6.0},
    "🍊 Naranja": {"codigo": "04", "tipo": "peso", "precio_kg": 0.70, "stock": 12.0},
    "🍓 Fresa": {"codigo": "05", "tipo": "peso", "precio_kg": 1.70, "stock": 5.0},
    "🍒 Cereza": {"codigo": "06", "tipo": "peso", "precio_kg": 2.20, "stock": 5.0},
    "🍑 Durazno": {"codigo": "07", "tipo": "peso", "precio_kg": 1.95, "stock": 8.0},
    "🍈 Melón": {"codigo": "08", "tipo": "unidad", "precio_kg": 2.54, "pesos": [0.850, 1.250]},
    "🍍 Piña": {"codigo": "09", "tipo": "unidad", "precio_kg": 1.54, "pesos": [0.800, 0.750, 1.300]},
    "🍉 Sandía": {"codigo": "10", "tipo": "unidad", "precio_kg": 1.44, "pesos": [1.800, 1.550, 1.400]},
    "🌴 Papaya": {"codigo": "11", "tipo": "unidad", "precio_kg": 1.64, "pesos": [0.800, 0.650, 1.040]},
    "🌰 Durian": {"codigo": "12", "tipo": "unidad", "precio_kg": 5.00, "pesos": [1.800, 2.000, 2.200, 1.950, 2.100]},
    "🍇 Uva": {"codigo": "13", "tipo": "peso", "precio_kg": 1.80, "stock": 2.0},
    "🥝 Kiwi": {"codigo": "14", "tipo": "peso", "precio_kg": 2.20, "stock": 6.0},
    "🥭 Mango": {"codigo": "15", "tipo": "peso", "precio_kg": 2.00, "stock": 7.0},
    "🍋 Limón": {"codigo": "16", "tipo": "peso", "precio_kg": 1.40, "stock": 10.0},
    "🥥 Coco": {"codigo": "17", "tipo": "unidad", "precio_kg": 3.14, "pesos": [0.860, 0.615, 0.704]},
}

CABECERA_INICIAL = {
    "titulo": "Catálogo de frutas",
    "version": 1,
    "descripcion": "Productos disponibles para la frutería.",
}
CABECERA_BDD = CABECERA_INICIAL.copy()


def guardar_frutas(frutas):
    """Guarda el catálogo en un JSON legible, conservando emojis y acentos."""
    documento = {
        "cabecera": CABECERA_BDD,
        "frutas": frutas,
    }
    with RUTA_BDD.open("w", encoding="utf-8") as archivo:
        json.dump(documento, archivo, ensure_ascii=False, indent=4)
        archivo.write("\n")


def cargar_frutas():
    """Carga el catálogo JSON o lo crea a partir de los datos iniciales."""
    global CABECERA_BDD
    if not RUTA_BDD.exists():
        guardar_frutas(FRUTAS_INICIALES)

    with RUTA_BDD.open(encoding="utf-8") as archivo:
        documento = json.load(archivo)

    if "frutas" not in documento:
        if not isinstance(documento, dict):
            raise ValueError("El catálogo JSON debe contener un objeto de frutas.")
        frutas = documento
        guardar_frutas(frutas)
        return frutas

    frutas = documento["frutas"]
    if not isinstance(frutas, dict):
        raise ValueError("La clave 'frutas' del JSON debe contener un objeto.")
    if isinstance(documento.get("cabecera"), dict):
        CABECERA_BDD = documento["cabecera"]
    return frutas


# El catálogo usado por la aplicación siempre procede del archivo JSON.
FRUTAS_DISPONIBLES = cargar_frutas()
