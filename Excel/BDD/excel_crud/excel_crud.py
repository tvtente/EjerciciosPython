import re
import unicodedata
from dataclasses import make_dataclass, asdict

from openpyxl import load_workbook

from data.const import FILE_PATH


# ---------------------------------------------------------------------------
# Configuración de Excel
# ---------------------------------------------------------------------------

wb = load_workbook(FILE_PATH)
ws = wb[wb.sheetnames[0]]


# ---------------------------------------------------------------------------
# Creación de los campos a partir de las cabeceras de Excel
# ---------------------------------------------------------------------------

def normalize_name(value: str) -> str:
    """
    Convierte una cabecera de Excel en un nombre de campo válido para Python.
    """
    value = str(value)

    # Normalizar Unicode
    value = unicodedata.normalize("NFKC", value)

    # Eliminar espacios al principio y al final
    value = value.strip()

    # Reemplazar cualquier secuencia de espacios por "_"
    value = re.sub(r"\s+", "_", value)

    # Eliminar caracteres que no sean válidos en identificadores
    value = re.sub(r"[^a-zA-Z0-9_]", "", value)

    # Un identificador no puede comenzar por un número
    if value and value[0].isdigit():
        value = "_" + value

    if not value:
        raise ValueError(
            "La cabecera de Excel produce un nombre de campo vacío."
        )

    return value.lower()


# Obtener las cabeceras de la primera fila
headers = next(ws.iter_rows(values_only=True))

field_names = []

for header in headers:
    name = normalize_name(header)

    # Evitar nombres de campos duplicados
    original_name = name
    counter = 2

    while name in field_names:
        name = f"{original_name}_{counter}"
        counter += 1

    field_names.append(name)


# Crear dinámicamente la clase TableHeader
TableHeader = make_dataclass(
    "TableHeader",
    [(name, object, None) for name in field_names],
)


# ---------------------------------------------------------------------------
# Funciones auxiliares
# ---------------------------------------------------------------------------

def get_records():
    """
    Lee todas las filas de Excel y las convierte en objetos TableHeader.
    """
    records = []

    for row in ws.iter_rows(
        min_row=2,
        values_only=True,
    ):
        # Ignorar filas completamente vacías
        if all(value is None for value in row):
            continue

        values = list(row)

        # Completar la fila si tiene menos valores que columnas
        values += [None] * (len(field_names) - len(values))

        records.append(
            TableHeader(*values[:len(field_names)])
        )

    return records


def save():
    """
    Guarda los cambios en el archivo Excel.
    """
    wb.save(FILE_PATH)


def print_record(record, index=None):
    """
    Muestra un registro por pantalla.
    """
    if index is not None:
        print(f"\n[{index}]")

    for field, value in asdict(record).items():
        print(f"  {field}: {value}")


def display_records(records):
    """
    Muestra todos los registros.
    """
    if not records:
        print("\nNo se encontraron registros.")
        return

    print()

    for index, record in enumerate(records, start=1):
        print_record(record, index)


def write_record(row_number, record):
    """
    Escribe un objeto TableHeader en una fila de Excel.
    """
    values = list(asdict(record).values())

    for column, value in enumerate(values, start=1):
        ws.cell(
            row=row_number,
            column=column,
            value=value,
        )


# ---------------------------------------------------------------------------
# Operaciones CRUD
# ---------------------------------------------------------------------------

def create_record():
    """
    Crea un nuevo registro.
    """
    print("\n=== Crear registro ===")

    values = []

    for field in field_names:
        value = input(f"{field}: ")

        if value == "":
            value = None

        values.append(value)

    record = TableHeader(*values)

    # Buscar la siguiente fila disponible
    row_number = ws.max_row + 1

    write_record(row_number, record)
    save()

    print("\nRegistro creado correctamente.")


def read_records():
    """
    Muestra todos los registros.
    """
    print("\n=== Lista de registros ===")

    records = get_records()
    display_records(records)


def update_record():
    """
    Actualiza un registro existente.
    """
    print("\n=== Actualizar registro ===")

    records = get_records()

    if not records:
        print("No hay registros para actualizar.")
        return

    display_records(records)

    try:
        index = int(
            input("\nIntroduce el número del registro: ")
        )
    except ValueError:
        print("Número no válido.")
        return

    if not 1 <= index <= len(records):
        print("El registro no existe.")
        return

    record = records[index - 1]

    print("\nPulsa Enter para mantener el valor actual.")

    updated_values = []

    for field in field_names:
        current_value = getattr(record, field)

        value = input(
            f"{field} [{current_value}]: "
        )

        if value == "":
            value = current_value

        updated_values.append(value)

    updated_record = TableHeader(*updated_values)

    # La fila de Excel es el índice del registro + 1
    excel_row = index + 1

    write_record(excel_row, updated_record)
    save()

    print("\nRegistro actualizado correctamente.")


def delete_record():
    """
    Elimina un registro.
    """
    print("\n=== Eliminar registro ===")

    records = get_records()

    if not records:
        print("No hay registros para eliminar.")
        return

    display_records(records)

    try:
        index = int(
            input("\nIntroduce el número del registro: ")
        )
    except ValueError:
        print("Número no válido.")
        return

    if not 1 <= index <= len(records):
        print("El registro no existe.")
        return

    record = records[index - 1]

    print("\nRegistro que se va a eliminar:")
    print_record(record)

    confirmation = input(
        "\n¿Estás seguro? [s/N]: "
    ).strip().lower()

    if confirmation != "s":
        print("Eliminación cancelada.")
        return

    # La fila de Excel es el índice del registro + 1
    excel_row = index + 1

    ws.delete_rows(excel_row, 1)
    save()

    print("\nRegistro eliminado correctamente.")


# ---------------------------------------------------------------------------
# Menú
# ---------------------------------------------------------------------------

def show_menu():
    """
    Muestra el menú principal.
    """
    print(
        """
==============================
       Aplicación CRUD Excel
==============================

1. Listar registros
2. Crear registro
3. Actualizar registro
4. Eliminar registro
5. Salir
"""
    )


def main():
    """
    Punto de entrada principal de la aplicación.
    """
    while True:
        show_menu()

        choice = input("Selecciona una opción: ").strip()

        if choice == "1":
            read_records()

        elif choice == "2":
            create_record()

        elif choice == "3":
            update_record()

        elif choice == "4":
            delete_record()

        elif choice == "5":
            print("¡Hasta luego!")
            break

        else:
            print("Opción no válida.")

        input("\nPulsa Enter para continuar...")


if __name__ == "__main__":
    main()