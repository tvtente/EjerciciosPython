"""Reglas de negocio reutilizables del TPV."""

import math

from Ejercicio63_A_constantes import CAPACIDAD_BOLSA_KG, COSTE_ENVIO_DOMICILIO, PRECIO_BOLSA


def calcular_total_final(carrito, tipo_compra, tipo_entrega):
    """Calcula el total, aplicando el envío cuando procede."""
    subtotal = sum(datos["subtotal"] for datos in carrito.values())
    envio = COSTE_ENVIO_DOMICILIO if tipo_compra == "1" and tipo_entrega == "2" else 0.0
    return round(subtotal + envio, 2)


def supera_presupuesto(carrito, presupuesto, tipo_compra, tipo_entrega, nombre, nuevo_producto, reemplazar=False):
    """Indica si la operación propuesta excede el presupuesto."""
    if presupuesto is None:
        return False
    total = peso = 0
    for producto, datos in carrito.items():
        if producto == "👜 Bolsa" or (reemplazar and producto == nombre):
            continue
        total += datos["subtotal"]
        peso += datos["peso"]
    total += nuevo_producto["subtotal"]
    peso += nuevo_producto["peso"]
    if tipo_compra == "1" and tipo_entrega == "2":
        total += math.ceil(peso / CAPACIDAD_BOLSA_KG) * PRECIO_BOLSA + COSTE_ENVIO_DOMICILIO
    return round(total, 2) > presupuesto
