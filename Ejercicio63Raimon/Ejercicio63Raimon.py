import sys
from datetime import datetime
from pathlib import Path

if __package__ in (None, ""):
    carpeta_paquete = Path(__file__).resolve().parent
    sys.path[:] = [
        ruta for ruta in sys.path
        if Path(ruta or ".").resolve() != carpeta_paquete
    ]
    sys.path.insert(0, str(carpeta_paquete.parent))
    __package__ = "Ejercicio63Raimon"

from . import Ejercicio63RaimonConstantes as const
from . import Ejercicio63RaimonUtilidades as util
from . import Ejercicio63RaimonFuncionalidades as func
from . import Ejercicio63RaimonCRUD as crud


# Las funciones del flujo se toman de sus módulos responsables.
agregar_producto = crud.agregar_producto
mostrar_cesta = func.mostrar_cesta
procesar_comando_global = crud.procesar_comando_global
mostrar_ticket = func.mostrar_ticket
procesar_pago = func.procesar_pago
crear_pdf = func.crear_pdf


def ejecutar_tpv():
    try:
        while True:
            cesta = {}

            while True:
                util.limpiar_pantalla()
                mostrar_cesta(cesta)

                fruta = input("¿Qué fruta quieres?: ").strip()
                accion = procesar_comando_global(fruta, cesta)

                if accion in ("CANCELAR", "CONTINUAR"):
                    continue
                if accion == "TICKET":
                    break

                if not agregar_producto(cesta, fruta):
                    continue

            id_ticket = datetime.now().strftime("%Y%m%d_%H%M%S")
            total_a_pagar = sum(
                item["total"]
                for item in cesta.values()
            )

            mostrar_ticket(cesta, id_ticket)
            metodo_pago, entrega, cambio = procesar_pago(total_a_pagar)
            crear_pdf(cesta, id_ticket, entrega, cambio, metodo_pago)

            prompt = (
                f"\n{const.AMARILLO}{const.BOLD}[/]{const.RESET} Nuevo pedido  | "
                f"{const.ROJO}{const.BOLD}[Ctrl+C]{const.RESET} Salir > "
            )
            if input(prompt) != "/":
                continue

    except KeyboardInterrupt:
        pass

    print("\n\n¡Hasta pronto! 👋\n")
    sys.exit(0)


if __name__ == "__main__":
    ejecutar_tpv()
