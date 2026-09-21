def validar_tipo_cuenta():
    """Solicita el tipo de cuenta hasta que sea Ahorros o Corriente."""
    while True:
        tipo_cuenta = input("Tipo de cuenta (Ahorros/Corriente): ").strip().capitalize()
        if tipo_cuenta in ("Ahorros", "Corriente"):
            return tipo_cuenta

        print("Tipo de cuenta no válido. Solo puede ser Ahorros o Corriente.")


class CuentaBancaria:
    """Representa una cuenta bancaria con titular, tipo y saldo."""

    def __init__(self, titular, tipo_cuenta, saldo=0):
        """Crea una cuenta con un titular, tipo y saldo inicial."""
        self.titular = titular
        self.tipo_cuenta = tipo_cuenta
        self.saldo = saldo

    def depositar(self, cantidad):
        """Suma una cantidad al saldo cuando es mayor que cero."""
        if cantidad > 0:
            self.saldo += cantidad
            print(f"Depósito exitoso: +{cantidad:.2f}€")
        else:
            print("Cantidad no válida.")

    def retirar(self, cantidad):
        """Resta una cantidad al saldo si es válida y existe saldo suficiente."""
        if cantidad <= 0:
            print("Cantidad no válida.")
        elif cantidad > self.saldo:
            print("Fondos insuficientes o cantidad no válida.")
        else:
            self.saldo -= cantidad
            print(f"Retiro exitoso: -{cantidad:.2f}€")

    def mostrar_saldo(self):
        """Muestra el titular, tipo y saldo actual de la cuenta."""
        print(
            f"Titular: {self.titular} | Tipo: {self.tipo_cuenta} | "
            f"Saldo actual: {self.saldo:.2f}€"
        )


def menu():
    """Muestra el menú y permite gestionar una cuenta bancaria."""
    cuenta = None

    while True:
        print("\n--- CUENTA BANCARIA ---")
        print("1. Crear cuenta")
        print("2. Ingresar saldo")
        print("3. Retirar saldo")
        print("4. Mostrar saldo")
        print("0. Salir")
        opcion = input("Elige una opción: ")

        if opcion == "1":
            titular = input("Nombre del titular: ").strip()
            if not titular:
                print("El titular no puede estar vacío.")
                continue

            tipo_cuenta = validar_tipo_cuenta()
            cuenta = CuentaBancaria(titular, tipo_cuenta)
            print(f"Cuenta {tipo_cuenta} creada para {titular}.")

        elif opcion in ("2", "3"):
            if cuenta is None:
                print("Primero debes crear una cuenta.")
                continue

            try:
                cantidad = float(input("Introduce la cantidad: ").replace(",", "."))
            except ValueError:
                print("Introduce una cantidad numérica válida.")
                continue

            if opcion == "2":
                cuenta.depositar(cantidad)
            else:
                cuenta.retirar(cantidad)

        elif opcion == "4":
            if cuenta is None:
                print("Primero debes crear una cuenta.")
            else:
                cuenta.mostrar_saldo()

        elif opcion == "0":
            print("Programa finalizado.")
            break

        else:
            print("Opción no válida.")


if __name__ == "__main__":
    menu()
