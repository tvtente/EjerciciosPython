import math
import re
import unicodedata
import subprocess
import platform
from datetime import datetime

# ============================================================
# COLORES DE CONSOLA
# ============================================================
ROJO="\033[31m"
VERDE="\033[32m"
AMARILLO="\033[33m"
AZUL="\033[34m"
MAGENTA="\033[35m"
CIAN="\033[36m"
NEGRITA="\033[1m"
RESET="\033[0m"
ADVERTENCIA=f"{AMARILLO}⚠️"
ERROR=f"{ROJO}❌"
EXITO=f"{VERDE}✅"
INFO=f"{CIAN}ℹ️"

# ============================================================
# REGLAS DE NEGOCIO
# ============================================================
PRECIO_BOLSA=0.10
CAPACIDAD_BOLSA_KG=5.0
COSTE_ENVIO_DOMICILIO=4.50
STOCK_BAJO=2
PATRON_DECIMAL=r"^\d{1,6}(?:[,.]\d{1,3})?$"

# PREGUNTA DE NEGOCIO: ¿el peso mínimo de venta es 0.001 kg o debe ser otro?
# PREGUNTA DE NEGOCIO: ¿a partir de qué importe debería ser gratis el envío?

# ============================================================
# CATÁLOGO
# ============================================================
FRUTAS_DISPONIBLES={
    "🍌 Plátano":{"codigo":"01","tipo":"peso","precio_kg":1.35,"stock":10.0},
    "🍎 Manzana":{"codigo":"02","tipo":"peso","precio_kg":0.80,"stock":8.0},
    "🍐 Pera":{"codigo":"03","tipo":"peso","precio_kg":0.85,"stock":6.0},
    "🍊 Naranja":{"codigo":"04","tipo":"peso","precio_kg":0.70,"stock":12.0},
    "🍓 Fresa":{"codigo":"05","tipo":"peso","precio_kg":1.70,"stock":5.0},
    "🍒 Cereza":{"codigo":"06","tipo":"peso","precio_kg":2.20,"stock":5.0},
    "🍑 Durazno":{"codigo":"07","tipo":"peso","precio_kg":1.95,"stock":8.0},
    "🍈 Melón":{"codigo":"08","tipo":"unidad","precio_kg":2.54,"pesos":[0.850,1.250]},
    "🍍 Piña":{"codigo":"09","tipo":"unidad","precio_kg":1.54,"pesos":[0.800,0.750,1.300]},
    "🍉 Sandía":{"codigo":"10","tipo":"unidad","precio_kg":1.44,"pesos":[1.800,1.550,1.400]},
    "🌴 Papaya":{"codigo":"11","tipo":"unidad","precio_kg":1.64,"pesos":[0.800, 0.650, 1.040]},
    "🌰 Durian":{"codigo":"12","tipo":"unidad","precio_kg":5.00,"pesos":[1.800,2.000,2.200,1.950,2.100]},
    "🍇 Uva":{"codigo":"13","tipo":"peso","precio_kg":1.80,"stock":2.0},
    "🥝 Kiwi":{"codigo":"14","tipo":"peso","precio_kg":2.20,"stock":6.0},
    "🥭 Mango":{"codigo":"15","tipo":"peso","precio_kg":2.00,"stock":7.0},
    "🍋 Limón":{"codigo":"16","tipo":"peso","precio_kg":1.40,"stock":10.0},
    "🥥 Coco":{"codigo":"17","tipo":"unidad","precio_kg":3.14,"pesos":[0.860,0.615,0.704]}
}

# PREGUNTA DE NEGOCIO: ¿el catálogo y el stock deben guardarse en un archivo
# para que no vuelvan a sus valores iniciales al cerrar el programa?

carrito={}
presupuesto=None
tipo_compra=None
tipo_entrega=None

# ============================================================
# UTILIDADES
# ============================================================
def limpiar_pantalla():
    '''Limpia la consola según el sistema operativo.'''
    if platform.system()=="Windows":
        subprocess.run(["cls"],shell=True)
    else:
        subprocess.run(["clear"])

