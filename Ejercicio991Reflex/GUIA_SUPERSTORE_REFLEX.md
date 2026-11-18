# Superstore interactivo en Reflex

Abre `http://localhost:3000/superstore` con Reflex arrancado. También hay un enlace desde la portada del contador.

## Cómo usarlo

1. Los datos de `data/superstore.csv` se cargan al entrar, sin subir el archivo.
2. Abre las secciones de filtros. Puedes combinar varios valores de cada categoría. Sin marcas significa «todos».
3. Ajusta fechas, importes o búsquedas y pulsa **Aplicar filtros**. El aviso «Cambios sin aplicar» distingue los controles editados de la selección que muestran las gráficas.
4. **Restablecer** recupera la selección completa, eliminando duplicados exactos por defecto.
5. Recorre la tabla de 25 filas por página o descarga todas las coincidencias en CSV.
6. Si hay al menos 30 filas, puedes entrenar un bosque aleatorio exploratorio. Cambiar y aplicar filtros elimina las métricas anteriores para no confundir selecciones.

Los importes mantienen las unidades monetarias del CSV original; no se convierten a euros. «Líneas de venta» cuenta registros y «Pedidos únicos» cuenta identificadores de pedido distintos. El margen global es beneficio total dividido por ventas totales.

## Relación con el notebook

| Notebook | Archivo / función Reflex |
|---|---|
| Lectura y normalización del CSV | `superstore_analysis.py` → `load_superstore` |
| Función de filtrado interactivo | `superstore_analysis.py` → `filtrar_superstore`, compartida con el notebook |
| Controles ipywidgets | `superstore_app.py` → `filters`, `text_filter`, `category_filter` |
| Recoger los filtros | `filter_config` traduce los campos a la configuración común |
| Aplicar filtros y agrupar | `SuperstoreState.apply` |
| Cuatro gráficas Matplotlib | `charts`, con componentes Recharts |
| Vista previa | Tabla paginada desde `SuperstoreState._show_page` |
| Modelo aleatorio original | `train_exploratory`, una variante con entradas revisadas |

La función compartida se importó también en el notebook. Si cambias sus reglas, se usan en ambos entornos; reinicia el kernel o recarga el módulo para actualizar una importación ya realizada.

## Filtros disponibles

Ubicación (región, país, estado, ciudad), categoría, subcategoría, segmento, modo de envío, año, mes y día de pedido; fechas de pedido y envío; búsquedas literales por cliente, producto, códigos e identificadores; límites de ventas, beneficio, cantidad y descuento; rentabilidad; ventas sin descuento; recorte opcional de ventas inferiores a 5000; eliminación de duplicados.

Entre filtros se usa Y. Dentro de una lista de categorías se usa O. Los límites numéricos y de fecha son inclusivos, excepto el recorte opcional de 5000, que es estricto. Las listas muestran opciones del conjunto completo: algunas combinaciones pueden no tener coincidencias.

## Gráficas y rendimiento

Los totales, las series mensuales y las barras se calculan sobre todas las filas filtradas. La dispersión muestra como máximo 1500 filas con semilla fija. Las agregaciones se redondean a dos decimales para mostrarlas: puede haber diferencias de un céntimo al sumar categorías ya redondeadas.

El DataFrame completo permanece en el servidor. Al navegador se envían los resúmenes, opciones y la página actual de la tabla. El CSV no se modifica y los filtros son independientes para cada sesión.

## Modelo exploratorio

La web utiliza categoría, subcategoría, segmento, región, envío, descuento y cantidad. No incluye `profit` ni precio derivado de ventas como entradas. Emplea una división aleatoria 80/20 y muestra MAE, RMSE y R². Es una adaptación didáctica: no reproduce todas las celdas de modelos del notebook ni constituye una predicción temporal. No demuestra causalidad y una validación real debería comprobar también dependencia entre líneas de un mismo pedido y posibles cambios temporales.

## Comprobación

Se validó la compilación de Reflex y se comprobaron carga, filtros combinados, fechas/años, paginación, rangos inválidos, selección vacía, restauración y entrenamiento. La comprobación del aspecto final debe hacerse en el navegador.

## Interpretar el entrenamiento

La sección del modelo explica MAE, RMSE, R², tamaños de entrenamiento/validación y MAE de referencia. Las tarjetas se muestran antes de entrenar; los diagnósticos aparecen al finalizar.

- **Real frente a predicha:** cada punto es una fila de validación; la diagonal indica predicción perfecta. Hasta 500 puntos para visualizar, pero métricas calculadas sobre toda la validación.
- **MAE comparado:** contrasta el bosque con predecir siempre la media del entrenamiento, utilizando la misma validación. Una barra menor indica menor MAE.
- **Mapa de calor:** Pearson sobre descuento, cantidad y ventas del entrenamiento. Valores entre −1 y +1; N/D si una variable es constante. No incluye las categorías ni equivale a importancia de variables o causalidad.

R² se muestra como no definido si las ventas de validación son constantes. No se presenta como porcentaje de aciertos. El MAE está en euros, pero no es una garantía de error máximo por operación. Cambiar los filtros y aplicarlos invalida todos los diagnósticos para evitar mezclar selecciones.
