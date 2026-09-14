import re


def validar_formato_hora(hora):
    """Comprueba que una hora tenga el formato HH:MM entre 00:00 y 23:59.

    La expresión regular usa ^ y $ para exigir que toda la cadena sea una hora.
    ([01]\d|2[0-3]) acepta horas de 00 a 19 o de 20 a 23.
    : exige los dos puntos entre la hora y los minutos.
    ([0-5]\d) acepta minutos de 00 a 59.
    """
    patron = r"^([01]\d|2[0-3]):([0-5]\d)$"
    return bool(re.match(patron, hora))


def validar_id_empleado(emp_id):
    """Comprueba que el ID tenga tres letras y tres números."""
    patron = r"^[A-Z]{3}\d{3}$"
    return bool(re.match(patron, emp_id))
