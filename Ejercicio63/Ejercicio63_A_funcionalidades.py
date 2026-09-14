import re
import unicodedata
from datetime import datetime

from Ejercicio63_A_bdd import FRUTAS_DISPONIBLES
from Ejercicio63_A_constantes import *
import Ejercicio63_A_crud as crud
import Ejercicio63_A_reglas as func
from Ejercicio63_A_utilidades import (
    formatear_linea,
    limpiar_pantalla,
)

carrito={}
presupuesto=None
tipo_compra=None
tipo_entrega=None
tipo_pago=None
efectivo_entregado=None


def configurar_compra(modalidad, limite_presupuesto):
    """Inicializa los datos de sesión que utilizan las funcionalidades."""
    global presupuesto, tipo_compra, tipo_entrega, tipo_pago, efectivo_entregado
    tipo_compra = modalidad
    presupuesto = limite_presupuesto
    tipo_entrega = None
    tipo_pago = None
    efectivo_entregado = None

def mostrar_menu_pedido():
    '''des: Cris | Muestra el menú principal y devuelve la opción seleccionada.'''
    ancho=58
    ancho_con_emoji=ancho-1
    print(f"\n{CIAN}╔{'═'*ancho}╗{RESET}")
    print(f"{CIAN}║{RESET}{NEGRITA}{'📋 GESTIÓN DEL PEDIDO':^{ancho_con_emoji}}{RESET}{CIAN}║{RESET}")
    print(f"{CIAN}╠{'═'*ancho}╣{RESET}")
    opciones=(
        ("1","➕ Agregar producto",VERDE),
        ("2","🔧 Actualizar producto",AMARILLO),
        ("3","❌ Eliminar producto",ROJO),
        ("4","✅ Finalizar compra",VERDE),
        ("5","⛔ Cancelar compra",ROJO),
    )
    for numero,texto,color in opciones:
        linea=f" {numero}. {texto}"
        print(f"{CIAN}║{RESET}{color}{linea:<{ancho_con_emoji}}{RESET}{CIAN}║{RESET}")
    print(f"{CIAN}╟{'─'*ancho}╢{RESET}")
    print(f"{CIAN}║{RESET}{'👉 Selecciona una opción del 1 al 5':<{ancho_con_emoji}}{CIAN}║{RESET}")
    print(f"{CIAN}╚{'═'*ancho}╝{RESET}")
    return input(f"{CIAN}👉 Elige una opción: {RESET}").strip()

def mostrar_catalogo():
    '''des: Cris | Muestra el catálogo con precio, stock y estado de cada fruta.'''
    ancho=54
    print(f"\n{CIAN}╔{'═'*ancho}╗{RESET}")
    print(f"{CIAN}║{RESET}{NEGRITA}{'FRUTAS DISPONIBLES':^{ancho}}{RESET}{CIAN}║{RESET}")
    print(f"{CIAN}╠{'═'*ancho}╣{RESET}")
    encabezado=f"{'Cód.':^6}│{'Fruta':^15}│{'€/kg':^9}│{'Stock':^10}│{'Estado':^10}"
    print(f"{CIAN}║{RESET}{encabezado}{CIAN}║{RESET}")
    print(f"{CIAN}╠{'─'*ancho}╣{RESET}")
    for nombre,datos in FRUTAS_DISPONIBLES.items():
        if datos["tipo"]=="peso":
            disponible=datos["stock"]
            texto_disponible=f"{disponible:.2f} kg"
        else:
            disponible=len(datos["pesos"])
            texto_disponible=f"{disponible} un."
        if disponible<=0:
            estado="❌"
        elif disponible<=STOCK_BAJO:
            estado="🟡 Bajo"
        else:
            estado="✅"
        nombre_formateado=formatear_linea(nombre,15)
        fila=f"{datos['codigo']:^6}│{nombre_formateado}│ {datos['precio_kg']:>6.2f} €│{texto_disponible:>10}│{estado:<9}"
        print(f"{CIAN}║{RESET}{fila}{CIAN}║{RESET}")
    print(f"{CIAN}╚{'═'*ancho}╝{RESET}")

