"""
Se han eliminado las 3 primeras líneas, porque no se puede crear una instancia antes de definir la clase.
También se han corregido las indentaciones.
Se ha anulado una de las llamadas al método cumpleaños, para evitar un incremento de 2 años seguidos.
Se han separado los inputs de nombre y edad, para poder aplicar reglas de validación.
"""

import subprocess, platform, sys
def Borro():
    if platform.system()=="Windows": subprocess.run(["cls"], shell=True)
    else: subprocess.run(["clear"])

#1. Definimos la clase Persona.
class Persona:
    def __init__(self, nombre, edad): #2. Definimos el método constructor
        self.nombre = nombre
        self.edad = edad

    def cumpleaños(self): #3. Definimos los demás métodos. En este caso, cumpleaños().
        self.edad += 1

#4. Ejecución
Borro()
while True: # Validación del nombre, evita que el nombre se quede vacío
    nombreInput = input("Ingrese nombre: ").strip().title() 
    if not nombreInput:
        print("El nombre no puede estar vacío.\n")
        continue
    break

while True: # Validación de la edad
    try:
        edadInput = int(input("Ingrese edad: ").strip())
        if edadInput < 0:
            print("La edad no puede ser negativa.\n")
            continue
        break
    except ValueError:
        print("La edad debe ser un número entero positivo.\n")
        
#5. Creamos una instancia de la clase
p = Persona(nombreInput, edadInput)
p.cumpleaños()
print(f"\n{p.nombre} cumple {p.edad} años\n")

sys.exit(0)