def calcular_ancho_visual(texto):
    '''Calcula el ancho visible de un texto teniendo en cuenta los emojis.'''
    """Calcula el ancho visible para alinear textos que contienen emojis."""
    ancho=0
    for caracter in texto:
        if unicodedata.east_asian_width(caracter) in("F","W") or ord(caracter)>0x1F600:
            ancho+=2
        else:
            ancho+=1
    return ancho

def formatear_linea(texto,ancho,alineacion="<"):
    '''Alinea un texto dentro de un ancho considerando su tamaño visual.'''
    """Añade espacios sin alterar el texto original, teniendo en cuenta emojis."""
    espacios=max(0,ancho-calcular_ancho_visual(texto))
    if alineacion=="^":
        izquierda=espacios//2
        return " "*izquierda+texto+" "*(espacios-izquierda)
    if alineacion==">":
        return " "*espacios+texto
    return texto+" "*espacios

def calcular_total_final():
    '''Calcula el total del carrito incluyendo el envío cuando corresponde.'''
    subtotal=sum(datos["subtotal"] for datos in carrito.values())
    envio=COSTE_ENVIO_DOMICILIO if tipo_compra=="1" and tipo_entrega=="2" else 0.0
    return round(subtotal+envio,2)

def mostrar_menu_pedido():
    '''Muestra el menú principal y devuelve la opción seleccionada.'''
    ancho=58
    ancho_con_emoji=ancho-1
    print(f"\n{CIAN}╔{'═'*ancho}╗{RESET}")
    print(f"{CIAN}║{RESET}{NEGRITA}{'📋 GESTIÓN DEL PEDIDO':^{ancho_con_emoji}}{RESET}{CIAN}║{RESET}")
    print(f"{CIAN}╠{'═'*ancho}╣{RESET}")
    opciones=(
        ("1", "➕ Agregar producto", VERDE),
        ("2", "🔎 Ver carrito", CIAN),
        ("3", "🔧 Actualizar producto", AMARILLO),
        ("4", "❌ Eliminar producto", ROJO),
        ("5", "✅ Finalizar compra", VERDE),
        ("6", "⛔ Cancelar compra", ROJO),
    )
    for numero, texto, color in opciones:
        linea=f" {numero}. {texto}"
        print(f"{CIAN}║{RESET}{color}{linea:<{ancho_con_emoji}}{RESET}{CIAN}║{RESET}")
    print(f"{CIAN}╟{'─'*ancho}╢{RESET}")
    print(f"{CIAN}║{RESET}{'👉 Selecciona una opción del 1 al 6':<{ancho_con_emoji}}{CIAN}║{RESET}")
    print(f"{CIAN}╚{'═'*ancho}╝{RESET}")
    return input(f"{CIAN}👉 Elige una opción: {RESET}").strip()

# ============================================================
# BOLSAS AUTOMÁTICAS
# ============================================================
def actualizar_bolsas_automaticas():
    '''Calcula y actualiza las bolsas necesarias para el envío a domicilio.'''
    if not(tipo_compra=="1" and tipo_entrega=="2"):
        return
    carrito.pop("👜 Bolsa",None)
    peso=sum(datos["peso"] for nombre,datos in carrito.items() if nombre!="👜 Bolsa")
    if peso<=0:
        return
    cantidad=math.ceil(peso/CAPACIDAD_BOLSA_KG)
    carrito["👜 Bolsa"]={"codigo":"B01","tipo":"bolsa","cantidad":cantidad,"peso":0,"precio":PRECIO_BOLSA,"unidad":"un.","subtotal":round(cantidad*PRECIO_BOLSA,2)}

