import sys
import time
from datetime import datetime
from reportlab.pdfgen import canvas
import Ejercicio63RaimonConstantes as const
import Ejercicio63RaimonUtilidades as util

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
    if clave in cesta:
        # Actualización de valores acumulados en memoria
        nuevo_kg = round(cesta[clave]["kg"] + kg, 3)
        
        if nuevo_kg <= 0:
            # Borrado individual en memoria si el peso queda en 0 o menos
            del cesta[clave]
        else:
            cesta[clave]["kg"] = nuevo_kg
            cesta[clave]["total"] = round(nuevo_kg * precio, 2)
            
    elif kg > 0:
        # Alta de nuevo elemento en memoria
        cesta[clave] = {
            "icono": icono,
            "nombre": nombre_bonito,
            "pvp": precio,
            "kg": round(kg, 3),
            "total": round(precio * kg, 2)
        }


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
