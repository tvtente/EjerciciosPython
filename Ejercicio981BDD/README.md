# Gestión de pedidos

Scripts y consultas del ejercicio. La base actual se llama `gestion_de_pedidos`, con «n».

## Archivos

- `gestion_de_pedidos_mysql.sql`: importación completa para MySQL 8.0/8.4; contiene estructura y 546 registros. Reemplaza las 11 tablas incluidas. No ejecutar los scripts de carga adicionales después de esta importación.
- `recrear_gestion_de_pedidos.sql`: crea la estructura de 11 tablas; borra y recrea la base, sin datos.
- `mock_gestion_de_pedidos.sql`: carga inicial de datos ficticios, para tablas vacías.
- `actualizar_mock_realista.sql`: actualiza los datos ficticios de la carga inicial con nombres y formatos más verosímiles.
- `consultas.sql`: consultas de lectura, expresiones regulares, totales, pagos, existencias y relaciones. La consulta con `REGEXP_LIKE` requiere MySQL 8.
- `crear_gestio_de_pedidos.sql`: versión histórica para `gestio_de_pedidos`, sin «n»; no corresponde al diseño actual.
- `tablas.sql`: archivo vacío que ya estaba en la carpeta.

## Diseño actual y pendientes

Las tablas intermedias `stock_tiendas` y `proveedores_productos` representan relaciones de muchos a muchos. Cada pedido referencia cliente, vendedor y tienda.

El diseño conserva cantidades enteras. Para vender kilos fraccionarios habría que usar decimales. `detalle_de_pedido` todavía no tiene clave primaria. También quedan pendientes controles de cantidad positiva, descuento entre 0 y 100 e importe positivo.

Se propusieron `historial_precios` y su registro automático de cambios, pero no forman parte de estos scripts.

Los datos son ficticios. Los correos usan dominios de ejemplo y los formatos de teléfono varían para practicar expresiones regulares. Los documentos fiscales no deben tratarse como identidades reales ni como un conjunto completamente válido.

La configuración activa de QueryDeck permanece fuera de esta carpeta para conservar la ruta usada por MCP. No contiene aquí copias de contraseñas.
