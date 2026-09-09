from datetime import datetime
from reportlab.pdfgen import canvas

import Ejercicio63RaimonConstantes as const

from Ejercicio63RaimonUtilidades import (
    limpiar_pantalla,
    mostrar_mensaje,
    pedir_confirmacion,
    formato_precio
)


# ==========================================
# 2.2 FLUJO DE COMPRA Y CESTA
# ==========================================


def mostrar_cesta(cesta):
    """Muestra los productos de la cesta actual."""

    if cesta:
        print("🛒 CESTA ACTUAL:")

        total_provisional = sum(
            item["total"]
            for item in cesta.values()
        )

        for item in cesta.values():

            kg_txt = (
                f"{item['kg']:.2f}"
                .replace(".00", "")
                .replace(".", ",")
            )

            tot_txt = formato_precio(
                item["total"]
            )

            print(
                f"   • {item['icono']} "
                f"{item['nombre']:<10}: "
                f"{kg_txt:>5} Kg  ->  "
                f"{tot_txt:>9}"
            )

        tot_prov_txt = formato_precio(
            total_provisional
        )

        print("-" * 46)

        print(
            f"   {'TOTAL PROVISIONAL':<26} "
            f"->  {tot_prov_txt:>9}"
        )

        print("-" * 46 + "\n")


def procesar_comando_global(fruta, cesta):
    """Procesa los comandos /, % y entrada vacía."""

    if fruta == "/":

        if cesta:

            if pedir_confirmacion(
                "¿Seguro que quieres CANCELAR "
                "este pedido y empezar uno nuevo?"
            ):
                cesta.clear()

                mostrar_mensaje(
                    "Pedido cancelado. "
                    "Iniciando nueva cesta...",
                    "info",
                    segundos=2
                )

                return "CANCELAR"

            return "CONTINUAR"

        mostrar_mensaje(
            "La cesta ya está vacía",
            "warning"
        )

        return "CONTINUAR"


    elif fruta == "%":

        if cesta:

            if pedir_confirmacion(
                "¿Generar el ticket final y cobrar?"
            ):
                return "TICKET"

            return "CONTINUAR"

        mostrar_mensaje(
            "La cesta está vacía. "
            "Añade al menos una fruta",
            "warning"
        )

        return "CONTINUAR"


    elif fruta == "":

        mostrar_mensaje(
            "Usa '%' para generar el ticket "
            "o '/' para cancelar el pedido",
            "info"
        )

        return "CONTINUAR"


    return "NINGUNA"


def buscar_fruta(fruta):
    """Busca frutas que coincidan con el texto introducido."""

    clave_entrada = (
        fruta.lower()
        .replace("á", "a")
        .replace("é", "e")
        .replace("í", "i")
        .replace("ó", "o")
        .replace("ú", "u")
    )

    coincidencias = []

    if clave_entrada != "":

        for clave in const.FRUTAS:

            if clave.startswith(clave_entrada):
                coincidencias.append(clave)

    return coincidencias


def solicitar_kilos(kg_acumulados, nombre_bonito):
    """Solicita y valida los kilos del producto."""

    kg_maximos_permitidos = round(
        10.0 - kg_acumulados,
        2
    )

    if kg_maximos_permitidos < 0.001:

        mensaje_aviso = (
            f"\nTienes {kg_acumulados:.2f} Kg "
            f"de {nombre_bonito}. "
            "Límite máximo (10,00 Kg) alcanzado. "
            "Usa '*' o '-' para reducir."
        ).replace(".", ",")

        mostrar_mensaje(
            mensaje_aviso,
            "warning",
            segundos=3
        )


    while True:

        kg_input = input(
            f"¿Cuántos kilos? "
            f"(máx. {kg_maximos_permitidos:.2f} kg): "
        ).strip().replace(",", ".")


        # Permite escribir .25, -.25 o *.25

        if kg_input.startswith("."):
            kg_input = "0" + kg_input

        elif kg_input.startswith("-."):
            kg_input = kg_input.replace(
                "-.",
                "-0.",
                1
            )

        elif kg_input.startswith("*."):
            kg_input = kg_input.replace(
                "*.",
                "*0.",
                1
            )


        es_fijado = False

        if kg_input.startswith("*"):
            es_fijado = True
            kg_input = kg_input.replace("*", "", 1)


        try:

            num_kilos = float(kg_input)


            # ======================================
            # 1. FIJAR PESO
            # ======================================

            if es_fijado:

                if num_kilos == 0:
                    return -kg_acumulados

                if 0.001 <= num_kilos <= 10.0:
                    return num_kilos - kg_acumulados

                mostrar_mensaje(
                    "El peso fijado debe estar "
                    "entre 0,001 y 10 Kg",
                    "error"
                )

                continue


            # ======================================
            # 2. RESTAR PESO
            # ======================================

            if num_kilos < 0:

                nuevo_total = round(
                    kg_acumulados + num_kilos,
                    3
                )

                if nuevo_total == 0:
                    return num_kilos

                elif nuevo_total > 0:
                    return num_kilos

                else:

                    mostrar_mensaje(
                        f"No puedes restar "
                        f"{abs(num_kilos):.2f} Kg. "
                        f"Solo hay "
                        f"{kg_acumulados:.2f} Kg "
                        "en la cesta",
                        "error"
                    )

                    continue


            # ======================================
            # 3. SUMAR PESO
            # ======================================

            if (
                0.001
                <= num_kilos
                <= kg_maximos_permitidos
            ):
                return num_kilos


            if kg_maximos_permitidos < 0.001:

                mostrar_mensaje(
                    "Límite de 10 Kg alcanzado. "
                    "Solo puedes restar "
                    "(ej: -2) o fijar "
                    "(ej: *5)",
                    "error"
                )

            else:

                mostrar_mensaje(
                    f"Introduce una cantidad válida "
                    f"(máx. "
                    f"{kg_maximos_permitidos:.2f} Kg)",
                    "error"
                )


        except ValueError:

            mostrar_mensaje(
                "Entrada no válida. "
                "Escribe un número "
                "(ej: ,05), "
                "resta (ej: -,5) "
                "o fija (ej: *,5)",
                "error"
            )


