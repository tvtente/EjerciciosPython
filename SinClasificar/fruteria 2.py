import subprocess
import platform

def Borro():
    if platform.system() == "Windows":
        subprocess.run(["cls"], shell=True)
    else:
        subprocess.run(["clear"])

Borro()



# ==========================================
#           🍓 FRUTERÍA ZYP 
# ==========================================


# ==========================================
# PRODUCTOS
# ==========================================

frutas = {
    "fresa": {"precio": 2.50, "stock": 5},
    "uva": {"precio": 1.80, "stock": 8},
    "kiwi": {"precio": 2.20, "stock": 6},
    "sandia": {"precio": 0.90, "stock": 10},
    "mango": {"precio": 2.00, "stock": 7},
    "manzana": {"precio": 1.20, "stock": 15},
    "pera": {"precio": 1.30, "stock": 12},
    "platano": {"precio": 1.50, "stock": 20},
    "naranja": {"precio": 1.10, "stock": 18},
    "limon": {"precio": 1.40, "stock": 10},
    "melocoton": {"precio": 2.30, "stock": 8},
    "piña": {"precio": 2.80, "stock": 6},
    "cereza": {"precio": 3.50, "stock": 5},
    "coco": {"precio": 2.50, "stock": 7},
    "papaya": {"precio": 2.70, "stock": 6}
}


# ==========================================
# MOSTRAR CABECERA
# ==========================================

def mostrar_cabecera():

    print("\n" + "=" * 60)
    print("              🍓 FRUTERÍA ZYP 🍓")
    print("=" * 60)


# ==========================================
# MOSTRAR PRODUCTOS
# ==========================================

def mostrar_frutas():

    print("\n🍎 PRODUCTOS DISPONIBLES")
    print("-" * 60)

    nombres = list(frutas.keys())

    for i, nombre in enumerate(nombres, start=1):

        precio = frutas[nombre]["precio"]
        stock = frutas[nombre]["stock"]

        if stock <= 0:
            estado = "AGOTADO"

        elif stock <= 3:
            estado = "⚠️ POCO STOCK"

        else:
            estado = f"{stock} kg"

        print(
            f"{i:2}. {nombre.capitalize():12}"
            f" {precio:5.2f} €/kg"
            f"   {estado}"
        )

    print("-" * 60)


# ==========================================
# ELEGIR FRUTA
# ==========================================

def elegir_fruta():

    nombres = list(frutas.keys())

    while True:

        mostrar_frutas()

        entrada = input(
            "\n🍓 ¿Qué fruta quieres? "
        ).lower().strip()

        # Elegir por número
        if entrada.isdigit():

            numero = int(entrada)

            if 1 <= numero <= len(nombres):

                fruta = nombres[numero - 1]

            else:

                print("❌ Ese número no existe.")
                continue

        else:

            fruta = entrada

            if fruta not in frutas:

                print("❌ Esa fruta no existe.")
                continue

        # Comprobar stock
        if frutas[fruta]["stock"] <= 0:

            print("❌ Esa fruta está agotada.")
            continue

        return fruta


# ==========================================
# PEDIR CANTIDAD
# ==========================================

def pedir_cantidad(stock):

    while True:

        entrada = input(
            "⚖️ ¿Cuántos kg quieres? "
        ).lower().strip()

        entrada = entrada.replace("kg", "")
        entrada = entrada.replace(",", ".")
        entrada = entrada.strip()

        try:

            cantidad = float(entrada)

            if cantidad <= 0:

                print(
                    "❌ La cantidad debe ser mayor que 0."
                )
                continue

            if cantidad > stock:

                print(
                    f"❌ Solo quedan {stock} kg."
                )
                continue

            return cantidad

        except ValueError:

            print(
                "❌ Cantidad incorrecta."
            )
            print(
                "Ejemplos: 1 | 1kg | 2.5kg | 2,5kg"
            )


# ==========================================
# AÑADIR AL CARRITO
# ==========================================

