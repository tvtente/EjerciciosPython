
    
  
wb = load_workbook(TRABAJO)
ws = wb[HOJA] if HOJA in wb.sheetnames else wb[wb.sheetnames[0]]

for celda in ws[1]:
    celda.value = normalizar(celda.value)

cabeceras = [celda.value for celda in ws[1]]

if "Total" not in cabeceras:
    ws.cell(1, ws.max_column + 1, "Total")
    cabeceras.append("Total")

def columna(nombre):
    return cabeceras.index(nombre) + 1

def guardar():
    wb.save(TRABAJO)

def recalcular_fila(fila):
    precio = ws.cell(fila, columna("Precio unidad")).value
    cantidad = ws.cell(fila, columna("Cantidad")).value
    descuento = ws.cell(fila, columna("Descuento")).value
    ws.cell(fila, columna("Total"), calcular_total(precio, cantidad, descuento))

def recalcular_todo():
    for fila in range(2, ws.max_row + 1):
        recalcular_fila(fila)
    guardar()

def listar():
    print("\n=== PEDIDOS ===")
    inicio = max(2, ws.max_row - 19)
    for fila in range(inicio, ws.max_row + 1):
        print(
            f"Fila {fila} | "
            f"{ws.cell(fila, columna('Cliente')).value} | "
            f"{ws.cell(fila, columna('Artículo')).value} | "
            f"{ws.cell(fila, columna('País Destino')).value} | "
            f"Cantidad: {ws.cell(fila, columna('Cantidad')).value} | "
            f"Total: {ws.cell(fila, columna('Total')).value} €"
        )

def crear():
    print("\n=== CREAR PEDIDO ===")
    nueva_fila = ws.max_row + 1

    for campo in CAMPOS:
        valor = input(f"{campo}: ").strip()

        if campo == "Precio unidad":
            valor = float(valor)
        elif campo == "Cantidad":
            valor = int(valor)
        elif campo == "Descuento":
            valor = float(valor)

        ws.cell(nueva_fila, columna(campo), valor)

    recalcular_fila(nueva_fila)
    guardar()
    print(f"Pedido creado en la fila {nueva_fila}.")

def consultar():
    print("\n=== CONSULTAR PEDIDO ===")
    fila = int(input("Fila Excel: "))

    if fila < 2 or fila > ws.max_row:
        print("La fila no existe.")
        return

    for campo in cabeceras:
        print(f"{campo}: {ws.cell(fila, columna(campo)).value}")

def actualizar():
    print("\n=== ACTUALIZAR PEDIDO ===")
    fila = int(input("Fila Excel: "))

    if fila < 2 or fila > ws.max_row:
        print("La fila no existe.")
        return

    campos_editables = [campo for campo in cabeceras if campo != "Total"]

    for numero, campo in enumerate(campos_editables, start=1):
        print(f"{numero}. {campo}")

    opcion = int(input("Campo que quieres modificar: "))

    if opcion < 1 or opcion > len(campos_editables):
        print("Opción incorrecta.")
        return

    campo = campos_editables[opcion - 1]
    actual = ws.cell(fila, columna(campo)).value

    print(f"Valor actual: {actual}")
    nuevo = input("Nuevo valor: ").strip()

    if campo == "Precio unidad":
        nuevo = float(nuevo)
    elif campo == "Cantidad":
        nuevo = int(nuevo)
    elif campo == "Descuento":
        nuevo = float(nuevo)

    ws.cell(fila, columna(campo), nuevo)
    recalcular_fila(fila)
    guardar()
    print("Pedido actualizado.")

def eliminar():
    print("\n=== ELIMINAR PEDIDO ===")
    fila = int(input("Fila Excel: "))

    if fila < 2 or fila > ws.max_row:
        print("La fila no existe.")
        return

    confirmar = input("¿Eliminar este pedido? (s/n): ").strip().lower()

    if confirmar == "s":
        ws.delete_rows(fila)
        guardar()
        print("Pedido eliminado.")
    else:
        print("Eliminación cancelada.")

def menu():
    while True:
        print("""
==============================
      CRUD DE PEDIDOS
==============================
1. Listar últimos pedidos
2. Crear pedido
3. Consultar pedido
4. Actualizar pedido
5. Eliminar pedido
6. Salir
""")

        opcion = input("Selecciona una opción: ").strip()

        try:
            if opcion == "1":
                listar()
            elif opcion == "2":
                crear()
            elif opcion == "3":
                consultar()
            elif opcion == "4":
                actualizar()
            elif opcion == "5":
                eliminar()
            elif opcion == "6":
                print("¡Hasta luego!")
                break
            else:
                print("Opción no válida.")
        except (ValueError, IndexError) as error:
            print(f"Error: {error}")

        input("\nPulsa Enter para continuar...")

recalcular_todo()

if __name__ == "__main__":
    menu()

