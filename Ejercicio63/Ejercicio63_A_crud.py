"""Operaciones de creación, actualización y borrado de cesta y stock."""

import math

from Ejercicio63_A_constantes import CAPACIDAD_BOLSA_KG, PRECIO_BOLSA
from Ejercicio63_A_bdd import guardar_frutas


def crear_fruta_tienda():
    """Comando futuro para crear una fruta desde el menú de tienda."""
    raise NotImplementedError("Crear fruta desde tienda todavía no está implementado.")


def consultar_frutas_tienda():
    """Comando futuro para consultar frutas desde el menú de tienda."""
    raise NotImplementedError("Consultar frutas desde tienda todavía no está implementado.")


def actualizar_fruta_tienda():
    """Comando futuro para actualizar una fruta desde el menú de tienda."""
    raise NotImplementedError("Actualizar fruta desde tienda todavía no está implementado.")


def eliminar_fruta_tienda():
    """Comando futuro para eliminar una fruta desde el menú de tienda."""
    raise NotImplementedError("Eliminar fruta desde tienda todavía no está implementado.")


def buscar_nombre_por_codigo(catalogo, codigo):
    """Devuelve el nombre asociado a un código o ``None`` si no existe."""
    return next(
        (nombre for nombre, datos in catalogo.items() if datos["codigo"] == codigo),
        None,
    )


def crear_fruta(catalogo, nombre, datos):
    """Da de alta una fruta nueva y persiste el catálogo JSON."""
    if nombre in catalogo:
        raise ValueError("Ya existe una fruta con ese nombre.")
    if buscar_nombre_por_codigo(catalogo, datos["codigo"]):
        raise ValueError("Ya existe una fruta con ese código.")
    catalogo[nombre] = datos
    guardar_frutas(catalogo)


def actualizar_fruta(catalogo, nombre, datos):
    """Actualiza los datos de una fruta existente y los guarda."""
    if nombre not in catalogo:
        raise KeyError("La fruta no existe.")
    catalogo[nombre].update(datos)
    guardar_frutas(catalogo)


def eliminar_fruta(catalogo, nombre):
    """Elimina una fruta del catálogo y persiste el cambio."""
    if nombre not in catalogo:
        raise KeyError("La fruta no existe.")
    del catalogo[nombre]
    guardar_frutas(catalogo)


def descontar_stock(catalogo, nombre, producto):
    datos = catalogo[nombre]
    if datos["tipo"] == "peso":
        datos["stock"] -= producto["cantidad"]
    else:
        for peso in producto["pesos"]:
            datos["pesos"].remove(peso)
    guardar_frutas(catalogo)


def devolver_stock(catalogo, nombre, producto):
    datos = catalogo[nombre]
    if datos["tipo"] == "peso":
        datos["stock"] += producto["cantidad"]
    else:
        datos["pesos"].extend(producto["pesos"])
        datos["pesos"].sort()
    guardar_frutas(catalogo)


def restaurar_compra_cancelada(carrito, catalogo):
    """Devuelve al catálogo todos los productos de una compra cancelada."""
    for nombre, producto in list(carrito.items()):
        if nombre != "👜 Bolsa":
            devolver_stock(catalogo, nombre, producto)
    carrito.clear()


def actualizar_bolsas_automaticas(carrito, tipo_compra, tipo_entrega):
    """Sincroniza las bolsas automáticas para un envío a domicilio."""
    if not (tipo_compra == "1" and tipo_entrega == "2"):
        return
    carrito.pop("👜 Bolsa", None)
    peso = sum(datos["peso"] for nombre, datos in carrito.items() if nombre != "👜 Bolsa")
    if peso:
        cantidad = math.ceil(peso / CAPACIDAD_BOLSA_KG)
        carrito["👜 Bolsa"] = {
            "codigo": "B01", "tipo": "bolsa", "cantidad": cantidad,
            "peso": 0, "precio": PRECIO_BOLSA, "unidad": "un.",
            "subtotal": round(cantidad * PRECIO_BOLSA, 2),
        }