def mostrar_carrito():
    '''des: Cris | Muestra los productos del carrito, subtotales, envío y total.'''
    ancho=62
    subtotal=sum(datos["subtotal"] for datos in carrito.values())
    envio=COSTE_ENVIO_DOMICILIO if tipo_compra=="1" and tipo_entrega=="2" else 0.0
    total=round(subtotal+envio,2)
    print(f"\n{CIAN}╔{'═'*ancho}╗{RESET}")
    print(f"{CIAN}║{RESET}{NEGRITA}{'CARRITO DE COMPRA':^{ancho}}{RESET}{CIAN}║{RESET}")
    if presupuesto is not None:
        restante=presupuesto-total
        resumen=f"Total actual: {total:.2f} € | Resta: {restante:.2f} €"
        print(f"{CIAN}║{RESET}{resumen:^{ancho}}{CIAN}║{RESET}")
    print(f"{CIAN}╠{'═'*ancho}╣{RESET}")
    encabezado=f"{'Cód.':^6}│{'Producto':^18}│{'Cant.':^8}│{'Precio':^9}│{'Ud.':^6}│{'Subtotal':^10}"
    print(f"{CIAN}║{RESET}{encabezado}{CIAN}║{RESET}")
    print(f"{CIAN}╠{'─'*ancho}╣{RESET}")
    if not carrito:
        print(f"{CIAN}║{RESET}{'El carrito está vacío.':^{ancho}}{CIAN}║{RESET}")
        print(f"{CIAN}╚{'═'*ancho}╝{RESET}")
        return
    for nombre,datos in carrito.items():
        cantidad=f"{datos['cantidad']}" if datos["tipo"] in("unidad","bolsa") else f"{datos['cantidad']:.3f}"
        nombre_formateado=formatear_linea(nombre,18)
        fila=f"{datos['codigo']:^6}│{nombre_formateado}│{cantidad:>8}│ {datos['precio']:>6.2f} €│{datos['unidad']:^6}│ {datos['subtotal']:>7.2f} €"
        print(f"{CIAN}║{RESET}{fila}{CIAN}║{RESET}")
    print(f"{CIAN}╟{'─'*ancho}╢{RESET}")
    print(f"{CIAN}║{RESET}{f'Subtotal: {subtotal:.2f} €':>{ancho}}{CIAN}║{RESET}")
    if envio>0:
        print(f"{CIAN}║{RESET}{f'Envío: {envio:.2f} €':>{ancho}}{CIAN}║{RESET}")
    elif tipo_compra=="1" and tipo_entrega=="1":
        print(f"{CIAN}║{RESET}{'Recogida: 0.00 €':>{ancho}}{CIAN}║{RESET}")
    print(f"{CIAN}║{RESET}{NEGRITA}{f'TOTAL: {total:.2f} €':>{ancho}}{RESET}{CIAN}║{RESET}")
    print(f"{CIAN}╚{'═'*ancho}╝{RESET}")

def buscar_fruta():
    '''des: Cris | Valida el tipo de búsqueda que utilizará la función que la llama.'''
    ancho=48
    ancho_con_emoji=ancho-1
    print(f"\n{CIAN}╔{'═'*ancho}╗{RESET}")
    print(f"{CIAN}║{RESET}{NEGRITA}{'🔎 BUSCAR PRODUCTO':^{ancho_con_emoji}}{RESET}{CIAN}║{RESET}")
    print(f"{CIAN}╠{'═'*ancho}╣{RESET}")
    print(f"{CIAN}║{RESET}{'Opción':^9}│{'Acción':^{ancho-10}}{CIAN}║{RESET}")
    print(f"{CIAN}╠{'─'*9}┼{'─'*(ancho-10)}╣{RESET}")
    print(f"{CIAN}║{RESET}{'1':^9}│{' Buscar por código':<{ancho-10}}{CIAN}║{RESET}")
    print(f"{CIAN}║{RESET}{'2':^9}│{' Buscar por nombre':<{ancho-10}}{CIAN}║{RESET}")
    print(f"{CIAN}║{RESET}{'0':^9}│{' Regresar al menú principal':<{ancho-10}}{CIAN}║{RESET}")
    print(f"{CIAN}╚{'═'*ancho}╝{RESET}")
    opcion=input(f"{CIAN}👉 Elige una opción: {RESET}").strip()
    while opcion not in("0","1","2"):
        opcion=input("⚠️ Escribe 1, 2 o 0: ").strip()
    if opcion=="0":
        return VOLVER_MENU
    return opcion

def buscar_por_codigo():
    '''des: Lindey | Busca y devuelve una fruta usando el código introducido por el usuario.'''
    ancho=48
    ancho_con_emoji=ancho-1
    limpiar_pantalla()
    mostrar_catalogo()
    mostrar_carrito()
    print(f"\n{CIAN}╔{'═'*ancho}╗{RESET}")
    print(f"{CIAN}║{RESET}{NEGRITA}{'🔢 BÚSQUEDA POR CÓDIGO':^{ancho_con_emoji}}{RESET}{CIAN}║{RESET}")
    print(f"{CIAN}║{RESET}{'Escribe 0 para regresar al menú principal.':^{ancho}}{CIAN}║{RESET}")
    print(f"{CIAN}╚{'═'*ancho}╝{RESET}")
    codigo=input(f"{CIAN}🔢 Código del producto: {RESET}").strip()
    if codigo=="0":
        return VOLVER_MENU
    codigo_normalizado=codigo.zfill(2) if codigo.isdigit() else codigo
    for nombre,datos in FRUTAS_DISPONIBLES.items():
        if datos["codigo"]==codigo_normalizado:
            return nombre
    print("⚠️ Código inexistente.")
    input("Pulsa Enter para continuar.")
    return None

