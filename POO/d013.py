
import platform
import random
import subprocess
import time


def Borro():
    if platform.system() == "Windows":
        subprocess.run(["cls"], check=False, shell=True)
    else:
        subprocess.run(["clear"], check=False)

Borro()

class Cuenta_Bancaria:
    saldo = 0

    def __init__(self, titular, numero_cuenta, tipo_cuenta="Ahorro"):
        self.titular = titular
        self.numero_cuenta = numero_cuenta
        self.tipo_cuenta= tipo_cuenta

    def mostrar_saldo(self):
        
        print("===MOSTRAR SALDO===")
        print(f"Titular de la cuenta: {self.titular}")
        print(f"Tipo de Cuenta: {self.tipo_cuenta}")
        print(f"Número de cuenta: {self.numero_cuenta} ")
        print(f"Este es tu saldo: {self.saldo}€\n")

    def depositar_saldo(self, deposito):
        Borro()
        if deposito >= 5:
            self.saldo = self.saldo + deposito
            print("Saldo ingresado.\n")
        else:
            print("Ingreso mínimo 5€.\n")   

        self.mostrar_saldo()
        time.sleep(4) 

    def retirar_saldo(self, retiro):
        Borro()
        if self.saldo >= retiro:  # Se cambia a >= para permitir retirar el total disponible
            self.saldo = self.saldo - retiro
            self.mostrar_saldo()
        else:
            print("No puede retirar mas de su saldo actual\n")
        time.sleep(4)  
    
    

##################################################################################

Cuenta_Oksana = None  # Para almacenar la cuenta que se crea en la Opción 1

def validar_tipo_cuenta():
    while True:
        tipo_cuenta = input("Ingrese su tipo de cuenta: ").capitalize ()
        if tipo_cuenta in["Ahorros", "Corriente"]:
            return tipo_cuenta
        print("Su cuenta debe ser Ahorros o Corriente")

while True:
    print("========================")
    print("1. Crear cuenta: ")
    print("2. Ingresar saldo: ")
    print("3. Retirar saldo: ")
    print("0. Salir")
    print("========================")

    opcion = input("Seleccione una opción: ").strip()

    if opcion == "1":
        Borro()
        cuenta_bancaria = input("Ingresa el nombre del titular: ")
        numero_cuenta = random.randint(10_000_000_000, 99_999_999_999)
        tipo_cuenta=validar_tipo_cuenta()
        Cuenta_Oksana = Cuenta_Bancaria(cuenta_bancaria.title(), numero_cuenta, tipo_cuenta)
        print("\nCuenta creada")
        Cuenta_Oksana.mostrar_saldo()
        

    elif opcion == "2":
        if Cuenta_Oksana is not None:
            try:
                monto = int(input("Ingrese la cantidad a depositar (€): "))
                Cuenta_Oksana.depositar_saldo(monto)
            except ValueError:
                print("❌ Ingrese un valor numérico válido.\n")
        else:
            print("\n❌ Primero debe crear una cuenta (Opción 1).\n")

    elif opcion == "3":
        if Cuenta_Oksana is not None:
            try:
                monto = int(input("Ingrese la cantidad a retirar (€): "))
                Cuenta_Oksana.retirar_saldo(monto)
            except ValueError:
                print("❌ Ingrese un valor numérico válido.\n")
        else:
            print("\n❌ Primero debe crear una cuenta (Opción 1).\n")

    elif opcion == "0":
        print("\n👋 ¡Gracias por usar el servicio bancario! Hasta luego.\n")
        break

    else:
        print("\n❌ Opción no válida. Intente de nuevo.\n")












