# Importa la librería 'platform' para detectar el sistema operativo donde corre el script
import platform
# Importa el módulo de expresiones regulares 're' para extraer patrones y números de textos
import re
# Importa 'subprocess' para ejecutar comandos del sistema operativo (como limpiar pantalla)
import subprocess
# Importa 'time' para pausar la ejecución del programa mediante time.sleep()
import time


# Declaración de la función para limpiar la pantalla según el sistema operativo
def Borro():
    # Comprueba si el sistema operativo actual es Windows
    if platform.system() == "Windows":
        # Ejecuta el comando 'cls' en la consola de Windows
        subprocess.run(["cls"], shell=True)
    # Si no es Windows (por ejemplo, Linux o macOS)
    else:
        # Ejecuta el comando 'clear' en la consola POSIX
        subprocess.run(["clear"])


# --- DATOS Y VARIABLES INICIALES ---
# Diccionario principal que actua como base de datos de productos, con precio y disponibilidad
catalogo = {
    "Mango": {"precio": 2.50, "disponible": True},
    "Maracuyá": {"precio": 3.80, "disponible": True},
    "Papaya": {"precio": 2.10, "disponible": True},
    "Aguacate": {"precio": 4.20, "disponible": True},
    "Pitahaya": {"precio": 5.50, "disponible": True},
    "Carambola": {"precio": 4.00, "disponible": False},
    "Guayaba": {"precio": 3.00, "disponible": False},
}

# Convierte las claves (nombres de frutas) del catálogo en una lista indexable
lista_cat = list(catalogo.keys())
# Lista vacía que almacenará los items añadidos al carrito de compras
cesta = []
# Variable para guardar el presupuesto global ingresado por el usuario (inicializada sin valor)
presupuesto_total = None