def buscar_por_nombre():
    '''des: Gustavo | Busca y devuelve una fruta usando el nombre introducido por el usuario.'''
    ancho=48
    ancho_con_emoji=ancho-1
    limpiar_pantalla()
    mostrar_catalogo()
    mostrar_carrito()
    print(f"\n{CIAN}╔{'═'*ancho}╗{RESET}")
    print(f"{CIAN}║{RESET}{NEGRITA}{'🔤 BÚSQUEDA POR NOMBRE':^{ancho_con_emoji}}{RESET}{CIAN}║{RESET}")
    print(f"{CIAN}║{RESET}{'Escribe 0 para regresar al menú principal.':^{ancho}}{CIAN}║{RESET}")
    print(f"{CIAN}╚{'═'*ancho}╝{RESET}")
    texto=input(f"{CIAN}🔤 Nombre de la fruta: {RESET}").strip()
    if texto=="0":
        return VOLVER_MENU
    buscado=unicodedata.normalize("NFD",texto.casefold())
    buscado="".join(c for c in buscado if unicodedata.category(c)!="Mn")
    coincidencias=[]
    for nombre in FRUTAS_DISPONIBLES:
        nombre_normalizado=unicodedata.normalize("NFD",nombre.casefold())
        nombre_normalizado="".join(c for c in nombre_normalizado if unicodedata.category(c)!="Mn")
        nombre_sin_emoji="".join(c for c in nombre_normalizado if c.isalnum() or c.isspace()).strip()
        if buscado==nombre_sin_emoji:
            return nombre
        if buscado in nombre_sin_emoji:
            coincidencias.append(nombre)
    if len(coincidencias)==1:
        sugerencia=coincidencias[0]
        respuesta=input(f"{INFO} ¿Te refieres a {sugerencia}? (S/N): {RESET}").strip().lower()
        while respuesta not in("s","n"):
            respuesta=input(f"{ADVERTENCIA} Escribe S o N: {RESET}").strip().lower()
        if respuesta=="s":
            return sugerencia
        print("↩️ Búsqueda cancelada.")
        input("Pulsa Enter para continuar.")
        return None
    if len(coincidencias)>1:
        print("\nCoincidencias:")
        for i,nombre in enumerate(coincidencias,1):
            print(f"{i}. {nombre}")
        while True:
            opcion=input("Selecciona una opción (0 regresar al menú principal): ").strip()
            if opcion=="0":
                return VOLVER_MENU
            if opcion.isdigit() and 1<=int(opcion)<=len(coincidencias):
                return coincidencias[int(opcion)-1]
            print("⚠️ Selecciona una opción válida.")
    print("⚠️ No encuentro esa fruta.")
    input("Pulsa Enter para continuar.")
    return None

# des: Oksana | Solicita un producto vendido por peso o importe.
def seleccionar_por_peso(nombre):
    '''Permite seleccionar un producto vendido por peso o por importe.'''
    datos=FRUTAS_DISPONIBLES[nombre]
    if datos["stock"]<=0:
        print("❌ Producto agotado.")
        return None
    ancho=54
    ancho_con_emoji=ancho-1
    titulo=f"⚖️ {nombre} · VENTA POR PESO"
    print(f"\n{AMARILLO}╔{'═'*ancho}╗{RESET}")
    print(f"{AMARILLO}║{RESET}{NEGRITA}{titulo:^{ancho_con_emoji + 1}}{RESET}{AMARILLO}║{RESET}")
    print(f"{AMARILLO}╠{'═'*ancho}╣{RESET}")
    precio=f"{datos['precio_kg']:.2f} €/kg"
    disponible=f"{datos['stock']:.2f} kg"
    print(f"{AMARILLO}║{RESET}{' Precio':<18}│{precio:>{ancho-19}}{AMARILLO}║{RESET}")
    print(f"{AMARILLO}║{RESET}{' Disponible':<18}│{disponible:>{ancho-19}}{AMARILLO}║{RESET}")
    print(f"{AMARILLO}╠{'─'*ancho}╣{RESET}")
    print(f"{AMARILLO}║{RESET}{'Opción':^9}│{'Acción':^{ancho-10}}{AMARILLO}║{RESET}")
    print(f"{AMARILLO}╠{'─'*9}┼{'─'*(ancho-10)}╣{RESET}")
    print(f"{AMARILLO}║{RESET}{'1':^9}│{' Introducir kilos':<{ancho-10}}{AMARILLO}║{RESET}")
    print(f"{AMARILLO}║{RESET}{'2':^9}│{' Introducir importe en euros':<{ancho-10}}{AMARILLO}║{RESET}")
    print(f"{AMARILLO}║{RESET}{'0':^9}│{' Regresar al menú principal':<{ancho-10}}{AMARILLO}║{RESET}")
    print(f"{AMARILLO}╚{'═'*ancho}╝{RESET}")
    opcion=input(f"{AMARILLO}👉 Elige una opción: {RESET}").strip()
    while opcion not in("0","1","2"):
        opcion=input("⚠️ Escribe 1, 2 o 0: ").strip()
    if opcion=="0":
        return VOLVER_MENU
    while True:
        if opcion=="1":
            entrada=input("¿Cuántos kilos deseas? (0 regresar al menú principal): ").strip()
            if entrada=="0":
                return VOLVER_MENU
            if not re.fullmatch(PATRON_DECIMAL,entrada):
                print("⚠️ Introduce una cantidad válida.")
                continue
            cantidad=float(entrada.replace(",","."))
            subtotal=round(cantidad*datos["precio_kg"],2)
        else:
            entrada=input("¿Cuántos euros deseas gastar? (0 regresar al menú principal): ").strip()
            if entrada=="0":
                return VOLVER_MENU
            if not re.fullmatch(PATRON_DECIMAL,entrada):
                print("⚠️ Introduce un importe válido.")
                continue
            importe=float(entrada.replace(",","."))
            cantidad=round(importe/datos["precio_kg"],3)
            subtotal=round(cantidad*datos["precio_kg"],2)
        if cantidad<=0:
            print("⚠️ La cantidad debe ser mayor que cero.")
            continue
        if cantidad>datos["stock"]:
            maximo=datos["stock"]*datos["precio_kg"]
            print(f"⚠️ Solo quedan {datos['stock']:.2f} kg. Importe máximo: {maximo:.2f} €")
            continue
        return {"codigo":datos["codigo"],"tipo":"peso","cantidad":cantidad,"peso":cantidad,"precio":datos["precio_kg"],"unidad":"kg.","subtotal":subtotal}