# ============================================================
# BUSCAR FRUTA
# ============================================================
def buscar_fruta():
    '''Busca una fruta por código o nombre y devuelve el producto seleccionado.'''
    ancho=48
    ancho_con_emoji=ancho-1
    print(f"\n{CIAN}╔{'═'*ancho}╗{RESET}")
    print(f"{CIAN}║{RESET}{NEGRITA}{'🔎 BUSCAR PRODUCTO':^{ancho_con_emoji}}{RESET}{CIAN}║{RESET}")
    print(f"{CIAN}╠{'═'*ancho}╣{RESET}")
    print(f"{CIAN}║{RESET}{'Opción':^9}│{'Acción':^{ancho-10}}{CIAN}║{RESET}")
    print(f"{CIAN}╠{'─'*9}┼{'─'*(ancho-10)}╣{RESET}")
    print(f"{CIAN}║{RESET}{'1':^9}│{' Buscar por código':<{ancho-10}}{CIAN}║{RESET}")
    print(f"{CIAN}║{RESET}{'2':^9}│{' Buscar por nombre':<{ancho-10}}{CIAN}║{RESET}")
    print(f"{CIAN}║{RESET}{'0':^9}│{' Volver':<{ancho-10}}{CIAN}║{RESET}")
    print(f"{CIAN}╚{'═'*ancho}╝{RESET}")
    opcion=input(f"{CIAN}👉 Elige una opción: {RESET}").strip()
    while opcion not in("0","1","2"):
        opcion=input("⚠️ Escribe 1, 2 o 0: ").strip()
    if opcion=="0":
        return None
    if opcion=="1":
        codigo=input("Código del producto (0 volver): ").strip()
        if codigo=="0":
            return None
        codigo_normalizado=codigo.zfill(2) if codigo.isdigit() else codigo
        for nombre,datos in FRUTAS_DISPONIBLES.items():
            if datos["codigo"]==codigo_normalizado:
                return nombre
        print("⚠️ Código inexistente.")
        input("Pulsa Enter para continuar.")
        return None
    texto=input("Nombre de la fruta (0 volver): ").strip()
    if texto=="0":
        return None
    buscado=unicodedata.normalize("NFD",texto.casefold())
    buscado="".join(c for c in buscado if unicodedata.category(c)!="Mn")
    coincidencias=[]
    for nombre in FRUTAS_DISPONIBLES:
        nombre_normalizado=unicodedata.normalize("NFD",nombre.casefold())
        nombre_normalizado="".join(c for c in nombre_normalizado if unicodedata.category(c)!="Mn")
        if buscado==nombre_normalizado or buscado in nombre_normalizado:
            coincidencias.append(nombre)
    if len(coincidencias)==1:
        return coincidencias[0]
    if len(coincidencias)>1:
        print("\nCoincidencias:")
        for i,nombre in enumerate(coincidencias,1):
            print(f"{i}. {nombre}")
        opcion=input("Selecciona una opción (0 cancelar): ").strip()
        if opcion.isdigit() and 1<=int(opcion)<=len(coincidencias):
            return coincidencias[int(opcion)-1]
        return None
    print("⚠️ No encuentro esa fruta.")
    input("Pulsa Enter para continuar.")
    return None

# ============================================================
# MOSTRAR CATÁLOGO
# ============================================================
def mostrar_catalogo():
    '''Muestra el catálogo con precio, stock y estado de cada fruta.'''
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

# ============================================================
# MOSTRAR CARRITO
# ============================================================
def mostrar_carrito():
    '''Muestra los productos del carrito, subtotales, envío y total.'''
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

# ============================================================
# COMPROBAR PRESUPUESTO
# ============================================================
def supera_presupuesto(nombre,nuevo_producto,reemplazar=False):
    '''Comprueba si una operación supera el presupuesto establecido.'''
    if presupuesto is None:
        return False
    total=0
    peso=0
    for producto,datos in carrito.items():
        if producto=="👜 Bolsa":
            continue
        if reemplazar and producto==nombre:
            continue
        total+=datos["subtotal"]
        peso+=datos["peso"]
    total+=nuevo_producto["subtotal"]
    peso+=nuevo_producto["peso"]
    if tipo_compra=="1" and tipo_entrega=="2":
        bolsas=math.ceil(peso/CAPACIDAD_BOLSA_KG) if peso>0 else 0
        total+=bolsas*PRECIO_BOLSA+COSTE_ENVIO_DOMICILIO
    return round(total,2)>presupuesto

