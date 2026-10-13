import subprocess,platform
def limpiar_pantalla(): #Incorporarmos limpiar pantalla en una Funcion().
    if platform.system()=="Windows":subprocess.run(["cls"], shell=True) #shell es necesario en los subprocesos.
    else: subprocess.run(["clear"])

import os
import subprocess
import sys

# Catálogo ampliado con precios y tipos de venta
FRUTAS_DISPONIBLES = {
    'Plátano 🍌': {'tipo': 'peso', 'precio': 1.35},
    'Manzana 🍎': {'tipo': 'peso', 'precio': 0.80},
    'Pera 🍐': {'tipo': 'peso', 'precio': 0.85},
    'Naranja 🍊': {'tipo': 'peso', 'precio': 0.70},
    'Fresa 🍓': {'tipo': 'peso', 'precio': 1.70},
    'Cereza 🍒': {'tipo': 'peso', 'precio': 2.20},
    'Durazno 🍑': {'tipo': 'peso', 'precio': 1.95},
    'Melón 🍈': {'tipo': 'unidad', 'precio_kg': 2.54, 'pesos': [0.850, 1.25, 1.10]},
    'Piña 🍍': {'tipo': 'unidad', 'precio_kg': 1.54, 'pesos': [0.800, 0.750, 1.30]},
    'Sandía 🍉': {'tipo': 'unidad', 'precio_kg': 1.44, 'pesos': [1.80, 1.55, 1.40]},
    'Papaya 🥭': {'tipo': 'unidad', 'precio_kg': 1.64, 'pesos': [0.800, 0.650, 1.04]}
}


def limpiar_pantalla():
    """Limpia la pantalla usando subprocess en lugar de os.system."""
    comando = 'cls' if os.name == 'nt' else 'clear'
    subprocess.run(comando, shell=True)


def formatear_precio(precio: float) -> str:
    """Formatea valores numéricos con coma decimal."""
    return f"{precio:.2f}".replace('.', ',')


def mostrar_menu_frutas(frutas_keys: list):
    """
    Muestra el catálogo de frutas limitando a máximo 4 filas por columna.
    Muestra solo 'Ud' en el tipo de venta por unidad.
    """
    FILAS_MAXIMAS = 4
    total_items = len(frutas_keys)
    
    print("=========================================================================")
    print("-------------------------- Frutas disponibles ---------------------------")

    filas = min(total_items, FILAS_MAXIMAS)

    for f in range(filas):
        linea = ""
        for idx in range(f, total_items, FILAS_MAXIMAS):
            nombre = frutas_keys[idx]
            info = FRUTAS_DISPONIBLES[nombre]
            
            if info['tipo'] == 'peso':
                precio_str = f"{formatear_precio(info['precio'])} €/kg"
            else:
                precio_str = "Por Unidad"

            num_str = f"[{idx + 1}]"
            item_str = f"{num_str:>4} {nombre:<12} {precio_str:<20}"
            linea += f"{item_str:<38}"

        print(linea)

    print("-------------------------------------------------------------------------")


def seleccionar_unidad(nombre_fruta: str, info: dict) -> tuple[float, float] | None:
    """Muestra las opciones disponibles de peso/precio por unidad para una fruta."""
    pesos = info['pesos']
    precio_kg = info['precio_kg']

    print(f"\n--- Unidades disponibles para {nombre_fruta} ---")
    for i, peso in enumerate(pesos, 1):
        precio_total = peso * precio_kg
        print(f"[{i}] Pieza de {formatear_precio(peso)} Kg -> {formatear_precio(precio_total)} €")

    entrada = input("\nSelecciona la opción deseada (o ENTER para cancelar): ").strip()
    if entrada.isdigit():
        op = int(entrada) - 1
        if 0 <= op < len(pesos):
            peso_elegido = pesos[op]
            costo_total = peso_elegido * precio_kg
            return peso_elegido, costo_total

    return None


def solicitar_kilos(nombre_fruta: str) -> float | None:
    """Pide la cantidad de kilos ingresada por el usuario."""
    entrada = input(f'¿Cuántos kilos de {nombre_fruta}? ').strip().replace(',', '.')
    try:
        kilos = float(entrada)
        return kilos if kilos > 0 else None
    except ValueError:
        return None


