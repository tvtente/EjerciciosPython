import sys
import time
from datetime import datetime
from reportlab.pdfgen import canvas
from . import Ejercicio63RaimonConstantes as const
from . import Ejercicio63RaimonUtilidades as util
from . import Ejercicio63RaimonFuncionalidades as func
from .domain.catalogo import buscar_fruta
from .domain.carrito import actualizar_cesta as actualizar_cesta_dominio
# Compatibilidad de 'select' según el sistema operativo (Windows vs. Linux/Mac)
try:
    import select
except ImportError:
    select = None


# =================================================================--
# MÓDULO DE GESTIÓN DE CESTA (CAPTURA, ACTUALIZACIÓN Y BORRADO)
# =================================================================--
# ------------------------------------------------------------------
# 1. ACTUALIZACIÓN Y BORRADO EN MEMORIA (OPERACIONES SOBRE LA CESTA)
# ------------------------------------------------------------------

def actualizar_cesta(cesta, clave, nombre_bonito, icono, precio, kg):
    actualizar_cesta_dominio(
        cesta,
        clave,
        nombre_bonito,
        icono,
        precio,
        kg
    )


def agregar_producto(cesta, fruta):
    coincidencias = buscar_fruta(fruta)
    if len(coincidencias) == 1:
        clave = coincidencias[0]
        icono, nombre_bonito, precio = const.FRUTAS[clave]
        print(
            f"{const.SUBIR}{const.BORRAR}"
            f"¿Qué fruta quieres?: {nombre_bonito} {icono}"
        )
        existente = cesta.get(clave)
        kg_acumulados = (
            existente["kg"]
            if existente
            else 0.0
        )
        kg = func.solicitar_kilos(
            kg_acumulados,
            nombre_bonito
        )
        actualizar_cesta(
            cesta,
            clave,
            nombre_bonito,
            icono,
            precio,
            kg
        )
        return True
    elif len(coincidencias) > 1:
        nombres_sug = [
            const.FRUTAS[k][1]
            for k in coincidencias
        ]
        util.mostrar_mensaje(
            f"Especifica más... Coincidencias: {nombres_sug}",
            "warning"
        )
        return False
    else:
        util.mostrar_mensaje(
            f"La fruta '{fruta}' no existe en el catálogo",
            "error"
        )
        return False

# ------------------------------------------------------------------
# 3. BORRADO TOTAL DEL PEDIDO Y COMANDOS GLOBALES
# ------------------------------------------------------------------

def procesar_comando_global(fruta, cesta):
    # Detección del comando '/' para borrado completo
    if fruta == "/":
        if cesta:
            if util.pedir_confirmacion("¿Seguro que quieres CANCELAR este pedido y empezar uno nuevo?"):
                cesta.clear()  # Vacía completamente la cesta en memoria
                util.mostrar_mensaje("Pedido cancelado. Iniciando nueva cesta...", "info", segundos=2)
                return "CANCELAR"
            return "CONTINUAR"
        util.mostrar_mensaje("La cesta ya está vacía", "warning")
        return "CONTINUAR"
    elif fruta == "%":
        if cesta:
            if util.pedir_confirmacion("¿Generar el ticket final y cobrar?"):
                return "TICKET"
            return "CONTINUAR"
        util.mostrar_mensaje("La cesta está vacía. Añade al menos una fruta", "warning")
        return "CONTINUAR"
    elif fruta == "":
        util.mostrar_mensaje("Usa '%' para generar el ticket o '/' para cancelar el pedido", "info")
        return "CONTINUAR"
    return "NINGUNA"
