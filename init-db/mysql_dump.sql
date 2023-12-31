-- MySQL dump 10.13  Distrib 8.1.0, for macos14.0 (arm64)
--
-- Host: localhost    Database: sarbaseapp
-- ------------------------------------------------------
-- Server version	8.1.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('acb38785f1a1');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comment`
--

DROP TABLE IF EXISTS `comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comment` (
  `id` int NOT NULL AUTO_INCREMENT,
  `text` text,
  `user_id` int NOT NULL,
  `sar_call_id` int NOT NULL,
  `created` datetime NOT NULL,
  `updated` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_comment_sar_call_id_sar_call` (`sar_call_id`),
  KEY `fk_comment_user_id_user` (`user_id`),
  CONSTRAINT `fk_comment_sar_call_id_sar_call` FOREIGN KEY (`sar_call_id`) REFERENCES `sar_call` (`id`),
  CONSTRAINT `fk_comment_user_id_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=60 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comment`
--

--
-- Table structure for table `file_attachment`
--

DROP TABLE IF EXISTS `file_attachment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `file_attachment` (
  `id` int NOT NULL AUTO_INCREMENT,
  `file_name` varchar(255) NOT NULL,
  `file_type` varchar(50) NOT NULL,
  `file_path` varchar(255) NOT NULL,
  `comment_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_file_attachment_comment_id_comment` (`comment_id`),
  CONSTRAINT `fk_file_attachment_comment_id_comment` FOREIGN KEY (`comment_id`) REFERENCES `comment` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `file_attachment`
--


--
-- Table structure for table `gps_track`
--

DROP TABLE IF EXISTS `gps_track`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gps_track` (
  `id` int NOT NULL AUTO_INCREMENT,
  `color` varchar(7) DEFAULT NULL,
  `gpx_name` text,
  `gpx_data` longtext,
  `comment_id` int NOT NULL,
  `file_name` varchar(255) NOT NULL,
  `sar_call_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_gps_track_comment_id_comment` (`comment_id`),
  KEY `fk_gps_track_sar_call_id_sar_call` (`sar_call_id`),
  CONSTRAINT `fk_gps_track_comment_id_comment` FOREIGN KEY (`comment_id`) REFERENCES `comment` (`id`),
  CONSTRAINT `fk_gps_track_sar_call_id_sar_call` FOREIGN KEY (`sar_call_id`) REFERENCES `sar_call` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=55 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gps_track`
--


--
-- Table structure for table `role`
--

DROP TABLE IF EXISTS `role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `role` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(80) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_role_name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role`
--

LOCK TABLES `role` WRITE;
/*!40000 ALTER TABLE `role` DISABLE KEYS */;
INSERT INTO `role` VALUES (1,'admin'),(4,'coordination officer'),(5,'external auditor'),(3,'search officer'),(2,'search technician');
/*!40000 ALTER TABLE `role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sar_call`
--

DROP TABLE IF EXISTS `sar_call`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sar_call` (
  `id` int NOT NULL AUTO_INCREMENT,
  `start_date` datetime NOT NULL,
  `finish_date` datetime DEFAULT NULL,
  `category` int NOT NULL,
  `status` int NOT NULL,
  `result` int DEFAULT NULL,
  `latitude` float NOT NULL,
  `longitude` float NOT NULL,
  `description` text,
  `description_hidden` text,
  `title` varchar(150) NOT NULL,
  `created` datetime NOT NULL,
  `updated` datetime NOT NULL,
  `latitude_found` float DEFAULT NULL,
  `longitude_found` float DEFAULT NULL,
  `search_officer_id` int DEFAULT NULL,
  `coordination_officer_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_sar_call_category_sar_category` (`category`),
  KEY `fk_sar_call_result_sar_result` (`result`),
  KEY `fk_sar_call_status_sar_status` (`status`),
  KEY `fk_sar_call_search_officer_id_user` (`search_officer_id`),
  KEY `fk_sar_call_coordination_officer_id_user` (`coordination_officer_id`),
  CONSTRAINT `fk_sar_call_category_sar_category` FOREIGN KEY (`category`) REFERENCES `sar_category` (`id`),
  CONSTRAINT `fk_sar_call_coordination_officer_id_user` FOREIGN KEY (`coordination_officer_id`) REFERENCES `user` (`id`),
  CONSTRAINT `fk_sar_call_result_sar_result` FOREIGN KEY (`result`) REFERENCES `sar_result` (`id`),
  CONSTRAINT `fk_sar_call_search_officer_id_user` FOREIGN KEY (`search_officer_id`) REFERENCES `user` (`id`),
  CONSTRAINT `fk_sar_call_status_sar_status` FOREIGN KEY (`status`) REFERENCES `sar_status` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sar_call`
--


--
-- Table structure for table `sar_category`
--

DROP TABLE IF EXISTS `sar_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sar_category` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_sar_category_id` (`id`),
  UNIQUE KEY `uq_sar_category_name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sar_category`
--

LOCK TABLES `sar_category` WRITE;
/*!40000 ALTER TABLE `sar_category` DISABLE KEYS */;
INSERT INTO `sar_category` VALUES (1,'child 0-3'),(3,'dementia'),(2,'gatherer');
/*!40000 ALTER TABLE `sar_category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sar_result`
--

DROP TABLE IF EXISTS `sar_result`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sar_result` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_sar_result_id` (`id`),
  UNIQUE KEY `uq_sar_result_name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sar_result`
--

LOCK TABLES `sar_result` WRITE;
/*!40000 ALTER TABLE `sar_result` DISABLE KEYS */;
INSERT INTO `sar_result` VALUES (2,'Found by other rescuers'),(1,'Found by our rescuers'),(4,'Not found'),(3,'Rescued by himself');
/*!40000 ALTER TABLE `sar_result` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sar_status`
--

DROP TABLE IF EXISTS `sar_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sar_status` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_sar_status_id` (`id`),
  UNIQUE KEY `uq_sar_status_name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sar_status`
--

LOCK TABLES `sar_status` WRITE;
/*!40000 ALTER TABLE `sar_status` DISABLE KEYS */;
INSERT INTO `sar_status` VALUES (4,'Finished'),(2,'In progress'),(1,'New'),(3,'Paused'),(5,'Stopped');
/*!40000 ALTER TABLE `sar_status` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(150) NOT NULL,
  `full_name` varchar(301) NOT NULL,
  `email` varchar(150) NOT NULL,
  `phone_number` varchar(50) DEFAULT NULL,
  `password` varchar(50) DEFAULT NULL,
  `role_id` int DEFAULT NULL,
  `created` datetime NOT NULL,
  `updated` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_user_email` (`email`),
  UNIQUE KEY `uq_user_username` (`username`),
  KEY `fk_user_role_id_role` (`role_id`),
  CONSTRAINT `fk_user_role_id_role` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'vadikas','vadik likholetov','vadikas@gmail.com','+358503052224','password',1,'0000-00-00 00:00:00','2023-11-19 11:36:20'),(2,'monakhov','Dmitry Monakhov','dmitry@otklik.team','+78122328506','password',2,'2023-11-19 11:36:12','2023-11-19 11:38:02'),(3,'kokozayka','Olga Reznik','olga@otklik.team','+79959111122','password',4,'2023-11-23 10:55:16','2023-11-23 10:55:16');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-12-09 20:44:20