def añadir_al_carrito(carrito, fruta, cantidad):

    precio = frutas[fruta]["precio"]

    # Buscar si ya existe
    for producto in carrito:

        if producto["nombre"] == fruta:

            producto["cantidad"] += cantidad

            producto["subtotal"] = (
                producto["cantidad"] * precio
            )

            frutas[fruta]["stock"] -= cantidad

            return

    # Producto nuevo
    producto = {
        "nombre": fruta,
        "cantidad": cantidad,
        "precio": precio,
        "subtotal": cantidad * precio
    }

    carrito.append(producto)

    frutas[fruta]["stock"] -= cantidad


# ==========================================
# MOSTRAR CARRITO
# ==========================================

def mostrar_carrito(carrito):

    print("\n🛒 TU CARRITO")
    print("=" * 60)

    if not carrito:

        print("El carrito está vacío.")
        return 0

    total = 0

    for i, producto in enumerate(carrito, start=1):

        print(
            f"{i}. "
            f"{producto['nombre'].capitalize():12} "
            f"{producto['cantidad']:6.2f} kg "
            f"x {producto['precio']:5.2f} € "
            f"= {producto['subtotal']:6.2f} €"
        )

        total += producto["subtotal"]

    print("-" * 60)
    print(f"💰 SUBTOTAL: {total:.2f} €")

    return total


# ==========================================
# ELIMINAR PRODUCTO
# ==========================================

def eliminar_producto(carrito):

    if not carrito:

        print("❌ El carrito está vacío.")
        return

    mostrar_carrito(carrito)

    while True:

        entrada = input(
            "\n🗑️ Número del producto a eliminar: "
        ).strip()

        try:

            numero = int(entrada)

            if 1 <= numero <= len(carrito):

                producto = carrito.pop(numero - 1)

                # Devolver stock
                frutas[producto["nombre"]]["stock"] += (
                    producto["cantidad"]
                )

                print(
                    f"✅ {producto['nombre'].capitalize()} "
                    "eliminado del carrito."
                )

                return

            print("❌ Número incorrecto.")

        except ValueError:

            print("❌ Introduce un número.")


# ==========================================
# CALCULAR DESCUENTO
# ==========================================

def calcular_descuento(subtotal):

    if subtotal >= 20:

        descuento = subtotal * 0.10

    elif subtotal >= 10:

        descuento = subtotal * 0.05

    else:

        descuento = 0

    return descuento


# ==========================================
# ELEGIR BOLSA
# ==========================================

def elegir_bolsa():

    while True:

        respuesta = input(
            "\n🛍️ ¿Quieres bolsa? (si/no): "
        ).lower().strip()

        if respuesta == "si":

            return 0.10

        elif respuesta == "no":

            return 0

        print("❌ Responde 'si' o 'no'.")


# ==========================================
# ELEGIR MÉTODO DE PAGO
# ==========================================

def elegir_pago():

    print("\n💳 MÉTODO DE PAGO")
    print("-" * 30)
    print("1. 💶 Efectivo")
    print("2. 💳 Tarjeta")
    print("3. 📱 Bizum")
    print("-" * 30)

    while True:

        opcion = input(
            "Elige una opción: "
        ).strip()

        if opcion == "1":
            return "Efectivo"

        elif opcion == "2":
            return "Tarjeta"

        elif opcion == "3":
            return "Bizum"

        print("❌ Opción no válida.")


# ==========================================
# CALCULAR CAMBIO
# ==========================================

def calcular_cambio(total):

    while True:

        entrada = input(
            f"💶 Entrega dinero ({total:.2f} €): "
        )

        entrada = entrada.replace(",", ".")

        try:

            dinero = float(entrada)

            if dinero < total:

                falta = total - dinero

                print(
                    f"❌ Faltan {falta:.2f} €."
                )

                continue

            cambio = dinero - total

            return dinero, cambio

        except ValueError:

            print(
                "❌ Introduce una cantidad válida."
            )


# ==========================================
# MOSTRAR TICKET
# ==========================================

