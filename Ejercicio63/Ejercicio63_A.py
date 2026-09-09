"""Punto de entrada y coordinación de la aplicación Frutería Python."""

import re

import Ejercicio63_A_crud as crud
import Ejercicio63_A_funcionalidades as func
from Ejercicio63_A_constantes import *
from Ejercicio63_A_utilidades import limpiar_pantalla


def main():
    """Coordina el menú principal y delega cada acción en su capa."""
    ancho = 52
    ancho_con_emoji = ancho - 1
    while True:
        limpiar_pantalla()
        print(f"{CIAN}╔{'═' * ancho}╗{RESET}")
        print(f"{CIAN}║{RESET}{NEGRITA}{'🛒 BIENVENIDO A FRUTERÍA PYTHON':^{ancho_con_emoji}}{RESET}{CIAN}║{RESET}")
        print(f"{CIAN}╠{'═' * ancho}╣{RESET}")
        print(f"{CIAN}║{RESET}{'Opción':^9}│{'Acción':^{ancho - 10}}{CIAN}║{RESET}")
        print(f"{CIAN}╠{'─' * 9}┼{'─' * (ancho - 10)}╣{RESET}")
        print(f"{CIAN}║{RESET}{'1':^9}│{' 🥬 Gestión de frutería':<{ancho - 11}}{CIAN}║{RESET}")
        print(f"{CIAN}║{RESET}{'2':^9}│{' 🌐 Compra online':<{ancho - 11}}{CIAN}║{RESET}")
        print(f"{CIAN}║{RESET}{'3':^9}│{' 🏪 Compra en tienda':<{ancho - 11}}{CIAN}║{RESET}")
        print(f"{CIAN}║{RESET}{'0':^9}│{' Salir':<{ancho - 11}}{CIAN}║{RESET}")
        print(f"{CIAN}╚{'═' * ancho}╝{RESET}")
        opcion_inicio = input(f"{CIAN}👉 Elige una opción: {RESET}").strip()

        if opcion_inicio == "0":
            return
        if opcion_inicio in ("2", "3"):
            tipo_compra = "1" if opcion_inicio == "2" else "2"
            break
        if opcion_inicio != "1":
            input(f"{ROJO}⚠️ Escribe una opción válida. Pulsa Enter para continuar.{RESET}")
            continue

        print("\n🥬 GESTIÓN DE FRUTERÍA")
        print("1. Crear fruta")
        print("2. Consultar frutas")
        print("3. Actualizar fruta")
        print("4. Eliminar fruta")
        print("0. Volver")
        operaciones = {
            "1": crud.crear_fruta_tienda,
            "2": crud.consultar_frutas_tienda,
            "3": crud.actualizar_fruta_tienda,
            "4": crud.eliminar_fruta_tienda,
        }
        operacion = input("Elige una operación: ").strip()
        if operacion == "0":
            continue
        try:
            operaciones[operacion]()
        except KeyError:
            print("⚠️ Operación no válida.")
        except NotImplementedError as error:
            print(f"⚠️ {error}")
        input("Pulsa Enter para continuar.")

    print(f"\n{AMARILLO}╔{'═' * ancho}╗{RESET}")
    print(f"{AMARILLO}║{RESET}{NEGRITA}{'💰 PRESUPUESTO':^{ancho_con_emoji}}{RESET}{AMARILLO}║{RESET}")
    print(f"{AMARILLO}╠{'═' * ancho}╣{RESET}")
    print(f"{AMARILLO}║{RESET}{'Puedes establecer un límite máximo para tu pedido.':^{ancho}}{AMARILLO}║{RESET}")
    print(f"{AMARILLO}╚{'═' * ancho}╝{RESET}")
    respuesta = input(f"{AMARILLO}💰 ¿Deseas establecer un presupuesto? (S/N): {RESET}").strip().lower()
    while respuesta not in ("s", "n"):
        respuesta = input(f"{ROJO}⚠️ Escribe S o N: {RESET}").strip().lower()

    presupuesto = None
    if respuesta == "s":
        entrada = input(f"{AMARILLO}💶 Introduce tu presupuesto: {RESET}").strip()
        while not re.fullmatch(PATRON_DECIMAL, entrada) or float(entrada.replace(",", ".")) <= 0:
            entrada = input(f"{ROJO}⚠️ Introduce un importe válido: {RESET}").strip()
        presupuesto = float(entrada.replace(",", "."))
    func.configurar_compra(tipo_compra, presupuesto)

    finalizar = False
    opcion_activa = None
    while not finalizar:
        limpiar_pantalla()
        crud.actualizar_bolsas_automaticas(
            func.carrito,
            func.tipo_compra,
            func.tipo_entrega,
        )
        func.mostrar_catalogo()
        func.mostrar_carrito()
        if opcion_activa is None:
            opcion_activa = func.mostrar_menu_pedido()

        match opcion_activa:
            case "1":
                print(f"{NEGRITA}{VERDE}➕ AGREGAR PRODUCTO{RESET}")
                if func.agregar_producto():
                    opcion_activa = None
            case "2":
                if func.actualizar_producto():
                    opcion_activa = None
            case "3":
                if func.eliminar_producto():
                    opcion_activa = None
            case "4":
                finalizar = func.finalizar_compra()
                opcion_activa = None
            case "5":
                if func.cancelar_compra():
                    return
                opcion_activa = None
            case _:
                input("⚠️ Opción incorrecta. Pulsa Enter para continuar.")
                opcion_activa = None

    respuesta = input("\n🧾 ¿Deseas generar el ticket de compra? (S/N): ").strip().lower()
    while respuesta not in ("s", "n"):
        respuesta = input("⚠️ Escribe S o N: ").strip().lower()
    if respuesta == "s":
        func.mostrar_ticket()
    else:
        print("\n👋 ¡Compra finalizada! Gracias por tu compra.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{INFO} Se ha pulsado Ctrl + C.{RESET}")
        print("👋 Saliendo de Frutería Python...")
    finally:
        print(f"{EXITO} Programa terminado{RESET}")
