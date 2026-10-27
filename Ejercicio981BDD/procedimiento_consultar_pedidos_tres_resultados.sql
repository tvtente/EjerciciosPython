USE gestion_de_pedidos;
SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci;

DROP PROCEDURE IF EXISTS consultar_pedidos_cliente;
DELIMITER $$
CREATE PROCEDURE consultar_pedidos_cliente(
    IN p_cliente VARCHAR(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    IN p_nif VARCHAR(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
)
READS SQL DATA
SQL SECURITY INVOKER
BEGIN
    -- Nombre/apellidos: búsqueda parcial con LIKE.
    -- NIF: coincidencia exacta, ignorando espacios exteriores y mayúsculas.
    -- NULL o texto vacío: no aplicar ese filtro; ambos filtros se combinan con AND.

    -- 1. Resumen del pedido y sus pagos. Agregaciones separadas evitan duplicados.
    SELECT p.id AS pedidoId, p.fecha, p.estado,
           CONCAT(c.nombre, ' ', c.apellidos) AS cliente,
           u.usuario, CONCAT(u.nombre, ' ', u.apellidos) AS vendedor,
           t.nombre AS tienda,
           COALESCE(d.lineas, 0) AS lineas,
           COALESCE(d.total, 0) AS total,
           COALESCE(g.efectivo, 0) AS efectivo,
           COALESCE(g.tarjeta, 0) AS tarjeta,
           COALESCE(g.cobrado, 0) AS cobrado,
           COALESCE(d.total, 0) - COALESCE(g.cobrado, 0) AS saldo_pendiente
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
    WHERE (NULLIF(TRIM(p_cliente), '') IS NULL
           OR CONVERT(CONCAT(c.nombre, ' ', c.apellidos) USING utf8mb4)
              COLLATE utf8mb4_unicode_ci
              LIKE CONCAT('%', TRIM(p_cliente), '%') COLLATE utf8mb4_unicode_ci)
      AND (NULLIF(TRIM(p_nif), '') IS NULL
           OR CONVERT(c.nif USING utf8mb4) COLLATE utf8mb4_unicode_ci
              = TRIM(p_nif) COLLATE utf8mb4_unicode_ci)
    ORDER BY p.id;

    -- 2. Productos de los pedidos encontrados.
    SELECT p.id AS pedidoId, pr.id AS productoId, pr.nombre AS producto,
           d.cantidad, d.precio_unitario, d.descuento_porcentaje,
           ROUND(d.cantidad * d.precio_unitario *
                 (1 - d.descuento_porcentaje / 100), 2) AS subtotal
    FROM pedidos p
    JOIN clientes c ON c.id = p.clienteId
    JOIN usuarios u ON u.id = p.vendedorId
    JOIN detalle_de_pedido d ON d.pedidoId = p.id
    JOIN productos pr ON pr.id = d.productoId
    WHERE (NULLIF(TRIM(p_cliente), '') IS NULL
           OR CONVERT(CONCAT(c.nombre, ' ', c.apellidos) USING utf8mb4)
              COLLATE utf8mb4_unicode_ci
              LIKE CONCAT('%', TRIM(p_cliente), '%') COLLATE utf8mb4_unicode_ci)
      AND (NULLIF(TRIM(p_nif), '') IS NULL
           OR CONVERT(c.nif USING utf8mb4) COLLATE utf8mb4_unicode_ci
              = TRIM(p_nif) COLLATE utf8mb4_unicode_ci)
    ORDER BY p.id, pr.nombre;

    -- 3. Cobros individuales: no se multiplican por los productos del pedido.
    SELECT p.id AS pedidoId, g.id AS pagoId,
           g.tipo_pago, g.monto, g.fecha_pago
    FROM pedidos p
    JOIN clientes c ON c.id = p.clienteId
    JOIN usuarios u ON u.id = p.vendedorId
    JOIN pagos g ON g.pedidoId = p.id
    WHERE (NULLIF(TRIM(p_cliente), '') IS NULL
           OR CONVERT(CONCAT(c.nombre, ' ', c.apellidos) USING utf8mb4)
              COLLATE utf8mb4_unicode_ci
              LIKE CONCAT('%', TRIM(p_cliente), '%') COLLATE utf8mb4_unicode_ci)
      AND (NULLIF(TRIM(p_nif), '') IS NULL
           OR CONVERT(c.nif USING utf8mb4) COLLATE utf8mb4_unicode_ci
              = TRIM(p_nif) COLLATE utf8mb4_unicode_ci)
    ORDER BY p.id, g.fecha_pago, g.id;
END$$
DELIMITER ;

-- Ejecutar por separado después de crear el procedimiento:
-- CALL consultar_pedidos_cliente('Lucía', NULL);
-- CALL consultar_pedidos_cliente('García', NULL);
-- CALL consultar_pedidos_cliente(NULL, '10037129K');
-- CALL consultar_pedidos_cliente('Lucía', '10037129K');
-- CALL consultar_pedidos_cliente(NULL, NULL); -- Todos los clientes.
