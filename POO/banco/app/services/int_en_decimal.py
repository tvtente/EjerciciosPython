from decimal import Decimal, ROUND_HALF_UP


def int_en_decimal(valor: int) -> tuple[int, int]:
    # Convierte céntimos (int) a una tupla (euros, céntimos).
    return (valor // 100,
            valor % 100,)

def decimal_en_int(valor: Decimal) -> int:
    # Convierte un Decimal en euros a céntimos (int), redondeando.
    return int((valor * 100).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