def mostrar_ticket(
    carrito,
    subtotal,
    descuento,
    bolsa,
    total,
    metodo,
    dinero=0,
    cambio=0
):

    print("\n")
    print("=" * 60)
    print("                 🧾 TICKET")
    print("              FRUTERÍA ZYP")
    print("=" * 60)

    for producto in carrito:

        print(
            f"{producto['nombre'].capitalize():12}"
            f" {producto['cantidad']:6.2f} kg"
            f"   {producto['subtotal']:7.2f} €"
        )

    print("-" * 60)

    print(f"Subtotal:              {subtotal:7.2f} €")

    if descuento > 0:

        porcentaje = 10 if subtotal >= 20 else 5

        print(
            f"Descuento ({porcentaje}%):        "
            f"-{descuento:6.2f} €"
        )

    print(f"Bolsa:                 {bolsa:7.2f} €")

    print("-" * 60)

    print(f"TOTAL:                 {total:7.2f} €")

    print(f"Método de pago:        {metodo}")

    if metodo == "Efectivo":

        print(
            f"Entregado:             {dinero:7.2f} €"
        )

        print(
            f"Cambio:                {cambio:7.2f} €"
        )

    print("=" * 60)
    print("       ✅ COMPRA REALIZADA")
    print("       🙏 ¡Gracias por comprar!")
    print("=" * 60)


# ==========================================
# FINALIZAR COMPRA
# ==========================================

def finalizar_compra(carrito):

    subtotal = mostrar_carrito(carrito)

    if subtotal == 0:

        return False

    descuento = calcular_descuento(subtotal)

    bolsa = elegir_bolsa()

    total = subtotal - descuento + bolsa

    print(
        f"\n💰 Total a pagar: {total:.2f} €"
    )

    metodo = elegir_pago()

    dinero = 0
    cambio = 0

    if metodo == "Efectivo":

        dinero, cambio = calcular_cambio(total)

    mostrar_ticket(
        carrito,
        subtotal,
        descuento,
        bolsa,
        total,
        metodo,
        dinero,
        cambio
    )

    return True


# ==========================================
# PROGRAMA PRINCIPAL
# ==========================================

def main():

    while True:

        carrito = []

        mostrar_cabecera()

        # ------------------------------
        # COMPRA
        # ------------------------------

        while True:

            fruta = elegir_fruta()

            stock = frutas[fruta]["stock"]

            cantidad = pedir_cantidad(stock)

            añadir_al_carrito(
                carrito,
                fruta,
                cantidad
            )

            print(
                f"\n✅ {cantidad:.2f} kg de "
                f"{fruta} añadidos al carrito."
            )

            # --------------------------
            # MENÚ
            # --------------------------

            while True:

                print("\n📋 MENÚ")
                print("-" * 40)
                print("1. 🍓 Comprar otra fruta")
                print("2. 🛒 Ver carrito")
                print("3. 🗑️ Eliminar producto")
                print("4. 💳 Finalizar compra")
                print("5. ❌ Cancelar compra")
                print("-" * 40)

                opcion = input(
                    "Elige una opción: "
                ).strip()

                if opcion == "1":

                    break

                elif opcion == "2":

                    mostrar_carrito(carrito)

                elif opcion == "3":

                    eliminar_producto(carrito)

                elif opcion == "4":

                    compra_realizada = finalizar_compra(
                        carrito
                    )

                    if compra_realizada:

                        break

                    continue

                elif opcion == "5":

                    # Devolver stock
                    for producto in carrito:

                        frutas[
                            producto["nombre"]
                        ]["stock"] += producto["cantidad"]

                    print(
                        "\n❌ Compra cancelada."
                    )

                    break

                else:

                    print(
                        "❌ Opción no válida."
                    )

            # --------------------------------
            # COMPROBAR SI TERMINÓ LA COMPRA
            # --------------------------------

            if opcion == "4" and compra_realizada:

                break

            if opcion == "5":

                break

        # --------------------------------
        # NUEVA COMPRA
        # --------------------------------

        while True:

            respuesta = input(
                "\n🔄 ¿Quieres realizar otra compra? "
                "(si/no): "
            ).lower().strip()

            if respuesta == "si":

                break

            elif respuesta == "no":

                print(
                    "\n👋 Programa finalizado."
                )

                return

            else:

                print(
                    "❌ Responde 'si' o 'no'."
                )


# ==========================================
# INICIAR PROGRAMA
# ==========================================

if __name__ == "__main__":

    main()