# --- BUCLE PRINCIPAL DE SELECCIÓN DE FRUTAS ---
# Inicia un ciclo infinito para el menú interactivo de la tienda
while True:
    # Limpia la pantalla al inicio de cada iteración del menú principal
    Borro()
    # Imprime el borde superior de la interfaz tabular en la consola
    print("╔══════════════════════════════════════════════════════════╗")
    # Imprime el encabezado del menú principal
    print("║                    FRUTERIA TROPICAL                     ║")
    # Imprime una línea divisoria de la caja visual
    print("╠══════════════════════════════════════════════════════════╣")
    

    # Verifica si ya existen productos añadidos en la cesta
    if cesta:
        # Calcula el gasto total acumulado sumando los subtotales de cada item en la cesta
        tot = sum(i["subtotal"] for i in cesta)
        # Calcula el presupuesto restante; si no hay presupuesto definido, asigna 0.0
        restante_actual = (
            (presupuesto_total - tot) if presupuesto_total is not None else 0.0
        )
        # Crea la cadena de texto estructurada para mostrar la barra de estado superior
        txt = f"Cesta: {len(cesta)} prod | Gastado: {tot:.2f}€ | Restante: {restante_actual:.2f}€"
        # Imprime la barra de estado alineada a la izquierda en un ancho fijo de 56 caracteres
        print(f"║ {txt:<56} ║")
        # Imprime una línea de separación en la caja visual
        print("╠══════════════════════════════════════════════════════════╣")

    # Recorre el catálogo usando enumerate para asignar un índice accesible (empezando en 1)
    for i, f in enumerate(lista_cat, 1):
        # Obtiene el precio por kilo de la fruta actual en la iteración
        p = catalogo[f]["precio"]
        # Formatea el precio a 2 decimales si está disponible, o muestra un texto de advertencia
        disp = (
            f"{p:.2f} EUR/kg" if catalogo[f]["disponible"] else "[SIN STOCK]"
        )
        # Construye la fila del producto indicando su opción, nombre y precio/estado
        txt = f" [{i}] {f:<12} ──────────> {disp}"
        # Imprime la fila formateada dentro del cuadro visual
        print(f"║ {txt:<56} ║")

    # Imprime el borde inferior del marco del menú de opciones
    print("╚══════════════════════════════════════════════════════════╝")

    # Pide al usuario que ingrese sus selecciones mediante texto o números
    entrada = input("\n👉 Elige frutas (ej: 1, 3): ").strip()
    # Utiliza expresiones regulares para extraer todos los dígitos del input y los filtra según rango
    nums = [
        int(n)
        for n in re.findall(r"\d+", entrada)
        if 1 <= int(n) <= len(lista_cat)
    ]

    # Si el usuario no ingresó ningún número válido dentro del rango
    if not nums:
        # Pausa la ejecución e informa al usuario del error
        input("\n⚠️  Selección no válida. Presiona ENTER...")
        # Vuelve al inicio del bucle principal
        continue

    # Lista temporal donde se procesarán las frutas validas con stock o sus reemplazos
    frutas_seleccionadas = []
    # Itera sobre cada número de opción válido que fue extraído
    for n in nums:
        # Obtiene el nombre de la fruta seleccionada corrigiendo el índice base 0
        fruta = lista_cat[n - 1]
        # Extrae los datos (precio y stock) de la fruta seleccionada
        info = catalogo[fruta]

        # Limpia la pantalla para mostrar el flujo particular del producto
        Borro()
        # Evalúa si la fruta seleccionada NO tiene disponibilidad en inventario
        if not info["disponible"]:
            # Muestra un aviso de producto sin stock en la consola
            print(f"❌ {fruta.upper()} NO tiene stock en este momento.\n")
            # Presenta la sección de recomendaciones
            print("💡 Opciones disponibles con stock:")

            # Filtra todas las frutas del catálogo que sí estén disponibles
            opciones_stock = [
                f for f in lista_cat if catalogo[f]["disponible"]
            ]
            # Muestra cada una de las alternativas con stock
            for idx, f_disp in enumerate(opciones_stock, 1):
                # Extrae el precio de la opción alternativa
                p_disp = catalogo[f_disp]["precio"]
                # Imprime la fila formateada de la opción disponible
                print(
                    f"   [{idx}] {f_disp:<12} ──────────> {p_disp:.2f} EUR/kg"
                )

            # Imprime la opción para descartar la fruta no disponible
            print("   [0] Saltar esta fruta")
            # Imprime una línea divisoria simple
            print("──────────────────────────────────────────")

            # Solicita la decisión del usuario sobre el sustituto
            eleccion_sust = input(
                "👉 Elige sustituto (1, 2...) o 0 para saltar: "
            ).strip()
            # Extrae los dígitos numéricos ingresados en la selección de sustituto
            nums_sust = [int(x) for x in re.findall(r"\d+", eleccion_sust)]

            # Comprueba si el número ingresado corresponde a una opción de sustituto válida
            if nums_sust and 1 <= nums_sust[0] <= len(opciones_stock):
                # Reemplaza la fruta original por la fruta sustituta seleccionada
                fruta = opciones_stock[nums_sust[0] - 1]
                # Notifica la elección del nuevo producto
                print(f"\n✅ Seleccionado sustituto: {fruta.upper()}")
                # Espera 1 segundo para visualización del mensaje
                time.sleep(1)
                # Agrega la fruta elegida a la lista de frutas a procesar
                frutas_seleccionadas.append(fruta)
            # Si se presionó 0 o una opción inválida
            else:
                # Muestra un aviso de omisión del producto
                print("\n⏭️  Saltando producto...")
                # Espera 1 segundo
                time.sleep(1)
        # Si la fruta seleccionada originalmente SÍ tiene stock
        else:
            # La añade directamente a la lista de frutas a procesar
            frutas_seleccionadas.append(fruta)

    # Verifica si hay frutas seleccionadas y si aún no se ha ingresado un presupuesto global
    if frutas_seleccionadas and presupuesto_total is None:
        # Limpia la pantalla para solicitar datos iniciales de caja
        Borro()
        # Bucle de validación para el monto del presupuesto
        while True:
            # Pide el presupuesto total en texto
            val_raw = input("👉 Presupuesto disponible (€): ").strip().lower()
            # Limpia símbolos y reemplaza comas por puntos para permitir conversión decimal
            val_limpio = re.sub(r"[^\d.]", "", val_raw.replace(",", "."))
            # Intenta la conversión a flotante de forma segura
            try:
                # Convierte la cadena limpia a tipo float
                presupuesto_total = float(val_limpio)
                # Garantiza que el presupuesto sea estrictamente positivo
                if presupuesto_total > 0:
                    # Sale del ciclo si la cifra es válida
                    break
                # Avisa si la cifra ingresada es cero o negativa
                print("⚠️  Ingresa un monto mayor a 0.")
            # Captura el fallo en la conversión numérica
            except ValueError:
                # Notifica que la entrada no es interpretable como número
                print("⚠️  Formato no válido.")

    # --- PROCESAR CANTIDADES PARA CADA FRUTA ---
    # Comprueba si quedaron frutas en la lista de procesamiento activa
    if frutas_seleccionadas:
        # Itera sobre cada fruta confirmada para consultar las cantidades a comprar
        for fruta in frutas_seleccionadas:
            # Recalcula el total consumido por items guardados en la cesta hasta el momento
            gastado_actual = sum(i["subtotal"] for i in cesta)
            # Determina la liquidez o saldo remanente disponible
            restante = presupuesto_total - gastado_actual

            # Comprueba si el usuario se ha quedado sin dinero antes de procesar el item
            if restante <= 0:
                # Limpia la pantalla para la alerta de sobregiro
                Borro()
                # Imprime el marco superior del aviso
                print(
                    "╔══════════════════════════════════════════════════════════╗"
                )
                # Imprime el título del aviso de falta de saldo
                print(
                    "║                  ⚠️  SIN SALDO DISPONIBLE                ║"
                )
                # Imprime la división intermedia
                print(
                    "╠══════════════════════════════════════════════════════════╣"
                )
                # Construye el mensaje personalizado sobre la fruta que no se puede costear
                txt_err = f"No tienes dinero para añadir: {fruta}"
                # Imprime el texto ajustado al marco
                print(f"║ {txt_err:<56} ║")
                # Imprime la base del cuadro
                print(
                    "╚══════════════════════════════════════════════════════════╝"
                )

                # Si ya hay elementos previos en la cesta, ofrece opciones de rescate/gestión
                if cesta:
                    # Imprime menú emergente de opciones de ajuste
                    print("\n💡 ¿Qué quieres hacer?")
                    print("   [1] Reajustar cantidades de tu cesta actual")
                    print("   [2] Continuar sin añadir esta fruta")
                    # Captura la opción elegida por el usuario
                    op_ajuste = input("\n👉 Elige opción (1 o 2): ").strip()

                    # Si el usuario decide reajustar los productos ya guardados en su cesta
                    if op_ajuste == "1":
                        # Bucle de reajuste de la cesta actual
                        while True:
                            # Limpia la pantalla para presentar el panel de edición
                            Borro()
                            # Recalcula lo gastado en la cesta activa
                            gastado = sum(i["subtotal"] for i in cesta)
                            # Recalcula el dinero restante disponible
                            restante = presupuesto_total - gastado

                            # Muestra cabecera del módulo de edición de productos
                            print(
                                "╔══════════════════════════════════════════════════════════╗"
                            )
                            print(
                                "║               REAJUSTAR / MODIFICAR CESTA                ║"
                            )
                            print(
                                "╠══════════════════════════════════════════════════════════╣"
                            )
                            # Imprime el desglose del saldo actual
                            txt_bal = f"Presupuesto: {presupuesto_total:.2f}€ | Restante: {restante:.2f}€"
                            print(f"║ {txt_bal:<56} ║")
                            print(
                                "╠──────────────────────────────────────────────────────────╣"
                            )

                            # Recorre e imprime los elementos que están dentro de la cesta
                            for idx, item in enumerate(cesta, 1):
                                # Formatea la línea de detalle de cada producto en la cesta
                                txt_item = f"[{idx}] {item['fruta']:<10} -> {item['kg']:.3f} kg | {item['subtotal']:.2f} EUR"
                                print(f"║  {txt_item:<55} ║")

                            # Imprime el cierre del cuadro interactivo
                            print(
                                "╚══════════════════════════════════════════════════════════╝"
                            )

                            # Pide al usuario el índice del producto a modificar o '0' para salir
                            op = input(
                                "\n👉 Modificar número de fruta (0 para salir): "
                            ).strip()
                            # Evalúa si la entrada es cero o una opción no válida para romper el bucle
                            if op == "0" or not op.isdigit():
                                break

                            # Convierte la selección a índice de base 0
                            idx_mod = int(op) - 1
                            # Verifica si el número seleccionado existe dentro de la lista 'cesta'
                            if 0 <= idx_mod < len(cesta):
                                # Obtiene la referencia del elemento a modificar
                                item = cesta[idx_mod]
                                # Muestra la fruta que se va a editar
                                print(
                                    f"\n🍊 Modificando: {item['fruta'].upper()} ({item['precio']:.2f}€/kg)"
                                )
                                # Submenú de operaciones sobre la fruta elegida
                                print("   [1] Cambiar cantidad")
                                print("   [2] Eliminar de la cesta")

                                # Captura la decisión sobre el item seleccionado
                                sub_op = input("👉 Elige opción (1 o 2): ").strip()
                                # Si la opción es '2', elimina el elemento de la cesta
                                if sub_op == "2":
                                    # Remueve el objeto usando pop y recupera la entidad eliminada
                                    eliminado = cesta.pop(idx_mod)
                                    # Notifica la eliminación
                                    print(
                                        f"✅ Se ha eliminado {eliminado['fruta']}."
                                    )
                                    # Pausa breve para lectura
                                    time.sleep(1.2)
                                # Si la opción es '1', permite cambiar peso o presupuesto asignado
                                elif sub_op == "1":
                                    # Suma el valor original del item al restante libre para recalcular límites
                                    saldo_item = restante + item["subtotal"]
                                    # Calcula la cantidad máxima en kg posible con el saldo disponible para este item
                                    max_kg = saldo_item / item["precio"]

                                    # Muestra al usuario su cupo financiero para esta fruta
                                    print(
                                        f"\n💰 Disponible: {saldo_item:.2f}€ (máx: {max_kg:.3f}kg)"
                                    )
                                    # Selecciona la unidad de medida para el cálculo
                                    modo_mod = input(
                                        "👉 Calcular por [1] Kg o [2] Euros?: "
                                    ).strip()

                                    # Bucle para validar la nueva cifra elegida
                                    while True:
                                        # Establece la etiqueta visual según la elección previa
                                        lbl = (
                                            "Kilos"
                                            if modo_mod == "1"
                                            else "Euros"
                                        )
                                        # Pide el valor numérico al usuario
                                        val_raw = input(
                                            f"👉 Nuevos {lbl}: "
                                        ).strip()
                                        # Elimina caracteres extraños y unifica comas decimales
                                        val_limpio = re.sub(
                                            r"[^\d.]",
                                            "",
                                            val_raw.replace(",", "."),
                                        )

                                        # Conversión y validación de la nueva cantidad
                                        try:
                                            # Convierte el valor limpio a float
                                            num_val = float(val_limpio)
                                            # Evalúa que sea una cantidad positiva
                                            if num_val <= 0:
                                                print(
                                                    "⚠️  Ingresa un valor mayor a 0."
                                                )
                                                continue

                                            # Si eligió ingresar Kilogramos
                                            if modo_mod == "1":
                                                nuevos_kg = num_val
                                                # Recalcula el subtotal en euros
                                                nuevo_subtotal = (
                                                    nuevos_kg * item["precio"]
                                                )
                                            # Si eligió ingresar Euros
                                            else:
                                                nuevo_subtotal = num_val
                                                # Recalcula los kilogramos resultantes
                                                nuevos_kg = (
                                                    nuevo_subtotal
                                                    / item["precio"]
                                                )

                                            # Verifica si el costo recalculado excede el saldo tope
                                            if nuevo_subtotal > saldo_item:
                                                print(
                                                    f"⚠️  Supera el saldo disponible ({saldo_item:.2f}€)."
                                                )
                                                continue

                                            # Asigna las nuevas propiedades calculadas al diccionario del item
                                            item["kg"] = nuevos_kg
                                            item["subtotal"] = nuevo_subtotal
                                            # Imprime la actualización satisfactoria
                                            print(
                                                f"✅ Actualizado: {nuevos_kg:.3f}kg de {item['fruta']} ({nuevo_subtotal:.2f}€)"
                                            )
                                            # Pausa de confirmación
                                            time.sleep(1.2)
                                            # Rompe el bucle de solicitud de la cifra
                                            break
                                        # Captura entradas inválidas (textos no numéricos)
                                        except ValueError:
                                            print("⚠️  Valor no válido.")

                        # Recalcula el saldo restante tras todo el bucle de reajuste
                        gastado_actual = sum(i["subtotal"] for i in cesta)
                        restante = presupuesto_total - gastado_actual
                        # Si aun después de editar la cesta no hay dinero suficiente, omite la fruta actual
                        if restante <= 0:
                            print("\n⚠️ Sigues sin saldo. Saltando producto...")
                            input("Presiona ENTER para continuar...")
                            break
                    # Si eligió la opción "2" (continuar sin añadir esta fruta)
                    else:
                        break
                # Si la cesta está completamente vacía y no hay saldo suficiente
                else:
                    input("\nPresiona ENTER para continuar...")
                    break

            # Determina el precio por unidad del producto a procesar
            precio = catalogo[fruta]["precio"]
            # Calcula los kilogramos máximos que el usuario se puede permitir con el dinero restante
            max_kg = restante / precio

            # Limpia pantalla para solicitar la cantidad del producto actual
            Borro()
            # Muestra el nombre de la fruta, precio unitario y saldo máximo en euros/kg
            print(
                f"🍊 {fruta.upper()} | {precio:.2f}€/kg | Saldo restante: {restante:.2f}€ (máx: {max_kg:.3f}kg)"
            )

            # Solicita si se especificará el pedido en kilogramos o en dinero
            modo = input("👉 ¿Calcular por [1] Kg o [2] Euros?: ").strip()
            # Bucle de validación para garantizar que se elija '1' o '2'
            while modo not in ["1", "2"]:
                modo = input("👉 Opción no válida. [1] Kg o [2] Euros: ").strip()

            # Bucle para pedir la cantidad numérica de la fruta
            while True:
                # Define la etiqueta según el modo elegido
                lbl = "Kilos" if modo == "1" else "Euros"
                # Lee la entrada del usuario para la cantidad
                val_raw = input(f"👉 Cantidad en {lbl}: ").strip()
                # Limpia caracteres extraños y homogeniza separador decimal
                val_limpio = re.sub(r"[^\d.]", "", val_raw.replace(",", "."))

                # Conversión y comprobación de límites financieros
                try:
                    # Convierte a entero/flotante de tipo float
                    num_val = float(val_limpio)
                    # Exige una cantidad positiva
                    if num_val <= 0:
                        print("⚠️  Ingresa un valor mayor a 0.")
                        continue

                    # Si fue por kilogramos, calcula costo total
                    if modo == "1":
                        kg = num_val
                        subtotal = kg * precio
                    # Si fue por importe en euros, calcula el volumen equivalente en kg
                    else:
                        subtotal = num_val
                        kg = subtotal / precio

                    # Valida que el dinero requerido no supere el saldo disponible en la sesión
                    if subtotal > restante:
                        print(
                            f"⚠️  Supera tu saldo disponible ({restante:.2f}€)."
                        )
                        time.sleep(1.5)
                        continue

                    # Añade la fruta con todas sus métricas calculadas a la lista cesta
                    cesta.append(
                        {
                            "fruta": fruta,
                            "kg": kg,
                            "precio": precio,
                            "subtotal": subtotal,
                        }
                    )
                    # Notifica el éxito del guardado en el carrito
                    print(
                        f"✅ Añadido: {kg:.3f}kg de {fruta} ({subtotal:.2f}€)"
                    )
                    # Pausa breve de 1 segundo
                    time.sleep(1)
                    # Sale del ciclo para pedir datos de esta fruta
                    break
                # Captura de error de parseo flotante
                except ValueError:
                    print("⚠️  Valor no válido.")

    # Limpia la pantalla al finalizar la inclusión de un bloque de productos
    Borro()
    # Pregunta si desea proceder al cierre de la compra o continuar navegando
    print("🛒 ¿Has terminado tu compra?")
    print(" [1] Sí, ir a pagar / envío")
    print(" [2] No, añadir más productos")
    # Si selecciona "1", rompe el bucle principal finalizando la selección
    if input("\n👉 Elige opción (1 o 2): ").strip() == "1":
        break

