"""Simulación animada de un semáforo con barra de progreso y peatón."""

import os
import time


ANCHO_BARRA = 30
ANCHO_CALLE = 42

# Color, duración y mensaje de cada fase.
FASES = (
    ("rojo", 6, "ESPERE"),
    ("verde", 12, "PUEDE CRUZAR"),
    ("amarillo", 4, "TERMINE DE CRUZAR"),
)


def limpiar_pantalla():
    """Limpia la consola en Windows, Linux o macOS."""
    os.system("cls" if os.name == "nt" else "clear")


def crear_barra(transcurrido, duracion):
    """Crea una barra de progreso proporcional al tiempo transcurrido."""
    ultimo_paso = max(duracion - 1, 1)
    completado = round(ANCHO_BARRA * transcurrido / ultimo_paso)
    pendiente = ANCHO_BARRA - completado
    porcentaje = round(transcurrido * 100 / ultimo_paso)
    return f"[{'█' * completado}{'░' * pendiente}] {porcentaje:3d}%"


def posicion_peaton(color, transcurrido, duracion):
    """Calcula la posición del peatón según la fase del semáforo."""
    recorrido_maximo = ANCHO_CALLE - 3
    ultimo_paso = max(duracion - 1, 1)

    if color == "rojo":
        return 0
    if color == "verde":
        # Durante el verde recorre el primer 80 % del paso de peatones.
        return round(recorrido_maximo * 0.8 * transcurrido / ultimo_paso)

    # Durante el amarillo completa rápidamente el 20 % restante.
    inicio_amarillo = recorrido_maximo * 0.8
    return round(
        inicio_amarillo
        + recorrido_maximo * 0.2 * transcurrido / ultimo_paso
    )


def dibujar_peaton(posicion, paso):
    """Dibuja un pequeño peatón alternando las piernas al caminar."""
    posicion = min(posicion, ANCHO_CALLE - 3)
    margen = " " * posicion
    piernas = "/ \\" if paso % 2 == 0 else "\\ /"

    print("┌" + "─" * ANCHO_CALLE + "┐")
    print("│" + margen + " O" + " " * (ANCHO_CALLE - posicion - 2) + "│")
    print("│" + margen + "/|\\" + " " * (ANCHO_CALLE - posicion - 3) + "│")
    print("│" + margen + piernas + " " * (ANCHO_CALLE - posicion - 3) + "│")
    print("└" + "─" * ANCHO_CALLE + "┘")
    print(" INICIO" + " " * (ANCHO_CALLE - 11) + "META")


def dibujar_pantalla(color, duracion, transcurrido, mensaje):
    """Muestra el semáforo, la barra y el peatón en la consola."""
    restante = duracion - transcurrido
    luces = {
        "rojo": "🔴" if color == "rojo" else "⚫",
        "amarillo": "🟡" if color == "amarillo" else "⚫",
        "verde": "🟢" if color == "verde" else "⚫",
    }

    print("╔════════════════════════════════════════════╗")
    print("║          SIMULADOR DE SEMÁFORO             ║")
    print("╚════════════════════════════════════════════╝")
    print(f"\n                 {luces['rojo']}")
    print(f"                 {luces['amarillo']}")
    print(f"                 {luces['verde']}")
    print(f"\n{mensaje:^44}")
    print(f"\n{crear_barra(transcurrido, duracion):^44}")
    print(f"Tiempo restante: {restante} segundo{'s' if restante != 1 else ''}\n")

    posicion = posicion_peaton(color, transcurrido, duracion)
    dibujar_peaton(posicion, transcurrido)
    print("\nPulsa Ctrl+C para finalizar.")


def simular_semaforo():
    """Repite indefinidamente todas las fases del semáforo."""
    while True:
        for color, duracion, mensaje in FASES:
            for transcurrido in range(duracion):
                limpiar_pantalla()
                dibujar_pantalla(color, duracion, transcurrido, mensaje)
                time.sleep(1)


if __name__ == "__main__":
    try:
        simular_semaforo()
    except KeyboardInterrupt:
        limpiar_pantalla()
        print("Simulación finalizada.")
        try:
            input("Presione Enter para cerrar...")
        except EOFError:
            pass
