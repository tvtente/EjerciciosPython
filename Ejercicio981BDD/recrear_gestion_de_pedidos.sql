DROP DATABASE IF EXISTS gestion_de_pedidos;
CREATE DATABASE gestion_de_pedidos;
USE gestion_de_pedidos;
CREATE TABLE categorias (
 id INT PRIMARY KEY AUTO_INCREMENT,
 nombre VARCHAR(50) NOT NULL UNIQUE,
 descripcion TEXT
);
CREATE TABLE clientes (
 id INT PRIMARY KEY AUTO_INCREMENT,
 nif VARCHAR(10) NOT NULL UNIQUE,
 nombre VARCHAR(50) NOT NULL,
 apellidos VARCHAR(50) NOT NULL,
 direccion TEXT NOT NULL,
 telefono VARCHAR(20) NOT NULL,
 email VARCHAR(50) NOT NULL
);
CREATE TABLE tiendas (
 id INT AUTO_INCREMENT PRIMARY KEY,
 nombre VARCHAR(100) NOT NULL,
 nif VARCHAR(15) UNIQUE,
 telefono VARCHAR(20),
 email VARCHAR(150),
 direccion VARCHAR(255)
);
CREATE TABLE usuarios (
 id INT AUTO_INCREMENT PRIMARY KEY,
 nombre VARCHAR(50) NOT NULL,
 apellidos VARCHAR(100) NOT NULL,
 usuario VARCHAR(50) NOT NULL UNIQUE,
 password_hash VARCHAR(255) NOT NULL,
 rol ENUM('administrador','vendedor') NOT NULL DEFAULT 'vendedor',
 activo BOOLEAN NOT NULL DEFAULT TRUE,
 tiendaId INT,
 FOREIGN KEY (tiendaId) REFERENCES tiendas(id) ON DELETE RESTRICT
);
CREATE TABLE productos (
 id INT PRIMARY KEY AUTO_INCREMENT,
 nombre VARCHAR(50) NOT NULL,
 descripcion TEXT,
 precio DECIMAL(6,2) UNSIGNED NOT NULL,
 disponibilidad BOOLEAN DEFAULT TRUE,
 categoriaId INT NOT NULL,
 FOREIGN KEY (categoriaId) REFERENCES categorias(id)
);
CREATE TABLE stock_tiendas (
 tiendaId INT NOT NULL,
 productoId INT NOT NULL,
 cantidad INT UNSIGNED DEFAULT 0,
 PRIMARY KEY (tiendaId,productoId),
 FOREIGN KEY (tiendaId) REFERENCES tiendas(id) ON DELETE CASCADE,
 FOREIGN KEY (productoId) REFERENCES productos(id) ON DELETE CASCADE
);
CREATE TABLE pedidos (
 id INT PRIMARY KEY AUTO_INCREMENT,
 fecha DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
 estado ENUM('pagado','pendiente','enviado','cancelado') NOT NULL DEFAULT 'pendiente',
 clienteId INT NOT NULL,
 vendedorId INT NOT NULL,
 tiendaId INT NOT NULL,
 FOREIGN KEY (clienteId) REFERENCES clientes(id),
 FOREIGN KEY (vendedorId) REFERENCES usuarios(id) ON DELETE RESTRICT,
 FOREIGN KEY (tiendaId) REFERENCES tiendas(id) ON DELETE RESTRICT
);
CREATE TABLE detalle_de_pedido (
 pedidoId INT NOT NULL,
 productoId INT NOT NULL,
 cantidad INT UNSIGNED NOT NULL DEFAULT 1,
 precio_unitario DECIMAL(6,2) UNSIGNED NOT NULL,
 descuento_porcentaje DECIMAL(5,2) UNSIGNED NOT NULL DEFAULT 0.00,
 FOREIGN KEY (pedidoId) REFERENCES pedidos(id) ON DELETE CASCADE,
 FOREIGN KEY (productoId) REFERENCES productos(id) ON DELETE RESTRICT
);
CREATE TABLE proveedores (
 id INT AUTO_INCREMENT PRIMARY KEY,
 nombre VARCHAR(100) NOT NULL,
 nif VARCHAR(15) UNIQUE,
 telefono VARCHAR(20),
 email VARCHAR(150),
 direccion VARCHAR(255)
);
CREATE TABLE proveedores_productos (
 proveedorId INT NOT NULL,
 productoId INT NOT NULL,
 precio_compra DECIMAL(6,2) UNSIGNED NOT NULL DEFAULT 0.00,
 PRIMARY KEY (proveedorId,productoId),
 FOREIGN KEY (proveedorId) REFERENCES proveedores(id) ON DELETE CASCADE,
 FOREIGN KEY (productoId) REFERENCES productos(id) ON DELETE CASCADE
);
CREATE TABLE pagos (
 id INT PRIMARY KEY AUTO_INCREMENT,
 pedidoId INT NOT NULL,
 tipo_pago ENUM('efectivo','tarjeta') NOT NULL,
 monto DECIMAL(6,2) UNSIGNED NOT NULL,
 fecha_pago DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
 FOREIGN KEY (pedidoId) REFERENCES pedidos(id) ON DELETE RESTRICT
);
