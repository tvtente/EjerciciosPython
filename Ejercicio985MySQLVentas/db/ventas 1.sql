-- phpMyAdmin SQL Dump
-- version 5.2.3
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `ventas`
-- ATENCIÓN: este script elimina las cuatro tablas y todos sus datos anteriores.
-- Después restaura la estructura, índices, relaciones y datos de este archivo.
-- Se elimina primero pedido porque referencia cliente y comercial.
-- No se elimina la base de datos ni otras tablas ajenas al script.
CREATE DATABASE IF NOT EXISTS `ventas`
  CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `ventas`;

DROP TABLE IF EXISTS `pedido`;
DROP TABLE IF EXISTS `clientesdos`;
DROP TABLE IF EXISTS `comercial`;
DROP TABLE IF EXISTS `cliente`;


-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cliente`
--

CREATE TABLE `cliente` (
  `idCliente` int(10) UNSIGNED NOT NULL,
  `Nombre` varchar(25) NOT NULL,
  `Apellido1` varchar(25) NOT NULL,
  `Apellido2` varchar(25) DEFAULT NULL,
  `Ciudad` varchar(35) DEFAULT NULL,
  `Categoria` int(10) UNSIGNED DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `cliente` (50 registros)
--

INSERT INTO `cliente` (`idCliente`, `Nombre`, `Apellido1`, `Apellido2`, `Ciudad`, `Categoria`) VALUES
(1, 'Aarón', 'Rivero', 'Gómez', 'Almería', 100),
(2, 'Adela', 'Salas', 'Díaz', 'Granada', 200),
(3, 'Adolfo', 'Rubio', 'Flores', 'Sevilla', NULL),
(4, 'Adrián', 'Suárez', NULL, 'Jaén', 300),
(5, 'Marcos', 'Loyola', 'Méndez', 'Almería', 200),
(6, 'María', 'Santana', 'Moreno', 'Cádiz', 100),
(7, 'Pilar', 'Ruiz', NULL, 'Sevilla', 300),
(8, 'Pepe', 'Ruiz', 'Santana', 'Huelva', 200),
(9, 'Guillermo', 'López', 'Gómez', 'Granada', 225),
(10, 'Daniel', 'Santana', 'Loyola', 'Sevilla', 125),
(11, 'Lucía', 'Martínez', 'Pérez', 'Málaga', 150),
(12, 'Carlos', 'García', 'López', 'Córdoba', 200),
(13, 'Sofía', 'Fernández', NULL, 'Almería', 100),
(14, 'Alejandro', 'González', 'Romero', 'Granada', 250),
(15, 'Elena', 'Rodríguez', 'Sánchez', 'Sevilla', 300),
(16, 'David', 'Jiménez', NULL, 'Cádiz', 100),
(17, 'Carmen', 'Moreno', 'Alonso', 'Huelva', 175),
(18, 'Javier', 'Muñoz', 'Álvarez', 'Jaén', 225),
(19, 'Rosa', 'Álvarez', 'Gutiérrez', 'Málaga', NULL),
(20, 'Miguel', 'Romero', 'Navarro', 'Córdoba', 125),
(21, 'Laura', 'Alonso', NULL, 'Almería', 200),
(22, 'Francisco', 'Gutiérrez', 'Torres', 'Granada', 300),
(23, 'Ana', 'Navarro', 'Domínguez', 'Sevilla', 100),
(24, 'Pedro', 'Torres', NULL, 'Cádiz', 150),
(25, 'Teresa', 'Domínguez', 'Vázquez', 'Huelva', 200),
(26, 'Manuel', 'Vázquez', 'Ramos', 'Jaén', 250),
(27, 'Isabel', 'Ramos', 'Gil', 'Málaga', 300),
(28, 'Jose', 'Gil', NULL, 'Córdoba', 100),
(29, 'Beatriz', 'Serrano', 'Blanco', 'Almería', 125),
(30, 'Antonio', 'Blanco', 'Molina', 'Granada', 175),
(31, 'Raquel', 'Molina', NULL, 'Sevilla', 200),
(32, 'Alberto', 'Morales', 'Ortega', 'Cádiz', 225),
(33, 'Patricia', 'Ortega', 'Delgado', 'Huelva', 250),
(34, 'Sergio', 'Delgado', NULL, 'Jaén', 300),
(35, 'Cristina', 'Castro', 'Ortiz', 'Málaga', 100),
(36, 'Rubén', 'Ortiz', 'Rubio', 'Córdoba', 150),
(37, 'Nuria', 'Silva', NULL, 'Almería', 200),
(38, 'Jorge', 'Iglesias', 'Sanz', 'Granada', 250),
(39, 'Marta', 'Sanz', 'Medina', 'Sevilla', 300),
(40, 'Raúl', 'Medina', NULL, 'Cádiz', 100),
(41, 'Claudia', 'Garrido', 'Castillo', 'Huelva', 125),
(42, 'Iván', 'Castillo', 'Cortes', 'Jaén', 175),
(43, 'Sonia', 'Cortes', NULL, 'Málaga', 200),
(44, 'Héctor', 'Cruz', 'Pascual', 'Córdoba', 225),
(45, 'Marina', 'Pascual', 'Herrero', 'Almería', 250),
(46, 'Vicente', 'Herrero', NULL, 'Granada', 300),
(47, 'Yolanda', 'Vidal', 'León', 'Sevilla', 100),
(48, 'Álvaro', 'León', 'Marín', 'Cádiz', 150),
(49, 'Lorena', 'Marín', NULL, 'Huelva', 200),
(50, 'Enrique', 'Ibáñez', 'Giménez', 'Jaén', 250);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `clientesdos`
--

CREATE TABLE `clientesdos` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `email` varchar(150) DEFAULT NULL,
  `creado_en` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish2_ci;

--
-- Volcado de datos para la tabla `clientesdos` (50 registros)
--

INSERT INTO `clientesdos` (`id`, `nombre`, `email`, `creado_en`) VALUES
(1, 'María Pérez', 'maria@ejemplo.com', '2026-10-15 12:57:45'),
(2, 'Juan Gómez', 'juan.gomez@ejemplo.com', '2026-01-10 08:30:00'),
(3, 'Ana López', 'ana.lopez@ejemplo.com', '2026-01-12 09:15:22'),
(4, 'Luis Martínez', 'luis.martinez@ejemplo.com', '2026-02-01 10:20:11'),
(5, 'Carmen Ruiz', 'carmen.ruiz@ejemplo.com', '2026-02-05 11:45:30'),
(6, 'José Sánchez', 'jose.sanchez@ejemplo.com', '2026-02-10 14:10:05'),
(7, 'Laura Díaz', 'laura.diaz@ejemplo.com', '2026-02-15 16:22:33'),
(8, 'David Moreno', 'david.moreno@ejemplo.com', '2026-03-01 09:05:40'),
(9, 'Sara Álvarez', 'sara.alvarez@ejemplo.com', '2026-03-05 11:30:15'),
(10, 'Javier Romero', 'javier.romero@ejemplo.com', '2026-03-10 13:50:20'),
(11, 'Elena Alonso', 'elena.alonso@ejemplo.com', '2026-03-15 15:40:50'),
(12, 'Miguel Gutiérrez', 'miguel.gutierrez@ejemplo.com', '2026-03-20 08:12:18'),
(13, 'Lucía Navarro', 'lucia.navarro@ejemplo.com', '2026-04-01 10:25:35'),
(14, 'Carlos Torres', 'carlos.torres@ejemplo.com', '2026-04-05 12:15:48'),
(15, 'Sofía Domínguez', 'sofia.dominguez@ejemplo.com', '2026-04-10 14:33:12'),
(16, 'Alejandro Vázquez', 'alejandro.vazquez@ejemplo.com', '2026-04-15 17:01:25'),
(17, 'Paula Ramos', 'paula.ramos@ejemplo.com', '2026-05-01 09:40:00'),
(18, 'Adrián Gil', 'adrian.gil@ejemplo.com', '2026-05-06 11:20:15'),
(19, 'Beatriz Serrano', 'beatriz.serrano@ejemplo.com', '2026-05-10 13:10:45'),
(20, 'Sergio Blanco', 'sergio.blanco@ejemplo.com', '2026-05-15 16:55:20'),
(21, 'Patricia Molina', 'patricia.molina@ejemplo.com', '2026-06-01 08:50:10'),
(22, 'Jorge Morales', 'jorge.morales@ejemplo.com', '2026-06-05 10:05:30'),
(23, 'Cristina Ortega', 'cristina.ortega@ejemplo.com', '2026-06-10 12:40:15'),
(24, 'Rubén Delgado', 'ruben.delgado@ejemplo.com', '2026-06-15 15:30:22'),
(25, 'Nuria Castro', 'nuria.castro@ejemplo.com', '2026-07-01 09:15:55'),
(26, 'Alberto Ortiz', 'alberto.ortiz@ejemplo.com', '2026-07-06 11:35:40'),
(27, 'Marta Silva', 'marta.silva@ejemplo.com', '2026-07-10 13:20:10'),
(28, 'Raúl Iglesias', 'raul.iglesias@ejemplo.com', '2026-07-15 16:10:25'),
(29, 'Claudia Sanz', 'claudia.sanz@ejemplo.com', '2026-08-01 08:30:45'),
(30, 'Iván Medina', 'ivan.medina@ejemplo.com', '2026-08-05 10:45:12'),
(31, 'Sonia Garrido', 'sonia.garrido@ejemplo.com', '2026-08-10 12:00:33'),
(32, 'Héctor Castillo', 'hector.castillo@ejemplo.com', '2026-08-15 14:15:50'),
(33, 'Marina Cortes', 'marina.cortes@ejemplo.com', '2026-09-01 09:22:15'),
(34, 'Vicente Cruz', 'vicente.cruz@ejemplo.com', '2026-09-05 11:05:20'),
(35, 'Yolanda Pascual', 'yolanda.pascual@ejemplo.com', '2026-09-10 13:40:10'),
(36, 'Álvaro Herrero', 'alvaro.herrero@ejemplo.com', '2026-09-15 15:50:45'),
(37, 'Lorena Vidal', 'lorena.vidal@ejemplo.com', '2026-10-01 08:15:00'),
(38, 'Enrique León', 'enrique.leon@ejemplo.com', '2026-10-02 09:30:15'),
(39, 'Raquel Marín', 'raquel.marin@ejemplo.com', '2026-10-03 10:45:22'),
(40, 'Daniela Ibáñez', 'daniela.ibanez@ejemplo.com', '2026-10-04 11:55:30'),
(41, 'Francisco Giménez', 'francisco.gimenez@ejemplo.com', '2026-10-05 12:10:05'),
(42, 'Antonia Cano', 'antonia.cano@ejemplo.com', '2026-10-06 13:25:40'),
(43, 'Gabriel Prieto', 'gabriel.prieto@ejemplo.com', '2026-10-07 14:40:12'),
(44, 'Silvia Calvo', 'silvia.calvo@ejemplo.com', '2026-10-08 15:15:50'),
(45, 'Alfonso Peña', 'alfonso.pena@ejemplo.com', '2026-10-09 16:30:20'),
(46, 'Rosa Cuesta', 'rosa.cuesta@ejemplo.com', '2026-10-10 17:05:15'),
(47, 'Manuel Campos', 'manuel.campos@ejemplo.com', '2026-10-11 08:45:33'),
(48, 'Teresa Vega', 'teresa.vega@ejemplo.com', '2026-10-12 09:50:11'),
(49, 'Guillermo Fuentes', 'guillermo.fuentes@ejemplo.com', '2026-10-13 11:10:25'),
(50, 'Adriana Benito', 'adriana.benito@ejemplo.com', '2026-10-14 12:20:40');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `comercial`
--

CREATE TABLE `comercial` (
  `id` int(10) UNSIGNED NOT NULL,
  `Nombre` varchar(30) NOT NULL,
  `Apellido1` varchar(25) NOT NULL,
  `Apellido2` varchar(25) DEFAULT NULL,
  `comision` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `comercial` (50 registros)
--

INSERT INTO `comercial` (`id`, `Nombre`, `Apellido1`, `Apellido2`, `comision`) VALUES
(1, 'Daniel', 'Sáez', 'Vega', 0.15),
(2, 'Juan', 'Gómez', 'López', 0.13),
(3, 'Diego', 'Flores', 'Salas', 0.11),
(4, 'Marta', 'Herrera', 'Gil', 0.14),
(5, 'Antonio', 'Carretero', 'Ortega', 0.12),
(6, 'Manuel', 'Domínguez', 'Hernández', 0.13),
(7, 'Antonio', 'Vega', 'Hernández', 0.11),
(8, 'Alfredo', 'Ruiz', 'Flores', 0.05),
(9, 'María', 'Jiménez', 'Pérez', 0.10),
(10, 'Carlos', 'Martínez', 'Sánchez', 0.12),
(11, 'Lucía', 'García', NULL, 0.14),
(12, 'Pedro', 'Rodríguez', 'Gómez', 0.15),
(13, 'Ana', 'López', 'Martín', 0.11),
(14, 'Javier', 'Sánchez', NULL, 0.13),
(15, 'Elena', 'Pérez', 'García', 0.12),
(16, 'Miguel', 'Gómez', 'Ruiz', 0.10),
(17, 'Laura', 'Martín', 'Jiménez', 0.14),
(18, 'Sergio', 'García', NULL, 0.15),
(19, 'Carmen', 'Fernández', 'López', 0.11),
(20, 'Francisco', 'González', 'Martínez', 0.13),
(21, 'Sofía', 'Rodríguez', 'Pérez', 0.12),
(22, 'David', 'Sánchez', NULL, 0.10),
(23, 'Paula', 'Pérez', 'García', 0.14),
(24, 'Alejandro', 'Martínez', 'Gómez', 0.15),
(25, 'Beatriz', 'García', 'Ruiz', 0.11),
(26, 'Jorge', 'López', NULL, 0.13),
(27, 'Marina', 'Jiménez', 'Martín', 0.12),
(28, 'Alberto', 'Ruiz', 'Sánchez', 0.10),
(29, 'Cristina', 'Gómez', 'Pérez', 0.14),
(30, 'Rubén', 'Martín', NULL, 0.15),
(31, 'Nuria', 'Pérez', 'García', 0.11),
(32, 'Raúl', 'García', 'Gómez', 0.13),
(33, 'Claudia', 'Fernández', 'Ruiz', 0.12),
(34, 'Iván', 'González', NULL, 0.10),
(35, 'Sonia', 'Rodríguez', 'Martín', 0.14),
(36, 'Héctor', 'Sánchez', 'Pérez', 0.15),
(37, 'Yolanda', 'Pérez', 'García', 0.11),
(38, 'Álvaro', 'Martínez', NULL, 0.13),
(39, 'Lorena', 'García', 'Gómez', 0.12),
(40, 'Enrique', 'López', 'Ruiz', 0.10),
(41, 'Raquel', 'Jiménez', 'Martín', 0.14),
(42, 'Daniela', 'Ruiz', 'Sánchez', 0.15),
(43, 'Gabriel', 'Gómez', NULL, 0.11),
(44, 'Silvia', 'Martín', 'Pérez', 0.13),
(45, 'Alfonso', 'Pérez', 'García', 0.12),
(46, 'Rosa', 'García', 'Gómez', 0.10),
(47, 'Manuel', 'Fernández', 'Ruiz', 0.14),
(48, 'Teresa', 'González', NULL, 0.15),
(49, 'Guillermo', 'Rodríguez', 'Martín', 0.11),
(50, 'Adriana', 'Sánchez', 'Pérez', 0.13);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pedido`
--