# ============================================================
# COMPRA POR PESO
# ============================================================
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
    print(f"{AMARILLO}║{RESET}{'0':^9}│{' Cancelar':<{ancho-10}}{AMARILLO}║{RESET}")
    print(f"{AMARILLO}╚{'═'*ancho}╝{RESET}")
    opcion=input(f"{AMARILLO}👉 Elige una opción: {RESET}").strip()
    while opcion not in("0","1","2"):
        opcion=input("⚠️ Escribe 1, 2 o 0: ").strip()
    if opcion=="0":
        return None
    while True:
        if opcion=="1":
            entrada=input("¿Cuántos kilos deseas? (0 cancelar): ").strip()
            if entrada=="0":
                return None
            if not re.fullmatch(PATRON_DECIMAL,entrada):
                print("⚠️ Introduce una cantidad válida.")
                continue
            cantidad=float(entrada.replace(",","."))
            subtotal=round(cantidad*datos["precio_kg"],2)
        else:
            entrada=input("¿Cuántos euros deseas gastar? (0 cancelar): ").strip()
            if entrada=="0":
                return None
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

# ============================================================
# COMPRA POR UNIDAD
# ============================================================
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
        print("0. Terminar selección")
        entrada=input("Selecciona una pieza: ").strip()
        if entrada=="0":
            break
        if not entrada.isdigit():
            print("⚠️ Introduce el número de una pieza.")
            continue
        indice=int(entrada)-1
        if indice<0 or indice>=len(datos["pesos"]):
            print("⚠️ Esa pieza no existe.")
            continue
        if indice in seleccionados:
            print("⚠️ Esa pieza ya está seleccionada.")
            continue
        seleccionados.append(indice)
    if not seleccionados:
        return None
    pesos=[datos["pesos"][i] for i in seleccionados]
    peso_total=sum(pesos)
    return {"codigo":datos["codigo"],"tipo":"unidad","cantidad":len(pesos),"pesos":pesos,"peso":peso_total,"precio":datos["precio_kg"],"unidad":"un.","subtotal":round(peso_total*datos["precio_kg"],2)}

# ============================================================
# STOCK
# ============================================================
def descontar_stock(nombre,producto):
    '''Descuenta del stock la cantidad o piezas añadidas al carrito.'''
    datos=FRUTAS_DISPONIBLES[nombre]
    if datos["tipo"]=="peso":
        datos["stock"]-=producto["cantidad"]
    else:
        for peso in producto["pesos"]:
            datos["pesos"].remove(peso)

def devolver_stock(nombre,producto):
    '''Devuelve al stock la cantidad o piezas de un producto.'''
    datos=FRUTAS_DISPONIBLES[nombre]
    if datos["tipo"]=="peso":
        datos["stock"]+=producto["cantidad"]
    else:
        datos["pesos"].extend(producto["pesos"])
        datos["pesos"].sort()

# ============================================================
# CANCELAR COMPRA
# ============================================================
def restaurar_compra_cancelada():
    '''Restaura todo el stock del carrito y vacía la compra cancelada.'''
    for nombre,producto in list(carrito.items()):
        if nombre!="👜 Bolsa":
            datos=FRUTAS_DISPONIBLES[nombre]
            if datos["tipo"]=="peso":
                datos["stock"]+=producto["cantidad"]
            else:
                datos["pesos"].extend(producto["pesos"])
                datos["pesos"].sort()
    carrito.clear()
    # PREGUNTA DE NEGOCIO: si hubiera pago, ¿también se debe anular aquí?
    print("\n❌ Compra cancelada.")
    print("✅ Todo el stock ha sido restaurado.")

# ============================================================
# BOLSAS MANUALES
# ============================================================
def solicitar_bolsas():
    '''Solicita y añade bolsas manuales respetando el presupuesto.'''
    carrito.pop("👜 Bolsa",None)
    while True:
        entrada=input("\n👜 ¿Cuántas bolsas deseas? ").strip()
        if not entrada.isdigit():
            print("⚠️ Introduce un número entero.")
            continue
        cantidad=int(entrada)
        if cantidad==0:
            return
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
        return