# des: Lindey | Permite seleccionar piezas individuales de una fruta.
def seleccionar_por_unidad(nombre):
    '''Permite seleccionar piezas individuales de un producto.'''
    datos=FRUTAS_DISPONIBLES[nombre]
    if not datos["pesos"]:
        print("❌ Producto agotado.")
        return None
    seleccionados=[]
    while True:
        print(f"\n📦 UNIDADES DISPONIBLES DE {nombre}")
        print("-"*55)
        for i,peso in enumerate(datos["pesos"],1):
            if i-1 in seleccionados:
                estado="✅ Seleccionada"
            else:
                estado=f"{peso:.3f} kg -> {peso*datos['precio_kg']:.2f} €"
            print(f"[{i}] {estado}")
        print("-"*55)
        print("S. Confirmar selección")
        print("0. Regresar al menú principal")
        entrada=input("Selecciona una pieza: ").strip().lower()
        if entrada=="0":
            return VOLVER_MENU
        if entrada=="s":
            if seleccionados:
                break
            print("⚠️ Selecciona al menos una pieza antes de confirmar.")
            continue
        if not entrada.isdigit():
            print("⚠️ Introduce el número de una pieza.")
            continue
        indice=int(entrada)-1
        if indice<0 or indice>=len(datos["pesos"]):
            print("⚠️ Esa pieza no existe.")
            continue
        if indice in seleccionados:
            seleccionados.remove(indice)
            print("↩️ Pieza deseleccionada.")
            continue
        seleccionados.append(indice)
    pesos=[datos["pesos"][i] for i in seleccionados]
    peso_total=sum(pesos)
    return {"codigo":datos["codigo"],"tipo":"unidad","cantidad":len(pesos),"pesos":pesos,"peso":peso_total,"precio":datos["precio_kg"],"unidad":"un.","subtotal":round(peso_total*datos["precio_kg"],2)}

# des: Oksana | Solicita bolsas manuales y comprueba el presupuesto.
def solicitar_bolsas():
    '''Solicita y añade bolsas manuales respetando el presupuesto.'''
    carrito.pop("👜 Bolsa",None)
    while True:
        entrada=input("\n👜 Bolsas (Enter: ninguna | 0 regresar al menú principal): ").strip()
        if entrada=="":
            return False
        if entrada=="0":
            return True
        if not entrada.isdigit():
            print("⚠️ Introduce un número entero.")
            continue
        cantidad=int(entrada)
        bolsa={"codigo":"B01","tipo":"bolsa","cantidad":cantidad,"peso":0,"precio":PRECIO_BOLSA,"unidad":"un.","subtotal":round(cantidad*PRECIO_BOLSA,2)}
        if presupuesto is not None:
            subtotal=sum(datos["subtotal"] for datos in carrito.values())
            envio=COSTE_ENVIO_DOMICILIO if tipo_compra=="1" and tipo_entrega=="2" else 0.0
            total=subtotal+bolsa["subtotal"]+envio
            if total>presupuesto:
                total_actual=subtotal+envio
                disponible=presupuesto-total_actual
                print(f"⚠️ Supera tu presupuesto. Disponible: {disponible:.2f} €.")
                continue
        carrito["👜 Bolsa"]=bolsa
        return False