CREATE TABLE `pedido` (
  `id` int(10) UNSIGNED NOT NULL,
  `Total` double NOT NULL,
  `Fecha` date DEFAULT NULL,
  `ID_Cliente` int(10) UNSIGNED NOT NULL,
  `ID_Comercial` int(10) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `pedido` (50 registros)
--

INSERT INTO `pedido` (`id`, `Total`, `Fecha`, `ID_Cliente`, `ID_Comercial`) VALUES
(1, 150.50, '2017-10-05', 5, 2),
(2, 270.65, '2016-09-10', 1, 5),
(3, 65.26, '2017-10-05', 2, 1),
(4, 110.50, '2016-08-17', 8, 3),
(5, 948.50, '2017-09-10', 5, 2),
(6, 2400.60, '2016-07-27', 7, 1),
(7, 5760.00, '2015-09-10', 2, 1),
(8, 1983.43, '2017-10-10', 4, 6),
(9, 2480.40, '2016-10-10', 8, 3),
(10, 250.45, '2015-06-27', 8, 2),
(11, 75.29, '2016-08-17', 3, 7),
(12, 3045.60, '2017-04-25', 2, 1),
(13, 545.75, '2019-01-25', 6, 1),
(14, 145.82, '2017-02-02', 6, 1),
(15, 370.85, '2019-03-11', 1, 5),
(16, 2389.23, '2019-03-11', 1, 5),
(17, 432.10, '2018-05-12', 12, 4),
(18, 1205.80, '2018-06-15', 15, 8),
(19, 89.90, '2018-07-20', 10, 12),
(20, 1560.00, '2018-08-22', 22, 15),
(21, 340.25, '2019-04-05', 14, 10),
(22, 780.12, '2019-05-14', 18, 20),
(23, 2350.00, '2019-06-18', 25, 22),
(24, 95.40, '2019-07-25', 30, 25),
(25, 4120.50, '2020-01-10', 33, 28),
(26, 615.30, '2020-02-15', 40, 30),
(27, 1820.75, '2020-03-20', 45, 32),
(28, 520.00, '2020-04-12', 50, 35),
(29, 1430.80, '2021-05-19', 11, 38),
(30, 310.20, '2021-06-21', 16, 40),
(31, 890.45, '2021-07-14', 19, 42),
(32, 2150.90, '2021-08-30', 23, 45),
(33, 460.10, '2022-01-11', 27, 48),
(34, 1250.00, '2022-02-22', 31, 50),
(35, 740.60, '2022-03-15', 36, 3),
(36, 1920.30, '2022-04-18', 41, 7),
(37, 3100.00, '2023-05-20', 46, 11),
(38, 550.25, '2023-06-25', 4, 14),
(39, 1340.80, '2023-07-12', 9, 18),
(40, 210.15, '2023-08-05', 13, 21),
(41, 980.50, '2024-01-15', 17, 24),
(42, 2450.00, '2024-02-18', 21, 27),
(43, 670.40, '2024-03-22', 26, 29),
(44, 1120.90, '2024-04-10', 29, 33),
(45, 3340.10, '2025-05-14', 34, 36),
(46, 490.75, '2025-06-19', 38, 39),
(47, 1680.20, '2025-07-25', 42, 43),
(48, 750.00, '2025-08-11', 47, 46),
(49, 2980.30, '2026-01-20', 48, 49),
(50, 620.50, '2026-02-14', 49, 2);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `cliente`
--
ALTER TABLE `cliente`
  ADD PRIMARY KEY (`idCliente`);

--
-- Indices de la tabla `clientesdos`
--
ALTER TABLE `clientesdos`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indices de la tabla `comercial`
--
ALTER TABLE `comercial`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `pedido`
--
ALTER TABLE `pedido`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_cliente` (`ID_Cliente`),
  ADD KEY `id_comercial` (`ID_Comercial`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `cliente`
--
ALTER TABLE `cliente`
  MODIFY `idCliente` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=51;

--
-- AUTO_INCREMENT de la tabla `clientesdos`
--
ALTER TABLE `clientesdos`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=51;

--
-- AUTO_INCREMENT de la tabla `comercial`
--
ALTER TABLE `comercial`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=51;

--
-- AUTO_INCREMENT de la tabla `pedido`
--
ALTER TABLE `pedido`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=51;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `pedido`
--
ALTER TABLE `pedido`
  ADD CONSTRAINT `pedido_ibfk_1` FOREIGN KEY (`ID_Cliente`) REFERENCES `cliente` (`idCliente`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `pedido_ibfk_2` FOREIGN KEY (`ID_Comercial`) REFERENCES `comercial` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;