# ============================================================
# TICKET
# ============================================================
def mostrar_ticket():
    '''Muestra el ticket final con productos, totales y modalidad de compra.'''
    fecha=datetime.now()
    codigo=fecha.strftime("PED-%Y%m%d-%H%M%S")
    peso=sum(datos["peso"] for nombre,datos in carrito.items() if nombre!="👜 Bolsa")
    envio=COSTE_ENVIO_DOMICILIO if tipo_compra=="1" and tipo_entrega=="2" else 0.0
    ancho=62
    ancho_con_emoji=ancho-1
    if platform.system()=="Windows":
        subprocess.run(["cls"],shell=True)
    else:
        subprocess.run(["clear"])

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
    if presupuesto is not None:
        cambio=round(presupuesto-total,2)
        print(f"{CIAN}║{RESET}{f'Presupuesto: {presupuesto:.2f} €':>{ancho}}{CIAN}║{RESET}")
        print(f"{CIAN}║{RESET}{f'Cambio: {cambio:.2f} €':>{ancho}}{CIAN}║{RESET}")
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
    print(f"{CIAN}╟{'─'*ancho}╢{RESET}")
    print(f"{CIAN}║{RESET}{'👋 ¡Gracias por tu compra!':^{ancho_con_emoji}}{CIAN}║{RESET}")
    print(f"{CIAN}╚{'═'*ancho}╝{RESET}")
    # PREGUNTA DE NEGOCIO: ¿el ticket debe guardarse para consultarlo después?

# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================
def main():
    '''Controla el flujo principal del programa y el menú de compra.'''
    global presupuesto,tipo_compra,tipo_entrega
    limpiar_pantalla()
    ancho=52
    ancho_con_emoji=ancho-1
    print(f"{CIAN}╔{'═'*ancho}╗{RESET}")
    print(f"{CIAN}║{RESET}{NEGRITA}{'🛒 BIENVENIDO A FRUTERÍA PYTHON':^{ancho_con_emoji}}{RESET}{CIAN}║{RESET}")
    print(f"{CIAN}╠{'═'*ancho}╣{RESET}")
    print(f"{CIAN}║{RESET}{'Opción':^9}│{'Modalidad':^{ancho-10}}{CIAN}║{RESET}")
    print(f"{CIAN}╠{'─'*9}┼{'─'*(ancho-10)}╣{RESET}")
    print(f"{CIAN}║{RESET}{'1':^9}│{' 🌐 Compra online':<{ancho-11}}{CIAN}║{RESET}")
    print(f"{CIAN}║{RESET}{'2':^9}│{' 🏪 Compra en tienda':<{ancho-11}}{CIAN}║{RESET}")
    print(f"{CIAN}╚{'═'*ancho}╝{RESET}")
    tipo_compra=input(f"{CIAN}👉 Elige una opción: {RESET}").strip()
    while tipo_compra not in("1","2"):
        tipo_compra=input(f"{ROJO}⚠️ Escribe 1 o 2: {RESET}").strip()

    print(f"\n{AMARILLO}╔{'═'*ancho}╗{RESET}")
    print(f"{AMARILLO}║{RESET}{NEGRITA}{'💰 PRESUPUESTO':^{ancho_con_emoji}}{RESET}{AMARILLO}║{RESET}")
    print(f"{AMARILLO}╠{'═'*ancho}╣{RESET}")
    print(f"{AMARILLO}║{RESET}{'Puedes establecer un límite máximo para tu pedido.':^{ancho}}{AMARILLO}║{RESET}")
    print(f"{AMARILLO}╚{'═'*ancho}╝{RESET}")
    respuesta=input(f"{AMARILLO}💰 ¿Deseas establecer un presupuesto? (S/N): {RESET}").strip().lower()
    while respuesta not in("s","n"):
        respuesta=input(f"{ROJO}⚠️ Escribe S o N: {RESET}").strip().lower()
    if respuesta=="s":
        entrada=input(f"{AMARILLO}💶 Introduce tu presupuesto: {RESET}").strip()
        while not re.fullmatch(PATRON_DECIMAL,entrada) or float(entrada.replace(",","."))<=0:
            entrada=input(f"{ROJO}⚠️ Introduce un importe válido: {RESET}").strip()
        presupuesto=float(entrada.replace(",","."))

    finalizar=False
    while not finalizar:
        limpiar_pantalla()
        actualizar_bolsas_automaticas()
        mostrar_catalogo()
        mostrar_carrito()
        opcion=mostrar_menu_pedido()

        match opcion:
            case "1":
                agregar_producto()
            case "2":
                mostrar_carrito()
                input("\nPulsa Enter para continuar.")
            case "3":
                actualizar_producto()
            case "4":
                eliminar_producto()
            case "5":
                finalizar=finalizar_compra()
            case "6":
                if cancelar_compra():
                    return
            case _:
                input("⚠️ Opción incorrecta. Pulsa Enter para continuar.")

    mostrar_ticket()

