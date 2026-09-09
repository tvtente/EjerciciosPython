import re
import sys
import time
from datetime import datetime

import Ejercicio63RaimonConstantes as const

from Ejercicio63RaimonUtilidades import (
    limpiar_pantalla,
    pedir_confirmacion,
    formato_precio
)


# ============================================================
# FUNCIONES DEL PROGRAMA
# ============================================================

def mostrar_cesta(cesta):
    print("\n" + const.CYAN + "╔══════════════════════════════════════════════════╗" + const.RESET)
    print(const.CYAN + "║                    CESTA                         ║" + const.RESET)
    print(const.CYAN + "╚══════════════════════════════════════════════════╝" + const.RESET)

    if not cesta:
        print("La cesta está vacía.")
        return

    total = 0

    for i, producto in enumerate(cesta, 1):
        fruta = producto["fruta"]
        kilos = producto["kilos"]
        precio = producto["precio"]
        subtotal = kilos * precio
        total += subtotal

        print(
            f"{i}. {fruta} - "
            f"{kilos:.2f} kg x {formato_precio(precio)} = "
            f"{formato_precio(subtotal)}"
        )

    print("-" * 52)
    print(f"TOTAL: {formato_precio(total)}")


def procesar_comando_global(comando, cesta):
    comando = comando.lower().strip()

    if comando == "salir":
        return "salir"

    if comando == "cesta":
        mostrar_cesta(cesta)
        return "continuar"

    if comando == "limpiar":
        limpiar_pantalla()
        return "continuar"

    return None


def buscar_fruta(nombre):
    nombre = nombre.lower().strip()

    for fruta in const.FRUTAS:
        if fruta["nombre"].lower() == nombre:
            return fruta

    return None


def solicitar_kilos():
    while True:
        entrada = input("¿Cuántos kilos quieres? ").strip()

        try:
            kilos = float(entrada)

            if kilos <= 0:
                print(const.ROJO + "Los kilos deben ser mayores que 0." + const.RESET)
                continue

            return kilos

        except ValueError:
            print(const.ROJO + "Introduce una cantidad válida." + const.RESET)


def actualizar_cesta(cesta, fruta, kilos):
    for producto in cesta:
        if producto["fruta"] == fruta["nombre"]:
            producto["kilos"] += kilos
            return

    cesta.append({
        "fruta": fruta["nombre"],
        "kilos": kilos,
        "precio": fruta["precio"]
    })


def mostrar_ticket(cesta):
    print("\n")
    print(const.CYAN + "════════════════════════════════════════════" + const.RESET)
    print(const.BOLD + "                 TICKET" + const.RESET)
    print(const.CYAN + "════════════════════════════════════════════" + const.RESET)

    if not cesta:
        print("La cesta está vacía.")
        return

    subtotal = 0

    for producto in cesta:
        importe = producto["kilos"] * producto["precio"]
        subtotal += importe

        print(
            f"{producto['fruta']:<15}"
            f"{producto['kilos']:>7.2f} kg  "
            f"{formato_precio(importe):>10}"
        )

    iva = subtotal * const.TIPO_IVA
    total = subtotal + iva

    print("-" * 44)
    print(f"Subtotal:       {formato_precio(subtotal)}")
    print(f"IVA:            {formato_precio(iva)}")
    print(f"TOTAL:          {formato_precio(total)}")
    print(const.CYAN + "════════════════════════════════════════════" + const.RESET)


def procesar_pago(total):
    while True:
        try:
            pago = float(input("Introduce el importe pagado: "))

            if pago < total:
                print(
                    const.ROJO +
                    f"Faltan {formato_precio(total - pago)}." +
                    const.RESET
                )
                continue

            cambio = pago - total

            print(
                const.VERDE +
                f"Pago aceptado. Cambio: {formato_precio(cambio)}" +
                const.RESET
            )

            return pago, cambio

        except ValueError:
            print(const.ROJO + "Introduce un importe válido." + const.RESET)


