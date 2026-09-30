import subprocess
import platform
import time
import sys
import json
from pathlib import Path


RUTA_ESTUDIANTES = Path(__file__).with_name("estudiantes.json")


# FUNCIÓN:
def Borro():
    if platform.system() == "Windows":
        subprocess.run(["cls"], shell=True)
    else:
        subprocess.run(["clear"])


Borro()


# CLASE:
class Estudiante:
    # MÉTODO CONSTRUCTOR:
    def __init__(self, nombre, nota):
        self.nombre = nombre
        self.nota = nota

    # MÉTODO:
    def imprimir(self):
        print("=" * 16)
        print(f"Nombre: {self.nombre} \nTu nota es: {self.nota}")
        print("=" * 16)

    # MÉTODO:
    def resultados(self):
        if self.nota >= 5:
            print("\n¡ENHORABUENA HAS APROBADO!👏🎓")
            time.sleep(3)
        else:
            print(
                "\n Lo sentimos, no has aprobado. "
                "\n ¡Sigue estudiando y lo conseguirás seguro!😎"
            )
            time.sleep(3)


def guardar_estudiantes(estudiantes):
    """Guarda el diccionario de estudiantes en formato JSON."""
    with RUTA_ESTUDIANTES.open("w", encoding="utf-8") as archivo:
        json.dump(estudiantes, archivo, ensure_ascii=False, indent=4)


def leer_estudiantes():
    """Lee y devuelve el diccionario guardado en el archivo JSON."""
    with RUTA_ESTUDIANTES.open("r", encoding="utf-8") as archivo:
        return json.load(archivo)




# REGISTRO DE ESTUDIANTES
estudiantes = {
    "Pedro": 5,
    "Elizabeth": 7,
    "Laura": 4,
    "Sheila": 9,
}

# Guardamos el diccionario y lo volvemos a leer desde el archivo JSON.
guardar_estudiantes(estudiantes)
estudiantes = leer_estudiantes()

# IMPRIMIR:
print("-" * 20)  # LÍNEA DEL TÍTULO O CABECERA
print("\n NOTAS DE ALUMNOS🏫 \n")  # TÍTULO O CABECERA
print("-" * 20)  # LÍNEA DEL TÍTULO O CABECERA
print("\n¡Buenos días querido alumno!🧑‍🎓")


# BÚSQUEDA DEL ESTUDIANTE
estudiante_ingresado = (
    input("Indica tu nombre para saber tu nota: ").strip().lower().capitalize()
)

if estudiante_ingresado in estudiantes:
    estudiante = Estudiante(
        estudiante_ingresado,
        estudiantes[estudiante_ingresado],
    )
    estudiante.imprimir()
    estudiante.resultados()
else:
    print(
        f"El estudiante '{estudiante_ingresado}' "
        "no se encuentra en el registro."
    )

# CERRAR
sys.exit(0)
