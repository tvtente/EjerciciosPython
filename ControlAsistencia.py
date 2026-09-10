import json,re,time
from datetime import datetime
from BorroPantalla import Borro  # Desde la aplicación BorroPantalla importo la funcion.

FILE_NAME = "asistencia.json"
Borro()
# 1. Función 
def cargar_datos():
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# 2. Función
def guardar_datos(datos):
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)

# 3. Función
def validar_formato_hora(hora):
    patron = r"^([01]\d|2[0-3]):([0-5]\d)$"
    return bool(re.match(patron, hora))

# 4. Función
def validar_id_empleado(emp_id):
    patron = r"^[A-Z]{3}\d{3}$"
    return bool(re.match(patron, emp_id))

# 5. Función
def calcular_horas(entrada, salida):
    fmt = "%H:%M"
    t_entrada = datetime.strptime(entrada, fmt)
    t_salida = datetime.strptime(salida, fmt)
    diferencia = t_salida - t_entrada
    horas = diferencia.total_seconds() / 3600
    return round(horas, 2)

# 6. Función
def crear_registro():
    datos = cargar_datos()
    emp_id = input("ID del empleado (ej. EMP001): ").upper()
    if not validar_id_empleado(emp_id):
        print("❌ Formato de ID inválido. Debe ser 3 letras y 3 números (ej. EMP001).❌")
        time.sleep(5) # Aplico un Temporizador.
        Borro()
        return

# Gestionamos formato de fechas y horas.
    fecha = datetime.now().strftime("%Y-%m-%d")
    entrada = input("Hora de entrada (HH:MM): ")
    if not validar_formato_hora(entrada):
        print("Formato de hora inválido. Use HH:MM.")
        return

    salida = input("Hora de salida (HH:MM, presione Enter si queda pendiente): ")
    horas_trabajadas = 0.0
    if salida:
        if not validar_formato_hora(salida):
            print("Formato de hora de salida inválido.")
            return
        horas_trabajadas = calcular_horas(entrada, salida)

    nuevo_id = 1 if not datos else datos[-1]["id"] + 1

    registro = {
        "id": nuevo_id,
        "empleado": emp_id,
        "fecha": fecha,
        "entrada": entrada,
        "salida": salida if salida else "Pendiente",
        "horas_trabajadas": horas_trabajadas
    }

# Alta de registros en el archivo.
    datos.append(registro)
    guardar_datos(datos)
    print("Registro guardado exitosamente.")

# 7. Función
def leer_registros():
    datos = cargar_datos()
    if not datos:
        print("No hay registros en el sistema.")
        time.sleep(5) # Aplico un Temporizador.
        Borro()
        return
    for r in datos:
        print(f"ID: {r['id']} | Empleado: {r['empleado']} | Fecha: {r['fecha']} | Entrada: {r['entrada']} | Salida: {r['salida']} | Horas: {r['horas_trabajadas']}")

# 8. Función
def actualizar_registro():
    datos = cargar_datos()
    try:
        reg_id = int(input("Ingrese el ID del registro a actualizar: "))
    except ValueError:
        print("ID inválido.")
        return

    for r in datos:
        if r["id"] == reg_id:
            print(f"Registro encontrado: {r}")
            nueva_entrada = input(f"Nueva entrada [{r['entrada']}]: ") or r['entrada']
            if not validar_formato_hora(nueva_entrada):
                print("Hora de entrada inválida.")
                return
            
            nueva_salida = input(f"Nueva salida [{r['salida']}]: ") or r['salida']
            if nueva_salida != "Pendiente" and not validar_formato_hora(nueva_salida):
                print("Hora de salida inválida.")
                return

            r['entrada'] = nueva_entrada
            r['salida'] = nueva_salida
            if nueva_salida != "Pendiente":
                r['horas_trabajadas'] = calcular_horas(nueva_entrada, nueva_salida)
            else:
                r['horas_trabajadas'] = 0.0

            guardar_datos(datos)
            print("Registro actualizado correctamente.")
            return
    print("Registro no encontrado.")

# 9. Función
def eliminar_registro():
    datos = cargar_datos()
    try:
        reg_id = int(input("Ingrese el ID del registro a eliminar: "))
    except ValueError:
        print("ID inválido.")
        return

    nuevos_datos = [r for r in datos if r["id"] != reg_id]
    if len(nuevos_datos) == len(datos):
        print("Registro no encontrado.")
    else:
        guardar_datos(nuevos_datos)
        print("Registro eliminado correctamente.")

# 10. Función
def menu():
    while True:
        print("\n--- 🔑 CONTROL DE ASISTENCIA 🔑 ---\n")
        print("1. Registrar Entrada/Salida (Crear)")
        print("2. Ver Registros (Leer)")
        print("3. Actualizar Registro")
        print("4. Eliminar Registro")
        print("5. Salir")
        opcion = input("\nSeleccione una opción: ")
        # Creamos todo el CRUD
        if opcion == "1":
            crear_registro()
        elif opcion == "2":
            leer_registros()
        elif opcion == "3":
            actualizar_registro()
        elif opcion == "4":
            eliminar_registro()
        elif opcion == "5":
            Borro() # Borramos pantalla antes de salir.
            break
        else:
            print("Opción inválida en el menú.")

# Comienzo del program evitando interferencias de terceros. ❓
if __name__ == "__main__":
    menu()
    