def actualizar_cesta(
    cesta,
    clave,
    nombre_bonito,
    icono,
    precio,
    kg
):
    """Añade, modifica o elimina un producto."""

    total_producto = precio * kg


    if clave in cesta:

        cesta[clave]["kg"] += kg

        cesta[clave]["total"] += total_producto

        if cesta[clave]["kg"] <= 0:
            del cesta[clave]


    elif kg > 0:

        cesta[clave] = {
            "icono": icono,
            "nombre": nombre_bonito,
            "pvp": precio,
            "kg": kg,
            "total": total_producto
        }


# ==========================================
# 2.3 CIERRE, PAGO Y FACTURACIÓN
# ==========================================


def mostrar_ticket(cesta, id_ticket):
    """Muestra el ticket final en pantalla."""

    if not cesta:
        return


    limpiar_pantalla()

    W_TEXTO = 51
    W_LINEA = 53

    total = sum(
        item["total"]
        for item in cesta.values()
    )

    base = total / (1 + const.TIPO_IVA)

    iva = total - base


    print("=" * W_LINEA)

    print(
        f" {const.BOLD}"
        f"{'TICKET DE COMPRA':^{W_LINEA}}"
        f"{const.RESET}"
    )

    print(" " + "=" * W_LINEA)

    print(
        f"  {f'Nº Ticket: {id_ticket}':>{W_TEXTO}}"
    )

    print(" " + "-" * W_LINEA)

    print(
        f"  {'PRODUCTO':<16} | "
        f"{'PESO':>8} | "
        f"{'PVP/Kg':>9} | "
        f"{'TOTAL':>9}"
    )

    print(" " + "-" * W_LINEA)


    for item in cesta.values():

        peso = (
            f"{item['kg']:.2f} Kg"
            .replace(".", ",")
        )

        print(
            f"  {item['nombre']:<16} | "
            f"{peso:>8} | "
            f"{formato_precio(item['pvp']):>9} | "
            f"{formato_precio(item['total']):>9}"
        )


    print(" " + "-" * W_LINEA)

    print(
        f"  "
        f"{f'Base Imponible: {formato_precio(base)}':>{W_TEXTO}}"
    )

    print(
        f"  "
        f"{f'IVA ({const.TIPO_IVA * 100:g}%): {formato_precio(iva)}':>{W_TEXTO}}"
    )

    print(" " + "=" * W_LINEA)

    print(
        f"  "
        f"{f'TOTAL A PAGAR: {formato_precio(total)}':>{W_TEXTO}}"
    )

    print(" " + "=" * W_LINEA + "\n")