# des: Lindey | Muestra el ticket final del pedido.
def mostrar_ticket():
    '''Muestra el ticket final con productos, totales y modalidad de compra.'''
    fecha=datetime.now()
    codigo=fecha.strftime("PED-%Y%m%d-%H%M%S")
    peso=sum(datos["peso"] for nombre,datos in carrito.items() if nombre!="👜 Bolsa")
    envio=COSTE_ENVIO_DOMICILIO if tipo_compra=="1" and tipo_entrega=="2" else 0.0
    ancho=62
    ancho_con_emoji=ancho-1
    limpiar_pantalla()
    subtotal=sum(datos["subtotal"] for datos in carrito.values())
    total=round(subtotal+envio,2)
    print(f"{CIAN}╔{'═'*ancho}╗{RESET}")
    print(f"{CIAN}║{RESET}{NEGRITA}{'🧾 TICKET DE COMPRA':^{ancho_con_emoji}}{RESET}{CIAN}║{RESET}")
    print(f"{CIAN}╠{'═'*ancho}╣{RESET}")
    print(f"{CIAN}║{RESET}{f' Pedido: {codigo}':<{ancho}}{CIAN}║{RESET}")
    fecha_texto=f" Fecha: {fecha.strftime('%d/%m/%Y %H:%M:%S')}"
    print(f"{CIAN}║{RESET}{fecha_texto:<{ancho}}{CIAN}║{RESET}")
    print(f"{CIAN}╠{'═'*ancho}╣{RESET}")
    encabezado=f"{'Cód.':^6}│{'Producto':^18}│{'Cant.':^8}│{'Precio':^9}│{'Ud.':^6}│{'Subtotal':^10}"
    print(f"{CIAN}║{RESET}{encabezado}{CIAN}║{RESET}")
    print(f"{CIAN}╠{'─'*ancho}╣{RESET}")
    for nombre,datos in carrito.items():
        cantidad=f"{datos['cantidad']}" if datos["tipo"] in("unidad","bolsa") else f"{datos['cantidad']:.3f}"
        nombre_formateado=formatear_linea(nombre,18)
        fila=f"{datos['codigo']:^6}│{nombre_formateado}│{cantidad:>8}│ {datos['precio']:>6.2f} €│{datos['unidad']:^6}│ {datos['subtotal']:>7.2f} €"
        print(f"{CIAN}║{RESET}{fila}{CIAN}║{RESET}")
    print(f"{CIAN}╟{'─'*ancho}╢{RESET}")
    print(f"{CIAN}║{RESET}{f'Subtotal: {subtotal:.2f} €':>{ancho}}{CIAN}║{RESET}")
    if envio>0:
        print(f"{CIAN}║{RESET}{f'Envío: {envio:.2f} €':>{ancho}}{CIAN}║{RESET}")
    print(f"{CIAN}║{RESET}{NEGRITA}{f'TOTAL: {total:.2f} €':>{ancho}}{RESET}{CIAN}║{RESET}")
    if tipo_pago=="1" and efectivo_entregado is not None:
        cambio=round(efectivo_entregado-total,2)
        print(f"{CIAN}║{RESET}{f'Efectivo recibido: {efectivo_entregado:.2f} €':>{ancho}}{CIAN}║{RESET}")
        print(f"{CIAN}║{RESET}{f'Vuelto: {cambio:.2f} €':>{ancho}}{CIAN}║{RESET}")
    elif presupuesto is not None:
        print(f"{CIAN}║{RESET}{f'Presupuesto: {presupuesto:.2f} €':>{ancho}}{CIAN}║{RESET}")
    print(f"{CIAN}╟{'─'*ancho}╢{RESET}")
    print(f"{CIAN}║{RESET}{f'⚖️ Peso total del pedido: {peso:.3f} kg':<{ancho_con_emoji + 2}}{CIAN}║{RESET}")
    if tipo_compra=="1" and tipo_entrega=="1":
        modalidad="🏪 Modalidad: Compra online - Recogida en tienda"
        entrega="🚚 Coste de entrega: 0.00 €"
    elif tipo_compra=="1" and tipo_entrega=="2":
        modalidad="🚚 Modalidad: Compra online - Envío a domicilio"
        entrega=f"🚚 Coste de envío: {envio:.2f} €"
    else:
        modalidad="🏪 Modalidad: Compra en tienda"
        entrega=""
    print(f"{CIAN}║{RESET}{modalidad:<{ancho_con_emoji}}{CIAN}║{RESET}")
    if entrega:
        print(f"{CIAN}║{RESET}{entrega:<{ancho_con_emoji}}{CIAN}║{RESET}")
    pagos={"1":"💵 Pago: Efectivo","2":"💳 Pago: Tarjeta","3":"📱 Pago: Bizum"}
    print(f"{CIAN}║{RESET}{pagos.get(tipo_pago,'Pago no indicado'):<{ancho_con_emoji}}{CIAN}║{RESET}")
    print(f"{CIAN}╟{'─'*ancho}╢{RESET}")
    print(f"{CIAN}║{RESET}{'👋 ¡Gracias por tu compra!':^{ancho_con_emoji}}{CIAN}║{RESET}")
    print(f"{CIAN}╚{'═'*ancho}╝{RESET}")

