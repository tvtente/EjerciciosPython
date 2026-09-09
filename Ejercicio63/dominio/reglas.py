"""Reglas comerciales sin dependencias de la interfaz."""

import math

from Ejercicio63_A_constantes import (
    CAPACIDAD_BOLSA_KG,
    COSTE_ENVIO_DOMICILIO,
    PRECIO_BOLSA,
)
from .carrito import BOLSA, peso_total, subtotal


def calcular_envio(tipo_compra, tipo_entrega):
    """Calcula el coste de envío según la modalidad seleccionada."""
    if tipo_compra == "1" and tipo_entrega == "2":
        return COSTE_ENVIO_DOMICILIO
    return 0.0


def calcular_bolsas(peso):
    """Calcula cuántas bolsas automáticas necesita un pedido."""
    if peso <= 0:
        return 0
    return math.ceil(peso / CAPACIDAD_BOLSA_KG)


def calcular_total_final(carrito, tipo_compra, tipo_entrega):
    """Calcula subtotal más envío, sin mutar el carrito."""
    return round(
        subtotal(carrito) + calcular_envio(tipo_compra, tipo_entrega),
        2,
    )


def supera_presupuesto(
    carrito,
    presupuesto,
    tipo_compra,
    tipo_entrega,
    nombre,
    nuevo_producto,
    reemplazar=False,
):
    """Indica si añadir o sustituir un producto supera el presupuesto."""
    if presupuesto is None:
        return False

    total = 0.0
    peso = 0.0
    for producto, datos in carrito.items():
        if producto == BOLSA or (reemplazar and producto == nombre):
            continue
        total += datos["subtotal"]
        peso += datos["peso"]

    total += nuevo_producto["subtotal"]
    peso += nuevo_producto["peso"]

    if tipo_compra == "1" and tipo_entrega == "2":
        total += calcular_bolsas(peso) * PRECIO_BOLSA
        total += COSTE_ENVIO_DOMICILIO

    return round(total, 2) > presupuesto