def proceso_seleccion_productos(frutas_keys: list) -> dict:
    """Bucle principal de selección e interacción para agregar a la cesta."""
    cesta = {}

    while True:
        limpiar_pantalla()
        print("=========================================================================")
        print(f" 🛒 CESTA DE COMPRA: {len(cesta)} producto(s)")
        mostrar_menu_frutas(frutas_keys)

        entrada = input('\nDigite el código de la fruta (o ENTER para finalizar): ').strip()

        if not entrada or entrada == "0":
            break

        if entrada.isdigit():
            indice = int(entrada) - 1
            if 0 <= indice < len(frutas_keys):
                fruta_sel = frutas_keys[indice]
                info = FRUTAS_DISPONIBLES[fruta_sel]

                if info['tipo'] == 'peso':
                    kilos = solicitar_kilos(fruta_sel)
                    if kilos:
                        costo = kilos * info['precio']
                        kg_act, costo_act = cesta.get(fruta_sel, (0.0, 0.0))
                        cesta[fruta_sel] = (kg_act + kilos, costo_act + costo)
                    else:
                        input("Cantidad no válida. Presiona ENTER para continuar...")

                elif info['tipo'] == 'unidad':
                    resultado = seleccionar_unidad(fruta_sel, info)
                    if resultado:
                        peso_sel, costo_sel = resultado
                        kg_act, costo_act = cesta.get(fruta_sel, (0.0, 0.0))
                        cesta[fruta_sel] = (kg_act + peso_sel, costo_act + costo_sel)
                    else:
                        input("Selección no válida. Presiona ENTER para continuar...")
            else:
                input("Código fuera de rango. Presiona ENTER para continuar...")
        else:
            input("Entrada no válida. Presiona ENTER para continuar...")

    return cesta


def mostrar_resumen(cesta: dict) -> float:
    """Muestra el resumen de productos agregados a la cesta."""
    total_acumulado = 0.0

    if not cesta:
        print("No compraste ninguna fruta.")
        return total_acumulado

    for fruta, (kg, costo) in cesta.items():
        total_acumulado += costo
        str_kg = formatear_precio(kg)
        str_costo = formatear_precio(costo)
        print(f"- {fruta:<14} {str_kg:>6} kg -> {str_costo:>6} €")

    print("----------------------------------")
    print(f"TOTAL A PAGAR:          {formatear_precio(total_acumulado):>6} €")
    return total_acumulado


def imprimir_ticket(cesta: dict, total: float):
    """Genera la vista del ticket impreso."""
    limpiar_pantalla()
    print("==================================")
    print("          IMPRIMIENDO...          ")
    print("==================================")
    print("TICKET DE COMPRA")
    print("----------------------------------")

    for fruta, (kg, costo) in cesta.items():
        print(f"{fruta:<14} {formatear_precio(kg):>6} kg   {formatear_precio(costo):>6} €")

    print("----------------------------------")
    print(f"TOTAL:                  {formatear_precio(total):>6} €")
    print("==================================")
    print("¡Gracias por su compra!\n")


def main():
    lista_frutas = list(FRUTAS_DISPONIBLES.keys())

    while True:
        cesta_compra = proceso_seleccion_productos(lista_frutas)

        limpiar_pantalla()
        print("==================================")
        print(f"RESUMEN DE TU COMPRA ({len(cesta_compra)} productos)")
        print("==================================")

        total_pagar = mostrar_resumen(cesta_compra)
        print("==================================")

        print("\n[1] Imprimir ticket")
        print("[2] Limpiar y nueva compra")
        print("[3] Salir")

        opcion = input("\nSelecciona una opción: ").strip()

        if opcion == "1":
            imprimir_ticket(cesta_compra, total_pagar)
            print("[1] Nueva compra")
            print("[2] Salir")
            op_post = input("\nSelecciona una opción: ").strip()
            if op_post != "1":
                break

        elif opcion == "2":
            continue

        elif opcion == "3":
            break

        else:
            input("Opción no válida. Presiona ENTER para continuar...")

    print("\n¡Gracias por su preferencia! Hasta luego.\n")
    sys.exit(0)


if __name__ == "__main__":
    main()