# des: Gus | Busca y añade productos al carrito.
def agregar_producto():
    '''Gestiona la búsqueda, selección y agregado de un producto al carrito.'''
    tipo_busqueda=buscar_fruta()
    if tipo_busqueda==VOLVER_MENU:
        return True
    if tipo_busqueda=="1":
        nombre=buscar_por_codigo()
    else:
        nombre=buscar_por_nombre()
    if nombre==VOLVER_MENU:
        return True
    if nombre is not None:
        if FRUTAS_DISPONIBLES[nombre]["tipo"]=="peso":
            nuevo=seleccionar_por_peso(nombre)
        else:
            nuevo=seleccionar_por_unidad(nombre)
        if nuevo==VOLVER_MENU:
            return True
        if nuevo is not None:
            if nuevo["tipo"]=="peso":
                detalle=f"{nuevo['cantidad']:.3f} kg de {nombre} por {nuevo['subtotal']:.2f} €"
            else:
                detalle=f"{nuevo['cantidad']} un. de {nombre} por {nuevo['subtotal']:.2f} €"
        if nuevo is None:
            input("↩️ Operación cancelada. Pulsa Enter para continuar.")
        elif nombre in carrito:
            actual=carrito[nombre]
            if nuevo["tipo"]=="peso":
                combinado={"codigo":actual["codigo"],"tipo":"peso","cantidad":actual["cantidad"]+nuevo["cantidad"],"peso":actual["peso"]+nuevo["peso"],"precio":nuevo["precio"],"unidad":"kg.","subtotal":round(actual["subtotal"]+nuevo["subtotal"],2)}
            else:
                combinado={"codigo":actual["codigo"],"tipo":"unidad","cantidad":actual["cantidad"]+nuevo["cantidad"],"pesos":actual["pesos"]+nuevo["pesos"],"peso":actual["peso"]+nuevo["peso"],"precio":nuevo["precio"],"unidad":"un.","subtotal":round(actual["subtotal"]+nuevo["subtotal"],2)}
            if func.supera_presupuesto(carrito, presupuesto, tipo_compra, tipo_entrega, nombre, combinado, True):
                input("⚠️ La compra supera tu presupuesto. Pulsa Enter para continuar.")
            else:
                crud.descontar_stock(FRUTAS_DISPONIBLES, nombre, nuevo)
                carrito[nombre]=combinado
                crud.actualizar_bolsas_automaticas(carrito, tipo_compra, tipo_entrega)
                input(f"{EXITO} {detalle} agregado correctamente. Pulsa Enter para continuar.{RESET}")
        elif func.supera_presupuesto(carrito, presupuesto, tipo_compra, tipo_entrega, nombre, nuevo):
            input("⚠️ La compra supera tu presupuesto. Pulsa Enter para continuar.")
        else:
            crud.descontar_stock(FRUTAS_DISPONIBLES, nombre, nuevo)
            carrito[nombre]=nuevo
            crud.actualizar_bolsas_automaticas(carrito, tipo_compra, tipo_entrega)
            input(f"{EXITO} {detalle} agregado correctamente. Pulsa Enter para continuar.{RESET}")
    return False

