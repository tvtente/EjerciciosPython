def mostrar_menu():
    while True:
        print("Seleccione un color del semáforo:")
        print("1. Verde")
        print("2. Amarillo")
        print("3. Rojo")
        print("4. Salir")

        opcion = input("Ingrese una opción (1-4): ")

        match opcion:
            case "1":
                return "Verde"
            case "2":
                return "Amarillo"
            case "3":
                return "Rojo"
            case "4":
                return "Salir"
            case _:
                print("Opción no válida. Intente nuevamente.\n")


def mostrar_resumen(contadores):
    print("\n--- Resumen de colores seleccionados ---")
    print(f"🟢 Verde: {contadores['Verde']}")
    print(f"🟡 Amarillo: {contadores['Amarillo']}")
    print(f"🔴 Rojo: {contadores['Rojo']}")


contadores = {"Verde": 0, "Amarillo": 0, "Rojo": 0}

try:
    while True:
        color = mostrar_menu()

        if color == "Salir":
            mostrar_resumen(contadores)
            print("¡Hasta mañana!")
            break

        contadores[color] += 1

        match color:
            case "Verde":
                print("🟢 Puede pasar\n")
            case "Amarillo":
                print("🟡 Precaución\n")
            case "Rojo":
                print("🔴 Stop: debe esperar.\n")
except KeyboardInterrupt:
    mostrar_resumen(contadores)
    print("\nPrograma terminado. ¡Hasta mañana!")
