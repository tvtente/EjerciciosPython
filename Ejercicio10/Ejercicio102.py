def mostrar_menu():
    """Muestra las opciones y devuelve el color seleccionado."""
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


try:
    while True:
        color = mostrar_menu()

        match color:
            case "Verde":
                print("🟢 Puede pasar\n")
            case "Amarillo":
                print("🟡 Precaución\n")
            case "Rojo":
                print("🔴 Stop: debe esperar.\n")
            case "Salir":
                print("¡Hasta mañana!")
                break
except KeyboardInterrupt:
    print("\nPrograma terminado. ¡Hasta mañana!")
