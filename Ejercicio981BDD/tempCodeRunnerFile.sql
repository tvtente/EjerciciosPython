    SELECT p.id AS pedidoId, p.fecha, p.estado,
           c.id AS clienteId, c.nif,
           CONCAT(c.nombre, ' ', c.apellidos) AS cliente,
           CONCAT(u.nombre, ' ', u.apellidos) AS vendedor,
           t.nombre AS tienda,
           COALESCE(d.lineas, 0) AS lineas_productos,
           COALESCE(d.total, 0.00) AS total_pedido,
           COALESCE(g.efectivo, 0.00) AS efectivo,
           COALESCE(g.tarjeta, 0.00) AS tarjeta,
           COALESCE(g.cobrado, 0.00) AS total_pagado,
           COALESCE(d.total, 0.00) - COALESCE(g.cobrado, 0.00) AS saldo_pendiente
    FROM pedidos p
    JOIN clientes c ON c.id = p.clienteId
    JOIN usuarios u ON u.id = p.vendedorId
    JOIN tiendas t ON t.id = p.tiendaId
    LEFT JOIN (
        SELECT pedidoId, COUNT(*) AS lineas,
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