# des: Yos | Sustituye un producto del carrito manteniendo el stock.
def actualizar_producto():
    '''Modifica un producto del carrito conservando la coherencia del stock.'''
    ancho=58
    print(f"\n{AMARILLO}╔{'═'*ancho}╗{RESET}")
    print(f"{AMARILLO}║{RESET}{NEGRITA}{formatear_linea('🔧 ACTUALIZAR PRODUCTO',ancho,'^')}{RESET}{AMARILLO}║{RESET}")
    productos=[nombre for nombre in carrito if nombre!="👜 Bolsa"]
    if not productos:
        print(f"{AMARILLO}╠{'═'*ancho}╣{RESET}")
        print(f"{AMARILLO}║{RESET}{formatear_linea('⚠️ CARRITO VACÍO',ancho+1,'^')}{AMARILLO}║{RESET}")
        print(f"{AMARILLO}║{RESET}{formatear_linea('No hay productos que actualizar.',ancho,'^')}{AMARILLO}║{RESET}")
        print(f"{AMARILLO}╚{'═'*ancho}╝{RESET}")
        input(f"{AMARILLO}👉 Pulsa Enter para regresar al menú principal.{RESET}")
        return True
    print(f"{AMARILLO}╚{'═'*ancho}╝{RESET}")
    tipo_busqueda=buscar_fruta()
    if tipo_busqueda==VOLVER_MENU:
        return True
    if tipo_busqueda=="1":
        nombre=buscar_por_codigo()
    else:
        nombre=buscar_por_nombre()
    if nombre==VOLVER_MENU:
        return True
    if nombre is not None:
        if nombre not in carrito:
            input("⚠️ Ese producto no está en el carrito. Pulsa Enter para continuar.")
        else:
            anterior=carrito[nombre]
            crud.devolver_stock(FRUTAS_DISPONIBLES, nombre, anterior)
            if FRUTAS_DISPONIBLES[nombre]["tipo"]=="peso":
                nuevo=seleccionar_por_peso(nombre)
            else:
                nuevo=seleccionar_por_unidad(nombre)
            if nuevo==VOLVER_MENU:
                crud.descontar_stock(FRUTAS_DISPONIBLES, nombre, anterior)
                return True
            if nuevo is None:
                crud.descontar_stock(FRUTAS_DISPONIBLES, nombre, anterior)
                input("↩️ Actualización cancelada. Pulsa Enter para continuar.")
            elif func.supera_presupuesto(carrito, presupuesto, tipo_compra, tipo_entrega, nombre, nuevo, True):
                crud.descontar_stock(FRUTAS_DISPONIBLES, nombre, anterior)
                input("⚠️ La nueva selección supera tu presupuesto. Pulsa Enter para continuar.")
            else:
                crud.descontar_stock(FRUTAS_DISPONIBLES, nombre, nuevo)
                carrito[nombre]=nuevo
                crud.actualizar_bolsas_automaticas(carrito, tipo_compra, tipo_entrega)
                input(f"✅ {nombre} actualizado correctamente. Pulsa Enter para continuar.")
    return False

# des: Yos | Elimina un producto del carrito y restaura su stock.
def eliminar_producto():
    '''Elimina un producto del carrito y devuelve su stock.'''
    ancho=58
    print(f"\n{ROJO}╔{'═'*ancho}╗{RESET}")
    print(f"{ROJO}║{RESET}{NEGRITA}{formatear_linea('❌ ELIMINAR PRODUCTO',ancho,'^')}{RESET}{ROJO}║{RESET}")
    productos=[nombre for nombre in carrito if nombre!="👜 Bolsa"]
    if not productos:
        print(f"{ROJO}╠{'═'*ancho}╣{RESET}")
        print(f"{ROJO}║{RESET}{formatear_linea('⚠️ CARRITO VACÍO',ancho+1,'^')}{ROJO}║{RESET}")
        print(f"{ROJO}║{RESET}{formatear_linea('No hay productos que eliminar.',ancho,'^')}{ROJO}║{RESET}")
        print(f"{ROJO}╚{'═'*ancho}╝{RESET}")
        input(f"{ROJO}👉 Pulsa Enter para regresar al menú principal.{RESET}")
        return True
    print(f"{ROJO}╚{'═'*ancho}╝{RESET}")
    tipo_busqueda=buscar_fruta()
    if tipo_busqueda==VOLVER_MENU:
        return True
    if tipo_busqueda=="1":
        nombre=buscar_por_codigo()
    else:
        nombre=buscar_por_nombre()
    if nombre==VOLVER_MENU:
        return True
    if nombre is not None:
        if nombre not in carrito:
            input("⚠️ Ese producto no está en tu carrito. Pulsa Enter para continuar.")
        else:
            confirmar=input(f"🗑️ ¿Eliminar {nombre}? (S/N): ").strip().lower()
            while confirmar not in("s","n"):
                confirmar=input("⚠️ Escribe S o N: ").strip().lower()
            if confirmar=="s":
                crud.devolver_stock(FRUTAS_DISPONIBLES, nombre, carrito[nombre])
                del carrito[nombre]
                crud.actualizar_bolsas_automaticas(carrito, tipo_compra, tipo_entrega)
                input(f"✅ {nombre} eliminado y stock restaurado. Pulsa Enter para continuar.")
    return False

