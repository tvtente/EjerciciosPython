/*
VISTA DE CONTROL DE PEDIDOS

Objetivo: obtener una fila por pedido con su cliente, vendedor, tienda,
productos, importes, cobros y saldo pendiente. Una vista guarda la consulta,
no una copia permanente de sus resultados: refleja los datos al consultarla.

WITH define tres consultas auxiliares (CTE): detalle, cobros y resumen.
Detalle y cobros se agrupan por separado antes de relacionarlos.
Esto evita duplicar importes: unir directamente tres líneas de productos con
dos pagos del mismo pedido produciría seis filas. Al agrupar primero,
cada conjunto aporta como máximo una fila por pedido.

La vista incluye todos los estados del pedido, también los cancelados.
El estado del pago se calcula a partir de los importes y es independiente
del estado comercial del pedido (pendiente, pagado, enviado o cancelado).
*/
USE gestion_de_pedidos;

CREATE OR REPLACE VIEW vw_control_pedidos AS
WITH detalle AS (
    -- Una fila por pedido: COUNT(*) cuenta líneas, no unidades.
    -- COUNT(DISTINCT productoId) cuenta productos diferentes.
    -- SUM(cantidad) suma unidades; el importe bruto no aplica descuentos.
    -- El total aplica el descuento de cada línea y redondea la suma a céntimos.
    SELECT pedidoId,
           COUNT(*) AS lineas_productos,
           COUNT(DISTINCT productoId) AS productos_distintos,
           SUM(cantidad) AS unidades,
           ROUND(SUM(cantidad * precio_unitario), 2) AS importe_bruto,
           ROUND(SUM(cantidad * precio_unitario *
                     (1 - descuento_porcentaje / 100)), 2) AS total_pedido
    FROM detalle_de_pedido
    GROUP BY pedidoId
),
cobros AS (
    -- Una fila por pedido con todos sus cobros.
    -- CASE separa efectivo y tarjeta; SUM(monto) suma ambos métodos.
    -- MIN y MAX obtienen las fechas del primer y último pago registrado.
    SELECT pedidoId,
           COUNT(*) AS numero_pagos,
           SUM(CASE WHEN tipo_pago = 'efectivo' THEN monto ELSE 0 END) AS efectivo,
           SUM(CASE WHEN tipo_pago = 'tarjeta' THEN monto ELSE 0 END) AS tarjeta,
           SUM(monto) AS total_pagado,
           MIN(fecha_pago) AS primer_pago,
           MAX(fecha_pago) AS ultimo_pago
    FROM pagos
    GROUP BY pedidoId
),
resumen AS (
    -- Relaciona los datos identificativos con los dos resúmenes económicos.
    -- COALESCE sustituye por cero los totales ausentes de los LEFT JOIN.
    -- Las fechas de pago se mantienen en NULL si no existen cobros.
    SELECT p.id AS pedidoId, p.fecha, p.estado,
           c.id AS clienteId, c.nif,
           CONCAT(c.nombre, ' ', c.apellidos) AS cliente,
           u.id AS vendedorId,
           CONCAT(u.nombre, ' ', u.apellidos) AS vendedor,
           t.id AS tiendaId, t.nombre AS tienda,
           COALESCE(d.lineas_productos, 0) AS lineas_productos,
           COALESCE(d.productos_distintos, 0) AS productos_distintos,
           COALESCE(d.unidades, 0) AS unidades,
           COALESCE(d.importe_bruto, 0.00) AS importe_bruto,
           COALESCE(d.total_pedido, 0.00) AS total_pedido,
           COALESCE(g.numero_pagos, 0) AS numero_pagos,
           COALESCE(g.efectivo, 0.00) AS efectivo,
           COALESCE(g.tarjeta, 0.00) AS tarjeta,
           COALESCE(g.total_pagado, 0.00) AS total_pagado,
           g.primer_pago, g.ultimo_pago
    FROM pedidos p
    -- JOIN equivale a INNER JOIN: exige una coincidencia en la tabla relacionada.
    -- Son relaciones obligatorias, respaldadas por claves foráneas NOT NULL.
    -- Clientes aporta el nombre y NIF del comprador.
    JOIN clientes c ON c.id = p.clienteId
    -- Usuarios identifica al vendedor que atendió el pedido.
    JOIN usuarios u ON u.id = p.vendedorId
    -- Tiendas identifica el establecimiento donde se realizó el pedido.
    JOIN tiendas t ON t.id = p.tiendaId
    -- LEFT JOIN conserva el pedido aunque aún no tenga líneas de productos.
    LEFT JOIN detalle d ON d.pedidoId = p.id
    -- LEFT JOIN conserva el pedido aunque todavía no tenga pagos.
    LEFT JOIN cobros g ON g.pedidoId = p.id
)
SELECT r.*,
       -- Descuento monetario efectivo tras redondear los totales.
       importe_bruto - total_pedido AS descuento_total,
       -- Un saldo negativo señala que se ha cobrado más que el total.
       total_pedido - total_pagado AS saldo_pendiente,
       -- NULLIF evita dividir entre cero: un pedido de total cero devuelve NULL.
       ROUND(100 * total_pagado / NULLIF(total_pedido, 0), 2) AS porcentaje_pagado,
       -- CASE clasifica el cobro; sin líneas se prioriza 'Sin productos'.
       -- Un pedido con líneas gratuitas y sin cobros se clasifica como pagado.
       CASE
           WHEN lineas_productos = 0 THEN 'Sin productos'
           WHEN total_pagado > total_pedido THEN 'Sobrepagado'
           WHEN total_pagado = total_pedido THEN 'Pagado'
           WHEN total_pagado = 0 THEN 'Sin pagos'
           ELSE 'Pago parcial'
       END AS estado_pago,
       -- Clasifica la combinación de métodos que tienen un importe positivo.
       CASE
           WHEN efectivo > 0 AND tarjeta > 0 THEN 'Mixto'
           WHEN efectivo > 0 THEN 'Efectivo'
           WHEN tarjeta > 0 THEN 'Tarjeta'
           ELSE 'Sin importe cobrado'
       END AS modalidad_pago,
       -- Antigüedad en días naturales; no implica que el pedido esté vencido.
       DATEDIFF(CURRENT_DATE, DATE(fecha)) AS dias_desde_pedido
FROM resumen r;

-- ORDER BY se aplica al consultar: la vista no garantiza un orden de filas.
-- Todos los pedidos, con los de mayor saldo primero.
SELECT * FROM vw_control_pedidos
ORDER BY saldo_pendiente DESC, pedidoId;

d@3m0i

-- Ejemplos adicionales (ejecutar por separado):
-- SELECT * FROM vw_control_pedidos WHERE estado_pago = 'Pago parcial';
-- SELECT * FROM vw_control_pedidos WHERE modalidad_pago = 'Mixto';
-- SELECT * FROM vw_control_pedidos WHERE nif = '10037129K' ORDER BY fecha;
-- SELECT * FROM vw_control_pedidos
-- WHERE estado <> 'cancelado' AND saldo_pendiente > 0 AND dias_desde_pedido >= 7;
