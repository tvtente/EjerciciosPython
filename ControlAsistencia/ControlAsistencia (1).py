from Funcionalidades import (
    actualizar_registro,
    crear_registro,
    eliminar_registro,
    leer_registros,
)
from BorrarPantalla import Borro

ROJO = "\033[31m"
VERDE = "\033[32m"
AMARILLO = "\033[33m"
CIAN = "\033[36m"
NEGRITA = "\033[1m"
RESET = "\033[0m"


def mostrar_menu_asistencia():
    """Muestra el menú principal y devuelve la opción elegida."""
    ancho = 58
    ancho_con_emoji = ancho - 1

    print(f"\n{CIAN}╔{'═' * ancho}╗{RESET}")
    print(
        f"{CIAN}║{RESET}{NEGRITA}"
        f"{'🔑 CONTROL DE ASISTENCIA':^{ancho_con_emoji}}"
        f"{RESET}{CIAN}║{RESET}"
    )
    print(f"{CIAN}╠{'═' * ancho}╣{RESET}")

    opciones = (
        ("1", "📝 Registrar entrada/salida", VERDE),
        ("2", "🔎 Ver registros", CIAN),
        ("3", "🔧 Actualizar registro", AMARILLO),
        ("4", "❌ Eliminar registro", ROJO),
        ("5", "🚪 Salir", ROJO),
    )
    for numero, texto, color in opciones:
        linea = f" {numero}. {texto}"
        print(
            f"{CIAN}║{RESET}{color}{linea:<{ancho_con_emoji}}"
            f"{RESET}{CIAN}║{RESET}"
        )

    print(f"{CIAN}╟{'─' * ancho}╢{RESET}")
    print(
        f"{CIAN}║{RESET}"
        f"{'👉 Selecciona una opción del 1 al 5':<{ancho_con_emoji}}"
        f"{CIAN}║{RESET}"
    )
    print(f"{CIAN}╚{'═' * ancho}╝{RESET}")
    return input(f"{CIAN}👉 Elige una opción: {RESET}").strip()


def menu():
    """Muestra el menú principal y dirige las opciones del programa."""
    while True:
        opcion = mostrar_menu_asistencia()

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
    try:
        Borro()
        menu()
    except KeyboardInterrupt:
        Borro()
        ancho = 58
        print(f"\n{CIAN}╔{'═' * ancho}╗{RESET}")
        print(
            f"{CIAN}║{RESET}{NEGRITA}"
            f"{'👋 PROGRAMA FINALIZADO':^{ancho - 1}}"
            f"{RESET}{CIAN}║{RESET}"
        )
        print(f"{CIAN}╠{'═' * ancho}╣{RESET}")
        print(
            f"{CIAN}║{RESET}"
            f"{'Gracias por usar el control de asistencia.':^{ancho}}"
            f"{CIAN}║{RESET}"
        )
        print(f"{CIAN}╚{'═' * ancho}╝{RESET}")
