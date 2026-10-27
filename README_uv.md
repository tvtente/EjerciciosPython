# Un entorno uv para todos los ejercicios

`pyproject.toml` y `uv.lock` están en la raíz de `EjerciciosPython`. Las carpetas de ejercicios utilizan el mismo entorno `.venv` de la raíz. No hace falta un proyecto uv por ejercicio.

## Preparar el entorno compartido

```bash
cd /home/tvt/MEGA/EjerciciosPython
uv sync
```

Las dependencias comunes incluyen MySQL Connector, SQLAlchemy, ttkbootstrap, Pygubu, pandas, openpyxl y reportlab. Tkinter/Tk debe estar disponible en el intérprete o sistema.

El editor visual Pygubu es opcional:

```bash
uv sync --extra designer
```

Para el ejercicio de Qt, sin instalarlo en los demás casos:

```bash
uv sync --extra qt
uv run --extra qt python ttkbootstrap/control_eventos_pyside6.py
```

Puedes combinar extras: `uv sync --extra designer --extra qt`.

## Ejecutar ejercicios

Desde la raíz, sin activar manualmente el entorno:

```bash
uv run python Ejercicio985MySQLVentas/db/consultar_cliente.py --nombre "Lucía"
uv run python Ejercicio985MySQLVentas/app/app.py
uv run python Ejercicio985MySQLVentas/app/app_pygubu.py
uv run python Ejercicio985MySQLVentas/app/app_pygubu.py --demo
```

Abrir la interfaz en el editor:

```bash
uv run --extra designer pygubu-designer Ejercicio985MySQLVentas/app/clientes.ui
```

Desde una subcarpeta uv busca el proyecto en las carpetas superiores:

```bash
cd Ejercicio985MySQLVentas/app
uv run python app_pygubu.py --demo
```

La búsqueda del proyecto funciona por directorios superiores, pero las rutas de los argumentos de Python siempre se interpretan desde tu directorio actual.

## Añadir una biblioteca

Ejecuta desde la raíz:

```bash
uv add nombre_del_paquete
```

Esto actualiza `pyproject.toml`, `uv.lock` y el entorno compartido. No edites `uv.lock` manualmente. Para ejecutar manteniendo exactamente las versiones bloqueadas, usa `uv run --locked ...`.

## Pruebas de Pygubu

Con un escritorio gráfico disponible:

```bash
uv run python -m unittest discover -s Ejercicio985MySQLVentas/app/tests -v
```

Estas pruebas usan datos en memoria, no conectan a MySQL y comprueban botones, selección, búsqueda con Enter y conexión simulada.