def procesar_pago(total_a_pagar):
    """Gestiona el pago mediante efectivo o tarjeta."""

    while True:

        entrega_input = input(
            f"\n{const.BOLD}"
            f"Total: {formato_precio(total_a_pagar)}"
            f"{const.RESET} | "
            f"{const.NARANJA}Entrega (€)"
            f"{const.RESET} "
            f"{const.CYAN}[ENTER = Tarjeta]"
            f"{const.RESET} > "
        ).strip()


        # ENTER = tarjeta

        if entrega_input == "":

            print(
                f"{const.CYAN}"
                "💳 PAGO CON TARJETA ACEPTADO"
                f"{const.RESET}\n"
            )

            return (
                "Tarjeta",
                total_a_pagar,
                0.0
            )


        try:

            entrega = float(
                entrega_input.replace(",", ".")
            )


            if entrega >= total_a_pagar:

                cambio = entrega - total_a_pagar

                print(
                    f"{const.NARANJA}"
                    "💶 CAMBIO A DEVOLVER: "
                    f"{formato_precio(cambio)}"
                    f"{const.RESET}\n"
                )

                return (
                    "Efectivo",
                    entrega,
                    cambio
                )


            faltante = (
                total_a_pagar - entrega
            )

            mostrar_mensaje(
                f"Cantidad insuficiente. "
                f"Faltan "
                f"{formato_precio(faltante)}",
                "error",
                segundos=2,
                lineas_a_borrar=4
            )


        except ValueError:

            mostrar_mensaje(
                "Introduce un número válido "
                "o pulsa ENTER para tarjeta",
                "error",
                segundos=2,
                lineas_a_borrar=4
            )


def crear_pdf(
    cesta,
    id_ticket,
    entrega,
    cambio,
    metodo_pago
):
    """Genera el ticket en formato PDF."""

    print("⏳ Generando ticket en PDF...")


    total = sum(
        item["total"]
        for item in cesta.values()
    )

    base = total / (1 + const.TIPO_IVA)

    iva = total - base

    ANCHO_L = 36


    fecha_actual = datetime.now().strftime(
        "%d/%m/%Y %H:%M"
    )


    lineas = [

        "FRUITERIA L'HORT".center(ANCHO_L),

        "CIF: B-12345678".center(ANCHO_L),

        "Carrer Major 123, Barcelona".center(
            ANCHO_L
        ),

        f"Fecha: {fecha_actual}".center(
            ANCHO_L
        ),

        f"Nº Ticket: {id_ticket}".center(
            ANCHO_L
        ),

        "=" * ANCHO_L,

        f"{'PRODUCTO':<12} "
        f"{'PESO(Kg)':>8} "
        f"{'PVP':>5} "
        f"{'TOTAL':>8}",

        "-" * ANCHO_L
    ]


    for item in cesta.values():

        nombre = item["nombre"][:12]

        peso = (
            f"{item['kg']:.2f}"
            .replace(".", ",")
        )

        pvp = (
            f"{item['pvp']:.2f}"
            .replace(".", ",")
        )

        lineas.append(
            f"{nombre:<12} "
            f"{peso:>8} "
            f"{pvp:>5} "
            f"{formato_precio(item['total']):>8}"
        )


    bloque_pago = [

        "-" * ANCHO_L,

        f"{'Base Imponible:':<27} "
        f"{formato_precio(base):>8}",

        f"{f'IVA ({const.TIPO_IVA * 100:g}%):':<27} "
        f"{formato_precio(iva):>8}",

        "=" * ANCHO_L,

        f"{'TOTAL A PAGAR:':<27} "
        f"{formato_precio(total):>8}",

        "=" * ANCHO_L,

        f"{'Forma de Pago:':<27} "
        f"{metodo_pago:>8}"
    ]


    if metodo_pago == "Efectivo":

        bloque_pago.extend([

            f"{'Entregado:':<27} "
            f"{formato_precio(entrega):>8}",

            f"{'Cambio:':<27} "
            f"{formato_precio(cambio):>8}"
        ])


    bloque_pago.extend([

        "- " * (ANCHO_L // 2),

        "",

        "¡Gracias por su compra!".center(
            ANCHO_L
        )
    ])


    lineas.extend(bloque_pago)


    ancho_ticket = 226

    alto_ticket = (
        40
        + len(lineas) * 12
    )


    nombre_archivo = (
        f"ticket_{id_ticket}.pdf"
    )


    documento = canvas.Canvas(
        nombre_archivo,
        pagesize=(
            ancho_ticket,
            alto_ticket
        )
    )


    texto = documento.beginText(
        14,
        alto_ticket - 20
    )

    texto.setFont(
        "Courier-Bold",
        8.5
    )

    texto.setLeading(12)


    for linea in lineas:
        texto.textLine(linea)


    documento.drawText(texto)

    documento.save()


    print(
        f"{const.VERDE}"
        f"📄 Ticket '{nombre_archivo}' "
        "guardado correctamente"
        f"{const.RESET}"
    )

    print(
        "🖨️  Ticket enviado a la impresora..."
    )