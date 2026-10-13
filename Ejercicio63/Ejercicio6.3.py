import math
import re
import unicodedata
import subprocess
import platform
from datetime import datetime

# ============================================================
# REGLAS DE NEGOCIO
# ============================================================
PRECIO_BOLSA=0.10
CAPACIDAD_BOLSA_KG=5.0
STOCK_BAJO=2
PATRON_DECIMAL=r"^\d+(?:[,.]\d+)?$"

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
    "🍈 Melón":{"codigo":"08","tipo":"unidad","precio_kg":2.54,"pesos":[0.850,1.250,1.100]},
    "🍍 Piña":{"codigo":"09","tipo":"unidad","precio_kg":1.54,"pesos":[0.800,0.750,1.300]},
    "🍉 Sandía":{"codigo":"10","tipo":"unidad","precio_kg":1.44,"pesos":[1.800,1.550,1.400]},
    "🧡 Papaya":{"codigo":"11","tipo":"unidad","precio_kg":1.64,"pesos":[0.800,0.650,1.040]},
    "🌰 Durian":{"codigo":"12","tipo":"unidad","precio_kg":5.00,"pesos":[1.800,2.000,2.200,1.950,2.100]},
    "🍇 Uva":{"codigo":"13","tipo":"peso","precio_kg":1.80,"stock":8.0},
    "🥝 Kiwi":{"codigo":"14","tipo":"peso","precio_kg":2.20,"stock":6.0},
    "🥭 Mango":{"codigo":"15","tipo":"peso","precio_kg":2.00,"stock":7.0},
    "🍋 Limón":{"codigo":"16","tipo":"peso","precio_kg":1.40,"stock":10.0},
    "🥥 Coco":{"codigo":"17","tipo":"peso","precio_kg":2.50,"stock":7.0}
}

carrito={}
presupuesto=None
tipo_compra=None
tipo_entrega=None

# ============================================================
# UTILIDADES
# ============================================================
def limpiar_pantalla():
    if platform.system()=="Windows":
        subprocess.run(["cls"],shell=True)
    else:
        subprocess.run(["clear"])

def normalizar_texto(texto):
    texto=unicodedata.normalize("NFD",texto.casefold())
    return "".join(c for c in texto if unicodedata.category(c)!="Mn")

def formatear_precio(precio):
    return f"{precio:.2f}"

# ============================================================
# PESO DEL CARRITO
# ============================================================
def calcular_peso_carrito():
    peso=0
    for nombre,datos in carrito.items():
        if nombre!="👜 Bolsa":
            peso+=datos["peso"]
    return peso

# ============================================================
# BOLSAS AUTOMÁTICAS
# ============================================================
def actualizar_bolsas_automaticas():
    if not(tipo_compra=="1" and tipo_entrega=="1"):
        return

    carrito.pop("👜 Bolsa",None)
    peso=calcular_peso_carrito()

    if peso<=0:
        return

    cantidad=math.ceil(peso/CAPACIDAD_BOLSA_KG)

    carrito["👜 Bolsa"]={
        "codigo":"B01",
        "tipo":"bolsa",
        "cantidad":cantidad,
        "peso":0,
        "precio":PRECIO_BOLSA,
        "unidad":"un.",
        "subtotal":cantidad*PRECIO_BOLSA
    }

# ============================================================
# TOTAL DEL CARRITO
# ============================================================
def calcular_total():
    return sum(datos["subtotal"] for datos in carrito.values())

# ============================================================
# BUSCAR FRUTA
# ============================================================
def buscar_fruta():
    print("\n🔎 BUSCAR PRODUCTO")
    print("1. Buscar por código")
    print("2. Buscar por nombre")
    print("0. Volver")

    opcion=input("Elige una opción: ").strip()

    while opcion not in("0","1","2"):
        opcion=input("⚠️ Escribe 1, 2 o 0: ").strip()

    if opcion=="0":
        return None

    if opcion=="1":
        codigo=input("Código del producto: ").strip()

        if codigo=="0":
            return None

        for nombre,datos in FRUTAS_DISPONIBLES.items():
            if datos["codigo"]==codigo:
                return nombre

        print("⚠️ Código inexistente.")
        input("Pulsa Enter para continuar.")
        return None

    texto=input("Nombre de la fruta: ").strip()

    if texto=="0":
        return None

    buscado=normalizar_texto(texto)

    for nombre in FRUTAS_DISPONIBLES:
        if buscado==normalizar_texto(nombre):
            return nombre

    coincidencias=[]

    if len(buscado)>=3:
        for nombre in FRUTAS_DISPONIBLES:
            if buscado in normalizar_texto(nombre):
                coincidencias.append(nombre)

    if len(coincidencias)==1:
        fruta=coincidencias[0]
        respuesta=input(f"🤔 ¿Te referías a {fruta}? (S/N): ").strip().lower()

        while respuesta not in("s","n"):
            respuesta=input("⚠️ Escribe S o N: ").strip().lower()

        if respuesta=="s":
            return fruta

    print("⚠️ No encuentro esa fruta.")
    input("Pulsa Enter para continuar.")
    return None

