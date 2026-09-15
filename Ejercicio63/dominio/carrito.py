"""Operaciones de negocio sobre el carrito."""

from copy import deepcopy


BOLSA = "👜 Bolsa"


def subtotal(carrito):
    """Devuelve el subtotal de los productos del carrito."""
    return round(
        sum(datos["subtotal"] for datos in carrito.values()),
        2,
    )


def peso_total(carrito):
    """Devuelve el peso total de los productos del carrito."""
    return round(
        sum(datos["peso"] for datos in carrito.values()),
        3,
    )


def agregar(carrito, nombre, producto):
    """Añade un producto o acumula otro del mismo nombre."""
    if nombre not in carrito:
        carrito[nombre] = deepcopy(producto)
        return

    actual = carrito[nombre]
    actual["cantidad"] += producto["cantidad"]
    actual["peso"] = round(actual["peso"] + producto["peso"], 3)
    actual["subtotal"] = round(actual["subtotal"] + producto["subtotal"], 2)

    if actual["tipo"] == "unidad":
        actual["pesos"].extend(producto["pesos"])


def eliminar(carrito, nombre):
    """Elimina un producto y devuelve una copia del producto eliminado."""
    return carrito.pop(nombre, None)


def reemplazar(carrito, nombre, producto):
    """Sustituye completamente un producto del carrito."""
    if nombre not in carrito:
        raise KeyError(f"El producto no está en el carrito: {nombre}")
    carrito[nombre] = deepcopy(producto)
