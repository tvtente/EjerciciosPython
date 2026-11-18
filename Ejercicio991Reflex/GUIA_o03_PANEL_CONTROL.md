# o03 · Panel de control

Abre http://localhost:3000/o03_panel_control. La portada tiene un enlace al nuevo ejemplo.

## Práctica

1. Pulsa Añadir cliente y completa el diálogo con datos ficticios.
2. Al guardar, el diálogo se cierra y cambian tabla, indicadores y gráficas.
3. Busca el cliente por nombre, correo o ciudad. Las gráficas representan los mismos clientes visibles.
4. Pulsa Editar para cambiar sus datos. Los correos deben ser únicos, sin distinguir mayúsculas.
5. Pulsa Borrar y confirma; cancelar conserva la fila.
6. Limpia filtros para recuperar la vista completa. Restaurar ejemplos sustituye los registros de la sesión por los seis iniciales.

No hay base de datos ni envío de correos. Los datos cambian por sesión y no tienen persistencia permanente.

## Relación con el tutorial

El archivo `Ejercicio991Reflex/o03_panel_control.py` desarrolla la misma secuencia conceptual: modelo de fila con dataclass, lista en State, tabla dinámica mediante foreach, formulario en diálogo y transformación de datos para Recharts.

`Cliente` describe una fila. `PanelControlState.guardar_cliente` recibe las claves name del formulario y valida antes de cerrar el diálogo. `clientes_visibles` centraliza los filtros. `users_for_graph` utiliza Counter como en el tutorial, pero con una propiedad calculada @rx.var para actualizar también al editar, borrar y filtrar. Las columnas de la gráfica son name y value.

Se añaden ciudad, búsqueda, edición, confirmación de borrado y una segunda gráfica. El género se introduce explícitamente en el formulario; no se infiere de nombres ni correos.

## Ejercicios

- Cambia los colores de las barras en `grafica`.
- Añade una ciudad a CIUDADES y prueba su aparición en el formulario y la gráfica.
- Añade un campo a Cliente y sigue su recorrido por el formulario, evento y fila.
- Compara la gráfica de clientes visibles con otra calculada sobre todos los clientes.

Compilación y cuatro pruebas de lógica verificadas. La presentación y las interacciones del navegador deben revisarse visualmente.

Referencia: https://reflex.dev/docs/getting-started/dashboard-tutorial/
