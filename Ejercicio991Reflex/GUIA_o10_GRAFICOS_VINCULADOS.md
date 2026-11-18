# o10 · Gráficos vinculados

Abre http://localhost:3000/o10_graficos_vinculados con Reflex en marcha. Hay un enlace en la portada.

## Prueba rápida

1. Arrastra un rectángulo que incluya los puntos (8, 2) y (9, 3).
2. La tabla debe mostrar pedido-a y pedido-b, y el total debe ser 300 €.
3. Selecciona otros puntos: la nueva selección reemplaza la anterior.
4. Dibuja una selección sin puntos: tabla y barras quedan vacías.
5. Pulsa Restablecer todos: vuelven los 12 pedidos y se remonta el origen para limpiar el resaltado y el zoom.
6. Abre Inspeccionar el último evento para observar el mensaje real que envía XY.

Los botones de prueba permiten verificar el estado y la tabla de forma independiente del gesto de selección. No generan eventos XY ni dibujan un resaltado de puntos.

## Archivos y recorrido

El módulo `Ejercicio991Reflex/o10_graficos_vinculados.py` contiene datos ficticios estables, columnas de gráficos, validación de eventos, estado y componentes. Los comentarios numerados orientan la lectura.

`source_data` publica el conjunto completo. `select_points` recibe el evento final, `selection_ids` valida las posiciones y las traduce a IDs. `visible_rows` calcula la selección; las barras y la tabla se derivan de ella. No hay trabajo Python en cada movimiento del ratón.

None significa sin filtro y una lista vacía significa ningún resultado. Si el mensaje está truncado, se resuelve en servidor; si es inválido, se conserva la selección anterior. Los IDs de RECORDS deben mantenerse alineados con las filas publicadas por source_data.

## Modificar el código

Prueba a cambiar ingresos, unidades o ciudades de RECORDS y observa cómo cambian las vistas. Para añadir registros, conserva IDs únicos y ajusta los textos que mencionan 12 pedidos. Mantén estable el origen durante una selección: sustituir o reordenar filas requiere controlar la generación de los eventos.

La página usa XY 0.0.7 y el XYPlugin que ya está instalado en rxconfig.py. Si no aparecen los gráficos, revisa los errores del navegador y del servidor: compilar no garantiza que el canal binario o el renderizador funcionen en un navegador concreto. Los botones y la tabla ayudan a aislar ese problema.

No se sincronizan los ejes del origen y las barras porque representan magnitudes diferentes (hora e ID). El filtrado cruzado mediante estado y el zoom compartido mediante link_group/link_axes son mecanismos distintos.

## Validación

La aplicación compila. Las cinco pruebas en `tests/test_o10_graficos_vinculados.py` verifican selección, vacío frente a borrado, eventos inválidos, resolución de mensajes truncados y reinicio. La interacción visual XY queda pendiente de revisión en el navegador.

Referencia: https://reflex.dev/docs/getting-started/linked-charts-tutorial/

## Modo compatible

La pestaña inicial utiliza un selector SVG (`selector_pedidos.py` y `selector_pedidos.jsx`) y barras Recharts. Arrastra desde un espacio vacío o pulsa puntos para seleccionar. Tab + Enter también permite seleccionarlos. El evento manda IDs a `select_compatible`, que actualiza el mismo estado, tabla y totales.

La pestaña «XY · Tutorial original» conserva las gráficas originales para investigar su canal/renderizador. El modo compatible es una adaptación de la interacción, no una reparación demostrada de XY. La compilación, el análisis sintáctico JSX y las pruebas de estado pasan; la interacción visual aún debe comprobarse en el navegador.
