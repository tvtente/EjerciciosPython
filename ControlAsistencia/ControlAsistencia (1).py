from Funcionalidades import (
    actualizar_registro,
    crear_registro,
    eliminar_registro,
    leer_registros,
)
from BorrarPantalla import Borro


def menu():
    """Muestra el menú principal y dirige las opciones del programa."""
    while True:
        print("\n--- 🔑 CONTROL DE ASISTENCIA 🔑 ---\n")
        print("1. Registrar Entrada/Salida (Crear)")
        print("2. Ver Registros (Leer)")
        print("3. Actualizar Registro")
        print("4. Eliminar Registro")
        print("5. Salir")
        opcion = input("\nSeleccione una opción: ")

        if opcion == "1":
            crear_registro()
        elif opcion == "2":
            leer_registros()
        elif opcion == "3":
            actualizar_registro()
        elif opcion == "4":
            eliminar_registro()
        elif opcion == "5":
            Borro()
            break
        else:
            print("Opción inválida en el menú.")


if __name__ == "__main__":
    Borro()
    menu()
