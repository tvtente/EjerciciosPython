import re


def validar_formato_hora(hora):
    """Devuelve ``True`` solo para horas válidas en formato estricto ``HH:MM``.

    Acepta desde ``00:00`` hasta ``23:59``: las horas ``00``–``19``
    se validan con ``[01][0-9]`` y las ``20``–``23`` con ``2[0-3]``.
    """
    if not isinstance(hora, str):
        return False

    patron = r"(?:[01][0-9]|2[0-3]):[0-5][0-9]"
    return re.fullmatch(patron, hora) is not None


def validar_id_empleado(emp_id):
    """Comprueba que el ID tenga tres letras y tres números."""
    patron = r"^[A-Z]{3}\d{3}$"
    return bool(re.match(patron, emp_id))
