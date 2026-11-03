# Aplicaciones de clientes MySQL

Este ejercicio contiene tres aplicaciones para gestionar los clientes de la
base de datos `ventas`. Ejecuta los comandos desde la carpeta principal del
proyecto `EjerciciosPython`.

## Preparar el proyecto

Instala y sincroniza las dependencias:

```powershell
uv sync
```

## 1. Aplicación básica

Archivo: `app_basica.py`

Es la versión más sencilla para estudiar. Está escrita en un único archivo y
se conecta directamente a MySQL.

```powershell
uv run python "Ejercicio985MySQLVentas\app\app_basica.py"
```

La contraseña de MySQL se solicita en la terminal antes de abrir la ventana.
Esta versión no tiene modo de demostración.

## 2. Aplicación completa con ttkbootstrap

Archivo: `app.py`

Incluye conexión, búsqueda, tabla de clientes y operaciones para crear,
actualizar y eliminar registros.

### Con datos de prueba

```powershell
uv run python "Ejercicio985MySQLVentas\app\app.py" --demo
```

Este modo carga tres clientes en memoria, no necesita MySQL y no conserva los
cambios al cerrar.

### Con MySQL

```powershell
uv run python "Ejercicio985MySQLVentas\app\app.py"
```

Introduce en la ventana el servidor, puerto, base de datos, usuario y
contraseña. La base predeterminada es `ventas`.

## 3. Aplicación diseñada con Pygubu

Archivos: `app_pygubu.py` y `clientes.ui`

Tiene las mismas operaciones que la aplicación completa, pero la pantalla se
puede modificar visualmente con Pygubu Designer.

### Con datos de prueba

```powershell
uv run python "Ejercicio985MySQLVentas\app\app_pygubu.py" --demo
```

### Con MySQL

```powershell
uv run python "Ejercicio985MySQLVentas\app\app_pygubu.py"
```

### Abrir el diseño visual

```powershell
uv run pygubu-designer "Ejercicio985MySQLVentas\app\clientes.ui"
```

Los comandos y bindings de la interfaz están guardados en `clientes.ui`. La
lógica permanece en los archivos Python; no sobrescribas `app.py` ni
`app_pygubu.py` al generar código desde el diseñador.

## Configuración opcional de MySQL

Las aplicaciones aceptan estas variables de entorno:

- `MYSQL_HOST`
- `MYSQL_PORT`
- `MYSQL_DATABASE`
- `MYSQL_USER`
- `MYSQL_PASSWORD`

Ejemplo en PowerShell:

```powershell
$env:MYSQL_HOST = "127.0.0.1"
$env:MYSQL_PORT = "3306"
$env:MYSQL_DATABASE = "ventas"
$env:MYSQL_USER = "root"
uv run python "Ejercicio985MySQLVentas\app\app.py"
```

## Resumen

| Aplicación | Uso recomendado | Modo `--demo` |
|---|---|---|
| `app_basica.py` | Aprender el funcionamiento básico | No |
| `app.py` | Utilizar la interfaz completa | Sí |
| `app_pygubu.py` | Editar la pantalla con Pygubu | Sí |
