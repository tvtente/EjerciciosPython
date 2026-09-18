def limpiar_pantalla():
    import os
    os.system('cls' if os.name == 'nt' else 'clear')
    
def mostrar_menu():
    print("Seleccione un color del semáforo:")
    print("1. Verde")
    print("2. Amarillo")
    print("3. Rojo")
    opcion = input("Ingrese el número correspondiente al color (1-3): ")

    match opcion:
        case "1":
            return "Verde"
        case "2":
            return "Amarillo"
        case "3":
            return "Rojo"
        case _:
            print("Opción no válida. Intente nuevamente.")
            return mostrar_menu()

while True:
    try:
        limpiar_pantalla()

        color = mostrar_menu()

        match color:
            case "Verde":
                print("🟢 Puede pasar")

            case "Amarillo":
                print("🟡 Precaución")

            case "Rojo":
                print("🔴 Stop")
                break

            case _:
                print("Color no válido")

    except KeyboardInterrupt:
        print("\n¡HASTA MAÑANA!")
        break    