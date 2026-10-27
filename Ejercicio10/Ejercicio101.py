
class Semaforo:
    
    COLORES = {1:"Verde", 2:"Amarillo", 3:"Rojo"}
    
    def __init__(self):
        self.color = None
        
    def cambiar_color(self, color):
        if color in self.COLORES.values():
            self.color = color
        else:
            raise ValueError(f"Color inválido. Los colores a seleccionar son: {', '.join(self.COLORES.values())}") 
        
        
def limpiar_pantalla():
    import os
    os.system('cls' if os.name == 'nt' else 'clear')
    
def mostrar_menu():
    print("Seleccione un color del semáforo:")
    print("1. Verde")
    print("2. Amarillo")
    print("3. Rojo")
    print("0. Salir")
    opcion = input("Ingrese una opción (0-3): ").strip()

    if opcion == "0":
        return "Salir"

    try:
        numero = int(opcion)
        color = Semaforo.COLORES[numero]
    except (ValueError, KeyError):
        print("Opción no válida. Debe introducir 1, 2 o 3.")
        input("Presione Enter para intentarlo de nuevo...")
        return None

    semaforo = Semaforo()
    semaforo.cambiar_color(color)
    return semaforo.color

while True:
    try:
        limpiar_pantalla()

        color = mostrar_menu()

        if color is None:
            continue

        match color:
            case "Verde":
                print("[VERDE] Puede pasar")
            case "Amarillo":
                print("[AMARILLO] Precaución")
            case "Rojo":
                print("[ROJO] Stop")
            case "Salir":
                print("Programa finalizado.")
                break
            case _:
                print("Color no válido")

        input("\nPresione Enter para continuar...")

    except (KeyboardInterrupt, EOFError):
        print("\n¡Ha cerrado el programa de semáforo!")
        break    