# ============================================================
# MOSTRAR CATÁLOGO
# ============================================================
def mostrar_catalogo():
    print("\n🛒 FRUTAS DISPONIBLES")
    print("+--------+-------------------+-------------+-------------+---------------+")
    print("| Código | Fruta             | Precio/kg   | Disponible  | Estado        |")
    print("+--------+-------------------+-------------+-------------+---------------+")

    for nombre,datos in FRUTAS_DISPONIBLES.items():
        if datos["tipo"]=="peso":
            disponible=datos["stock"]
            texto_disponible=f"{disponible:.2f} kg"

            if disponible<=0:
                estado="❌ Agotado"
            elif disponible<=STOCK_BAJO:
                estado="⚠️ Bajo"
            else:
                estado="✅ Disponible"

        else:
            disponible=len(datos["pesos"])
            texto_disponible=f"{disponible} un."

            if disponible==0:
                estado="❌ Agotado"
            elif disponible<=STOCK_BAJO:
                estado="⚠️ Bajo"
            else:
                estado="✅ Disponible"

        print(f"| {datos['codigo']:^6} | {nombre:<16} | {datos['precio_kg']:>9.2f} € | {texto_disponible:>11} | {estado:<12} |")

    print("+--------+------------------+-------------+-------------+--------------+")

# ============================================================
# MOSTRAR CARRITO
# ============================================================
def mostrar_carrito():
    actualizar_bolsas_automaticas()
    total=calcular_total()

    if presupuesto is not None:
        disponible=presupuesto-total
        print(f"\n🛒 RESUMEN DE COMPRA     💰 Gastado: {total:.2f} € | Disponible: {disponible:.2f} €")
    else:
        print("\n🛒 RESUMEN DE COMPRA")

    print("+--------+------------------+----------+-------------+--------+-------------+")
    print("| Código | Producto         | Cantidad | P. unitario | Unidad | Subtotal    |")
    print("+--------+------------------+----------+-------------+--------+-------------+")

    if not carrito:
        print(f"| {'El carrito está vacío.':^78} |")
        print("+--------+------------------+----------+-------------+--------+-------------+")
        return

    for nombre,datos in carrito.items():
        if datos["tipo"]=="unidad":
            cantidad=f"{datos['cantidad']}"
        elif datos["tipo"]=="bolsa":
            cantidad=f"{datos['cantidad']}"
        else:
            cantidad=f"{datos['cantidad']:.3f}"

        print(f"| {datos['codigo']:^6} | {nombre:<15} | {cantidad:>8} | {datos['precio']:>9.2f} € | {datos['unidad']:^6} | {datos['subtotal']:>9.2f} € |")

    print("+--------+------------------+----------+-------------+--------+-------------+")
    print(f"| {'Total a pagar':<61}| {total:>9.2f} € |")
    print("+--------+------------------+----------+-------------+--------+-------------+")

# ============================================================
# COMPROBAR PRESUPUESTO
# ============================================================
def supera_presupuesto(nombre,nuevo_producto,reemplazar=False):
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

    if tipo_compra=="1" and tipo_entrega=="1":
        bolsas=math.ceil(peso/CAPACIDAD_BOLSA_KG) if peso>0 else 0
        total+=bolsas*PRECIO_BOLSA

    return total>presupuesto