# des: Oksana | Gestiona entrega, bolsas, presupuesto y confirmación final.
def finalizar_compra():
    '''Gestiona entrega, bolsas, presupuesto y confirmación final de la compra.'''
    global tipo_entrega,tipo_pago,efectivo_entregado
    tipo_pago=None
    efectivo_entregado=None
    limpiar_pantalla()
    mostrar_catalogo()
    mostrar_carrito()
    productos=[nombre for nombre in carrito if nombre!="👜 Bolsa"]
    if not productos:
        ancho=58
        print(f"\n{VERDE}╔{'═'*ancho}╗{RESET}")
        print(f"{VERDE}║{RESET}{NEGRITA}{formatear_linea('✅ FINALIZAR COMPRA',ancho,'^')}{RESET}{VERDE}║{RESET}")
        print(f"{VERDE}╠{'═'*ancho}╣{RESET}")
        print(f"{VERDE}║{RESET}{formatear_linea('⚠️ CARRITO VACÍO',ancho+1,'^')}{VERDE}║{RESET}")
        print(f"{VERDE}║{RESET}{formatear_linea('No hay productos que finalizar.',ancho,'^')}{VERDE}║{RESET}")
        print(f"{VERDE}╚{'═'*ancho}╝{RESET}")
        input(f"{VERDE}👉 Pulsa Enter para regresar al menú principal.{RESET}")
        return False
    print(f"{NEGRITA}{VERDE}✅ FINALIZAR COMPRA{RESET}")
    if tipo_compra=="1":
        print("\n📦 MÉTODO DE ENTREGA")
        print("1. 🏪 Recogida en tienda - Gratis")
        print(f"2. 🚚 Envío a domicilio - {COSTE_ENVIO_DOMICILIO:.2f} €")
        print("0. ↩️ Regresar al menú principal")
        tipo_entrega=input("Elige una opción: ").strip()
        while tipo_entrega not in("0","1","2"):
            tipo_entrega=input("⚠️ Escribe 0, 1 o 2: ").strip()
        if tipo_entrega=="0":
            tipo_entrega=None
            return False
    else:
        tipo_entrega=None
    if tipo_compra=="1" and tipo_entrega=="2":
        crud.actualizar_bolsas_automaticas(carrito, tipo_compra, tipo_entrega)
    else:
        carrito.pop("👜 Bolsa",None)
        if solicitar_bolsas():
            tipo_entrega=None
            return False
    if presupuesto is not None and func.calcular_total_final(carrito, tipo_compra, tipo_entrega)>presupuesto:
        carrito.pop("👜 Bolsa",None)
        tipo_entrega=None
        input(f"\n⚠️ El pedido supera el presupuesto de {presupuesto:.2f} €. Pulsa Enter para continuar.")
        return False
    limpiar_pantalla()
    print(f"{NEGRITA}{VERDE}✅ RESUMEN FINAL DEL PEDIDO{RESET}")
    mostrar_carrito()
    print("\n💳 MÉTODO DE PAGO")
    if tipo_compra=="2":
        print("1. 💵 Efectivo")
        opciones_pago=("0","1","2","3")
        mensaje_pago="⚠️ Escribe 0, 1, 2 o 3: "
    else:
        opciones_pago=("0","2","3")
        mensaje_pago="⚠️ En compra online escribe 0, 2 o 3: "
    print("2. 💳 Tarjeta")
    print("3. 📱 Bizum")
    print("0. ↩️ Regresar al menú principal")
    tipo_pago=input("Elige una opción: ").strip()
    while tipo_pago not in opciones_pago:
        tipo_pago=input(mensaje_pago).strip()
    if tipo_pago=="0":
        carrito.pop("👜 Bolsa",None)
        tipo_entrega=None
        tipo_pago=None
        return False
    if tipo_pago=="1":
        entrada=input("💶 Efectivo entregado (0 regresar al menú principal): ").strip()
        while entrada!="0" and (not re.fullmatch(PATRON_DECIMAL,entrada) or float(entrada.replace(",","."))<func.calcular_total_final(carrito, tipo_compra, tipo_entrega)):
            print(f"⚠️ Debes entregar al menos {func.calcular_total_final(carrito, tipo_compra, tipo_entrega):.2f} €.")
            entrada=input("💶 Efectivo entregado (0 regresar al menú principal): ").strip()
        if entrada=="0":
            carrito.pop("👜 Bolsa",None)
            tipo_entrega=None
            tipo_pago=None
            return False
        efectivo_entregado=float(entrada.replace(",","."))
    respuesta=input("\n✅ ¿Confirmas la compra? (S/N): ").strip().lower()
    while respuesta not in("s","n"):
        respuesta=input("⚠️ Escribe S o N: ").strip().lower()
    if respuesta=="s":
        return True
    carrito.pop("👜 Bolsa",None)
    tipo_entrega=None
    tipo_pago=None
    efectivo_entregado=None
    input("↩️ Finalización cancelada. Pulsa Enter para continuar.")
    return False

# des: Yos | Confirma la cancelación completa del pedido.
def cancelar_compra():
    '''Solicita confirmación y cancela toda la compra si el usuario acepta.'''
    respuesta=input("❌ ¿Seguro que deseas cancelar toda la compra? (S/N): ").strip().lower()
    while respuesta not in("s","n"):
        respuesta=input("⚠️ Escribe S o N: ").strip().lower()
    if respuesta=="s":
        crud.restaurar_compra_cancelada(carrito, FRUTAS_DISPONIBLES)
        print("\n❌ Compra cancelada.")
        print("✅ Todo el stock ha sido restaurado.")
        return True
    return False