# --- SELECCIÓN DE ENVÍO ---
# Inicializa el costo del envío en 0.0
envio = 0.0
# Establece la descripción por defecto del método de entrega
metodo = "Recogida en tienda"

# Comprueba si la cesta contiene productos para seleccionar métodos de despacho
def metodo_de_entrega():
    # Limpia la pantalla para mostrar opciones de logística
    Borro()
    # Imprime cabecera del cuadro de logística
    print("╔══════════════════════════════════════════════════════════╗")
    print("║                    METODO DE ENTREGA                     ║")
    print("╠══════════════════════════════════════════════════════════╣")
    print("║  [1] Recogida en tienda  ──────────> Gratis (0.00 EUR)   ║")
    print("║  [2] Envío a domicilio   ──────────> 4.50 EUR            ║")
    print("╚══════════════════════════════════════════════════════════╝")

    # Si se selecciona "2", ajusta el valor del flete y actualiza el tipo de método
    if input("\n👉 Elige opción (1 o 2): ").strip() == "2":
        envio = 4.50
        metodo = "Envío a domicilio"
    return envio,metodo

if cesta:
    envio, metodo = metodo_de_entrega()

# --- GENERACIÓN DEL TICKET FINAL CORREGIDO Y ALINEADO ---
# Limpia la consola antes de imprimir la factura/ticket final
Borro()
# Solo se genera la representación visual si hay items en la cesta
if cesta:
    # Imprime la sección superior de la representación del ticket
    print("╔══════════════════════════════════════════════════════════╗")
    print("║                     TICKET DE COMPRA                     ║")
    print("╠══════════════════════════════════════════════════════════╣")
    # Imprime la cabecera con nombres de columna
    print("║ Producto     │    Kilos │ Precio/kg │           Subtotal ║")
    print("╠──────────────┼──────────┼───────────┼────────────────────╣")

    # Variable acumuladora para la suma directa de los subtotales de fruta
    subtotal_frutas = 0.0
    # Itera por cada diccionario de item almacenado en la cesta
    for i in cesta:
        # Recupera el nombre de la fruta
        nom = i["fruta"]
        # Formatea los kilogramos en texto con 3 posiciones decimales
        kg_str = f"{i['kg']:.3f} kg"
        # Formatea el precio unitario en texto a 2 posiciones decimales
        pr_str = f"{i['precio']:.2f} EUR"
        # Formatea el subtotal parcial a 2 decimales
        sub_str = f"{i['subtotal']:.2f} EUR"

        # Imprime la fila del producto alineando cada valor mediante formateo de ancho fijo
        # nom:<12 (alineado a izquierda, 12 pos), kg_str:>8 (derecha, 8 pos), etc.
        print(f"║ {nom:<12} │ {kg_str:>8} │ {pr_str:>9} │ {sub_str:>18} ║")
        # Suma el valor parcial al acumulador global del ticket
        subtotal_frutas += i["subtotal"]

    # Imprime la separación visual previa a las secciones de totales
    print("╠──────────────┴──────────┴───────────┴────────────────────╣")
    # Imprime la suma acumulada de las frutas
    print(f"║ {'Subtotal Frutas: ' + f'{subtotal_frutas:.2f} EUR':<56} ║")
    # Imprime el método de envío elegido y su valor de costo
    print(f"║ {f'Entrega ({metodo}): ' + f'{envio:.2f} EUR':<56} ║")

    # Suma el total neto a pagar (frutas + logística)
    total = subtotal_frutas + envio
    print("╠──────────────────────────────────────────────────────────╣")
    # Muestra el total neto alineado dentro del recuadro
    print(f"║ {'TOTAL A PAGAR: ' + f'{total:.2f} EUR':<56} ║")

    # Evalúa si se había establecido un presupuesto inicial para calcular la devuelta
    if presupuesto_total is not None:
        # Calcula la diferencia (devuelta o saldo sobrante del cliente)
        cambio = presupuesto_total - total
        # Imprime el cambio restante formateado a 2 decimales
        print(
            f"║ {'Cambio / Saldo restante: ' + f'{cambio:.2f} EUR':<56} ║"
        )

    # Imprime la línea de cierre inferior del marco del ticket
    print("╚══════════════════════════════════════════════════════════╝")
    # Mensaje de agradecimiento al cliente al terminar la ejecución
    print("\n¡Gracias por tu compra en Frutería Tropical!")
# Si la cesta quedó totalmente vacía tras el flujo
else:
    # Notifica que no se ejecutó transacción alguna por falta de items
    print("🛒 No has añadido productos a la cesta.")