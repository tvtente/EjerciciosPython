#<<<<<<<Calculadora con 4 operaciones basicas>>>>>>
import subprocess,platform,sys
def borrar_pantalla(): #Limpiamos la consola
    if platform.system() == "Windows":subprocess.run(["cls"], shell=True)
    else:subprocess.run(["clear"])

borrar_pantalla()
class Calculadora():
    def __init__(self, num1, num2):# Metodo constructor de instancias de clase
        self._num1= num1 #Primer atributo
        self._num2= num2 # Segundo atributo

    def suma(self):#Metodo de sumar (con el atributo self que siempre debe estar presente)
        while True:
            num1 = str(self._num1).strip()
            num2 = str(self._num2).strip()

            # Quitamos un posible signo negativo y comprobamos que el resto sean dígitos.
            if num1.lstrip("-").isdigit() and num2.lstrip("-").isdigit():
                self._num1 = int(num1)
                self._num2 = int(num2)
                resultado = self._num1 + self._num2
                print(
                    f"El resultado de la suma es: "
                    f"{self._num1} + {self._num2} = {resultado}"
                )
                break

            print("Por favor, asegúrese de que ambos valores sean numéricos.")
            self._num1 = input("Introduce el primer número entero: ")
            self._num2 = input("Introduce el segundo número entero: ")

    def resta(self): #metodo de restar (con el atributo self que siempre debe estar presente)
        try: #captamos errores de tipo
            resultado = self._num1 - self._num2
        except TypeError:
            print("Por favor, asegúrese de que ambos valores sean numéricos.")
        else:# Ejecutamos esto si no hay errores captados
            print(f"El resultado de la resta es: {self._num1} - {self._num2} = {resultado}")

    def division(self): #metodo de dividir (con el atributo self que siempre debe estar presente)
        try:
            resultado=self._num1 // self._num2
        except:
            print("Por favor, asegúrese de que ambos valores sean numéricos y que el segundo no sea 0")
        else:
            print(f"El resultado de la divisón es: {self._num1} // {self._num2} = {resultado}")

    def multiplicacion(self): #metodo de multiplicar (con el atributo self que siempre debe estar presente)
        try:
            resultado=self._num1 * self._num2
        except TypeError:
            print("Por favor, asegúrese de que ambos valores sean numéricos.")
        else:
            print(f"El resultado de la multiplicación es: {self._num1} * {self._num2} = {resultado}")

operacion=Calculadora(5, 10)# Creamos una instancia de clase Calculadora
operacion.suma()# Llamamos el metodo suma de la clase Calculadora

operacion=Calculadora(20, 5)# Creamos una otra instancia de clase Calculadora
operacion.resta()# Llamamos el metodo resta de la clase Calculadora

operacion=Calculadora(15, 3)# Creamos una otra instancia de clase Calculadora
operacion.division()# Llamamos el metodo division de la clase Calculadora

operacion=Calculadora(8, 4)# Creamos una otra instancia de clase Calculadora
operacion.multiplicacion()# Llamamos el metodo multiplicacion de la clase Calculadora

sys.exit(0)