# ============================================================
# SOLICITAR COMPRA POR PESO
# ============================================================
def seleccionar_por_peso(nombre):
    datos=FRUTAS_DISPONIBLES[nombre]

    if datos["stock"]<=0:
        print("❌ Producto agotado.")
        return None

    print(f"\n⚖️ {nombre} se vende por peso.")
    print(f"Precio: {datos['precio_kg']:.2f} €/kg")
    print(f"Disponible: {datos['stock']:.2f} kg")
    print("\n1. Introducir kilos")
    print("2. Introducir importe en euros")
    print("0. Cancelar")

    opcion=input("Elige una opción: ").strip()

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
            subtotal=cantidad*datos["precio_kg"]

        else:
            entrada=input("¿Cuántos euros deseas gastar? (0 cancelar): ").strip()

            if entrada=="0":
                return None

            if not re.fullmatch(PATRON_DECIMAL,entrada):
                print("⚠️ Introduce un importe válido.")
                continue

            subtotal=float(entrada.replace(",","."))
            cantidad=round(subtotal/datos["precio_kg"],3)

        if cantidad<=0:
            print("⚠️ La cantidad debe ser mayor que cero.")
            continue

        if cantidad>datos["stock"]:
            maximo=datos["stock"]*datos["precio_kg"]
            print(f"⚠️ Solo quedan {datos['stock']:.2f} kg.")
            print(f"💰 Importe máximo: {maximo:.2f} €")
            continue

        return {
            "codigo":datos["codigo"],
            "tipo":"peso",
            "cantidad":cantidad,
            "peso":cantidad,
            "precio":datos["precio_kg"],
            "unidad":"kg.",
            "subtotal":subtotal
        }

# ============================================================
# SELECCIONAR PIEZAS POR UNIDAD
# ============================================================
def seleccionar_por_unidad(nombre):
    datos=FRUTAS_DISPONIBLES[nombre]

    if not datos["pesos"]:
        print("❌ Producto agotado.")
        return None

    pesos_disponibles=datos["pesos"]
    seleccionados=[]

    while True:
        print(f"\n📦 UNIDADES DISPONIBLES DE {nombre}")
        print("-"*55)

        for i,peso in enumerate(pesos_disponibles,1):
            if i-1 in seleccionados:
                estado="✅ Seleccionada"
            else:
                precio=peso*datos["precio_kg"]
                estado=f"{peso:.3f} kg -> {precio:.2f} €"

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

        if indice<0 or indice>=len(pesos_disponibles):
            print("⚠️ Esa pieza no existe.")
            continue

        if indice in seleccionados:
            print("⚠️ Esa pieza ya está seleccionada.")
            continue

        seleccionados.append(indice)

    if not seleccionados:
        return None

    pesos=[pesos_disponibles[i] for i in seleccionados]
    peso_total=sum(pesos)
    subtotal=peso_total*datos["precio_kg"]

    return {
        "codigo":datos["codigo"],
        "tipo":"unidad",
        "cantidad":len(pesos),
        "pesos":pesos,
        "indices":seleccionados,
        "peso":peso_total,
        "precio":datos["precio_kg"],
        "unidad":"un.",
        "subtotal":subtotal
    }

# ============================================================
# CAPTURAR PRODUCTO
# ============================================================
def seleccionar_producto(nombre):
    if FRUTAS_DISPONIBLES[nombre]["tipo"]=="peso":
        return seleccionar_por_peso(nombre)
    return seleccionar_por_unidad(nombre)

# ============================================================
# DESCONTAR STOCK
# ============================================================
def descontar_stock(nombre,producto):
    datos=FRUTAS_DISPONIBLES[nombre]

    if datos["tipo"]=="peso":
        datos["stock"]-=producto["cantidad"]
    else:
        for peso in producto["pesos"]:
            datos["pesos"].remove(peso)

# ============================================================
# DEVOLVER STOCK
# ============================================================
def devolver_stock(nombre,producto):
    datos=FRUTAS_DISPONIBLES[nombre]

    if datos["tipo"]=="peso":
        datos["stock"]+=producto["cantidad"]
    else:
        datos["pesos"].extend(producto["pesos"])
        datos["pesos"].sort()

# ============================================================
# AGREGAR PRODUCTO
# ============================================================
def agregar_producto():
    nombre=buscar_fruta()

    if nombre is None:
        return

    nuevo=seleccionar_producto(nombre)

    if nuevo is None:
        print("↩️ Operación cancelada.")
        input("Pulsa Enter para continuar.")
        return

    if nombre in carrito:
        actual=carrito[nombre]

        if nuevo["tipo"]=="peso":
            combinado={
                "codigo":actual["codigo"],
                "tipo":"peso",
                "cantidad":actual["cantidad"]+nuevo["cantidad"],
                "peso":actual["peso"]+nuevo["peso"],
                "precio":nuevo["precio"],
                "unidad":"kg.",
                "subtotal":actual["subtotal"]+nuevo["subtotal"]
            }
        else:
            combinado={
                "codigo":actual["codigo"],
                "tipo":"unidad",
                "cantidad":actual["cantidad"]+nuevo["cantidad"],
                "pesos":actual["pesos"]+nuevo["pesos"],
                "peso":actual["peso"]+nuevo["peso"],
                "precio":nuevo["precio"],
                "unidad":"un.",
                "subtotal":actual["subtotal"]+nuevo["subtotal"]
            }

        if supera_presupuesto(nombre,combinado,reemplazar=True):
            print("⚠️ La compra supera tu presupuesto.")
            input("Pulsa Enter para continuar.")
            return

        descontar_stock(nombre,nuevo)
        carrito[nombre]=combinado

    else:
        if supera_presupuesto(nombre,nuevo):
            print("⚠️ La compra supera tu presupuesto.")
            input("Pulsa Enter para continuar.")
            return

        descontar_stock(nombre,nuevo)
        nuevo.pop("indices",None)
        carrito[nombre]=nuevo

    actualizar_bolsas_automaticas()
    print(f"✅ {nombre} agregado correctamente.")
    input("Pulsa Enter para continuar.")

