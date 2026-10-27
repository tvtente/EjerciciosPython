-- Conversión del volcado MariaDB a MySQL 8.0 / 8.4.
-- ATENCIÓN: reemplaza las 11 tablas listadas y sus datos en gestion_de_pedidos.
-- Ejecutar como script completo; detener la importación ante cualquier error.
SET @OLD_CHARACTER_SET_CLIENT = @@CHARACTER_SET_CLIENT;
SET @OLD_CHARACTER_SET_RESULTS = @@CHARACTER_SET_RESULTS;
SET @OLD_COLLATION_CONNECTION = @@COLLATION_CONNECTION;
SET @OLD_TIME_ZONE = @@TIME_ZONE;
SET @OLD_SQL_MODE = @@SQL_MODE;
SET @OLD_FOREIGN_KEY_CHECKS = @@FOREIGN_KEY_CHECKS;
SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci;
SET TIME_ZONE = '+00:00';
SET SQL_MODE = 'STRICT_TRANS_TABLES,NO_AUTO_VALUE_ON_ZERO,NO_ENGINE_SUBSTITUTION';
CREATE DATABASE IF NOT EXISTS gestion_de_pedidos
 CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE gestion_de_pedidos;
SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS `pagos`;
DROP TABLE IF EXISTS `proveedores_productos`;
DROP TABLE IF EXISTS `proveedores`;
DROP TABLE IF EXISTS `detalle_de_pedido`;
DROP TABLE IF EXISTS `pedidos`;
DROP TABLE IF EXISTS `stock_tiendas`;
DROP TABLE IF EXISTS `productos`;
DROP TABLE IF EXISTS `usuarios`;
DROP TABLE IF EXISTS `tiendas`;
DROP TABLE IF EXISTS `clientes`;
DROP TABLE IF EXISTS `categorias`;
SET FOREIGN_KEY_CHECKS = 1;

-- Estructura: categorias
CREATE TABLE `categorias` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  `descripcion` text DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Estructura: clientes
CREATE TABLE `clientes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nif` varchar(10) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `apellidos` varchar(50) NOT NULL,
  `direccion` text NOT NULL,
  `telefono` varchar(20) NOT NULL,
  `email` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nif` (`nif`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Estructura: tiendas
CREATE TABLE `tiendas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `nif` varchar(15) DEFAULT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `email` varchar(150) DEFAULT NULL,
  `direccion` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nif` (`nif`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Estructura: usuarios
CREATE TABLE `usuarios` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  `apellidos` varchar(100) NOT NULL,
  `usuario` varchar(50) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `rol` enum('administrador','vendedor') NOT NULL DEFAULT 'vendedor',
  `activo` tinyint(1) NOT NULL DEFAULT 1,
  `tiendaId` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `usuario` (`usuario`),
  KEY `tiendaId` (`tiendaId`),
  CONSTRAINT `usuarios_ibfk_1` FOREIGN KEY (`tiendaId`) REFERENCES `tiendas` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Estructura: productos
CREATE TABLE `productos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `precio` decimal(6,2) unsigned NOT NULL,
  `disponibilidad` tinyint(1) DEFAULT 1,
  `categoriaId` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `categoriaId` (`categoriaId`),
  CONSTRAINT `productos_ibfk_1` FOREIGN KEY (`categoriaId`) REFERENCES `categorias` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Estructura: stock_tiendas
