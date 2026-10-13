import subprocess
import platform


def borrar():
    if platform.system() == "Windows":
        subprocess.run(["cls"], shell=True)
    else:
        subprocess.run(["clear"])   


def mostrar_fruits():
    print("fruits disponibles:")

    for fruta in fruits:
        print(fruta, emojis[fruta])  # show the fruits


def calcular_total():
    total = 0

    for fruta in carrito:
        total += carrito[fruta]["precio"]  # Calculate the fruits

    return total     


def calcular_total_kilos():
    total_kilos = 0

    for fruta in carrito:
        total_kilos += carrito[fruta]["kilos"]  # Calculate the kilos

    return total_kilos     


def mostrar_carrito():
    print("\n--- Carrito final ---")

    for fruta in carrito:
        kilos = carrito[fruta]["kilos"]
        precio = carrito[fruta]["precio"]

        print(f"{fruta}: {kilos:.2f} kg - €{precio:.2f}")     # show the fruits kilos price in cart shopping cart 


borrar()  # clean the terminal


fruits = {        # dictionary  of fruits
    "pera": {
        "precio": 0.90,
        "disponibilidad": 10.0
    },
    "manzana": {
        "precio": 0.70,
        "disponibilidad": 9.0
    },
    "uva": {
        "precio": 0.85,
        "disponibilidad": 6.0
    },
    "naranja": {
        "precio": 0.80,
        "disponibilidad": 7.0
    }
}

emojis = {
    "pera": "🍐",
    "manzana": "🍎",
    "uva": "🍇",
    "naranja": "🍊"
}


carrito = {}  # empty carrito shopping cart


mostrar_fruits()  # show available fruits


while True:     # while loop for repeat the process

    fruta = input("¿Qué fruta quieres? ").lower()   # ask the user which fruit they want

    if fruta in fruits:     # check if the fruit exists in the dictionary
        print("La fruta está disponible.")

        kilos = float(input("¿Cuántos kilos quieres? "))     # convert the quantity to a decimal number 

        if kilos > 0:    # if quantity is greater then 0 

            if kilos <= fruits[fruta]["disponibilidad"]:   # check if there is enough stock
                print("Hay suficiente stock.")    # tell the user there is enough stock

                fruits[fruta]["disponibilidad"] -= kilos   # subtract the purchased kilos from the stock

                precio = fruits[fruta]["precio"] * kilos   # calculate the price using the price per kilo

                if fruta in carrito:
                    carrito[fruta]["kilos"] += kilos
                    carrito[fruta]["precio"] += precio

                else:
                    carrito[fruta] = {     # add a new fruit to the cart
                        "kilos": kilos,
                        "precio": precio
                    }

                print(f"Precio: €{precio:.2f}")    # show the price with 2 decimal places

                print("Tu carrito:")
                print(carrito)

                comprar_mas = input(    # asking whant to buy more fruits
                    "¿Quieres comprar más? (si/no): "
                ).lower()   # lower means pera  not Pera

                if comprar_mas == "no":    # if user say no then break stop
                    break

            else:   # if there is not enough stock
                print("No hay suficiente stock.")

        else:    # if the quantity is 0 or negative
            print("Cantidad no válida.")

    else:
        print("Lo siento, esa fruta no está disponible.")


total = calcular_total()     # get the total price from the function
print(f"Total: €{total:.2f}")


total_kilos = calcular_total_kilos()     # get the total kilos from the function
print(f"Total kilos: {total_kilos:.2f} kg")


mostrar_carrito()   # show in cart shopping cart


print("Gracias por tu compra.")   # in the end message 