def agregar_producto():
    '''Gestiona la búsqueda, selección y agregado de un producto al carrito.'''
    # PREGUNTA DE NEGOCIO: antes de elegir entrega, el presupuesto
                # solo controla productos; envío y bolsas se revisan al finalizar.
    nombre=buscar_fruta()
    if nombre is not None:
        if FRUTAS_DISPONIBLES[nombre]["tipo"]=="peso":
            nuevo=seleccionar_por_peso(nombre)
        else:
            nuevo=seleccionar_por_unidad(nombre)

        if nuevo is None:
            input("↩️ Operación cancelada. Pulsa Enter para continuar.")
        elif nombre in carrito:
            actual=carrito[nombre]
            if nuevo["tipo"]=="peso":
                combinado={"codigo":actual["codigo"],"tipo":"peso","cantidad":actual["cantidad"]+nuevo["cantidad"],"peso":actual["peso"]+nuevo["peso"],"precio":nuevo["precio"],"unidad":"kg.","subtotal":round(actual["subtotal"]+nuevo["subtotal"],2)}
            else:
                combinado={"codigo":actual["codigo"],"tipo":"unidad","cantidad":actual["cantidad"]+nuevo["cantidad"],"pesos":actual["pesos"]+nuevo["pesos"],"peso":actual["peso"]+nuevo["peso"],"precio":nuevo["precio"],"unidad":"un.","subtotal":round(actual["subtotal"]+nuevo["subtotal"],2)}
            if supera_presupuesto(nombre,combinado,True):
                input("⚠️ La compra supera tu presupuesto. Pulsa Enter para continuar.")
            else:
                descontar_stock(nombre,nuevo)
                carrito[nombre]=combinado
                actualizar_bolsas_automaticas()
                input(f"{EXITO} {nombre} agregado correctamente. Pulsa Enter para continuar.{RESET}")
        elif supera_presupuesto(nombre,nuevo):
            input("⚠️ La compra supera tu presupuesto. Pulsa Enter para continuar.")
        else:
            descontar_stock(nombre,nuevo)
            carrito[nombre]=nuevo
            actualizar_bolsas_automaticas()
            input(f"{EXITO} {nombre} agregado correctamente. Pulsa Enter para continuar.{RESET}")

def actualizar_producto():
    '''Modifica un producto del carrito conservando la coherencia del stock.'''
    productos=[nombre for nombre in carrito if nombre!="👜 Bolsa"]
    if not productos:
        input(f"{ADVERTENCIA} El carrito está vacío. Pulsa Enter para continuar.{RESET}")
    else:
        nombre=buscar_fruta()
        if nombre is not None:
            if nombre not in carrito:
                input("⚠️ Ese producto no está en el carrito. Pulsa Enter para continuar.")
            else:
                anterior=carrito[nombre]
                devolver_stock(nombre,anterior)
                if FRUTAS_DISPONIBLES[nombre]["tipo"]=="peso":
                    nuevo=seleccionar_por_peso(nombre)
                else:
                    nuevo=seleccionar_por_unidad(nombre)

                if nuevo is None:
                    descontar_stock(nombre,anterior)
                    input("↩️ Actualización cancelada. Pulsa Enter para continuar.")
                elif supera_presupuesto(nombre,nuevo,True):
                    descontar_stock(nombre,anterior)
                    input("⚠️ La nueva selección supera tu presupuesto. Pulsa Enter para continuar.")
                else:
                    descontar_stock(nombre,nuevo)
                    carrito[nombre]=nuevo
                    actualizar_bolsas_automaticas()
                    input(f"✅ {nombre} actualizado correctamente. Pulsa Enter para continuar.")

