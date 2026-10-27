"""Gustavo Moyano Díaz - Simulación de un semáforo."""

import os
import time


# Orden y duración (en segundos) de cada estado del semáforo.
ESTADOS = (
    ("rojo", 5, "STOP"),
    ("verde", 8, "PUEDE PASAR"),
    ("amarillo", 3, "PRECAUCIÓN"),
)


def limpiar_pantalla():
    """Limpia la consola tanto en Windows como en Linux y macOS."""
    os.system("cls" if os.name == "nt" else "clear")


def dibujar_semaforo(color_activo, segundos, mensaje):
    """Dibuja el semáforo mostrando únicamente la luz activa."""
    luces = {
        "rojo": "🔴" if color_activo == "rojo" else "⚫",
        "amarillo": "🟡" if color_activo == "amarillo" else "⚫",
        "verde": "🟢" if color_activo == "verde" else "⚫",
    }

    print("╔══════════════════════╗")
    print("║       SEMÁFORO       ║")
    print("╠══════════════════════╣")
    print(f"║          {luces['rojo']}          ║")
    print("║                      ║")
    print(f"║          {luces['amarillo']}          ║")
    print("║                      ║")
    print(f"║          {luces['verde']}          ║")
    print("╚══════════════════════╝")
    print(f"\n{mensaje}")
    print(f"Cambio en {segundos} segundo{'s' if segundos != 1 else ''}.")
    print("\nPresione Ctrl+C para detener el semáforo.")


def simular_semaforo():
    """Repite continuamente la secuencia de un semáforo real."""
    while True:
        for color, duracion, mensaje in ESTADOS:
            for segundos in range(duracion, 0, -1):
                limpiar_pantalla()
                dibujar_semaforo(color, segundos, mensaje)
                time.sleep(1)


if __name__ == "__main__":
    try:
        simular_semaforo()
    except KeyboardInterrupt:
        limpiar_pantalla()
        print("Simulación finalizada.")
        input("Presione Enter para cerrar la ventana...")