# ============================================================
# ACTUALIZAR PRODUCTO
# ============================================================
def actualizar_producto():
    productos=[nombre for nombre in carrito if nombre!="👜 Bolsa"]

    if not productos:
        print("⚠️ El carrito está vacío.")
        input("Pulsa Enter para continuar.")
        return

    nombre=buscar_fruta()

    if nombre is None:
        return

    if nombre not in carrito:
        print("⚠️ Ese producto no está en el carrito.")
        input("Pulsa Enter para continuar.")
        return

    anterior=carrito[nombre]
    devolver_stock(nombre,anterior)

    nuevo=seleccionar_producto(nombre)

    if nuevo is None:
        descontar_stock(nombre,anterior)
        print("↩️ Actualización cancelada.")
        input("Pulsa Enter para continuar.")
        return

    if supera_presupuesto(nombre,nuevo,reemplazar=True):
        descontar_stock(nombre,anterior)
        print("⚠️ La nueva selección supera tu presupuesto.")
        input("Pulsa Enter para continuar.")
        return

    descontar_stock(nombre,nuevo)
    nuevo.pop("indices",None)
    carrito[nombre]=nuevo

    actualizar_bolsas_automaticas()
    print(f"✅ {nombre} actualizado correctamente.")
    input("Pulsa Enter para continuar.")

# ============================================================
# ELIMINAR PRODUCTO
# ============================================================
def eliminar_producto():
    productos=[nombre for nombre in carrito if nombre!="👜 Bolsa"]

    if not productos:
        print("⚠️ El carrito está vacío.")
        input("Pulsa Enter para continuar.")
        return

    nombre=buscar_fruta()

    if nombre is None:
        return

    if nombre not in carrito:
        print("⚠️ Ese producto no está en tu carrito.")
        input("Pulsa Enter para continuar.")
        return

    confirmar=input(f"🗑️ ¿Eliminar {nombre}? (S/N): ").strip().lower()

    while confirmar not in("s","n"):
        confirmar=input("⚠️ Escribe S o N: ").strip().lower()

    if confirmar=="n":
        return

    devolver_stock(nombre,carrito[nombre])
    del carrito[nombre]
    actualizar_bolsas_automaticas()

    print(f"✅ {nombre} eliminado y stock restaurado.")
    input("Pulsa Enter para continuar.")

# ============================================================
# CANCELAR COMPRA
# ============================================================
def cancelar_compra():
    for nombre,producto in list(carrito.items()):
        if nombre!="👜 Bolsa":
            devolver_stock(nombre,producto)

    carrito.clear()
    print("\n❌ Compra cancelada.")
    print("✅ Todo el stock ha sido restaurado.")

# ============================================================
# BOLSAS MANUALES
# ============================================================
def solicitar_bolsas():
    carrito.pop("👜 Bolsa",None)

    while True:
        entrada=input("\n👜 ¿Cuántas bolsas deseas? ").strip()

        if not entrada.isdigit():
            print("⚠️ Introduce un número entero.")
            continue

        cantidad=int(entrada)

        if cantidad==0:
            return True

        producto={
            "codigo":"B01",
            "tipo":"bolsa",
            "cantidad":cantidad,
            "peso":0,
            "precio":PRECIO_BOLSA,
            "unidad":"un.",
            "subtotal":cantidad*PRECIO_BOLSA
        }

        if presupuesto is not None:
            total=calcular_total()+producto["subtotal"]

            if total>presupuesto:
                disponible=presupuesto-calcular_total()
                print(f"⚠️ Supera tu presupuesto. Disponible: {disponible:.2f} €.")
                continue

        carrito["👜 Bolsa"]=producto
        return True