def crear_pdf(cesta, total, pago, cambio):
    nombre_archivo = (
        f"ticket_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    )

    try:
        from reportlab.pdfgen import canvas

        pdf = canvas.Canvas(nombre_archivo)

        y = 800

        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(50, y, "TICKET DE COMPRA")

        y -= 40

        pdf.setFont("Helvetica", 10)

        for producto in cesta:
            importe = producto["kilos"] * producto["precio"]

            texto = (
                f"{producto['fruta']} - "
                f"{producto['kilos']:.2f} kg - "
                f"{importe:.2f} €"
            )

            pdf.drawString(50, y, texto)
            y -= 20

        y -= 10

        pdf.drawString(50, y, f"Total: {total:.2f} €")
        y -= 20
        pdf.drawString(50, y, f"Pagado: {pago:.2f} €")
        y -= 20
        pdf.drawString(50, y, f"Cambio: {cambio:.2f} €")

        pdf.save()

        print(
            const.VERDE +
            f"\nPDF creado correctamente: {nombre_archivo}" +
            const.RESET
        )

    except ImportError:
        print(
            const.ROJO +
            "No se pudo crear el PDF porque falta ReportLab." +
            const.RESET
        )


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

def ejecutar_tpv():

    cesta = []

    limpiar_pantalla()

    print(const.CYAN + const.CABECERA + const.RESET)

    while True:

        print("\n" + const.BOLD + "MENÚ PRINCIPAL" + const.RESET)
        print("1. Comprar fruta")
        print("2. Ver cesta")
        print("3. Finalizar compra")
        print("4. Salir")

        opcion = input("\nSelecciona una opción: ").strip()

        # --------------------------------------------
        # COMPRAR FRUTA
        # --------------------------------------------

        if opcion == "1":

            print("\nFrutas disponibles:")

            for i, fruta in enumerate(const.FRUTAS, 1):
                print(
                    f"{i}. {fruta['nombre']} - "
                    f"{formato_precio(fruta['precio'])}/kg"
                )

            entrada = input(
                "\nEscribe el nombre de la fruta o su número: "
            ).strip()

            fruta = None

            # Buscar por número
            if entrada.isdigit():

                numero = int(entrada)

                if 1 <= numero <= len(const.FRUTAS):
                    fruta = const.FRUTAS[numero - 1]

            # Buscar por nombre
            else:
                fruta = buscar_fruta(entrada)

            if fruta is None:
                print(
                    const.ROJO +
                    "Fruta no encontrada." +
                    const.RESET
                )
                continue

            kilos = solicitar_kilos()

            actualizar_cesta(cesta, fruta, kilos)

            print(
                const.VERDE +
                f"\nAñadido: {kilos:.2f} kg de {fruta['nombre']}." +
                const.RESET
            )

        # --------------------------------------------
        # VER CESTA
        # --------------------------------------------

        elif opcion == "2":

            mostrar_cesta(cesta)

        # --------------------------------------------
        # FINALIZAR COMPRA
        # --------------------------------------------

        elif opcion == "3":

            if not cesta:
                print(
                    const.ROJO +
                    "La cesta está vacía." +
                    const.RESET
                )
                continue

            mostrar_ticket(cesta)

            subtotal = sum(
                producto["kilos"] * producto["precio"]
                for producto in cesta
            )

            iva = subtotal * const.TIPO_IVA
            total = subtotal + iva

            print(
                f"\nTotal a pagar: "
                f"{formato_precio(total)}"
            )

            confirmar = pedir_confirmacion(
                "¿Quieres continuar con el pago?"
            )

            if not confirmar:
                continue

            pago, cambio = procesar_pago(total)

            crear_pdf(
                cesta,
                total,
                pago,
                cambio
            )

            cesta.clear()

            print(
                const.VERDE +
                "\nCompra finalizada correctamente." +
                const.RESET
            )

        # --------------------------------------------
        # SALIR
        # --------------------------------------------

        elif opcion == "4":

            print("\nPrograma finalizado.")
            break

        # --------------------------------------------
        # OPCIÓN INCORRECTA
        # --------------------------------------------

        else:

            print(
                const.ROJO +
                "Opción no válida." +
                const.RESET
            )


# ============================================================
# INICIO
# ============================================================

if __name__ == "__main__":
    ejecutar_tpv()