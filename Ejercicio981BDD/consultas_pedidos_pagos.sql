USE gestion_de_pedidos;
SET @pedido_id = 1;

-- 1. Cabecera del pedido.
SELECT p.id, p.fecha, p.estado,
       CONCAT(c.nombre, ' ', c.apellidos) AS cliente,
       t.nombre AS tienda,
       CONCAT(u.nombre, ' ', u.apellidos) AS vendedor
FROM pedidos p
JOIN clientes c ON c.id = p.clienteId
JOIN tiendas t ON t.id = p.tiendaId
JOIN usuarios u ON u.id = p.vendedorId
WHERE p.id = @pedido_id;

-- 2. Productos del mismo pedido.
SELECT d.pedidoId, pr.nombre AS producto, d.cantidad,
       d.precio_unitario, d.descuento_porcentaje,
       ROUND(d.cantidad * d.precio_unitario *
             (1 - d.descuento_porcentaje / 100), 2) AS subtotal
FROM detalle_de_pedido d
JOIN productos pr ON pr.id = d.productoId
WHERE d.pedidoId = @pedido_id
ORDER BY pr.nombre;

-- 3. Todos sus pagos: método, importe y momento.
SELECT id, pedidoId, tipo_pago, monto, fecha_pago
FROM pagos WHERE pedidoId = @pedido_id
ORDER BY fecha_pago, id;

-- 4. Resumen de todos los pedidos.
-- Agrupar detalle y pagos por separado evita multiplicar sus filas al unirlos.
SELECT p.id, p.estado, d.productos, d.total,
       COALESCE(g.efectivo, 0) AS efectivo,
       COALESCE(g.tarjeta, 0) AS tarjeta,
       COALESCE(g.cobrado, 0) AS cobrado,
       d.total - COALESCE(g.cobrado, 0) AS pendiente
FROM pedidos p
JOIN (
    SELECT pedidoId, COUNT(*) AS productos,
           ROUND(SUM(cantidad * precio_unitario *
                     (1 - descuento_porcentaje / 100)), 2) AS total
    FROM detalle_de_pedido GROUP BY pedidoId
) d ON d.pedidoId = p.id
LEFT JOIN (
    SELECT pedidoId,
           SUM(CASE WHEN tipo_pago = 'efectivo' THEN monto ELSE 0 END) AS efectivo,
           SUM(CASE WHEN tipo_pago = 'tarjeta' THEN monto ELSE 0 END) AS tarjeta,
           SUM(monto) AS cobrado
    FROM pagos GROUP BY pedidoId
) g ON g.pedidoId = p.id
ORDER BY p.id;