# ============================================================
# TICKET
# ============================================================
def mostrar_ticket():
    fecha=datetime.now()
    codigo=fecha.strftime("PED-%Y%m%d-%H%M%S")
    peso=calcular_peso_carrito()

    limpiar_pantalla()
    print("="*70)
    print("                         🧾 TICKET DE COMPRA")
    print("="*70)
    print(f"Pedido: {codigo}")
    print(f"Fecha: {fecha.strftime('%d/%m/%Y %H:%M:%S')}")

    mostrar_carrito()

    print(f"\n⚖️ Peso total del pedido: {peso:.3f} kg")

    if tipo_compra=="1" and tipo_entrega=="1":
        print("🚚 Modalidad: Compra online - Entrega a domicilio")
    elif tipo_compra=="1" and tipo_entrega=="2":
        print("📦 Modalidad: Compra online - Recogida")
    else:
        print("🏪 Modalidad: Compra en tienda")

    print("\n👋 ¡Gracias por tu compra!")

# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================
def main():
    global presupuesto,tipo_compra,tipo_entrega

    limpiar_pantalla()
    print("==============================================")
    print("         🛒 BIENVENIDO A FRUTERÍA PYTHON")
    print("==============================================")
    print("1. 🌐 Compra online")
    print("2. 🏪 Compra en tienda")

    tipo_compra=input("Elige una opción: ").strip()

    while tipo_compra not in("1","2"):
        tipo_compra=input("⚠️ Escribe 1 o 2: ").strip()

    if tipo_compra=="1":
        print("\n📦 ¿Cómo quieres recibir la compra?")
        print("1. 🚚 Entrega a domicilio")
        print("2. 🏪 Recogida")

        tipo_entrega=input("Elige una opción: ").strip()

        while tipo_entrega not in("1","2"):
            tipo_entrega=input("⚠️ Escribe 1 o 2: ").strip()

        respuesta=input("\n💰 ¿Deseas establecer un presupuesto? (S/N): ").strip().lower()

        while respuesta not in("s","n"):
            respuesta=input("⚠️ Escribe S o N: ").strip().lower()

        if respuesta=="s":
            entrada=input("Introduce tu presupuesto: ").strip()

            while not re.fullmatch(PATRON_DECIMAL,entrada) or float(entrada.replace(",","."))<=0:
                entrada=input("⚠️ Introduce un importe válido: ").strip()

            presupuesto=float(entrada.replace(",","."))

    finalizar=False

    while not finalizar:
        limpiar_pantalla()
        actualizar_bolsas_automaticas()
        mostrar_catalogo()
        mostrar_carrito()

        print("\n📋 GESTIÓN DEL PEDIDO")
        print("1. ➕ Crear / agregar producto")
        print("2. 👁️ Ver carrito")
        print("3. ✏️ Actualizar producto")
        print("4. 🗑️ Eliminar producto")
        print("5. ✅ Finalizar compra")
        print("6. ❌ Cancelar compra")

        opcion=input("Elige una opción: ").strip()

        if opcion=="1":
            agregar_producto()

        elif opcion=="2":
            mostrar_carrito()
            input("\nPulsa Enter para continuar.")

        elif opcion=="3":
            actualizar_producto()

        elif opcion=="4":
            eliminar_producto()

        elif opcion=="5":
            productos=[nombre for nombre in carrito if nombre!="👜 Bolsa"]

            if not productos:
                input("\n⚠️ El carrito está vacío. Pulsa Enter para continuar.")
                continue

            if not(tipo_compra=="1" and tipo_entrega=="1"):
                solicitar_bolsas()

            actualizar_bolsas_automaticas()

            if presupuesto is not None and calcular_total()>presupuesto:
                input("\n⚠️ El pedido supera el presupuesto. Pulsa Enter para continuar.")
                continue

            mostrar_carrito()
            respuesta=input("\n✅ ¿Confirmas la compra? (S/N): ").strip().lower()

            while respuesta not in("s","n"):
                respuesta=input("⚠️ Escribe S o N: ").strip().lower()

            if respuesta=="s":
                finalizar=True

        elif opcion=="6":
            respuesta=input("❌ ¿Seguro que deseas cancelar toda la compra? (S/N): ").strip().lower()

            while respuesta not in("s","n"):
                respuesta=input("⚠️ Escribe S o N: ").strip().lower()

            if respuesta=="s":
                cancelar_compra()
                return

        else:
            input("⚠️ Opción incorrecta. Pulsa Enter para continuar.")

    mostrar_ticket()

# ============================================================
# INICIAR PROGRAMA
# ============================================================
if __name__=="__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Se ha pulsado Ctrl + C.")
        print("👋 Saliendo de Frutería Python...")
    finally:
        print("✅ Programa terminado.")