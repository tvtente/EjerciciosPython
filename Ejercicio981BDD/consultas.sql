-- Consultas de práctica para gestion_de_pedidos. No modifican datos.
USE gestion_de_pedidos;

-- Tablas disponibles.
SHOW TABLES;

-- Primeros 10 clientes.
SELECT id, nombre, apellidos, nif, telefono, email
FROM clientes ORDER BY id LIMIT 10;

-- Teléfonos con prefijo +34 (evita escapes dependientes del cliente SQL).
SELECT nombre, telefono FROM clientes
WHERE telefono REGEXP '^[+]34';

-- Teléfonos formados exclusivamente por nueve dígitos.
SELECT nombre, telefono FROM clientes
WHERE telefono REGEXP '^[0-9]{9}$';

-- Nombres con tildes o ñ: comparación sensible a acentos en MySQL 8.
SELECT nombre, apellidos FROM clientes
WHERE REGEXP_LIKE(
    CONCAT(nombre, ' ', apellidos) COLLATE utf8mb4_bin,
    '[áéíóúÁÉÍÓÚñÑ]', 'c'
);

-- Correos que contienen una etiqueta con +.
SELECT nombre, email FROM clientes WHERE email REGEXP '[+]';

-- Total de cada pedido, incluidos descuentos.
SELECT p.id, p.fecha, p.estado,
       ROUND(SUM(d.cantidad * d.precio_unitario *
                 (1 - d.descuento_porcentaje / 100)), 2) AS total
FROM pedidos p JOIN detalle_de_pedido d ON d.pedidoId = p.id
GROUP BY p.id, p.fecha, p.estado ORDER BY p.id;

-- Total, cobros y saldo pendiente; agregaciones separadas para evitar duplicados.
SELECT p.id, COALESCE(d.total, 0) AS total,
       COALESCE(g.cobrado, 0) AS cobrado,
       COALESCE(d.total, 0) - COALESCE(g.cobrado, 0) AS saldo
FROM pedidos p
LEFT JOIN (
    SELECT pedidoId,
           ROUND(SUM(cantidad * precio_unitario *
                     (1 - descuento_porcentaje / 100)), 2) AS total
    FROM detalle_de_pedido GROUP BY pedidoId
) d ON d.pedidoId = p.id
LEFT JOIN (
    SELECT pedidoId, SUM(monto) AS cobrado FROM pagos GROUP BY pedidoId
) g ON g.pedidoId = p.id
ORDER BY p.id;

-- Existencias por tienda y producto.
SELECT t.nombre AS tienda, p.nombre AS producto, s.cantidad
FROM stock_tiendas s
JOIN tiendas t ON t.id = s.tiendaId
JOIN productos p ON p.id = s.productoId
ORDER BY t.nombre, p.nombre;

-- Proveedores de cada producto y precio de compra.
SELECT p.nombre AS producto, v.nombre AS proveedor, pp.precio_compra
FROM proveedores_productos pp
JOIN proveedores v ON v.id = pp.proveedorId
JOIN productos p ON p.id = pp.productoId
ORDER BY p.nombre, pp.precio_compra;

-- Auditoría de las relaciones existentes.
SELECT TABLE_NAME, COLUMN_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME
FROM information_schema.KEY_COLUMN_USAGE
WHERE TABLE_SCHEMA = 'gestion_de_pedidos'
  AND REFERENCED_TABLE_NAME IS NOT NULL
ORDER BY TABLE_NAME, COLUMN_NAME;
