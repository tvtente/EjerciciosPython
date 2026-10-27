# Aplicación de clientes con ttkbootstrap

## Versión básica para aprender (empieza aquí)

```bash
cd /home/tvt/MEGA/EjerciciosPython
uv run python Ejercicio985MySQLVentas/app/app_basica.py
```

`app_basica.py` es una aplicación pequeña en un único archivo, sin clases propias,
hilos, colas ni diseñador. Utiliza los métodos MySQL de la carpeta `db`.

1. Primero se definen las funciones `listar`, `seleccionar`, `crear`, `actualizar` y `eliminar`.
2. `main()` conecta con MySQL y crea la ventana, la tabla y las entradas.
3. Cada botón llama a una función mediante `command=...`.
4. `tabla.bind("<<TreeviewSelect>>", seleccionar)` copia la fila seleccionada al formulario.
5. `ventana.mainloop()` espera los clics del usuario.

La contraseña se pide en la terminal antes de abrir la ventana. Puedes configurar
la conexión con las variables `MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_USER`,
`MYSQL_PASSWORD` y `MYSQL_DATABASE`, igual que en los ejemplos de consola.

**Insertar** siempre crea un cliente nuevo, aunque haya una fila seleccionada.
**Actualizar** y **Eliminar** actúan sobre el ID seleccionado. **Limpiar** deja el
formulario vacío. Los campos opcionales vacíos se guardan como NULL.

En esta versión las consultas son síncronas: la ventana puede esperar mientras
MySQL responde. Es una simplificación para estudiar el flujo del código.
Las versiones completas y la interfaz Pygubu se conservan a continuación.

## Inicio rápido: ejecutar las aplicaciones con uv

Todos estos comandos se ejecutan desde la raíz del proyecto:

```bash
cd /home/tvt/MEGA/EjerciciosPython

# Interfaz editable con Pygubu: conectar con MySQL.
uv run python Ejercicio985MySQLVentas/app/app_pygubu.py

# La misma interfaz con datos de demostración, sin MySQL.
uv run python Ejercicio985MySQLVentas/app/app_pygubu.py --demo

# Interfaz original creada directamente con ttkbootstrap.
uv run python Ejercicio985MySQLVentas/app/app.py

# Interfaz original en modo demostración.
uv run python Ejercicio985MySQLVentas/app/app.py --demo

# Abrir el diseño visual en Pygubu Designer.
uv run --extra designer pygubu-designer Ejercicio985MySQLVentas/app/clientes.ui
```

Ejecuta solo el comando de la aplicación que quieras abrir. El modo demostración
no necesita conexión y no guarda cambios en la base. Si acabas de modificar el
código o el diseño, cierra la ventana y vuelve a ejecutar el comando.

Interfaz de escritorio para la tabla `ventas.cliente`, con MySQL Connector/Python.

## Ejecutar

Desde `/home/tvt/MEGA/EjerciciosPython`:

```bash
uv sync
uv run python Ejercicio985MySQLVentas/app/app.py
```

En el formulario de conexión, indica servidor, puerto, base, usuario y contraseña. El puerto predeterminado es 3306; para el MySQL de Docker usa 3307 si es el puerto publicado por tu contenedor. Pulsa **Conectar** para cargar los clientes. La contraseña no se guarda en archivos.

Se pueden rellenar los campos mediante las variables de entorno `MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_DATABASE`, `MYSQL_USER` y `MYSQL_PASSWORD`. La aplicación no lee la configuración MCP. La base y su tabla deben existir; la interfaz no ejecuta scripts de recreación.

Para probar sin MySQL:

```bash
uv run python Ejercicio985MySQLVentas/app/app.py --demo
```

La demostración utiliza tres clientes en memoria y no conserva los cambios al cerrar. Su búsqueda es una aproximación sencilla: no reproduce las colaciones ni los comodines SQL.

## Operaciones

- **Consultar:** carga la lista al conectar. Busca por ID numérico o por parte del nombre/apellidos. **Ver todos** elimina el filtro. En MySQL, `%` y `_` se interpretan como comodines de LIKE.
- **Crear:** pulsa **Nuevo / limpiar**, completa el formulario y pulsa **Crear cliente**. El ID se genera automáticamente.
- **Editar:** selecciona una fila, modifica los campos y pulsa **Guardar cambios**. Puedes editar nombre, ambos apellidos, ciudad y categoría.
- **Eliminar:** selecciona una fila y pulsa **Eliminar cliente**. Se solicita confirmación. En el esquema actual, `ON DELETE CASCADE` elimina también los pedidos asociados a ese cliente.
- **Validar:** nombre y primer apellido obligatorios, longitudes acordes al esquema, categoría entera no negativa. Segundo apellido, ciudad y categoría vacíos se guardan como NULL.
- **Atajos:** Ctrl+F enfoca la búsqueda; Ctrl+N prepara un nuevo cliente.

