USE gestion_de_pedidos;
SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci;
DROP PROCEDURE IF EXISTS consultar_pedidos_cliente;
DELIMITER $$
CREATE PROCEDURE consultar_pedidos_cliente(
    IN p_cliente VARCHAR(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    IN p_nif VARCHAR(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    OUT p_total_gastado DECIMAL(18,2)
)
SQL SECURITY INVOKER
BEGIN
    SET p_total_gastado = 0.00;
    DROP TEMPORARY TABLE IF EXISTS tmp_resumen_pedidos_cliente;

    -- Tabla final: una fila por pedido. Detalle y pagos se agregan por separado.
    CREATE TEMPORARY TABLE tmp_resumen_pedidos_cliente ENGINE=InnoDB AS
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
    WHERE (NULLIF(TRIM(p_cliente), '') IS NULL
           OR CONVERT(CONCAT(c.nombre, ' ', c.apellidos) USING utf8mb4)
              COLLATE utf8mb4_unicode_ci
              LIKE CONCAT('%', TRIM(p_cliente), '%') COLLATE utf8mb4_unicode_ci)
      AND (NULLIF(TRIM(p_nif), '') IS NULL
           OR CONVERT(c.nif USING utf8mb4) COLLATE utf8mb4_unicode_ci
              = TRIM(p_nif) COLLATE utf8mb4_unicode_ci);

    SELECT COALESCE(SUM(total_pagado), 0.00)
    INTO p_total_gastado
    FROM tmp_resumen_pedidos_cliente;

    -- Único conjunto de resultados del procedimiento.
    SELECT * FROM tmp_resumen_pedidos_cliente ORDER BY pedidoId;
END$$
DELIMITER ;

-- Ejecutar estas sentencias en la misma conexión:
-- CALL consultar_pedidos_cliente('Lucia', NULL, @total_gastado);
-- SELECT @total_gastado AS total_gastado;
-- CALL consultar_pedidos_cliente(NULL, '10037129K', @total_gastado);
-- SELECT @total_gastado AS total_gastado;
-- La tabla temporal final se puede consultar en esa misma sesión:
-- SELECT * FROM tmp_resumen_pedidos_cliente;
-- Se reemplaza al llamar de nuevo y desaparece al cerrar la conexión.
-- NULL en ambos filtros consulta todos los clientes.