def eliminar_producto():
    '''Elimina un producto del carrito y devuelve su stock.'''
    productos=[nombre for nombre in carrito if nombre!="👜 Bolsa"]
    if not productos:
        input("⚠️ El carrito está vacío. Pulsa Enter para continuar.")
    else:
        nombre=buscar_fruta()
        if nombre is not None:
            if nombre not in carrito:
                input("⚠️ Ese producto no está en tu carrito. Pulsa Enter para continuar.")
            else:
                confirmar=input(f"🗑️ ¿Eliminar {nombre}? (S/N): ").strip().lower()
                while confirmar not in("s","n"):
                    confirmar=input("⚠️ Escribe S o N: ").strip().lower()
                if confirmar=="s":
                    devolver_stock(nombre,carrito[nombre])
                    del carrito[nombre]
                    actualizar_bolsas_automaticas()
                    input(f"✅ {nombre} eliminado y stock restaurado. Pulsa Enter para continuar.")

def finalizar_compra():
    '''Gestiona entrega, bolsas, presupuesto y confirmación final de la compra.'''
    global tipo_entrega
    productos=[nombre for nombre in carrito if nombre!="👜 Bolsa"]
    if not productos:
        input("\n⚠️ El carrito está vacío. Pulsa Enter para continuar.")
        return False
    limpiar_pantalla()
    print(f"{NEGRITA}{VERDE}✅ FINALIZAR COMPRA{RESET}")
    # PREGUNTA DE NEGOCIO: ¿una compra online debe pedir dirección,
    # franja de entrega y método de pago antes de confirmarse?
    if tipo_compra=="1":
        print("\n📦 MÉTODO DE ENTREGA")
        print("1. 🏪 Recogida en tienda - Gratis")
        print(f"2. 🚚 Envío a domicilio - {COSTE_ENVIO_DOMICILIO:.2f} €")
        tipo_entrega=input("Elige una opción: ").strip()
        while tipo_entrega not in("1","2"):
            tipo_entrega=input("⚠️ Escribe 1 o 2: ").strip()
    else:
        tipo_entrega=None
    if tipo_compra=="1" and tipo_entrega=="2":
        actualizar_bolsas_automaticas()
    else:
        carrito.pop("👜 Bolsa",None)
        solicitar_bolsas()
    if presupuesto is not None and calcular_total_final()>presupuesto:
        carrito.pop("👜 Bolsa",None)
        tipo_entrega=None
        input(f"\n⚠️ El pedido supera el presupuesto de {presupuesto:.2f} €. Pulsa Enter para continuar.")
        return False
    mostrar_carrito()
    respuesta=input("\n✅ ¿Confirmas la compra? (S/N): ").strip().lower()
    while respuesta not in("s","n"):
        respuesta=input("⚠️ Escribe S o N: ").strip().lower()
    if respuesta=="s":
        return True
    carrito.pop("👜 Bolsa",None)
    tipo_entrega=None
    input("↩️ Finalización cancelada. Pulsa Enter para continuar.")
    return False

def cancelar_compra():
    '''Solicita confirmación y cancela toda la compra si el usuario acepta.'''
    respuesta=input("❌ ¿Seguro que deseas cancelar toda la compra? (S/N): ").strip().lower()
    while respuesta not in("s","n"):
        respuesta=input("⚠️ Escribe S o N: ").strip().lower()
    if respuesta=="s":
        restaurar_compra_cancelada()
        return True
    return False

# ============================================================
# INICIAR PROGRAMA
# ============================================================
if __name__=="__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n")
        print(f"{INFO} Se ha pulsado Ctrl + C.{RESET}")
        print("👋 Saliendo de Frutería Python...")
        
    finally:
        print(f"{EXITO} Programa terminado{RESET}")
