import time
import os
from datetime import datetime
import Datospersonal

# --- CÓDIGOS DE COLORES ANSI ---
COLOR_ROJO = "\033[91m"
COLOR_AZUL = "\033[94m"
RESET_COLOR = "\033[0m"

# Subimos el ancho a 72 para dar margen holgado a todos los títulos y bordes
ANCHO = 72

def borrar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def imprimir_encabezado():
    borrar_pantalla()
    linea = "+" + "-" * (ANCHO - 2) + "+"
    print(linea)
    print("|" + "CONTROL DE ASISTENCIA".center(ANCHO - 2) + "|")
    print("|" + "[ MARCACIONES Y REGISTRO ]".center(ANCHO - 2) + "|")
    print(linea)

def pedir_hora(mensaje):
    while True:
        print(mensaje)
        hora_raw = input("  Formato (HH:MM) -> : ").strip()
        
        if len(hora_raw) == 4 and hora_raw.isdigit():
            hora_raw = f"{hora_raw[:2]}:{hora_raw[2:]}"
            
        if Datospersonal.validar_formato_hora(hora_raw):
            return hora_raw
            
        print(f"\n{COLOR_ROJO} [X] Error: Formato de hora inválido. Intente de nuevo.{RESET_COLOR}")
        time.sleep(1.5)

def crear_registro():
    while True:
        imprimir_encabezado()
        datos = Datospersonal.cargar_datos()
        
        msg = "[ MODO CONTINUO ] (Presione Enter para volver al menú)"
        print(f"\n{msg.center(ANCHO)}\n")
        
        while True:
            emp_id = input(" ID del empleado (ej. EMP001): ").upper().strip()
            
            if emp_id == "":
                return

            if Datospersonal.validar_id_empleado(emp_id):
                break
            
            print(f"\n{COLOR_ROJO} [X] Error: ID inválido (debe ser 3 letras y 3 números).{RESET_COLOR}")
            time.sleep(1.5)
            imprimir_encabezado()
            msg_sub = "[ MODO MARCACIÓN CONTINUA ] (Presione Enter en vacío para volver al menú)"
            print(f"\n{msg_sub.center(ANCHO)}\n")

        fecha = datetime.now().strftime("%Y-%m-%d")
        entrada = pedir_hora("\n Hora de Entrada:")
        nuevo_id = Datospersonal.obtener_nuevo_id(datos)

        registro = {
            "id": nuevo_id,
            "empleado": emp_id,
            "fecha": fecha,
            "entrada": entrada,
            "salida": "Pendiente",
            "horas_trabajadas": 0.0
        }

        datos.append(registro)
        Datospersonal.Datos_personal(datos)
        
        print(f"\n{COLOR_AZUL} [ok] Entrada registrada correctamente. ¡Gracias, {emp_id}!{RESET_COLOR}")
        time.sleep(2)

def leer_registros():
    imprimir_encabezado()
    datos = Datospersonal.cargar_datos()
    
    if not datos:
        print(f"\n{COLOR_ROJO} [X] No hay registros en el sistema.{RESET_COLOR}")
    else:
        # Formato de tabla ajustado para ocupar exactamente 72 caracteres
        print("\n+" + "-"*5 + "+" + "-"*13 + "+" + "-"*13 + "+" + "-"*10 + "+" + "-"*10 + "+" + "-"*13 + "+")
        print(f"| {'ID':<3} | {'Empleado':<11} | {'Fecha':<11} | {'Entrada':<8} | {'Salida':<8} | {'Horas':<11} |")
        print("+" + "-"*5 + "+" + "-"*13 + "+" + "-"*13 + "+" + "-"*10 + "+" + "-"*10 + "+" + "-"*13 + "+")
        
        for r in datos:
            print(f"| {r['id']:<3} | {r['empleado']:<11} | {r['fecha']:<11} | {r['entrada']:<8} | {r['salida']:<8} | {r['horas_trabajadas']:<11} |")
        
        print("+" + "-"*5 + "+" + "-"*13 + "+" + "-"*13 + "+" + "-"*10 + "+" + "-"*10 + "+" + "-"*13 + "+")
    
    input("\n Presione Enter para regresar al menú...")

