# Ejercicio 992 · CRUD de tareas con Reflex y SQLite

Aplicación reconstruida a partir de `video/frames`. Mantiene la lista de tareas del vídeo y añade edición de texto para completar Crear, Leer, Actualizar y Eliminar.

## Instalar y ejecutar

Necesitas Python 3.11 o posterior. Desde la carpeta de este proyecto, prepara el entorno local:

```bash
uv sync
source .venv/bin/activate
reflex run
```

Si no utilizas `uv`:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
reflex run
```

En Windows, activa el entorno con `.venv\Scripts\Activate.ps1`.

Abre **http://localhost:3001**. El backend usa **8001**. Mantén estos puertos libres o cambia conjuntamente `frontend_port`, `backend_port`, `api_url` y `deploy_url` en `rxconfig.py`.

El código se entrega sin entorno virtual, frontend compilado, estado temporal ni metadatos de instalación. Al instalar o ejecutar pueden reaparecer `.venv`, `.web`, `.states`, `reflex.lock` y `*.egg-info`: son archivos generados y están excluidos de Git y de las búsquedas.

`uv.lock` conserva las versiones de las dependencias para poder reproducir la instalación.

## Qué puedes hacer

- Añadir una tarea con título obligatorio y descripción opcional.
- Marcar o desmarcar su casilla de completada.
- Editar título y descripción manteniendo fecha y estado.
- Confirmar antes de eliminarla de la base de datos.
- Buscar por título/descripción y filtrar por estado.
- Pulsar Actualizar para consultar cambios realizados desde otra pestaña.

La base empieza vacía. Crea «Grabar vídeo» e «Ir al gimnasio» si quieres reproducir la demostración. Los datos se conservan al reiniciar el servidor.

## Archivos

```text
todo_app/
  models.py       # Modelo Todo: columnas, ID y fecha por instancia.
  database.py     # Engine propio, ruta de SQLite y creación inicial de tablas.
  repository.py   # CRUD con SQLModel, transacciones y validaciones.
  todo_app.py     # TodoState, eventos, formulario, tarjetas y diálogos.
rxconfig.py       # Nombre, tema oscuro y puertos.
tests/test_crud.py
RECONSTRUCCION_CAPTURAS.md
```

SQLite se crea automáticamente en `data/todos.db` al entrar en la aplicación. La ruta se calcula desde el proyecto, no desde la terminal. `TODO_DATABASE_URL` permite configurar otra conexión si se instala su driver; el flujo comprobado es SQLite local. No se ha tocado ninguna base de datos de otro ejercicio.

## Qué se completó o corrigió

Se conservaron nombres reconocibles del vídeo: `Todo`, `TodoState`, `load_todos`, `add_todo`, `toggle_complete`, `delete_todo`, `todo_item`, `todo_form`, `todo_list` e `index`.

- SQLModel sustituye a `rx.Model` y usa sesiones y engine propios, recomendados para aplicaciones nuevas de Reflex.
- La fecha usa `default_factory`, evitando compartir la hora de importación entre las tareas.
- Fechas guardadas en UTC y mostradas en Europe/Madrid.
- Setters explícitos para los controles: el Reflex actual no los genera automáticamente.
- Se limpian título y descripción solo después de guardar correctamente.
- La edición del texto y la confirmación de borrado completan el ejemplo.
- Límites de 160 caracteres para título y 3000 para descripción, verificados en servidor.

Consulta [RECONSTRUCCION_CAPTURAS.md](RECONSTRUCCION_CAPTURAS.md) para relacionar cada parte con las imágenes y distinguir lo visible de lo añadido.

## Persistencia y límites

Las tareas se comparten entre sesiones del mismo servidor; se actualizan al entrar, tras modificar o al pulsar Actualizar. No hay autenticación ni separación por usuario: es un ejercicio local. No se han implementado notificaciones en tiempo real entre pestañas.

`create_all` crea las tablas que falten sin borrar datos. No aplica cambios a columnas de tablas existentes: si amplías el modelo, utiliza migraciones o una base nueva conservando una copia de los datos.

## Comprobar

Desde esta carpeta y con el entorno activo:

```bash
reflex compile --dry
python -m unittest discover -s tests -v
```

Las pruebas usan bases SQLite temporales: verifican persistencia al reconectar, altas, lectura, edición, completado, borrado, validación, fechas, filtros y lectura desde otro estado. No escriben en tu base real. La compilación de Reflex, el build de producción (incluido prerender) y las cuatro pruebas pasan. La interacción visual final queda pendiente de revisión en el navegador.

## Guía HTML del código

Abre [la guía interactiva](entregables/guia_crud_interactiva.html) en un navegador para seguir los recorridos del CRUD, pulsar funciones y saltar a su código real. Incluye búsqueda, teoría, capturas y enlaces internos al código incluido. Funciona sin internet y sin arrancar Reflex.

La [presentación con enlaces al HTML](entregables/CRUD_Reflex_con_guia_HTML.pptx) debe permanecer en la misma carpeta que la guía. Consulta [las instrucciones de uso y actualización](entregables/LEEME_GUIA_CRUD.md).

Para actualizar el código incluido después de editar los archivos:

```bash
python3 scripts/generar_guia_crud.py
```
