"""Gustavo Moyano Díaz - Simulador interactivo de un semáforo."""

import os
import time
from datetime import datetime

def limpiar_pantalla():
    """Limpia la consola en Windows, Linux y macOS."""
    os.system("cls" if os.name == "nt" else "clear")

DURACIONES = {"rojo": 5, "verde": 7, "amarillo": 3}
MENSAJES = {
    "rojo": "STOP",
    "amarillo": "Precaución",
    "verde": "Pase"
}
ESTADISTICAS = {"ciclos": 0, "cambios": 0, "segundos": 0}


def pausa():
    input("\nPresione Enter para continuar...")


def barra_progreso(color_activo, actual, total, longitud=20):
    """Devuelve una barra que representa el tiempo restante."""
    completados = round(actual / total * longitud)
    peaton = "🚶" if color_activo == "verde" else "🏃" if color_activo == "amarillo" else "🧍"
    return "█" * completados + "░" * (longitud - completados) + f" {peaton}"


def dibujar_semaforo(color_activo, segundos=None, duracion=None, modo="AUTOMÁTICO"):
    """Dibuja el panel completo del semáforo."""
    luces = {
        "rojo": "🔴" if color_activo == "rojo" else "⚫",
        "amarillo": "🟡" if color_activo == "amarillo" else "⚫",
        "verde": "🟢" if color_activo == "verde" else "⚫",
    }

    limpiar_pantalla()
    print("╔══════════════════════════════════════╗")
    print("║       CENTRAL DE TRÁFICO BCN         ║")
    print("╠═══════════════════╦══════════════════╣")
    print("║     SEMÁFORO      ║    INFORMACIÓN   ║")
    print("╠═══════════════════╬══════════════════╣")
    print(f"║        {luces['rojo']}         ║ Estado: {color_activo.upper():<9}║")
    print("║                   ║                  ║")
    print(f"║        {luces['amarillo']}         ║ Modo: {modo:<11}║")
    print("║                   ║                  ║")
    print(f"║        {luces['verde']}         ║ Hora: {datetime.now():%H:%M:%S}   ║")
    print("╠═══════════════════╩══════════════════╣")
    print(f"║ {MENSAJES[color_activo]:^36} ║")

    if segundos is not None and duracion is not None:
        barra = barra_progreso(color_activo, segundos, duracion)
        print(f"║ Tiempo: [{barra}] {segundos:>2}s║")

    print("╚══════════════════════════════════════╝")


def ejecutar_estado(color, duracion, modo="AUTOMÁTICO"):
    """Muestra un estado durante la cantidad indicada de segundos."""
    ESTADISTICAS["cambios"] += 1
    for segundos in range(duracion, 0, -1):
        dibujar_semaforo(color, segundos, duracion, modo)
        print("\nCtrl+C: volver al menú")
        time.sleep(1)
        ESTADISTICAS["segundos"] += 1


def pedir_entero(mensaje, minimo=0):
    """Solicita un número entero válido."""
    while True:
        try:
            numero = int(input(mensaje))
            if numero >= minimo:
                return numero
            print(f"El valor debe ser igual o mayor que {minimo}.")
        except ValueError:
            print("Introduzca un número entero válido.")


def modo_automatico():
    """Ejecuta uno o varios ciclos completos."""
    limpiar_pantalla()
    print("MODO AUTOMÁTICO")
    ciclos = pedir_entero("Número de ciclos (0 = infinitos): ")
    realizados = 0

    try:
        while ciclos == 0 or realizados < ciclos:
            for color in ("rojo", "verde", "amarillo"):
                ejecutar_estado(color, DURACIONES[color])
            realizados += 1
            ESTADISTICAS["ciclos"] += 1
    except KeyboardInterrupt:
        pass


def modo_manual():
    """Permite controlar las luces desde el teclado."""
    opciones = {"1": "rojo", "2": "amarillo", "3": "verde"}
    while True:
        limpiar_pantalla()
        print("MODO MANUAL\n")
        print("1. Encender rojo")
        print("2. Encender amarillo")
        print("3. Encender verde")
        print("0. Volver al menú")
        opcion = input("\nSeleccione una luz: ").strip()

        if opcion == "0":
            return
        if opcion in opciones:
            color = opciones[opcion]
            ESTADISTICAS["cambios"] += 1
            dibujar_semaforo(color, modo="MANUAL")
            pausa()
        else:
            print("Opción no válida.")
            time.sleep(1)


def configurar_tiempos():
    """Cambia las duraciones usadas por el modo automático."""
    limpiar_pantalla()
    print("CONFIGURACIÓN DE TIEMPOS\n")
    for color in ("rojo", "verde", "amarillo"):
        actual = DURACIONES[color]
        DURACIONES[color] = pedir_entero(
            f"Duración de {color} (actual: {actual} s): ", 1
        )
    print("\nConfiguración guardada durante esta ejecución.")
    pausa()


def mostrar_estadisticas():
    limpiar_pantalla()
    print("╔═══════════════════════════╗")
    print("║  ESTADÍSTICAS DEL SISTEMA ║")
    print("╠═══════════════════════════╣")
    print(f"║ Ciclos completados: {ESTADISTICAS['ciclos']:<6}║")
    print(f"║ Cambios de estado:  {ESTADISTICAS['cambios']:<6}║")
    print(f"║ Segundos simulados: {ESTADISTICAS['segundos']:<6}║")
    print("╚═══════════════════════════╝")
    pausa()


def mostrar_menu():
    """Muestra el menú principal y devuelve la opción elegida."""
    limpiar_pantalla()
    print("╔════════════════════════════╗")
    print("║ SIMULADOR DE TRÁFICO - BCN ║")
    print("╠════════════════════════════╣")
    print("║ 1. Iniciar modo automático ║")
    print("║ 2. Control manual          ║")
    print("║ 3. Configurar tiempos      ║")
    print("║ 4. Ver estadísticas        ║")
    print("║ 0. Salir                   ║")
    print("╚════════════════════════════╝")
    return input("\nSeleccione una opción: ").strip()


def main():
    acciones = {
        "1": modo_automatico,
        "2": modo_manual,
        "3": configurar_tiempos,
        "4": mostrar_estadisticas,
    }

    while True:
        opcion = mostrar_menu()
        if opcion == "0":
            limpiar_pantalla()
            print("Simulación finalizada. ¡Hasta luego!")
            break
        if opcion in acciones:
            acciones[opcion]()
        else:
            print("Opción no válida.")
            time.sleep(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        limpiar_pantalla()
        print("Simulación finalizada.")
