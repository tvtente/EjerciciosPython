import platform
import re
import subprocess


def borro():
    """Limpia la consola en Windows, Linux y macOS."""
    if platform.system() == "Windows":
        subprocess.run(["cls"], shell=True)
    else:
        subprocess.run(["clear"])

def pedir_numero(mensaje):
    while True:
        try:
            numero = int(input(mensaje))

            if 1 <= numero <= 10:
                return numero  # Número correcto: termina la función

            print("Error: introduce un número entre 1 y 10.")

        except ValueError:
            print("Error: introduce solo números enteros.")


borro()
# Pedir n: tabla que se quiere consultar
tabla = pedir_numero("Introduce la tabla que quieres consultar (1-10): ")
# Pedir m: línea de la tabla que se quiere consultar
numero_fila = pedir_numero("Introduce la línea que quieres consultar (1-10): ")

nombre_fichero = f"tabla-{tabla}.txt"

try:
    # Intentar leer la tabla
    with open(nombre_fichero, "r", encoding="utf-8") as fichero:
        lineas = fichero.readlines()

except FileNotFoundError:
    # Si no existe, crearla
    print(f"La tabla del {tabla} no existe. Se va a crear.")

    with open(nombre_fichero, "w", encoding="utf-8") as fichero:
        for numero in range(1, 11):
            fichero.write(f"{tabla:<3} x {numero:<3} = {tabla * numero:<3}\n")

    # Leer la tabla recién creada
    with open(nombre_fichero, "r", encoding="utf-8") as fichero:
        lineas = fichero.readlines()


resultado = lineas[numero_fila - 1]

print(f"\nResultado: {resultado}")

with open("resultado_final.txt", "w", encoding="utf-8") as fichero_final:
    fichero_final.write(resultado)

print("Se ha creado el archivo resultado_final.txt")