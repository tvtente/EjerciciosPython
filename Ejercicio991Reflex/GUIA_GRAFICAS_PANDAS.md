# Gráficas con Pandas y Reflex

Abre `/pandas` y pulsa **Cargar data/orders.csv**. El botón lee el fichero del servidor cada vez: puedes editar el CSV y volver a pulsarlo. También puedes subir otro CSV con el mismo formato.

Los 72 registros son ficticios: seis meses, cuatro regiones y tres productos. Las columnas son:

| Columna | Significado |
|---|---|
| region | North, South, East o West |
| product | Nombre del producto |
| units | Unidades enteras, de 0 a 1.000.000 |
| date | Fecha válida YYYY-MM-DD |
| unit_price | Precio unitario en euros; punto decimal, máximo dos decimales |
| unit_cost | Coste unitario en euros; mismo formato que el precio |
| channel | Online, Store o Wholesale |

## Orden recomendado para leer pandas_data_app.py

1. **read_orders** valida el CSV y convierte las columnas a sus tipos. Sigue aceptando archivos antiguos con region,product,units; en ese caso no hay fechas y los importes son cero.
2. **load_sample** lee `data/orders.csv` mediante una ruta relativa al módulo, independiente de dónde abras la terminal.
3. **analyze_orders** filtra y agrupa unidades por región. La vista previa se limita a 50 filas, pero los totales usan todas.
4. **PandasAppState._refresh** construye los otros resúmenes a partir de todas las filas filtradas. Calcula importes en céntimos enteros antes de sumar.
5. **extra_charts** conecta las listas resultantes con Recharts. `data_key` tiene que coincidir con la clave de cada diccionario.

## Cada gráfica

- **Unidades por región:** barras, `summary`, claves `region` y `units`.
- **Ingresos y beneficio por mes:** dos líneas, `monthly`, claves `month`, `revenue` y `profit`. Las fechas ISO permiten ordenar los meses cronológicamente.
- **Unidades por producto:** barras, `products`, claves `product` y `units`.
- **Ingresos por canal:** barras, `channels`, claves `channel` y `revenue`.

Ingresos = unidades × precio unitario. Beneficio bruto = unidades × (precio − coste). No incluye impuestos, descuentos ni otros gastos. Los meses sin registros se omiten; no se inventan ventas para rellenarlos.

## Ejercicios

1. Cambia `fill` en una barra y `stroke` en una línea.
2. Modifica unidades o precios en el CSV y vuelve a cargarlo.
3. Filtra por North y Tea: habrá seis registros, uno por mes.
4. Compara `groupby('product')` y `groupby('channel')`.
5. Añade una gráfica de beneficio por producto siguiendo el mismo recorrido: datos → agregación → estado → componente.

Las validaciones y los cálculos se han comprobado con el conjunto completo, filtros sin resultados y el formato CSV antiguo. La compilación de Reflex pasa; el aspecto visual debe revisarse en el navegador.
