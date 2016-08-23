-- MySQL dump 10.13  Distrib 5.7.13, for osx10.11 (x86_64)
--
-- Host: localhost    Database: cmdb
-- ------------------------------------------------------
-- Server version	5.7.13

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `cmdb`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `cmdb` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `cmdb`;

--
-- Table structure for table `idcs`
--

DROP TABLE IF EXISTS `idcs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `idcs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `idcName` varchar(64) DEFAULT NULL,
  `pods` varchar(64) DEFAULT NULL,
  `bandwidth` int(11) DEFAULT '10',
  `t_contact` varchar(16) DEFAULT NULL,
  `t_phone` varchar(16) DEFAULT NULL,
  `kf_contact` varchar(16) DEFAULT NULL,
  `kf_phone` varchar(16) DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `status` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `idcs`
--

LOCK TABLES `idcs` WRITE;
/*!40000 ALTER TABLE `idcs` DISABLE KEYS */;
INSERT INTO `idcs` VALUES (2,'亦庄','A13-A20',80,'亦庄网管','18612247474','刘慧娟','18611671008','2016-08-01','北京市亦庄经济技术开发区北环东路一号网通国际大厦',0),(3,'数北联通机房','T15',10,'aa','aa','11122233344','bb','2016-08-01','北辰西路1号',0);
/*!40000 ALTER TABLE `idcs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `oses`
--

DROP TABLE IF EXISTS `oses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `oses` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `osname` varchar(20) DEFAULT NULL,
  `status` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `oses`
--

LOCK TABLES `oses` WRITE;
/*!40000 ALTER TABLE `oses` DISABLE KEYS */;
INSERT INTO `oses` VALUES (1,'esxi5.5',0),(2,'esxi5.1',0),(3,'esxi6.0',0),(4,'centos6.5',0),(5,'centos6.6',0),(6,'centos6.8',0),(7,'centos7.0',0),(8,'centos5.5',0);
/*!40000 ALTER TABLE `oses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `physics_host`
--

DROP TABLE IF EXISTS `physics_host`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `physics_host` (
  `pid` int(11) NOT NULL AUTO_INCREMENT,
  `sn` varchar(64) DEFAULT NULL,
  `pip` varchar(32) DEFAULT NULL,
  `vendor` varchar(32) DEFAULT NULL,
  `model` varchar(32) DEFAULT NULL,
  `esxi_version` int(11) DEFAULT '2',
  `cpuModel` varchar(24) DEFAULT NULL,
  `pmem` varchar(32) DEFAULT NULL,
  `PurchaseDate` date DEFAULT '2010-01-10',
  `warranty` int(11) DEFAULT '3',
  `bIdc` int(11) DEFAULT NULL,
  `bPod` varchar(16) DEFAULT NULL,
  `bPu` int(11) DEFAULT NULL,
  `status` int(11) DEFAULT '0',
  PRIMARY KEY (`pid`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `physics_host`
--

LOCK TABLES `physics_host` WRITE;
/*!40000 ALTER TABLE `physics_host` DISABLE KEYS */;
/*!40000 ALTER TABLE `physics_host` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_types`
--

DROP TABLE IF EXISTS `user_types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_types` (
  `tid` int(11) NOT NULL AUTO_INCREMENT,
  `tname` varchar(16) DEFAULT NULL,
  PRIMARY KEY (`tid`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_types`
--

LOCK TABLES `user_types` WRITE;
/*!40000 ALTER TABLE `user_types` DISABLE KEYS */;
INSERT INTO `user_types` VALUES (1,'管理员'),(2,'普通用户');
/*!40000 ALTER TABLE `user_types` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(20) DEFAULT NULL,
  `password` varchar(32) DEFAULT NULL,
  `email` varchar(32) DEFAULT NULL,
  `user_type` int(11) DEFAULT '1',
  `status` int(11) DEFAULT '0',
  PRIMARY KEY (`uid`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'yhzhao','b2332aa78d83be6ba6d2993d5c7ec69d','543551194@qq.com',1,0),(7,'user11','25d55ad283aa400af464c76d713c07ad','user11@mail.com',2,0);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vms`
--

DROP TABLE IF EXISTS `vms`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vms` (
  `vid` int(11) NOT NULL AUTO_INCREMENT,
  `vmid` varchar(64) DEFAULT NULL,
  `application` varchar(32) DEFAULT NULL,
  `vmip` varchar(24) DEFAULT NULL,
  `os` int(11) DEFAULT '6',
  `cpuThread` int(11) DEFAULT NULL,
  `mem` int(11) DEFAULT NULL,
  `disk` int(11) DEFAULT NULL,
  `bHost` int(11) DEFAULT '1',
  `status` int(11) DEFAULT '0',
  PRIMARY KEY (`vid`)
) ENGINE=InnoDB AUTO_INCREMENT=687 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vms`
--

LOCK TABLES `vms` WRITE;
/*!40000 ALTER TABLE `vms` DISABLE KEYS */;
/*!40000 ALTER TABLE `vms` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-08-23 17:52:41
