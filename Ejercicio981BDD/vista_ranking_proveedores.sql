USE gestion_de_pedidos;

-- Indicador de ventas de productos asociados, NO de suministro real.
-- Las ventas de un producto cuentan para cada uno de sus proveedores asociados.
CREATE OR REPLACE VIEW vista_ranking_proveedores_de_la_red AS
WITH ventas_por_producto AS (
    SELECT dp.productoId,
           SUM(dp.cantidad) AS unidades_vendidas
    FROM detalle_de_pedido dp
    JOIN pedidos p ON p.id = dp.pedidoId
    WHERE p.estado = 'enviado'
    GROUP BY dp.productoId
),
ventas_por_proveedor AS (
    SELECT pr.id AS proveedor_id,
           pr.nombre AS proveedor,
           COALESCE(SUM(v.unidades_vendidas), 0) AS unidades_vendidas
    FROM proveedores pr
    LEFT JOIN proveedores_productos pp ON pp.proveedorId = pr.id
    LEFT JOIN ventas_por_producto v ON v.productoId = pp.productoId
    GROUP BY pr.id, pr.nombre
)
SELECT proveedor_id, proveedor, unidades_vendidas,
       ROW_NUMBER() OVER (
           ORDER BY unidades_vendidas DESC, proveedor_id ASC
       ) AS ranking
FROM ventas_por_proveedor;

-- Vista fija para los cinco primeros.
CREATE OR REPLACE VIEW vista_5_mejores_proveedores_de_la_red AS
SELECT proveedor_id, proveedor, unidades_vendidas, ranking
FROM vista_ranking_proveedores_de_la_red
WHERE ranking <= 5;

-- Número variable: ejecutar SET y SELECT en la misma conexión.
SET @numero_proveedores = 5;
SELECT proveedor_id, proveedor, unidades_vendidas, ranking
FROM vista_ranking_proveedores_de_la_red
WHERE ranking <= @numero_proveedores
ORDER BY ranking;

-- Para consultar la vista fija:
-- SELECT * FROM vista_5_mejores_proveedores_de_la_red ORDER BY ranking;
