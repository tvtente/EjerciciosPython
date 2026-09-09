"""Operaciones puras sobre la cesta de compra."""


def actualizar_cesta(cesta, clave, nombre, icono, precio, kg):
    """Añade, modifica o elimina un producto de la cesta."""
    if clave in cesta:
        nuevo_kg = round(cesta[clave]["kg"] + kg, 3)
        if nuevo_kg <= 0:
            del cesta[clave]
        else:
            cesta[clave]["kg"] = nuevo_kg
            cesta[clave]["total"] = round(nuevo_kg * precio, 2)
        return

    if kg > 0:
        cesta[clave] = {
            "icono": icono,
            "nombre": nombre,
            "pvp": precio,
            "kg": round(kg, 3),
            "total": round(precio * kg, 2),
        }


def total_cesta(cesta):
    """Calcula el importe total de la cesta."""
    return round(sum(item["total"] for item in cesta.values()), 2)