CREATE TABLE `stock_tiendas` (
  `tiendaId` int NOT NULL,
  `productoId` int NOT NULL,
  `cantidad` int unsigned DEFAULT 0,
  PRIMARY KEY (`tiendaId`,`productoId`),
  KEY `productoId` (`productoId`),
  CONSTRAINT `stock_tiendas_ibfk_1` FOREIGN KEY (`tiendaId`) REFERENCES `tiendas` (`id`) ON DELETE CASCADE,
  CONSTRAINT `stock_tiendas_ibfk_2` FOREIGN KEY (`productoId`) REFERENCES `productos` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Estructura: pedidos
CREATE TABLE `pedidos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `fecha` datetime NOT NULL DEFAULT current_timestamp(),
  `estado` enum('pagado','pendiente','enviado','cancelado') NOT NULL DEFAULT 'pendiente',
  `clienteId` int NOT NULL,
  `vendedorId` int NOT NULL,
  `tiendaId` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `clienteId` (`clienteId`),
  KEY `vendedorId` (`vendedorId`),
  KEY `tiendaId` (`tiendaId`),
  CONSTRAINT `pedidos_ibfk_1` FOREIGN KEY (`clienteId`) REFERENCES `clientes` (`id`),
  CONSTRAINT `pedidos_ibfk_2` FOREIGN KEY (`vendedorId`) REFERENCES `usuarios` (`id`),
  CONSTRAINT `pedidos_ibfk_3` FOREIGN KEY (`tiendaId`) REFERENCES `tiendas` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=101 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Estructura: detalle_de_pedido
CREATE TABLE `detalle_de_pedido` (
  `pedidoId` int NOT NULL,
  `productoId` int NOT NULL,
  `cantidad` int unsigned NOT NULL DEFAULT 1,
  `precio_unitario` decimal(6,2) unsigned NOT NULL,
  `descuento_porcentaje` decimal(5,2) unsigned NOT NULL DEFAULT 0.00,
  KEY `pedidoId` (`pedidoId`),
  KEY `productoId` (`productoId`),
  CONSTRAINT `detalle_de_pedido_ibfk_1` FOREIGN KEY (`pedidoId`) REFERENCES `pedidos` (`id`) ON DELETE CASCADE,
  CONSTRAINT `detalle_de_pedido_ibfk_2` FOREIGN KEY (`productoId`) REFERENCES `productos` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Estructura: proveedores
CREATE TABLE `proveedores` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `nif` varchar(15) DEFAULT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `email` varchar(150) DEFAULT NULL,
  `direccion` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nif` (`nif`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Estructura: proveedores_productos
CREATE TABLE `proveedores_productos` (
  `proveedorId` int NOT NULL,
  `productoId` int NOT NULL,
  `precio_compra` decimal(6,2) unsigned NOT NULL DEFAULT 0.00,
  PRIMARY KEY (`proveedorId`,`productoId`),
  KEY `productoId` (`productoId`),
  CONSTRAINT `proveedores_productos_ibfk_1` FOREIGN KEY (`proveedorId`) REFERENCES `proveedores` (`id`) ON DELETE CASCADE,
  CONSTRAINT `proveedores_productos_ibfk_2` FOREIGN KEY (`productoId`) REFERENCES `productos` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Estructura: pagos
CREATE TABLE `pagos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `pedidoId` int NOT NULL,
  `tipo_pago` enum('efectivo','tarjeta') NOT NULL,
  `monto` decimal(6,2) unsigned NOT NULL,
  `fecha_pago` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `pedidoId` (`pedidoId`),
  CONSTRAINT `pagos_ibfk_1` FOREIGN KEY (`pedidoId`) REFERENCES `pedidos` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=101 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

START TRANSACTION;

-- Datos: categorias (5 registros)
INSERT INTO `categorias` VALUES
(1,'Fruta fresca','Frutas de temporada y variedades de proximidad'),
(2,'Verduras y hortalizas','Hortalizas para ensalada, guisos y cocina diaria'),
(3,'Cítricos','Naranjas, mandarinas, limones y pomelos'),
(4,'Frutos secos','Frutos secos naturales y tostados'),
(5,'Hierbas aromáticas','Hierbas frescas para cocinar');

-- Datos: clientes (20 registros)
INSERT INTO `clientes` VALUES
(1,'10037129K','Lucía','García López','C/ del Olivo, 14, 2.º B, 28012 Madrid','610073129','lucia.garcia@example.com'),
(2,'10074258M','José Luis','Martínez Ruiz','Av. de los Naranjos, 32, bajo, 46022 Valencia','+34 610 146 258','jose-luis.martinez@example.com'),
(3,'10111387N','María del Mar','Sánchez Pérez','Plaza del Mercado, 5, 1.º A, 41003 Sevilla','610-219-387','maria.delmar@example.com'),
(4,'10148516L','Óscar','Fernández Díaz','Calle Mayor, 108, 3.º C, 50001 Zaragoza','0034 610292516','oscar_fernandez@example.com'),
(5,'10185645A','Ana Belén','López Romero','P.º de la Alameda, 7, 29016 Málaga','(610) 365 645','ana.belen+5@example.com'),
(6,'X1007404G','Iñaki','Etxeberria Martín','C/ de la Estación, 21, 48008 Bilbao','610438774','inaki.etxeberria@example.com'),
(7,'10259903V','Núria','Puig Soler','Rambla de les Flors, 18, 08002 Barcelona','+34 610 511 903','nuria.puig@example.com'),
(8,'10297032R','Álvaro','Muñoz Jiménez','Avda. de Castilla, 45, 47008 Valladolid','610-585-032','alvaro.munoz@example.com'),
(9,'10334161P','Carmen','De la Fuente Gil','Calle Río Ebro, 9, 4.º D, 26004 Logroño','0034 610658161','carmen.delafuente@example.com'),
(10,'10371290S','Miguel Ángel','Torres Navarro','Plaza de España, 3, 03001 Alicante','(610) 731 290','miguel.angel+10@example.com'),
(11,'10408419E','Rocío','Ortega Molina','C/ del Almendro, 27, 14006 Córdoba','610804419','rocio.ortega@example.com'),
(12,'10445548Y','Héctor','Castro Iglesias','Paseo del Parque, 6, 33203 Gijón','+34 610 877 548','hector.castro@example.com'),
(13,'X1016042V','Ainhoa','Vázquez Alonso','Calle San Pedro, 11, 31001 Pamplona','610-950-677','ainhoa.vazquez@example.com'),
(14,'10519806C','Pablo','Del Río Santos','Av. de Galicia, 64, 15004 A Coruña','0034 611023806','pablo.delrio@example.com'),
(15,'10556935G','Inés','Herrera Marín','C/ de la Huerta, 8, 30002 Murcia','(611) 096 935','ines.herrera+15@example.com'),
(16,'10594064B','Adrián','Moreno Serrano','Calle del Mar, 16, 07012 Palma','611170064','adrian.moreno@example.com'),
(17,'10631193H','Mónica','Pascual Ferrer','Avda. del Puerto, 92, 12003 Castellón','+34 611 243 193','monica.pascual@example.com'),
(18,'10668322W','Raúl','Núñez Vega','C/ de la Acequia, 4, 18010 Granada','611-316-322','raul.nunez@example.com'),
(19,'X1023446S','Elena','Ramos Cabrera','Plaza del Carmen, 12, 39003 Santander','0034 611389451','elena.ramos@example.com'),
(20,'10742580Q','Víctor','Peña Domínguez','Calle de los Pinos, 30, 20009 Donostia','(611) 462 580','victor.pena+20@example.com');

-- Datos: tiendas (3 registros)
INSERT INTO `tiendas` VALUES
(1,'Frutería La Huerta — Centro','B1000001','+34 910 120 301','centro@lahuerta.example.com','C/ del Olivo, 2, local 1, 28012 Madrid'),
(2,'Frutería La Huerta — Mercado','B1000002','910 120 302','mercado@lahuerta.example.com','Plaza del Mercado, 8, puesto 14, 28005 Madrid'),
(3,'Frutería La Huerta — Norte','B1000003','910-120-303','norte@lahuerta.example.com','Av. de los Pinos, 36, bajo, 28029 Madrid');

-- Datos: usuarios (8 registros)
INSERT INTO `usuarios` VALUES
(1,'Ana Belén','López Romero','ana_belen1','scrypt:32768:8:1$650403989421a487ebfda3ae788eee57$1d9ef228587362b97c728c4bfde8c71d99e0cffe815101953cb8da77ecfd5545b43c33909ac2154fd5a147dc1a1d0dd7af767e4c978be9ec7e3b90c5bca71d12','vendedor',1,1),
(2,'Iñaki','Etxeberria Martín','inaki_etxeberria2','scrypt:32768:8:1$fd3d94d9991ff26c0609ade893294ff5$37d7ec298510cf53ed76d7d36384056738554728b50f91937a9ac0458da566ea1ed9c0e47aee77ec2fbe1bdbce9cc11975491a19c1dc78a54ae708fb6eb0e92b','vendedor',1,2),
(3,'Núria','Puig Soler','nuria_puig3','scrypt:32768:8:1$3ffc668c5bfec1f0ffbed4b54c5233af$7f27f43cc673afb4792dbc8436311cde29c86da307056de98970659c1259654e3cfd651ef58e1ffba9a8e6675348caefe6a6e58903e81cc8ff4f2c7cb330080b','vendedor',1,3),
(4,'Álvaro','Muñoz Jiménez','alvaro_munoz4','scrypt:32768:8:1$7cfdd2e30134c269e4507ba61e07c145$23e8e4d9aa75fe523b6e1b41e57328c4950545b838f2a8cf6677fcd92be9cfed8aadf7fe3a2b17d0df1b38c3b64930bb053c9038329dd2b7cf4fb0877bab42a9','vendedor',1,1),
(5,'Carmen','De la Fuente Gil','carmen_delafuente5','scrypt:32768:8:1$70e7371096212c9b163258a1f45a997f$009bae48d06b61bbcf9a512804aae17445d780c4461a1a5ae6f3210a6f5003f60f5ddf2bdfa2ffc234ce53f82ee9ba057104fb83829557f79c3070ceaae617d6','vendedor',1,2),
(6,'Miguel Ángel','Torres Navarro','miguel_angel6','scrypt:32768:8:1$a268755220c3126670061434c6d90065$83701e32091b94eb6f3d3a606fac163dcbf12a7f0261faa3feeb22945abbea9e85648f206e227736dff22fac1054765ec40d5643b2009bde605e6831aa6b0f56','vendedor',1,3),
(7,'Rocío','Ortega Molina','rocio_ortega7','scrypt:32768:8:1$2df5bc1d6f72076ad01cffb5579746d5$a0b3c7bd6f3528071251a356498043dd97e35fe3d7557f72ae3ac7309021126484741fe79a6d42b4cd9f988d40f487e906ace465ea15bd83a05924b097271712','vendedor',1,1),
(8,'Héctor','Castro Iglesias','hector_castro8','scrypt:32768:8:1$3c0a41822c351e91a5d405e61c904954$d9ffb2a46e6b9aa787128a04dac820cb6caefe3780a7ff595d7ff2336a4d2602c80066f8b66b737993fb8b9052d220aee8c97d258062b3a7ddc666270381abe9','administrador',1,2);

-- Datos: productos (25 registros)
INSERT INTO `productos` VALUES
(1,'Manzana Golden','Pieza de calibre mediano; origen: Lleida',1.20,1,1),
(2,'Pera conferencia','Pieza madura para consumo; origen: La Rioja',0.95,1,1),
(3,'Plátano de Canarias','Venta por pieza; categoría extra',0.45,1,1),
(4,'Fresa de Huelva','Bandeja de 500 g',3.25,1,1),
(5,'Uva blanca sin pepitas','Bandeja de 500 g',2.80,1,1),
(6,'Melocotón amarillo','Pieza de temporada',1.10,1,1),
(7,'Ciruela roja','Bandeja de 500 g',2.35,1,1),
(8,'Kiwi verde','Pieza de calibre 27',0.75,1,1),
(9,'Melón piel de sapo','Pieza de aproximadamente 2 kg',4.90,1,1),
(10,'Sandía sin semillas','Media pieza envasada',3.95,1,1),
(11,'Tomate de ensalada','Bandeja de 1 kg',2.40,1,2),
(12,'Lechuga romana','Unidad fresca',1.15,1,2),
(13,'Zanahoria lavada','Bolsa de 1 kg',1.30,1,2),
(14,'Calabacín verde','Bandeja de 1 kg',1.95,1,2),
(15,'Pepino holandés','Unidad de aproximadamente 400 g',0.85,1,2),
(16,'Pimiento rojo','Bandeja de 500 g',2.25,1,2),
(17,'Naranja de zumo','Malla de 2 kg',3.60,1,3),
(18,'Mandarina clementina','Malla de 1 kg',2.10,1,3),
(19,'Limón de Murcia','Malla de 500 g',1.25,1,3),
(20,'Pomelo rosa','Unidad de aproximadamente 350 g',1.05,1,3),
(21,'Almendra cruda','Bolsa de 250 g; sin sal',3.75,1,4),
(22,'Nuez con cáscara','Bolsa de 500 g',4.20,1,4),
(23,'Avellana tostada','Bolsa de 200 g; sin sal',2.95,1,4),
(24,'Perejil fresco','Manojo de aproximadamente 50 g',0.80,1,5),
(25,'Albahaca fresca','Bandeja de 30 g',1.45,1,5);

-- Datos: stock_tiendas (75 registros)
INSERT INTO `stock_tiendas` VALUES
(1,1,253),
(1,2,180),
(1,3,187),
(1,4,116),
(1,5,268),
(1,6,102),
(1,7,112),
(1,8,104),
(1,9,272),
(1,10,247),
(1,11,265),
(1,12,273),
(1,13,299),
(1,14,199),
(1,15,124),
(1,16,251),
(1,17,154),
(1,18,155),
(1,19,158),
(1,20,139),
(1,21,144),
(1,22,148),
(1,23,144),
(1,24,204),
(1,25,204),
(2,1,166),
(2,2,125),
(2,3,245),
(2,4,156),
(2,5,265),
(2,6,105),
(2,7,254),
(2,8,281),
(2,9,254),
(2,10,287),
(2,11,245),
(2,12,269),
(2,13,300),
(2,14,162),
(2,15,197),
(2,16,121),
(2,17,198),
(2,18,250),
(2,19,243),
(2,20,219),
(2,21,213),
(2,22,131),
(2,23,114),
(2,24,166),
(2,25,212),
(3,1,111),
(3,2,192),
(3,3,159),
(3,4,247),
(3,5,283),
(3,6,238),
(3,7,229),
(3,8,292),
(3,9,229),
(3,10,261),
(3,11,161),
(3,12,177),
(3,13,228),
(3,14,142),
(3,15,249),
(3,16,280),
(3,17,152),
(3,18,294),
(3,19,130),
(3,20,205),
(3,21,200),
(3,22,186),
(3,23,275),
(3,24,149),
(3,25,191);

-- Datos: pedidos (100 registros)
INSERT INTO `pedidos` VALUES
(1,'2026-09-01 19:00:00','pagado',1,4,1),
(2,'2026-09-02 05:00:00','pagado',2,5,2),
(3,'2026-09-02 15:00:00','pagado',3,6,3),
(4,'2026-09-03 01:00:00','enviado',4,7,1),
(5,'2026-09-03 11:00:00','pagado',5,2,2),
(6,'2026-09-03 21:00:00','pagado',6,3,3),
(7,'2026-09-04 07:00:00','pagado',7,4,1),
(8,'2026-09-04 17:00:00','enviado',8,5,2),
(9,'2026-09-05 03:00:00','pagado',9,3,3),
(10,'2026-09-05 13:00:00','pagado',10,7,1),
(11,'2026-09-05 23:00:00','pagado',11,2,2),
(12,'2026-09-06 09:00:00','enviado',12,6,3),
(13,'2026-09-06 19:00:00','pagado',13,7,1),
(14,'2026-09-07 05:00:00','pagado',14,5,2),
(15,'2026-09-07 15:00:00','pagado',15,3,3),
(16,'2026-09-08 01:00:00','enviado',16,7,1),
(17,'2026-09-08 11:00:00','pagado',17,5,2),
(18,'2026-09-08 21:00:00','pagado',18,3,3),
(19,'2026-09-09 07:00:00','pagado',19,1,1),
(20,'2026-09-09 17:00:00','enviado',20,5,2),
(21,'2026-09-10 03:00:00','pagado',1,6,3),
(22,'2026-09-10 13:00:00','pagado',2,1,1),
(23,'2026-09-10 23:00:00','pagado',3,2,2),
(24,'2026-09-11 09:00:00','enviado',4,6,3),
(25,'2026-09-11 19:00:00','pagado',5,1,1),
(26,'2026-09-12 05:00:00','pagado',6,5,2),
(27,'2026-09-12 15:00:00','pagado',7,6,3),
(28,'2026-09-13 01:00:00','enviado',8,1,1),
(29,'2026-09-13 11:00:00','pagado',9,5,2),
(30,'2026-09-13 21:00:00','pagado',10,3,3),
(31,'2026-09-14 07:00:00','pagado',11,7,1),
(32,'2026-09-14 17:00:00','enviado',12,2,2),
(33,'2026-09-15 03:00:00','pagado',13,6,3),
(34,'2026-09-15 13:00:00','pagado',14,7,1),
(35,'2026-09-15 23:00:00','pagado',15,5,2),
(36,'2026-09-16 09:00:00','enviado',16,3,3),
(37,'2026-09-16 19:00:00','pagado',17,7,1),
(38,'2026-09-17 05:00:00','pagado',18,5,2),
(39,'2026-09-17 15:00:00','pagado',19,6,3),
(40,'2026-09-18 01:00:00','enviado',20,4,1),
(41,'2026-09-18 11:00:00','pagado',1,2,2),
(42,'2026-09-18 21:00:00','pagado',2,6,3),
(43,'2026-09-19 07:00:00','pagado',3,1,1),
(44,'2026-09-19 17:00:00','enviado',4,2,2),
(45,'2026-09-20 03:00:00','pagado',5,6,3),
(46,'2026-09-20 13:00:00','pagado',6,1,1),
(47,'2026-09-20 23:00:00','pagado',7,5,2),
(48,'2026-09-21 09:00:00','enviado',8,6,3),
(49,'2026-09-21 19:00:00','pagado',9,1,1),
(50,'2026-09-22 05:00:00','pagado',10,2,2),
(51,'2026-09-22 15:00:00','pagado',11,3,3),
(52,'2026-09-23 01:00:00','enviado',12,4,1),
(53,'2026-09-23 11:00:00','pagado',13,2,2),
(54,'2026-09-23 21:00:00','pagado',14,3,3),
(55,'2026-09-24 07:00:00','pagado',15,1,1),
(56,'2026-09-24 17:00:00','enviado',16,2,2),
(57,'2026-09-25 03:00:00','pagado',17,6,3),
(58,'2026-09-25 13:00:00','pagado',18,7,1),
(59,'2026-09-25 23:00:00','pagado',19,5,2),
(60,'2026-09-26 09:00:00','enviado',20,3,3),
(61,'2026-09-26 19:00:00','pagado',1,1,1),
(62,'2026-09-27 05:00:00','pagado',2,2,2),
(63,'2026-09-27 15:00:00','pagado',3,6,3),
(64,'2026-09-28 01:00:00','enviado',4,4,1),
(65,'2026-09-28 11:00:00','pagado',5,2,2),
(66,'2026-09-28 21:00:00','pagado',6,6,3),
(67,'2026-09-29 07:00:00','pagado',7,4,1),
(68,'2026-09-29 17:00:00','enviado',8,5,2),
(69,'2026-09-30 03:00:00','pagado',9,6,3),
(70,'2026-09-30 13:00:00','pagado',10,1,1),
(71,'2026-09-30 23:00:00','pagado',11,2,2),
(72,'2026-10-01 09:00:00','enviado',12,3,3),
(73,'2026-10-01 19:00:00','pagado',13,1,1),
(74,'2026-10-02 05:00:00','pagado',14,5,2),
(75,'2026-10-02 15:00:00','pagado',15,6,3),
(76,'2026-10-03 01:00:00','enviado',16,1,1),
(77,'2026-10-03 11:00:00','pagado',17,2,2),
(78,'2026-10-03 21:00:00','pagado',18,3,3),
(79,'2026-10-04 07:00:00','pagado',19,1,1),
(80,'2026-10-04 17:00:00','enviado',20,5,2),
(81,'2026-10-05 03:00:00','pagado',1,6,3),
(82,'2026-10-05 13:00:00','pagado',2,7,1),
(83,'2026-10-05 23:00:00','pagado',3,2,2),
(84,'2026-10-06 09:00:00','enviado',4,6,3),
(85,'2026-10-06 19:00:00','pagado',5,4,1),
(86,'2026-10-07 05:00:00','pagado',6,2,2),
(87,'2026-10-07 15:00:00','pagado',7,3,3),
(88,'2026-10-08 01:00:00','enviado',8,7,1),
(89,'2026-10-08 11:00:00','pagado',9,5,2),
(90,'2026-10-08 21:00:00','pagado',10,6,3),
(91,'2026-10-09 07:00:00','pagado',11,4,1),
(92,'2026-10-09 17:00:00','enviado',12,2,2),
(93,'2026-10-10 03:00:00','pagado',13,3,3),
(94,'2026-10-10 13:00:00','pagado',14,7,1),
(95,'2026-10-10 23:00:00','pagado',15,2,2),
(96,'2026-10-11 09:00:00','enviado',16,6,3),
(97,'2026-10-11 19:00:00','pagado',17,1,1),
(98,'2026-10-12 05:00:00','pagado',18,5,2),
(99,'2026-10-12 15:00:00','pagado',19,6,3),
(100,'2026-10-13 01:00:00','enviado',20,7,1);

-- Datos: detalle_de_pedido (100 registros)
INSERT INTO `detalle_de_pedido` VALUES
(1,1,3,3.24,5.00),
(2,2,1,1.56,10.00),
(3,3,2,2.40,5.00),
(4,4,2,4.60,0.00),
(5,5,2,4.70,5.00),
(6,6,1,8.29,5.00),
(7,7,2,6.05,0.00),
(8,8,3,2.04,5.00),
(9,9,1,8.78,5.00),
(10,10,4,4.71,5.00),
(11,11,1,5.72,5.00),
(12,12,5,5.74,10.00),
(13,13,3,6.59,5.00),
(14,14,1,6.07,0.00),
(15,15,5,2.76,10.00),
(16,16,5,2.62,5.00),
(17,17,1,4.16,0.00),
(18,18,3,1.54,10.00),
(19,19,3,5.93,0.00),
(20,20,1,2.52,10.00),
(21,21,1,8.45,5.00),
(22,22,3,8.44,0.00),
(23,23,3,2.54,10.00),
(24,24,5,4.67,0.00),
(25,25,3,3.97,10.00),
(26,1,4,3.24,5.00),
(27,2,5,1.56,0.00),
(28,3,2,2.40,5.00),
(29,4,2,4.60,10.00),
(30,5,4,4.70,5.00),
(31,6,5,8.29,10.00),
(32,7,5,6.05,0.00),
(33,8,1,2.04,0.00),
(34,9,1,8.78,5.00),
(35,10,4,4.71,10.00),
(36,11,2,5.72,0.00),
(37,12,5,5.74,0.00),
(38,13,1,6.59,0.00),
(39,14,1,6.07,10.00),
(40,15,4,2.76,5.00),
(41,16,5,2.62,10.00),
(42,17,3,4.16,10.00),
(43,18,3,1.54,0.00),
(44,19,4,5.93,5.00),
(45,20,5,2.52,0.00),
(46,21,3,8.45,0.00),
(47,22,2,8.44,0.00),
(48,23,2,2.54,0.00),
(49,24,2,4.67,0.00),
(50,25,2,3.97,0.00),
(51,1,2,3.24,10.00),
(52,2,3,1.56,0.00),
(53,3,2,2.40,10.00),
(54,4,2,4.60,0.00),
(55,5,5,4.70,10.00),
(56,6,2,8.29,0.00),
(57,7,3,6.05,0.00),
(58,8,4,2.04,0.00),
(59,9,1,8.78,0.00),
(60,10,3,4.71,0.00),
(61,11,1,5.72,0.00),
(62,12,4,5.74,0.00),
(63,13,1,6.59,5.00),
(64,14,2,6.07,0.00),
(65,15,5,2.76,10.00),
(66,16,1,2.62,0.00),
(67,17,5,4.16,5.00),
(68,18,5,1.54,10.00),
(69,19,2,5.93,0.00),
(70,20,2,2.52,5.00),
(71,21,3,8.45,10.00),
(72,22,4,8.44,0.00),
(73,23,2,2.54,0.00),
(74,24,1,4.67,5.00),
(75,25,3,3.97,0.00),
(76,1,4,3.24,10.00),
(77,2,1,1.56,5.00),
(78,3,2,2.40,0.00),
(79,4,3,4.60,0.00),
(80,5,3,4.70,0.00),
(81,6,4,8.29,10.00),
(82,7,5,6.05,0.00),
(83,8,1,2.04,5.00),
(84,9,3,8.78,10.00),
(85,10,1,4.71,5.00),
(86,11,5,5.72,10.00),
(87,12,1,5.74,10.00),
(88,13,3,6.59,0.00),
(89,14,4,6.07,0.00),
(90,15,2,2.76,0.00),
(91,16,3,2.62,5.00),
(92,17,2,4.16,5.00),
(93,18,2,1.54,5.00),
(94,19,1,5.93,0.00),
(95,20,2,2.52,10.00),
(96,21,1,8.45,0.00),
(97,22,4,8.44,5.00),
(98,23,3,2.54,0.00),
(99,24,1,4.67,10.00),
(100,25,1,3.97,0.00);

-- Datos: proveedores (10 registros)
INSERT INTO `proveedores` VALUES
(1,'Huertas del Turia, S. L.','B1000001','+34 960 123 401','pedidos@proveedor1.example.com','Av. de los Naranjos, 32, bajo, 46022 Valencia'),
(2,'Cítricos Azahar, S. Coop.','B1000002','955-240-802','comercial@proveedor2.example.com','Calle Mayor, 108, 3.º C, 50001 Zaragoza'),
(3,'Frutas del Ebro, S. L.','B1000003','976 350 603','ventas@proveedor3.example.com','C/ de la Estación, 21, 48008 Bilbao'),
(4,'Hortalizas Vega Sur, S. L.','B1000004','0034 968 415 204','administracion@proveedor4.example.com','Avda. de Castilla, 45, 47008 Valladolid'),
(5,'Platanera Insular, S. Coop.','B1000005','922450705','distribucion@proveedor5.example.com','Plaza de España, 3, 03001 Alicante'),
(6,'Frutos Secos La Encina, S. L.','B1000006','+34 925 618 306','pedidos@proveedor6.example.com','Paseo del Parque, 6, 33203 Gijón'),
(7,'Aromáticas del Mediterráneo, S. L.','B1000007','950.720.907','info@proveedor7.example.com','Av. de Galicia, 64, 15004 A Coruña'),
(8,'Fresas Marisma, S. Coop.','B1000008','959 832 108','ventas@proveedor8.example.com','Calle del Mar, 16, 07012 Palma'),
(9,'Distribuciones Huerta Norte, S. L.','B1000009','944-915-609','logistica@proveedor9.example.com','C/ de la Acequia, 4, 18010 Granada'),
(10,'Agrofruta Sierra Verde, S. L.','B1000010','958026410','contacto@proveedor10.example.com','Calle de los Pinos, 30, 20009 Donostia');

-- Datos: proveedores_productos (100 registros)
INSERT INTO `proveedores_productos` VALUES
(1,1,0.72),
(1,8,0.45),
(1,9,2.94),
(1,10,2.37),
(1,11,1.44),
(1,18,1.26),
(1,19,0.75),
(1,20,0.63),
(1,21,2.25),
(2,1,0.78),
(2,2,0.62),
(2,9,3.19),
(2,10,2.57),
(2,11,1.56),
(2,12,0.75),
(2,19,0.81),
(2,20,0.68),
(2,21,2.44),
(2,22,2.73),
(3,1,0.84),
(3,2,0.67),
(3,3,0.32),
(3,10,2.77),
(3,11,1.68),
(3,12,0.81),
(3,13,0.91),
(3,20,0.74),
(3,21,2.63),
(3,22,2.94),
(3,23,2.07),
(4,1,0.66),
(4,2,0.52),
(4,3,0.25),
(4,4,1.79),
(4,11,1.32),
(4,12,0.63),
(4,13,0.72),
(4,14,1.07),
(4,21,2.06),
(4,22,2.31),
(4,23,1.62),
(4,24,0.44),
(5,2,0.57),
(5,3,0.27),
(5,4,1.95),
(5,5,1.68),
(5,12,0.69),
(5,13,0.78),
(5,14,1.17),
(5,15,0.51),
(5,22,2.52),
(5,23,1.77),
(5,24,0.48),
(5,25,0.87),
(6,3,0.29),
(6,4,2.11),
(6,5,1.82),
(6,6,0.72),
(6,13,0.85),
(6,14,1.27),
(6,15,0.55),
(6,16,1.46),
(6,23,1.92),
(6,24,0.52),
(6,25,0.94),
(7,4,2.28),
(7,5,1.96),
(7,6,0.77),
(7,7,1.65),
(7,14,1.37),
(7,15,0.60),
(7,16,1.58),
(7,17,2.52),
(7,24,0.56),
(7,25,1.02),
(8,5,1.54),
(8,6,0.61),
(8,7,1.29),
(8,8,0.41),
(8,15,0.47),
(8,16,1.24),
(8,17,1.98),
(8,18,1.16),
(8,25,0.80),
(9,6,0.66),
(9,7,1.41),
(9,8,0.45),
(9,9,2.94),
(9,16,1.35),
(9,17,2.16),
(9,18,1.26),
(9,19,0.75),
(10,7,1.53),
(10,8,0.49),
(10,9,3.19),
(10,10,2.57),
(10,17,2.34),
(10,18,1.37),
(10,19,0.81),
(10,20,0.68);

-- Datos: pagos (100 registros)
INSERT INTO `pagos` VALUES
(1,1,'tarjeta',9.23,'2026-09-01 19:05:00'),
(2,2,'efectivo',1.40,'2026-09-02 05:05:00'),
(3,3,'tarjeta',4.56,'2026-09-02 15:05:00'),
(4,4,'efectivo',9.20,'2026-09-03 01:05:00'),
(5,5,'tarjeta',8.93,'2026-09-03 11:05:00'),
(6,6,'efectivo',7.88,'2026-09-03 21:05:00'),
(7,7,'tarjeta',12.10,'2026-09-04 07:05:00'),
(8,8,'efectivo',5.81,'2026-09-04 17:05:00'),
(9,9,'tarjeta',8.34,'2026-09-05 03:05:00'),
(10,10,'efectivo',17.90,'2026-09-05 13:05:00'),
(11,11,'tarjeta',5.43,'2026-09-05 23:05:00'),
(12,12,'efectivo',25.83,'2026-09-06 09:05:00'),
(13,13,'tarjeta',18.78,'2026-09-06 19:05:00'),
(14,14,'efectivo',6.07,'2026-09-07 05:05:00'),
(15,15,'tarjeta',12.42,'2026-09-07 15:05:00'),
(16,16,'efectivo',12.45,'2026-09-08 01:05:00'),
(17,17,'tarjeta',4.16,'2026-09-08 11:05:00'),
(18,18,'efectivo',4.16,'2026-09-08 21:05:00'),
(19,19,'tarjeta',17.79,'2026-09-09 07:05:00'),
(20,20,'efectivo',2.27,'2026-09-09 17:05:00'),
(21,21,'tarjeta',8.03,'2026-09-10 03:05:00'),
(22,22,'efectivo',25.32,'2026-09-10 13:05:00'),
(23,23,'tarjeta',6.86,'2026-09-10 23:05:00'),
(24,24,'efectivo',23.35,'2026-09-11 09:05:00'),
(25,25,'tarjeta',10.72,'2026-09-11 19:05:00'),
(26,26,'efectivo',12.31,'2026-09-12 05:05:00'),
(27,27,'tarjeta',7.80,'2026-09-12 15:05:00'),
(28,28,'efectivo',4.56,'2026-09-13 01:05:00'),
(29,29,'tarjeta',8.28,'2026-09-13 11:05:00'),
(30,30,'efectivo',17.86,'2026-09-13 21:05:00'),
(31,31,'tarjeta',37.31,'2026-09-14 07:05:00'),
(32,32,'efectivo',30.25,'2026-09-14 17:05:00'),
(33,33,'tarjeta',2.04,'2026-09-15 03:05:00'),
(34,34,'efectivo',8.34,'2026-09-15 13:05:00'),
(35,35,'tarjeta',16.96,'2026-09-15 23:05:00'),
(36,36,'efectivo',11.44,'2026-09-16 09:05:00'),
(37,37,'tarjeta',28.70,'2026-09-16 19:05:00'),
(38,38,'efectivo',6.59,'2026-09-17 05:05:00'),
(39,39,'tarjeta',5.46,'2026-09-17 15:05:00'),
(40,40,'efectivo',10.49,'2026-09-18 01:05:00'),
(41,41,'tarjeta',11.79,'2026-09-18 11:05:00'),
(42,42,'efectivo',11.23,'2026-09-18 21:05:00'),
(43,43,'tarjeta',4.62,'2026-09-19 07:05:00'),
(44,44,'efectivo',22.53,'2026-09-19 17:05:00'),
(45,45,'tarjeta',12.60,'2026-09-20 03:05:00'),
(46,46,'efectivo',25.35,'2026-09-20 13:05:00'),
(47,47,'tarjeta',16.88,'2026-09-20 23:05:00'),
(48,48,'efectivo',5.08,'2026-09-21 09:05:00'),
(49,49,'tarjeta',9.34,'2026-09-21 19:05:00'),
(50,50,'efectivo',7.94,'2026-09-22 05:05:00'),
(51,51,'tarjeta',5.83,'2026-09-22 15:05:00'),
(52,52,'efectivo',4.68,'2026-09-23 01:05:00'),
(53,53,'tarjeta',4.32,'2026-09-23 11:05:00'),
(54,54,'efectivo',9.20,'2026-09-23 21:05:00'),
(55,55,'tarjeta',21.15,'2026-09-24 07:05:00'),
(56,56,'efectivo',16.58,'2026-09-24 17:05:00'),
(57,57,'tarjeta',18.15,'2026-09-25 03:05:00'),
(58,58,'efectivo',8.16,'2026-09-25 13:05:00'),
(59,59,'tarjeta',8.78,'2026-09-25 23:05:00'),
(60,60,'efectivo',14.13,'2026-09-26 09:05:00'),
(61,61,'tarjeta',5.72,'2026-09-26 19:05:00'),
(62,62,'efectivo',22.96,'2026-09-27 05:05:00'),
(63,63,'tarjeta',6.26,'2026-09-27 15:05:00'),
(64,64,'efectivo',12.14,'2026-09-28 01:05:00'),
(65,65,'tarjeta',12.42,'2026-09-28 11:05:00'),
(66,66,'efectivo',2.62,'2026-09-28 21:05:00'),
(67,67,'tarjeta',19.76,'2026-09-29 07:05:00'),
(68,68,'efectivo',6.93,'2026-09-29 17:05:00'),
(69,69,'tarjeta',11.86,'2026-09-30 03:05:00'),
(70,70,'efectivo',4.79,'2026-09-30 13:05:00'),
(71,71,'tarjeta',22.82,'2026-09-30 23:05:00'),
(72,72,'efectivo',33.76,'2026-10-01 09:05:00'),
(73,73,'tarjeta',5.08,'2026-10-01 19:05:00'),
(74,74,'efectivo',4.44,'2026-10-02 05:05:00'),
(75,75,'tarjeta',11.91,'2026-10-02 15:05:00'),
(76,76,'efectivo',11.66,'2026-10-03 01:05:00'),
(77,77,'tarjeta',1.48,'2026-10-03 11:05:00'),
(78,78,'efectivo',4.80,'2026-10-03 21:05:00'),
(79,79,'tarjeta',13.80,'2026-10-04 07:05:00'),
(80,80,'efectivo',14.10,'2026-10-04 17:05:00'),
(81,81,'tarjeta',29.84,'2026-10-05 03:05:00'),
(82,82,'efectivo',30.25,'2026-10-05 13:05:00'),
(83,83,'tarjeta',1.94,'2026-10-05 23:05:00'),
(84,84,'efectivo',23.71,'2026-10-06 09:05:00'),
(85,85,'tarjeta',4.47,'2026-10-06 19:05:00'),
(86,86,'efectivo',25.74,'2026-10-07 05:05:00'),
(87,87,'tarjeta',5.17,'2026-10-07 15:05:00'),
(88,88,'efectivo',19.77,'2026-10-08 01:05:00'),
(89,89,'tarjeta',24.28,'2026-10-08 11:05:00'),
(90,90,'efectivo',5.52,'2026-10-08 21:05:00'),
(91,91,'tarjeta',7.47,'2026-10-09 07:05:00'),
(92,92,'efectivo',7.90,'2026-10-09 17:05:00'),
(93,93,'tarjeta',2.93,'2026-10-10 03:05:00'),
(94,94,'efectivo',5.93,'2026-10-10 13:05:00'),
(95,95,'tarjeta',4.54,'2026-10-10 23:05:00'),
(96,96,'efectivo',8.45,'2026-10-11 09:05:00'),
(97,97,'tarjeta',32.07,'2026-10-11 19:05:00'),
(98,98,'efectivo',7.62,'2026-10-12 05:05:00'),
(99,99,'tarjeta',4.20,'2026-10-12 15:05:00'),
(100,100,'efectivo',3.97,'2026-10-13 01:05:00');

COMMIT;
SET FOREIGN_KEY_CHECKS = @OLD_FOREIGN_KEY_CHECKS;
SET SQL_MODE = @OLD_SQL_MODE;
SET TIME_ZONE = @OLD_TIME_ZONE;
SET CHARACTER_SET_CLIENT = @OLD_CHARACTER_SET_CLIENT;
SET CHARACTER_SET_RESULTS = @OLD_CHARACTER_SET_RESULTS;
SET COLLATION_CONNECTION = @OLD_COLLATION_CONNECTION;

-- Recuento tras la importación.

SELECT 'categorias' AS tabla, COUNT(*) AS registros FROM `categorias`
UNION ALL
SELECT 'clientes' AS tabla, COUNT(*) AS registros FROM `clientes`
UNION ALL
SELECT 'tiendas' AS tabla, COUNT(*) AS registros FROM `tiendas`
UNION ALL
SELECT 'usuarios' AS tabla, COUNT(*) AS registros FROM `usuarios`
UNION ALL
SELECT 'productos' AS tabla, COUNT(*) AS registros FROM `productos`
UNION ALL
SELECT 'stock_tiendas' AS tabla, COUNT(*) AS registros FROM `stock_tiendas`
UNION ALL
SELECT 'pedidos' AS tabla, COUNT(*) AS registros FROM `pedidos`
UNION ALL
SELECT 'detalle_de_pedido' AS tabla, COUNT(*) AS registros FROM `detalle_de_pedido`
UNION ALL
SELECT 'proveedores' AS tabla, COUNT(*) AS registros FROM `proveedores`
UNION ALL
SELECT 'proveedores_productos' AS tabla, COUNT(*) AS registros FROM `proveedores_productos`
UNION ALL
SELECT 'pagos' AS tabla, COUNT(*) AS registros FROM `pagos`;
