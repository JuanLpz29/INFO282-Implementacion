-- phpMyAdmin SQL Dump
-- version 4.9.5
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Dec 06, 2021 at 10:52 PM
-- Server version: 5.7.36-google-log
-- PHP Version: 5.5.38

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `taller`
--

-- --------------------------------------------------------

--
-- Table structure for table `Compra`
--

CREATE TABLE `Compra` (
  `idCompra` int(11) NOT NULL,
  `idProveedor` int(11) NOT NULL,
  `montoTotal` int(11) DEFAULT NULL,
  `montoNeto` int(11) DEFAULT NULL,
  `fecha` date DEFAULT NULL,
  `tipoDocumento` varchar(64) DEFAULT NULL,
  `folio` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `Compra`
--

INSERT INTO `Compra` (`idCompra`, `idProveedor`, `montoTotal`, `montoNeto`, `fecha`, `tipoDocumento`, `folio`) VALUES
(1, 1, 32873, 24606, '2021-09-24', 'FACTURA ELECTRÓNICA', 123828080),
(2, 1, 51473, 38312, '2021-09-14', 'FACTURA ELECTRÓNICA', 123558274),
(3, 2, 68955, 57945, '2021-10-05', 'FACTURA ELECTRÓNICA', 22702580),
(4, 1, 116127, 85118, '2021-09-24', 'FACTURA ELECTRÓNICA', 123828086),
(5, 3, 12651, 10632, '2021-10-06', 'FACTURA ELECTRÓNICA', 13453534),
(6, 1, 782187, 573639, '2021-09-24', 'FACTURA ELECTRÓNICA', 123828085),
(7, 3, 74489, 62597, '2021-10-06', 'FACTURA ELECTRÓNICA', 13453533);

-- --------------------------------------------------------

--
-- Table structure for table `Producto`
--

CREATE TABLE `Producto` (
  `idProducto` int(11) NOT NULL,
  `nombre` varchar(50) DEFAULT NULL,
  `descripcion` varchar(50) DEFAULT NULL,
  `stock` int(11) DEFAULT NULL,
  `categoria` varchar(25) DEFAULT NULL,
  `formato` varchar(25) DEFAULT NULL,
  `codigoBarra` varchar(16) DEFAULT NULL,
  `foto` blob,
  `cantidadRiesgo` int(11) DEFAULT NULL,
  `precioVenta` int(11) DEFAULT NULL,
  `precioUnitario` int(11) DEFAULT NULL,
  `valorItem` int(11) DEFAULT NULL,
  `oculto` tinyint(1) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `Producto`
--

INSERT INTO `Producto` (`idProducto`, `nombre`, `descripcion`, `stock`, `categoria`, `formato`, `codigoBarra`, `foto`, `cantidadRiesgo`, `precioVenta`, `precioUnitario`, `valorItem`, `oculto`) VALUES
(1, 'Red Bull Tradicional 12Pc Lat250Cc', 'RED BULL TRADICIONAL 12PC LAT250CC', 1, NULL, NULL, '870657', NULL, NULL, NULL, 9976, 9976, 0),
(2, 'Red Bull 355Ml', 'RED BULL TRADIC_12PF-LATA355CC', 1, NULL, NULL, '9002490221010', NULL, NULL, NULL, 14183, 14183, 0),
(3, 'Rb Sugarfree Import 8Pf-Lat250Cc', 'RB SUGARFREE IMPORT 8PF-LAT250CC', 2, NULL, NULL, '871093', NULL, NULL, NULL, 6821, 6821, 0),
(4, 'Flete De Mercaderias', 'Flete de Mercaderias', 4, NULL, NULL, '9999', NULL, NULL, NULL, 2428, 2428, 0),
(5, 'Red Bull Tradic 12Pc-Lata473Cc', 'RED BULL TRADIC 12PC-LATA473CC', 13, NULL, NULL, '870837', NULL, NULL, NULL, 15979, 15979, 0),
(6, 'Mant. Colun 250', 'MANT. COLUN 250', 8, NULL, NULL, '2203308', NULL, NULL, NULL, 5264, 5264, 0),
(7, 'Uht Crema Colun 200', 'UHT CREMA COLUN 200', 2, NULL, NULL, '2225336', NULL, NULL, NULL, 2790, 2790, 0),
(8, 'Manjar Colun Pot 200', 'MANJAR COLUN POT 200', 1, NULL, NULL, '2241129', NULL, NULL, NULL, 2526, 2526, 0),
(9, 'Manjar Colun Bol 500', 'MANJAR COLUN BOL 500', 3, NULL, NULL, '2241366', NULL, NULL, NULL, 2052, 2052, 0),
(10, 'Manjar Colun Bol 1K', 'MANJAR COLUN BOL 1K', 9, NULL, NULL, '2241455', NULL, NULL, NULL, 1685, 1685, 0),
(11, 'Yog. Colun 1K Frambuesa', 'YOG. COLUN 1K FRAMBUESA', 2, NULL, NULL, '2242095', NULL, NULL, NULL, 937, 937, 0),
(12, 'Yog. Colun 1K Frutilla', 'YOG. COLUN 1K FRUTILLA', 2, NULL, NULL, '2242265', NULL, NULL, NULL, 937, 937, 0),
(13, 'Yog. Colun 1K Platano', 'YOG. COLUN 1K PLATANO', 2, NULL, NULL, '2242362', NULL, NULL, NULL, 937, 937, 0),
(14, 'Yog. Colun 1K Damasco', 'YOG. COLUN 1K DAMASCO', 2, NULL, NULL, '2242478', NULL, NULL, NULL, 937, 937, 0),
(15, 'Yog. Colun 1K Cereza', 'YOG. COLUN 1K CEREZA', 2, NULL, NULL, '2242710', NULL, NULL, NULL, 937, 937, 0),
(16, 'Yog. Colun 1K Mora', 'YOG. COLUN 1K MORA', 2, NULL, NULL, '2242729', NULL, NULL, NULL, 937, 937, 0),
(17, 'Yog. Colun 125 Frambuesa', 'YOG. COLUN 125 FRAMBUESA', 1, NULL, NULL, '2242877', NULL, NULL, NULL, 1137, 1137, 0),
(18, 'Yog. Colun 125 Damasco', 'YOG. COLUN 125 DAMASCO', 1, NULL, NULL, '2242893', NULL, NULL, NULL, 1137, 1137, 0),
(19, 'Yog. Colun 125 Mora', 'YOG. COLUN 125 MORA', 1, NULL, NULL, '2242907', NULL, NULL, NULL, 1137, 1137, 0),
(20, 'Manquehuito Piña Botella 800 Cc', 'MANQUEHUITO PI  A_VNR800CCX12', 3, NULL, NULL, '7804300127671', NULL, NULL, NULL, 16405, 16405, 0),
(21, 'Vino Gato 500 Cc Blanco Tetrapack', 'GATO-B-NVO-CB8-500CCX12-TR', 1, NULL, NULL, '7804300122157', NULL, NULL, NULL, 9031, 9031, 0),
(22, 'Gato-Nvo-Cs-Cb4-1500Ccx8-Tr', 'GATO-NVO-CS-CB4-1500CCX8-TR', 2, NULL, NULL, '700561', NULL, NULL, NULL, 16058, 16058, 0),
(23, 'Gato Botellon Cabernet Sauvignon1.500 Cc', 'GATO-FIESTAS-PATRIAS-CS-VNR1500CCX8-TR', 1, NULL, NULL, '7804300122928', NULL, NULL, NULL, 17948, 17948, 0),
(24, 'cocacola 1 L', 'bebida pulentamente de pana que toma la gente g', 39, NULL, NULL, '1234567', NULL, NULL, NULL, 1200, 1200, 0),
(25, 'Atun Agua Esmeralda I Mp  170 G', '101540150 ATUN AGUA ESM I MP  170 G', 6, NULL, NULL, '7802420510205', NULL, NULL, NULL, 389, 389, 0),
(26, 'Atun Aceite Esmeralda I Mp  170 G', '101540050 ATUN ACEITE ESM I MP  170 G', 6, NULL, NULL, '10154005C', NULL, NULL, NULL, 389, 389, 0),
(27, 'Atun Aceite Van Camps 160G', '102140410 ATUN ACEITE VAN CAMPS 160G', 6, NULL, NULL, '7702367003900', NULL, NULL, NULL, 994, 994, 0),
(28, 'Austral Lager 4Pkx6 Vnr330', 'AUSTRAL LAGER 4PKX6 VNR330', 1, NULL, NULL, '7809634100192', NULL, NULL, NULL, 24680, 24680, 0),
(29, 'Stones Lemon 1500 Cc 2.5Gl', 'LEMON STONES PET1500CCX6-TR', 3, NULL, NULL, '7802100000170', NULL, NULL, NULL, 8252, 8252, 0),
(30, 'Dolbek Lager Belga - Nnr 12X330Cc', 'DOLBEK LAGER BELGA - NNR 12X330CC', 1, NULL, NULL, '7804616480040', NULL, NULL, NULL, 12540, 12540, 0),
(31, 'Pack Stones Maracuya 6 X 350 Cc', 'MARACUYA STONES 6PFX4-LAT350CC', 5, NULL, NULL, '7802100002532', NULL, NULL, NULL, 11467, 11467, 0),
(32, 'Cerveza Escudo Silver 470 Cc', 'ESCUDO SILVER LAT470CCX24', 30, NULL, NULL, '7802100002952', NULL, NULL, NULL, 8474, 8474, 0),
(33, 'Escudo Vre1200Ccx10-Tc', 'ESCUDO VRE1200CCX10-TC', 6, NULL, NULL, '450604', NULL, NULL, NULL, 8737, 8737, 0),
(34, 'Malta Morenita 1200Cc', 'MORENITA VRE1200CCX10-TC', 1, NULL, NULL, '7802100002563', NULL, NULL, NULL, 10194, 10194, 0),
(35, 'Cristal Vre1200Ccx10-Tc', 'CRISTAL VRE1200CCX10-TC', 15, NULL, NULL, '450607', NULL, NULL, NULL, 8737, 8737, 0),
(36, 'Royal Guard 6Pfx4-Lat470', 'ROYAL GUARD 6PFX4-LAT470', 10, NULL, NULL, '7802100002747', NULL, NULL, NULL, 16117, 16117, 0),
(37, 'Imperial 6Pfx04-Lat470Cc', 'IMPERIAL 6PFX04-LAT470CC', 1, NULL, NULL, '7802100003799', NULL, NULL, NULL, 11752, 11752, 0),
(38, 'Salsa Ajo Dj18 Uds. 100 G', '201221990 SALSA AJO DJ18 uds. 100 G', 1, NULL, NULL, '7802420003493', NULL, NULL, NULL, 6734, 6734, 0),
(39, 'Aceitunas Don Juan 200 Gr Huasco', '235002090 ACEITUNA HUASCO DJ 6x200G', 6, NULL, NULL, '7802351121204', NULL, NULL, NULL, 860, 860, 0),
(40, 'Pan Tradicional Bauducco 40', '105100053 PAN TRADICIONAL BAUDUCCO 40', 8, NULL, NULL, '7891962056746', NULL, NULL, NULL, 856, 856, 0),
(41, 'Jugo De Limon Don Juan 500 Cc Sucedaneo', '201230120 SUCEDANEO JUGO LIMON 500 ml', 12, NULL, NULL, '7802351534707', NULL, NULL, NULL, 319, 319, 0),
(42, 'Jugo De Limon Don Juan 250 Cc Sucedaneo', '201230470 JUGO DE LIMON DJ250 cc', 15, NULL, NULL, '7802351534509', NULL, NULL, NULL, 231, 231, 0),
(43, 'Mani Japones Inferno 100G', '101310121 MANI JAPONES INFERNO 100G', 8, NULL, NULL, '7802351002046', NULL, NULL, NULL, 464, 464, 0),
(44, 'Mani Salado  Mp 160Gr', '201700142 MANI SALADO  MP 160GR', 6, NULL, NULL, '7802420125423', NULL, NULL, NULL, 611, 611, 0),
(45, 'Mani Marcopolo 100 Gr Japones', '201700041 MANI JAPONES MP 100G', 10, NULL, NULL, '7802420125492', NULL, NULL, NULL, 544, 544, 0),
(46, 'Ramita Queso Mp 250G.', '201700199 RAMITA QUESO MP 250G.', 10, NULL, NULL, '7802420127694', NULL, NULL, NULL, 638, 638, 0),
(47, 'Pepino Dill Extra Dj 6X180G', '235002121 Pepino Dill Extra DJ 6x180G', 6, NULL, NULL, '7802351451400', NULL, NULL, NULL, 843, 843, 0),
(48, 'Pickles En Vinagre Don Juan 200 Gr', '235002155 Pickle Surtido DJ 6x180G', 6, NULL, NULL, '7802351461201', NULL, NULL, NULL, 646, 646, 0),
(49, 'Papas Fritas Marco Polo 230 Gr Corte Americano', '201700210 PF C/AMERI MARCO POLO 250g', 10, NULL, NULL, '7802420003912', NULL, NULL, NULL, 843, 843, 0);

-- --------------------------------------------------------

--
-- Table structure for table `ProductoCompra`
--

CREATE TABLE `ProductoCompra` (
  `idProducto` int(11) NOT NULL,
  `idCompra` int(11) NOT NULL,
  `cantidad` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `ProductoCompra`
--

INSERT INTO `ProductoCompra` (`idProducto`, `idCompra`, `cantidad`) VALUES
(1, 1, 1),
(2, 1, 1),
(3, 1, 1),
(4, 1, 1),
(1, 2, 1),
(2, 2, 1),
(3, 2, 1),
(4, 2, 1),
(5, 2, 1),
(6, 3, 2),
(7, 3, 2),
(8, 3, 1),
(9, 3, 3),
(10, 3, 9),
(11, 3, 2),
(12, 3, 2),
(13, 3, 2),
(14, 3, 2),
(15, 3, 2),
(16, 3, 2),
(17, 3, 1),
(18, 3, 1),
(19, 3, 1),
(4, 4, 3),
(20, 4, 3),
(21, 4, 1),
(22, 4, 2),
(23, 4, 1),
(25, 5, 6),
(26, 5, 6),
(27, 5, 6),
(4, 6, 1),
(28, 6, 1),
(29, 6, 3),
(30, 6, 1),
(31, 6, 5),
(32, 6, 30),
(33, 6, 6),
(34, 6, 1),
(35, 6, 15),
(36, 6, 10),
(37, 6, 1),
(38, 7, 1),
(39, 7, 6),
(40, 7, 8),
(41, 7, 12),
(42, 7, 15),
(43, 7, 8),
(44, 7, 6),
(45, 7, 10),
(46, 7, 10),
(47, 7, 6),
(48, 7, 6),
(49, 7, 10);

-- --------------------------------------------------------

--
-- Table structure for table `ProductoVenta`
--

CREATE TABLE `ProductoVenta` (
  `idProducto` int(11) NOT NULL,
  `idVenta` int(11) NOT NULL,
  `cantidad` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `ProductoVenta`
--

INSERT INTO `ProductoVenta` (`idProducto`, `idVenta`, `cantidad`) VALUES
(6, 1, 2),
(1, 1, 3),
(2, 1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `Proveedor`
--

CREATE TABLE `Proveedor` (
  `idProveedor` int(11) NOT NULL,
  `razonSocial` varchar(50) DEFAULT NULL,
  `rut` varchar(15) DEFAULT NULL,
  `comuna` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `Proveedor`
--

INSERT INTO `Proveedor` (`idProveedor`, `razonSocial`, `rut`, `comuna`) VALUES
(1, 'COMERCIAL CCU S.A.', '99554560-8', 'OSORNO'),
(2, 'COOPERATIVA AGRICOLA Y LECHERA DE LA UNION LTDA', '81094100-6', 'La Union'),
(3, 'IMPORTADORA CAFE DO BRASIL S A', '93178000-K', 'Quilicura');

-- --------------------------------------------------------

--
-- Table structure for table `Usuario`
--

CREATE TABLE `Usuario` (
  `idUsuario` int(11) NOT NULL,
  `nombre` varchar(60) NOT NULL,
  `rol` varchar(20) NOT NULL,
  `contraseña` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `Usuario`
--

INSERT INTO `Usuario` (`idUsuario`, `nombre`, `rol`, `contraseña`) VALUES
(1, 'matias', 'admin', '123');

-- --------------------------------------------------------

--
-- Table structure for table `Venta`
--

CREATE TABLE `Venta` (
  `idVenta` int(11) NOT NULL,
  `idUsuario` int(11) NOT NULL,
  `medioDePago` varchar(15) DEFAULT NULL,
  `estado` set('En Curso','Confirmada','Pagada','Anulada') NOT NULL,
  `fecha` datetime DEFAULT NULL,
  `total` int(11) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `Venta`
--

INSERT INTO `Venta` (`idVenta`, `idUsuario`, `medioDePago`, `estado`, `fecha`, `total`) VALUES
(1, 1, NULL, 'Confirmada', NULL, 54639);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Compra`
--
ALTER TABLE `Compra`
  ADD PRIMARY KEY (`idCompra`),
  ADD KEY `idProveedor` (`idProveedor`);

--
-- Indexes for table `Producto`
--
ALTER TABLE `Producto`
  ADD PRIMARY KEY (`idProducto`);

--
-- Indexes for table `ProductoCompra`
--
ALTER TABLE `ProductoCompra`
  ADD KEY `idCompra` (`idCompra`),
  ADD KEY `idProducto` (`idProducto`);

--
-- Indexes for table `ProductoVenta`
--
ALTER TABLE `ProductoVenta`
  ADD KEY `idProducto` (`idProducto`),
  ADD KEY `idVenta` (`idVenta`);

--
-- Indexes for table `Proveedor`
--
ALTER TABLE `Proveedor`
  ADD PRIMARY KEY (`idProveedor`);

--
-- Indexes for table `Usuario`
--
ALTER TABLE `Usuario`
  ADD PRIMARY KEY (`idUsuario`);

--
-- Indexes for table `Venta`
--
ALTER TABLE `Venta`
  ADD PRIMARY KEY (`idVenta`),
  ADD KEY `idUsuario` (`idUsuario`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `Compra`
--
ALTER TABLE `Compra`
  MODIFY `idCompra` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `Producto`
--
ALTER TABLE `Producto`
  MODIFY `idProducto` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=50;

--
-- AUTO_INCREMENT for table `Proveedor`
--
ALTER TABLE `Proveedor`
  MODIFY `idProveedor` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `Usuario`
--
ALTER TABLE `Usuario`
  MODIFY `idUsuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `Venta`
--
ALTER TABLE `Venta`
  MODIFY `idVenta` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `Compra`
--
ALTER TABLE `Compra`
  ADD CONSTRAINT `Compra_ibfk_1` FOREIGN KEY (`idProveedor`) REFERENCES `Proveedor` (`idProveedor`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Constraints for table `ProductoCompra`
--
ALTER TABLE `ProductoCompra`
  ADD CONSTRAINT `ProductoCompra_ibfk_1` FOREIGN KEY (`idCompra`) REFERENCES `Compra` (`idCompra`),
  ADD CONSTRAINT `ProductoCompra_ibfk_2` FOREIGN KEY (`idProducto`) REFERENCES `Producto` (`idProducto`);

--
-- Constraints for table `ProductoVenta`
--
ALTER TABLE `ProductoVenta`
  ADD CONSTRAINT `ProductoVenta_ibfk_1` FOREIGN KEY (`idProducto`) REFERENCES `Producto` (`idProducto`),
  ADD CONSTRAINT `ProductoVenta_ibfk_2` FOREIGN KEY (`idVenta`) REFERENCES `Venta` (`idVenta`);

--
-- Constraints for table `Venta`
--
ALTER TABLE `Venta`
  ADD CONSTRAINT `Venta_ibfk_1` FOREIGN KEY (`idUsuario`) REFERENCES `Usuario` (`idUsuario`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