def actualizar_registro():
    while True:
        imprimir_encabezado()
        datos = Datospersonal.cargar_datos()
        
        print(" [ Presione Enter sin escribir nada para volver al menú ]\n")
        entrada_id = input(" Ingrese el ID a actualizar: ").strip()
        
        if entrada_id == "":
            return

        try:
            reg_id = int(entrada_id)
        except ValueError:
            print(f"\n{COLOR_ROJO} [X] Error: ID inválido. Debe ingresar un número.{RESET_COLOR}")
            time.sleep(3)
            continue

        registro = Datospersonal.buscar_registro_por_id(datos, reg_id)

        if not registro:
            print(f"\n{COLOR_ROJO} [X] Código no es correcto!.{RESET_COLOR}")
            time.sleep(3)
            continue

        print(f"\n Registro actual: [{registro['empleado']}] Entrada: {registro['entrada']} | Salida: {registro['salida']}")
        
        if input("\n ¿Modificar entrada? (s/n): ").lower() == 's':
            registro['entrada'] = pedir_hora(" Nueva Entrada:")

        if input(" ¿Registrar/Modificar salida? (s/n): ").lower() == 's':
            registro['salida'] = pedir_hora(" Nueva Salida:")

        if registro['salida'] != "Pendiente":
            registro['horas_trabajadas'] = Datospersonal.calcular_horas(registro['entrada'], registro['salida'])

        Datospersonal.Datos_personal(datos)
        print(f"\n{COLOR_AZUL} [ok] Registro actualizado.{RESET_COLOR}")
        time.sleep(2)
        return

def eliminar_registro():
    imprimir_encabezado()
    datos = Datospersonal.cargar_datos()
    
    try:
        reg_id = int(input("\n Ingrese el ID del registro a eliminar: "))
    except ValueError:
        print(f"\n{COLOR_ROJO} [X] Error: ID inválido.{RESET_COLOR}")
        time.sleep(2)
        return

    nuevos_datos = [r for r in datos if r["id"] != reg_id]
    
    if len(nuevos_datos) == len(datos):
        print(f"\n{COLOR_ROJO} [X] Registro no encontrado.{RESET_COLOR}")
        time.sleep(2)
    else:
        Datospersonal.Datos_personal(nuevos_datos)
        print(f"\n{COLOR_ROJO} [-] Registro eliminado correctamente.{RESET_COLOR}")
        time.sleep(2)

def menu():
    linea = "+" + "-" * (ANCHO - 2) + "+"
    opciones = [
        "1. Registrar Entrada (Crear Marcación)",
        "2. Ver Registros de Asistencia (Leer)",
        "3. Actualizar Registro (Salida / Edición)",
        "4. Eliminar Registro",
        "5. Salir"
    ]
    
    while True:
        imprimir_encabezado()
        
        # Generar cuerpo del menú alineado exactamente dentro del marco
        for opcion in opciones:
            contenido = f"  {opcion}".ljust(ANCHO - 2)
            print(f"|{contenido}|")
            
        print(linea)
        
        opcion_user = input("\n Seleccione una opción (1-5): ").strip()
        
        if opcion_user == "1":
            crear_registro()
        elif opcion_user == "2":
            leer_registros()
        elif opcion_user == "3":
            actualizar_registro()
        elif opcion_user == "4":
            eliminar_registro()
        elif opcion_user == "5":
            borrar_pantalla()
            break
        else:
            print(f"\n{COLOR_ROJO} [X] Opción inválida.{RESET_COLOR}")
            time.sleep(2)

if __name__ == "__main__":
    menu()