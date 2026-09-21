from services.cuenta import Cuenta
from services.int_en_decimal import int_en_decimal, decimal_en_int
from utils.limpiar_pantalla import limpiar
from validators.valor_validacion import pedir_importe


def menu():
    # Bucle principal del menú de la aplicación bancaria.
    limpiar()
    titular = Cuenta('Ana')  # Cuenta de ejemplo con titular inicial.
    while True:
        menu_list = ["0. Salir del programa", "1. Ingresar nombre de cliente", "2. Ingresar dinero",
                     "3. Retirar dinero", "4. Mostrar saldo"]
        print(f"{'Banco':^{29}}")
        print(
            "Utilice los números del menú.\n"
        )
        print("\n".join(menu_list))

        opcion = input("\nSeleccione una opción: ").strip().lower()

        match opcion:
            case "0":
                # Termina el bucle y cierra el programa.
                break
            case 1:
                # Nota: nunca coincide, la opción llega como str, no int.
                nombre = input("Ingrese el nombre del cliente: ")
                pass

            case "2":
                # Pide un importe, lo convierte a céntimos y lo deposita.
                valor = pedir_importe()
                valor = decimal_en_int(valor)
                valor = titular.depositar(valor)
                decimal = int_en_decimal(valor)
                print(f'Deposito exitoso: +{decimal[0]},{decimal[1]:02d}€')
                decimal = int_en_decimal(titular.get_saldo)
                print(f'Saldo actual: {decimal[0]},{decimal[1]:02d}€')

            case "3":
                # Pide un importe, lo convierte a céntimos y lo retira.
                valor = pedir_importe()
                valor = decimal_en_int(valor)
                valor = titular.retirar(valor)

                if titular and valor:
                    decimal = int_en_decimal(valor)
                    print(f'Retiro exitoso: -{decimal[0]},{decimal[1]:02d}€')
                    decimal = int_en_decimal(titular.get_saldo)
                    print(f'Saldo actual: {decimal[0]},{decimal[1]:02d}€')

                else:
                    # Retiro no permitido: fondos insuficientes o valor inválido.
                    print(f'Fondos insuficientes o cantidad no valida')
                    decimal = int_en_decimal(titular.get_saldo)
                    print(f'Saldo actual: {decimal[0]},{decimal[1]:02d}€')

            case "4":
                # Muestra el titular y el saldo actual.
                decimal = int_en_decimal(titular.get_saldo)
                print(f'Titular: {titular.get_titular} | Saldo actual: {decimal[0]},{decimal[1]:02d}€')

            case _:
                # Cualquier opción no reconocida.
                input(
                    "\nOpción inválida en el menú. Pulsa [ENTER] para volver al menú principal."
                )

        input('Pulsa [ENTER] para continuar...')
        limpiar()


if __name__ == '__main__':
    menu()
