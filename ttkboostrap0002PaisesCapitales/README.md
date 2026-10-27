# Países y capitales con Pygubu

Aplicación que lee los países y sus capitales desde un archivo JSON.
La interfaz se puede editar visualmente con **Pygubu Designer** y utiliza el
tema `flatly` de **ttkbootstrap** cuando se ejecuta.

## Archivos del proyecto

Los siguientes archivos deben permanecer juntos en esta misma carpeta:

- `paises_capitales.ui`: diseño visual creado con Pygubu.
- `paises_capitales.py`: lógica de la aplicación.
- `paises_capitales.json`: países y capitales.
- `paises_catalanes_intefaz.py`: generacion de código a partir de pygubu

## Abrir la pantalla en Pygubu Designer

Desde la carpeta principal ejecutar:

```Shell
uv run pygubu-designer "paises_capitales.ui"
```

## Binding del Combobox

El `Combobox` se llama `selector_pais`. En Pygubu debe tener este
binding en la sección **Bindings**:

| Propiedad | Valor                    |
| --------- | ------------------------ |
| Sequence  | `<<ComboboxSelected>>` |
| Handler   | `mostrar_capital`      |
| Add       | vacío                   |

Cuando se selecciona un país, Pygubu ejecuta el método `mostrar_capital` del archivo Python:

El argumento `evento=None` es necesario porque el binding entrega un evento,
mientras que el botón **Buscar** llama al mismo método sin argumentos.

## Generar código Python desde Pygubu

1. Guardar el `.ui` en pygubu.
2. Entrar en la pestaña **Code**.
3. En **Main widget**, seleccionar `contenedor`.
4. Escribir el nombre de la clase que se quiera generar.
5. Elegir **Application** para generar una aplicación basada en clases, o
   **Code Script** para producir una interfaz Python que no necesite el `.ui`
   durante la ejecución.
6. Pulsar **Generate**.
7. Revisar la vista previa y usar **Save** para guardar el código generado.

Es recomendable guardar el código generado con otro nombre, por ejemplo
`paises_catalanes_interfaz.py`. No se debe sobrescribir `paises_capitales.py`, porque
contiene la lectura del JSON y la lógica de las capitales. Una vez que se tiene
generada la interfaz generada usar un combinador de archivos para integrar las lógica
que basicamente es agregar la lectura del json.

## Ejecutar la aplicación

Desde la carpeta principal:

```Shell
uv run python "paises_capitales.py"
```
