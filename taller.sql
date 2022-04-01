-- MariaDB dump 10.19  Distrib 10.7.3-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: taller
-- ------------------------------------------------------
-- Server version	10.7.3-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Compra`
--

DROP TABLE IF EXISTS `Compra`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Compra` (
  `idCompra` int(11) NOT NULL AUTO_INCREMENT,
  `idProveedor` int(11) NOT NULL,
  `montoTotal` int(11) DEFAULT NULL,
  `montoNeto` int(11) DEFAULT NULL,
  `fecha` date DEFAULT NULL,
  `tipoDocumento` varchar(64) DEFAULT NULL,
  `folio` int(11) NOT NULL,
  PRIMARY KEY (`idCompra`),
  KEY `idProveedor` (`idProveedor`),
  CONSTRAINT `Compra_ibfk_1` FOREIGN KEY (`idProveedor`) REFERENCES `Proveedor` (`idProveedor`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Compra`
--

LOCK TABLES `Compra` WRITE;
/*!40000 ALTER TABLE `Compra` DISABLE KEYS */;
INSERT INTO `Compra` VALUES
(2,2,115448,84363,'2021-10-01','FACTURA ELECTRÓNICA',124072235),
(3,3,1284738,1068554,'2021-10-05','FACTURA ELECTRÓNICA',10694282);
/*!40000 ALTER TABLE `Compra` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Producto`
--

DROP TABLE IF EXISTS `Producto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Producto` (
  `idProducto` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) DEFAULT NULL,
  `stock` int(11) DEFAULT NULL,
  `cantidadRiesgo` int(11) DEFAULT NULL,
  `codigoBarra` varchar(16) DEFAULT NULL,
  `valorItem` int(11) DEFAULT NULL,
  `precioUnitario` int(11) DEFAULT NULL,
  `precioVenta` int(11) DEFAULT NULL,
  `descripcion` varchar(100) DEFAULT NULL,
  `categoria` varchar(25) DEFAULT NULL,
  `formato` varchar(25) DEFAULT NULL,
  `foto` blob DEFAULT NULL,
  `oculto` tinyint(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (`idProducto`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Producto`
--

LOCK TABLES `Producto` WRITE;
/*!40000 ALTER TABLE `Producto` DISABLE KEYS */;
INSERT INTO `Producto` VALUES
(7,'Nescafe Moka 18g',6,NULL,'7613033458507',NULL,300,450,'Café Mixes Moka 18g Nescafé (1 sobre)',NULL,NULL,NULL,0),
(8,'asdfasfd',12,0,NULL,NULL,300,400,NULL,NULL,NULL,NULL,0),
(9,'Vino Gato Cabernet Sauvignon 1/2 Lt Tetra',1,NULL,'7804300122140',9031,9031,11740,'GATO-NVO-CS-CB8-500CCX12-TR',NULL,'CJ',NULL,0),
(10,'Vino Gato 1000 Cc Blanco',1,NULL,'7804300004019',18579,18579,24150,'GATO-NVO-B-CF8-1000CCX12-TR',NULL,'CJ',NULL,0),
(11,'Vino Gato 1000 Cc Cabernet Sauvignon',1,NULL,'7804300004002',18579,18579,24150,'GATO-NVO-CS-CF8-1000CCX12-TR',NULL,'CJ',NULL,0),
(12,'Vino Gato 2000 Cc Merlot Tetrax',2,NULL,'7804300131692',41570,20785,27020,'GATO-NVO-ME-CB4-2000CCX8-TR',NULL,'CJ',NULL,0),
(13,'Gato_Dulce-Dc-Vnr750Ccx12-Co',0,NULL,'700808',17160,17160,22310,'GATO_DULCE-DC-VNR750CCX12-CO',NULL,'CJ',NULL,0),
(14,'Flete De Mercaderias',1,NULL,'9999',10920,10920,14200,'Flete de Mercaderias',NULL,NULL,NULL,0),
(15,'Kent Belmont - Rc10',3,NULL,'10070892',94362,31454,40890,'1020 Kent Belmont - RC10',NULL,NULL,NULL,0),
(16,'Kent Belmont - Hl20',6,NULL,'10070700',188724,31454,40890,'0627 Kent Belmont - HL20',NULL,NULL,NULL,0),
(17,'Kent Neo Ikon Mix Ds90',1,NULL,'10107101',27522,27522,35780,'Kent Neo Ikon Mix DS90',NULL,NULL,NULL,0),
(18,'Pall Mall Azul Hl20S',2,NULL,'10111410',50582,25291,32880,'Pall Mall Azul HL20s',NULL,NULL,NULL,0),
(19,'Pall Mall Boost - Hl10',2,NULL,'10102304',63228,31614,41100,'9065 Pall Mall Boost - HL10',NULL,NULL,NULL,0),
(20,'Pall Mall Boost Xl - Hl20',4,NULL,'10091121',110648,27662,35960,'5059 Pall Mall Boost XL - HL20',NULL,NULL,NULL,0),
(21,'Pall Clonb 10/200 Kre Sq Chi F&S',2,NULL,'10119670',63228,31614,41100,'9041 PALL CLONB 10/200 KRE SQ CHI F&S',NULL,NULL,NULL,0),
(22,'Pall Clonb 20/200 Kre Sq Chi F&S',5,NULL,'10119688',138310,27662,35960,'8884 PALL CLONB 20/200 KRE SQ CHI F&S',NULL,NULL,NULL,0),
(23,'Pall Mall Azul Sc20S',12,NULL,'10111132',265560,22130,28770,'Pall Mall Azul SC20s',NULL,NULL,NULL,0),
(24,'Pall Mall Rojo - Sc20',3,NULL,'10111094',66390,22130,28770,'Pall Mall Rojo - SC20',NULL,NULL,NULL,0);
/*!40000 ALTER TABLE `Producto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ProductoCompra`
--

DROP TABLE IF EXISTS `ProductoCompra`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ProductoCompra` (
  `idProducto` int(11) NOT NULL,
  `idCompra` int(11) NOT NULL,
  `cantidad` int(11) DEFAULT NULL,
  `precio` int(11) NOT NULL,
  KEY `idCompra` (`idCompra`),
  KEY `idProducto` (`idProducto`),
  CONSTRAINT `ProductoCompra_ibfk_1` FOREIGN KEY (`idCompra`) REFERENCES `Compra` (`idCompra`),
  CONSTRAINT `ProductoCompra_ibfk_2` FOREIGN KEY (`idProducto`) REFERENCES `Producto` (`idProducto`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ProductoCompra`
--

LOCK TABLES `ProductoCompra` WRITE;
/*!40000 ALTER TABLE `ProductoCompra` DISABLE KEYS */;
INSERT INTO `ProductoCompra` VALUES
(9,2,1,9031),
(10,2,1,18579),
(11,2,1,18579),
(12,2,2,20785),
(13,2,1,17160),
(14,2,1,10920),
(15,3,3,31454),
(16,3,6,31454),
(17,3,1,27522),
(18,3,2,25291),
(19,3,2,31614),
(20,3,4,27662),
(21,3,2,31614),
(22,3,5,27662),
(23,3,12,22130),
(24,3,3,22130);
/*!40000 ALTER TABLE `ProductoCompra` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ProductoVenta`
--

DROP TABLE IF EXISTS `ProductoVenta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ProductoVenta` (
  `idProducto` int(11) NOT NULL,
  `idVenta` int(11) NOT NULL,
  `cantidad` int(11) DEFAULT NULL,
  `precio` int(11) NOT NULL,
  KEY `idProducto` (`idProducto`),
  KEY `idVenta` (`idVenta`),
  CONSTRAINT `ProductoVenta_ibfk_1` FOREIGN KEY (`idProducto`) REFERENCES `Producto` (`idProducto`),
  CONSTRAINT `ProductoVenta_ibfk_2` FOREIGN KEY (`idVenta`) REFERENCES `Venta` (`idVenta`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ProductoVenta`
--

LOCK TABLES `ProductoVenta` WRITE;
/*!40000 ALTER TABLE `ProductoVenta` DISABLE KEYS */;
INSERT INTO `ProductoVenta` VALUES
(7,12,1,450),
(7,13,1,450),
(7,14,1,450),
(7,15,1,450),
(7,16,1,450),
(7,17,1,450),
(7,18,1,450),
(7,19,4,450),
(7,20,1,450),
(7,21,6,450),
(7,22,5,450),
(7,23,1,450),
(7,24,1,450),
(7,25,9,450),
(7,26,1,450),
(7,27,1,450),
(7,29,2,450),
(7,30,7,450),
(7,31,2,450),
(7,32,1,450),
(13,32,1,22310);
/*!40000 ALTER TABLE `ProductoVenta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Proveedor`
--

DROP TABLE IF EXISTS `Proveedor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Proveedor` (
  `idProveedor` int(11) NOT NULL AUTO_INCREMENT,
  `razonSocial` varchar(50) DEFAULT NULL,
  `rut` varchar(15) DEFAULT NULL,
  `comuna` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`idProveedor`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Proveedor`
--

LOCK TABLES `Proveedor` WRITE;
/*!40000 ALTER TABLE `Proveedor` DISABLE KEYS */;
INSERT INTO `Proveedor` VALUES
(2,'COMERCIAL CCU S.A.','99554560-8','OSORNO'),
(3,'BAT Chile S.A','88502900-0','Valdivia');
/*!40000 ALTER TABLE `Proveedor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Usuario`
--

DROP TABLE IF EXISTS `Usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Usuario` (
  `idUsuario` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(60) NOT NULL,
  `rol` varchar(20) NOT NULL,
  `contraseña` varchar(255) NOT NULL,
  PRIMARY KEY (`idUsuario`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Usuario`
--

LOCK TABLES `Usuario` WRITE;
/*!40000 ALTER TABLE `Usuario` DISABLE KEYS */;
INSERT INTO `Usuario` VALUES
(3,'matias','admin','123'),
(4,'joselo','vendedor','hiaw');
/*!40000 ALTER TABLE `Usuario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Venta`
--

DROP TABLE IF EXISTS `Venta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Venta` (
  `idVenta` int(11) NOT NULL AUTO_INCREMENT,
  `idUsuario` int(11) NOT NULL,
  `medioDePago` varchar(15) DEFAULT NULL,
  `tipoDocumento` set('Boleta','Factura','Guía de despacho') DEFAULT NULL,
  `estado` set('En Curso','Confirmada','Pagada','Anulada','No Finalizada') NOT NULL,
  `fecha` datetime DEFAULT NULL,
  `montoNeto` int(11) DEFAULT NULL,
  `IVA` int(11) DEFAULT NULL,
  `total` int(11) NOT NULL DEFAULT 0,
  PRIMARY KEY (`idVenta`),
  KEY `idUsuario` (`idUsuario`),
  CONSTRAINT `Venta_ibfk_1` FOREIGN KEY (`idUsuario`) REFERENCES `Usuario` (`idUsuario`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Venta`
--

LOCK TABLES `Venta` WRITE;
/*!40000 ALTER TABLE `Venta` DISABLE KEYS */;
INSERT INTO `Venta` VALUES
(12,4,NULL,NULL,'No Finalizada','2022-01-05 18:04:02',NULL,NULL,450),
(13,4,NULL,NULL,'No Finalizada','2022-01-05 18:04:16',NULL,NULL,450),
(14,4,NULL,NULL,'No Finalizada','2022-01-05 18:05:40',NULL,NULL,450),
(15,4,NULL,NULL,'No Finalizada','2022-01-05 18:07:42',NULL,NULL,450),
(16,4,'Efectivo',NULL,'Pagada','2022-01-05 18:08:55',365,85,450),
(17,4,NULL,NULL,'No Finalizada','2022-01-05 18:14:20',NULL,NULL,450),
(18,4,NULL,NULL,'No Finalizada','2022-01-05 18:18:35',NULL,NULL,450),
(19,4,NULL,NULL,'No Finalizada','2022-01-05 18:24:36',NULL,NULL,1800),
(20,4,NULL,NULL,'No Finalizada','2022-01-05 18:26:03',NULL,NULL,450),
(21,4,NULL,NULL,'No Finalizada','2022-01-05 18:27:10',NULL,NULL,2700),
(22,4,NULL,NULL,'No Finalizada','2022-01-05 18:28:18',NULL,NULL,2250),
(23,4,NULL,NULL,'No Finalizada','2022-01-05 18:29:26',NULL,NULL,450),
(24,4,NULL,NULL,'No Finalizada','2022-01-05 18:30:37',NULL,NULL,450),
(25,4,NULL,NULL,'No Finalizada','2022-01-05 18:34:02',NULL,NULL,4050),
(26,4,NULL,NULL,'No Finalizada','2022-01-05 18:34:18',NULL,NULL,450),
(27,4,NULL,NULL,'No Finalizada','2022-01-05 18:34:33',NULL,NULL,450),
(28,4,NULL,NULL,'No Finalizada','2022-01-05 18:38:25',NULL,NULL,0),
(29,4,'Efectivo',NULL,'Pagada','2022-01-05 18:38:44',729,171,900),
(30,4,NULL,NULL,'No Finalizada','2022-01-12 18:56:41',NULL,NULL,3150),
(31,4,NULL,NULL,'No Finalizada','2022-03-30 16:05:07',NULL,NULL,900),
(32,4,'Efectivo',NULL,'Pagada','2022-03-31 22:45:10',18436,4324,22760);
/*!40000 ALTER TABLE `Venta` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-03-31 22:52:47
