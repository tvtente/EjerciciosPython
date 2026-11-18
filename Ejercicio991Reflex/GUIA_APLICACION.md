# Aprende Reflex: panel de ventas

## Arranque

Desde `/home/tvt/MEGA/EjerciciosPython/Ejercicio991Reflex`, con el entorno de Python que tiene Reflex instalado:

```bash
source ../.venv/bin/activate
reflex run
```

Abre la dirección que aparece en la terminal, normalmente http://localhost:3000.
La página `/` muestra el contador visual construido con las clases y funciones originales; `/ejemplos` también abre el contador. El tutorial de ventas está en `/tutorial`.

## Archivos

- `Ejercicio991Reflex/Ejercicio991Reflex.py`: ejemplos anteriores y registro de las dos páginas.
- `Ejercicio991Reflex/tutorial.py`: nueva aplicación, separada en estado y componentes.
- `rxconfig.py`: configuración del proyecto.

## Recorrido práctico

1. Escribe tu nombre: `on_change` ejecuta `set_preview` y la vista muestra el valor actualizado.
2. Marca la casilla y observa el cambio del mensaje. `checked` lee un booleano del estado.
3. Prueba «Aviso breve»: `rx.toast` muestra una notificación temporal.
4. Abre «Abrir mensaje»: `rx.dialog` muestra una ventana con un botón para cerrarla.
5. Registra una venta con cliente, categoría, importe y estado de cobro.
6. Observa cómo aumentan las tarjetas, la gráfica y las filas de la tabla.
7. Busca un cliente o filtra por categoría: todos los indicadores usan las ventas visibles.
8. Marca una venta como cobrada: cambia la cifra cobrada y el porcentaje por número de ventas.
9. Prueba «Borrar todas las ventas»: `rx.alert_dialog` pide confirmación antes de ejecutar el evento. Afecta a todas las ventas de la sesión, incluso a las filtradas.
10. Usa «Restaurar ejemplos» para volver a los tres registros iniciales.

## Qué hace cada bloque de código

### Datos: Sale

Una `dataclass` define cada venta: identificador, cliente, categoría, importe en céntimos y booleano de cobro. Guardar céntimos enteros evita acumular errores de cálculo con decimales binarios.

### Estado: DashboardState

La lista `sales` es la fuente de datos. `search` y `category` guardan los filtros; `preview` y `confirmed` sirven para practicar controles; `error` contiene el mensaje de validación.

### Eventos: @rx.event

Son métodos que reaccionan a acciones del usuario. Dentro de ellos se usa `self`. `save_sale` recibe los datos del formulario, valida y añade una venta. `toggle_paid` cambia su estado de cobro. El formulario conserva lo escrito para permitir corregir errores.

Los controles del formulario tienen `name`; esa clave permite recuperar cada valor desde el diccionario de `on_submit`. La validación HTML ayuda en el navegador y el evento vuelve a comprobar los datos en el servidor.

### Valores calculados: @rx.var

`visible_sales` aplica la búsqueda y la categoría. `total_count`, `total`, `paid_total`, `paid_percent` y `chart_data` se calculan desde esas ventas. Así no tienes que actualizar manualmente cada tarjeta cuando cambia un registro.

`paid_percent` mide el porcentaje de registros cobrados, no el porcentaje del importe cobrado.

### Interfaz: funciones que devuelven componentes

- `panel`: contenedor reutilizable con título, explicación y estilos CSS.
- `controls`: entrada de texto, casilla y mensajes.
- `sales_form`: formulario de alta de ventas.
- `metric`: tarjeta de indicador reutilizable.
- `sale_row`: representación de una venta en la tabla.
- `dashboard`: filtros, métricas, barra de progreso, gráfica y tabla.
- `tutorial_index`: reúne toda la pantalla.

En la interfaz se utiliza `DashboardState.campo`. `rx.foreach` dibuja cada fila de la lista y `rx.cond` elige qué mostrar según una condición reactiva.

## Estilos

Se combinan propiedades de componentes (`size`, `variant`, `color_scheme`) con CSS (`padding`, `border_radius`, `background_color`, `gap`). `rx.breakpoints` adapta las columnas a móvil y escritorio.

## Limitaciones del ejemplo

Los registros son ficticios y pertenecen al estado de cada sesión. No hay almacenamiento permanente, inicio de sesión ni datos compartidos entre usuarios. El botón de restauración reemplaza los registros actuales por los ejemplos iniciales.

## Siguientes ejercicios

Añade un campo de observaciones a `Sale` y al formulario. Después crea un filtro de cobro. Como siguiente paso más avanzado, sustituye la lista por una base de datos para conservar las ventas.
