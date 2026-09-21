import re
from decimal import Decimal

from errors.amount import AmountError
from utils.limpiar_pantalla import limpiar


def pedir_importe(mensaje="Ingrese el valor de la bancaria: "):
    # Pide un importe por consola hasta que sea válido.
    while True:
        try:
            return validar_importe(input(mensaje))
        except AmountError as e:
            print(e.args[0])
            input("Pulsa [ENTER] para continuar...")
            limpiar()


def validar_importe(valor: str) -> Decimal:
    # Acepta números enteros o con hasta 2 decimales (coma como separador).
    regex = r"(0|[1-9]\d*)(,\d{1,2})?"

    if valor is None or not valor.strip():
        raise AmountError("Introduce una cantidad.", code="entrada_vacia", raw_input=valor)

    valor_limpio = valor.strip()

    if not re.fullmatch(regex, valor_limpio):
        raise AmountError("Revisa el valor introducido.", code="format_invalido", raw_input=valor)

    # Se reemplaza la coma por punto para convertir a Decimal.
    valor_decimal = Decimal(valor_limpio.replace(",", "."))

    if valor_decimal <= 0:
        raise AmountError("La cantidad debe ser mayor que cero.", code="no_positivo", raw_input=valor_limpio)
    return valor_decimal