Cada operación abre y cierra una conexión. Las modificaciones usan commit o rollback. La conexión y las consultas se ejecutan en un hilo de trabajo para mantener la ventana disponible; solo el hilo principal actualiza los controles. No se permite cerrar la ventana durante una operación en curso.

## Archivos y reutilización

- `app.py`: ventana, tabla, formulario, conexión y eventos.
- `clientes_datos.py`: validación y repositorios MySQL/demostración.
- `../db/consultar_cliente.py`: búsqueda mediante parámetros.
- `../db/insertar_cliente.py`: inserción y recuperación del ID.
- `../db/actualizar_cliente.py`: se añadió `actualizar_cliente_completo`, sin cambiar el método original que actualiza ciudad y categoría.
- `../db/eliminar_cliente.py`: borrado por ID.

Se validaron los flujos de la interfaz en modo demostración y el repositorio MySQL con una tabla temporal. No se modificaron clientes ni pedidos reales durante las pruebas.

## Ejecución con uv (opción recomendada)

El proyecto y el archivo de bloqueo se comparten con todos los ejercicios y están en `/home/tvt/MEGA/EjerciciosPython`, no en esta carpeta.

Desde esa raíz:

```bash
uv run python Ejercicio985MySQLVentas/app/app.py
uv run python Ejercicio985MySQLVentas/app/app_pygubu.py
uv run python Ejercicio985MySQLVentas/app/app_pygubu.py --demo
```

## Interfaz editable en Pygubu

```bash
uv run --extra designer pygubu-designer Ejercicio985MySQLVentas/app/clientes.ui
```

- `clientes.ui`: diseño XML editable; contiene widgets, columnas, variables, comandos y bindings.
- `app_pygubu.py`: carga el XML y conecta sus callbacks con `builder.connect_callbacks(self)`.
- `ClientesPygubuApp` hereda de `ClientesApp`: ambas versiones ejecutan la misma lógica CRUD y utilizan el mismo repositorio.
- El estilo se aplica con ttkbootstrap; los widgets estándar del XML permiten abrirlo en el diseñador sin un plugin personalizado.

### Conexiones de eventos y métodos

| Control o evento          | Callback                                          | Operación                                   |
| ------------------------- | ------------------------------------------------- | -------------------------------------------- |
| Conectar                  | `conectar`                                      | Crea `ClientesMySQL` y carga la lista      |
| Buscar                    | `buscar`                                        | Llama a `repositorio.listar` con el filtro |
| Ver todos                 | `ver_todos`                                     | Borra el filtro y consulta de nuevo          |
| Crear / Guardar cambios   | `guardar`                                       | Valida y llama a `repositorio.guardar`     |
| Nuevo / limpiar           | `nuevo`                                         | Limpia el formulario y la selección         |
| Eliminar                  | `eliminar`                                      | Confirma y llama a `repositorio.eliminar`  |
| Enter en búsqueda        | `on_buscar_enter`                               | Ejecuta `buscar`                           |
| Enter en contraseña      | `on_conectar_enter`                             | Ejecuta `conectar`                         |
| Enter en categoría       | `on_guardar_enter`                              | Ejecuta `guardar`                          |
| `<<TreeviewSelect>>`    | `_seleccionar`                                  | Carga el cliente en el formulario            |
| Doble clic en la tabla    | `on_editar_doble_click`                         | Selecciona y enfoca Nombre                   |
| Barras de desplazamiento  | `on_scroll_vertical` / `on_scroll_horizontal` | Desplazan la tabla                           |
| Cambios de vista de tabla | `on_tabla_yview` / `on_tabla_xview`           | Actualizan las barras                        |

Ctrl+F, Ctrl+N y el cierre de ventana se conectan en la clase base, porque pertenecen a la ventana principal ttkbootstrap y el XML tiene un Frame como raíz. Los cambios de disposición se hacen en el `.ui`; la lógica de base de datos permanece en Python.

Ejemplo de comando guardado en el XML:

```xml
<property name="command" type="command" cbtype="simple">guardar</property>
```

Ejemplo de binding:

```xml
<bind sequence="<Return>" handler="on_buscar_enter" add="+" />
```

No regeneres `app.py` desde el diseñador: ya contiene el controlador compartido. Edita y guarda `clientes.ui` y ejecuta `app_pygubu.py`. El controlador comprueba que no haya callbacks sin implementar al arrancar.
