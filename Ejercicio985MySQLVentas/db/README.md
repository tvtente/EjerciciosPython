# CRUD de clientes: MySQL directo y SQLAlchemy

Estos ejemplos trabajan con `ventas.cliente` y complementan los dos scripts de inserción existentes. La tabla debe estar creada previamente.

| Operación | mysql.connector | SQLAlchemy ORM |
|---|---|---|
| Crear | insertar_cliente.py | insertar_cliente_sqlalchemy.py |
| Consultar | consultar_cliente.py | consultar_cliente_sqlalchemy.py |
| Actualizar | actualizar_cliente.py | actualizar_cliente_sqlalchemy.py |
| Eliminar | eliminar_cliente.py | eliminar_cliente_sqlalchemy.py |

## Preparación

Desde `/home/tvt/MEGA/EjerciciosPython`, utilizando el entorno uv compartido:

```bash
uv sync
```

Los nuevos scripts usan `conexion_mysql.py` y `conexion_sqlalchemy.py`. Admiten las variables `MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_USER`, `MYSQL_PASSWORD` y `MYSQL_DATABASE`. Por defecto conectan a `127.0.0.1:3306`, usuario `root`, base `ventas`. Si no defines `MYSQL_PASSWORD`, solicitan la contraseña sin mostrarla. No leen las credenciales de MCP.

```bash
# Si necesitas el servidor Docker, cambia el puerto antes de ejecutar:
export MYSQL_PORT=3307
```

`insertar_cliente.py` también utiliza la conexión compartida. El ejemplo de inserción SQLAlchemy conserva su configuración mediante las mismas variables de entorno.

## Insertar con mysql.connector

Sin argumentos inserta a Lucía Gómez Martínez, de Valencia, categoría 150:

```bash
uv run python Ejercicio985MySQLVentas/db/insertar_cliente.py
```

Puedes pasar otros datos:

```bash
uv run python Ejercicio985MySQLVentas/db/insertar_cliente.py --nombre "Ana" --apellido1 "López" --apellido2 "Ruiz" --ciudad "Madrid" --categoria 200
```

La función `insertar_cliente(conexion, nombre, apellido1, apellido2=None, ciudad=None, categoria=None)` devuelve el ID asignado. Quien la llama controla el commit o rollback; `main` lo hace automáticamente. Los argumentos no indicados en la terminal conservan los valores del ejemplo.

## Consultar

```bash
uv run python Ejercicio985MySQLVentas/db/consultar_cliente.py
uv run python Ejercicio985MySQLVentas/db/consultar_cliente.py --id 1
uv run python Ejercicio985MySQLVentas/db/consultar_cliente.py --nombre "Lucía"

uv run python Ejercicio985MySQLVentas/db/consultar_cliente_sqlalchemy.py --nombre "Lucía"
```

Ambos filtros son opcionales. Si se proporcionan ID y nombre, deben cumplirse ambos. El nombre busca también en los apellidos, incluso cuando el segundo apellido es NULL. `%` y `_` conservan su significado como comodines de LIKE.

## Actualizar

Indica el ID, la nueva ciudad y la nueva categoría:

```bash
uv run python Ejercicio985MySQLVentas/db/actualizar_cliente.py 51 "Barcelona" 200
uv run python Ejercicio985MySQLVentas/db/actualizar_cliente_sqlalchemy.py 51 "Barcelona" 200
```

Solo se actualizan Ciudad y Categoria, y solo para el ID indicado. Si no existe, se informa sin crear un registro. Los ejemplos no garantizan que el ID 51 exista; elige un cliente consultándolo primero.

## Eliminar

```bash
uv run python Ejercicio985MySQLVentas/db/eliminar_cliente.py 51
uv run python Ejercicio985MySQLVentas/db/eliminar_cliente_sqlalchemy.py 51
```

En el esquema de `ventas 1.sql`, la relación de `pedido` con `cliente` tiene `ON DELETE CASCADE`: eliminar un cliente elimina también sus pedidos. Los comandos anteriores son alternativas para la misma operación, no pasos que haya que ejecutar consecutivamente.

## Diferencias en el código

- MySQL directo: cursor, SQL con parámetros `%s`, `commit`, `rollback` y cierre de recursos.
- SQLAlchemy: modelo `Cliente` reutilizado del script de inserción, `select`, `session.get`, asignación de atributos y `session.delete`. `session.begin()` confirma al salir y revierte ante una excepción.
- Las funciones reciben una conexión o sesión. La confirmación de la transacción se realiza desde `main`, lo que permite reutilizarlas en otra aplicación.
- Cada script tiene `--help`. Importar los módulos nuevos no ejecuta operaciones en la base.
