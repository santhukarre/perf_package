-- MySQL dump 10.13  Distrib 8.0.19, for Win64 (x86_64)
--
-- Host: localhost    Database: xindus_db
-- ------------------------------------------------------
-- Server version	8.0.19

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
-- Current Database: `xindus_db`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `xindus_db` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `xindus_db`;

--
-- Table structure for table `androbench_result`
--

DROP TABLE IF EXISTS `androbench_result`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `androbench_result` (
  `RESULT_ID` int DEFAULT NULL,
  `SEQ_READ` int DEFAULT NULL,
  `SEQ_WRITE` int DEFAULT NULL,
  `RAND_READ` int DEFAULT NULL,
  `RAND_WRITE` int DEFAULT NULL,
  `SQL_INSERT` int DEFAULT NULL,
  `SQL_UPDATE` int DEFAULT NULL,
  `SQL_DELETE` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `androbench_result`
--

LOCK TABLES `androbench_result` WRITE;
/*!40000 ALTER TABLE `androbench_result` DISABLE KEYS */;
INSERT INTO `androbench_result` VALUES (1,1451,399,177,30,2742,4511,5217),(2,1451,399,177,30,2742,4511,5217),(3,1463,228,181,188,2718,3097,4081),(4,1463,228,181,188,2718,3097,4081);
/*!40000 ALTER TABLE `androbench_result` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `antutu_result`
--

DROP TABLE IF EXISTS `antutu_result`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `antutu_result` (
  `RESULT_ID` int DEFAULT NULL,
  `ANTUTU_TOTAL_SCORE` int DEFAULT NULL,
  `ANTUTU_CPU_SCORE` int DEFAULT NULL,
  `ANTUTU_GPU_SCORE` int DEFAULT NULL,
  `ANTUTU_MEMORY_SCORE` int DEFAULT NULL,
  `ANTUTU_UX_SCORE` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `antutu_result`
--

LOCK TABLES `antutu_result` WRITE;
/*!40000 ALTER TABLE `antutu_result` DISABLE KEYS */;
INSERT INTO `antutu_result` VALUES (1,460640,135960,173064,75937,75679);
/*!40000 ALTER TABLE `antutu_result` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `benchmark_result`
--

DROP TABLE IF EXISTS `benchmark_result`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `benchmark_result` (
  `RUN_ID` int DEFAULT NULL,
  `ID` int DEFAULT NULL,
  `RESULT_ID` int DEFAULT NULL,
  KEY `fk_category` (`RUN_ID`),
  KEY `fk_category_12` (`ID`),
  CONSTRAINT `fk_category` FOREIGN KEY (`RUN_ID`) REFERENCES `run` (`RUN_ID`),
  CONSTRAINT `fk_category_12` FOREIGN KEY (`ID`) REFERENCES `tools` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `benchmark_result`
--

LOCK TABLES `benchmark_result` WRITE;
/*!40000 ALTER TABLE `benchmark_result` DISABLE KEYS */;
INSERT INTO `benchmark_result` VALUES (1,3,1),(2,3,1),(3,3,1),(4,3,1),(4,3,2),(7,3,3),(7,3,4);
/*!40000 ALTER TABLE `benchmark_result` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `device`
--

DROP TABLE IF EXISTS `device`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `device` (
  `DEVICE_ID` varchar(255) NOT NULL,
  `NAME` varchar(255) DEFAULT NULL,
  `CPU` varchar(255) DEFAULT NULL,
  `CORES` int DEFAULT NULL,
  `DDR_SIZE` int DEFAULT NULL,
  `DDR_VENDOR` int DEFAULT NULL,
  `STORAGE` int DEFAULT NULL,
  `STORAGE_VENDOR` int DEFAULT NULL,
  PRIMARY KEY (`DEVICE_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `device`
--

LOCK TABLES `device` WRITE;
/*!40000 ALTER TABLE `device` DISABLE KEYS */;
/*!40000 ALTER TABLE `device` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `geekbench_result`
--

DROP TABLE IF EXISTS `geekbench_result`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `geekbench_result` (
  `RESULT_ID` int DEFAULT NULL,
  `SINGLE_CORE_ELEMENT` int DEFAULT NULL,
  `MULTI_CORE_ELEMENT` int DEFAULT NULL,
  `OPENCL_SCORE_ELEMENT` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `geekbench_result`
--

LOCK TABLES `geekbench_result` WRITE;
/*!40000 ALTER TABLE `geekbench_result` DISABLE KEYS */;
INSERT INTO `geekbench_result` VALUES (1,749,2558,2353);
/*!40000 ALTER TABLE `geekbench_result` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `kpis`
--

DROP TABLE IF EXISTS `kpis`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `kpis` (
  `KPI_ID` int NOT NULL AUTO_INCREMENT,
  `NAME` varchar(255) DEFAULT NULL,
  `UNITS` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`KPI_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kpis`
--

LOCK TABLES `kpis` WRITE;
/*!40000 ALTER TABLE `kpis` DISABLE KEYS */;
INSERT INTO `kpis` VALUES (1,'FLASH_SEQ_READ','MBPS'),(2,'FLASH_SEQ_WRITE','MBPS'),(3,'FLASH_RAND_READ','MBPS'),(4,'FLASH_RAND_WRITE','MBPS'),(5,'SQLITE_INSERT','QPS'),(6,'SQLITE_UPDATE','QPS'),(7,'SQLITE_DELETE','QPS');
/*!40000 ALTER TABLE `kpis` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lmbench_result`
--

DROP TABLE IF EXISTS `lmbench_result`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `lmbench_result` (
  `RESULT_ID` int DEFAULT NULL,
  `BYTES_Transferred` int DEFAULT NULL,
  `DDR_BW` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lmbench_result`
--

LOCK TABLES `lmbench_result` WRITE;
/*!40000 ALTER TABLE `lmbench_result` DISABLE KEYS */;
/*!40000 ALTER TABLE `lmbench_result` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `run`
--

DROP TABLE IF EXISTS `run`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `run` (
  `RUN_ID` int NOT NULL,
  `START_DATE` varchar(255) DEFAULT NULL,
  `START_TIME` varchar(255) DEFAULT NULL,
  `END_DATE` varchar(255) DEFAULT NULL,
  `END_TIME` varchar(255) DEFAULT NULL,
  `MODE` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`RUN_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `run`
--

LOCK TABLES `run` WRITE;
/*!40000 ALTER TABLE `run` DISABLE KEYS */;
INSERT INTO `run` VALUES (1,'2020-02-19','14:33:41.145485','2020-02-19','14:47:13.385860','perf'),(2,'2020-02-19','14:47:57.053008','2020-02-19','14:53:43.345704','perf'),(3,'2020-02-19','14:54:14.430545','2020-02-19','15:03:40.356902','perf'),(4,'2020-02-19','15:04:48.186550','2020-02-19','15:05:50.777313','perf'),(5,NULL,NULL,NULL,NULL,NULL),(6,NULL,NULL,NULL,NULL,NULL),(7,'2020-02-20','16:43:57.740503','2020-02-20','16:45:04.924074','perf');
/*!40000 ALTER TABLE `run` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `run_kpi`
--

DROP TABLE IF EXISTS `run_kpi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `run_kpi` (
  `RUN_ID` int DEFAULT NULL,
  `KPI_ID` int NOT NULL,
  `END_DATE` varchar(255) DEFAULT NULL,
  `END_TIME` varchar(255) DEFAULT NULL,
  KEY `fk_category_3` (`RUN_ID`),
  KEY `fk_category_4` (`KPI_ID`),
  CONSTRAINT `fk_category_3` FOREIGN KEY (`RUN_ID`) REFERENCES `run` (`RUN_ID`),
  CONSTRAINT `fk_category_4` FOREIGN KEY (`KPI_ID`) REFERENCES `kpis` (`KPI_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `run_kpi`
--

LOCK TABLES `run_kpi` WRITE;
/*!40000 ALTER TABLE `run_kpi` DISABLE KEYS */;
/*!40000 ALTER TABLE `run_kpi` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `subsystems`
--

DROP TABLE IF EXISTS `subsystems`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `subsystems` (
  `ID` int DEFAULT NULL,
  `SUSSYSTEM` varchar(255) DEFAULT NULL,
  KEY `SUBSYSTEMS` (`ID`),
  CONSTRAINT `subsystems_ibfk_1` FOREIGN KEY (`ID`) REFERENCES `tools` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `subsystems`
--

LOCK TABLES `subsystems` WRITE;
/*!40000 ALTER TABLE `subsystems` DISABLE KEYS */;
/*!40000 ALTER TABLE `subsystems` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `testing_sequence`
--

DROP TABLE IF EXISTS `testing_sequence`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `testing_sequence` (
  `RUN_ID` int NOT NULL,
  `ID` int DEFAULT NULL,
  `START_TIME` varchar(255) DEFAULT NULL,
  `END_TIME` varchar(255) DEFAULT NULL,
  KEY `fk_category_7` (`RUN_ID`),
  KEY `fk_category_8` (`ID`),
  CONSTRAINT `fk_category_7` FOREIGN KEY (`RUN_ID`) REFERENCES `run` (`RUN_ID`),
  CONSTRAINT `fk_category_8` FOREIGN KEY (`ID`) REFERENCES `tools` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `testing_sequence`
--

LOCK TABLES `testing_sequence` WRITE;
/*!40000 ALTER TABLE `testing_sequence` DISABLE KEYS */;
/*!40000 ALTER TABLE `testing_sequence` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `threedmark_result`
--

DROP TABLE IF EXISTS `threedmark_result`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `threedmark_result` (
  `RESULT_ID` int DEFAULT NULL,
  `SLINGOPENGL_OVERALL` varchar(255) DEFAULT NULL,
  `SLINGOPENGL_GRAPHICS` varchar(255) DEFAULT NULL,
  `SLINGOPENGL_PHYSICS` varchar(255) DEFAULT NULL,
  `SLING_OVERALL` varchar(255) DEFAULT NULL,
  `SLING_GRAPHICS` varchar(255) DEFAULT NULL,
  `SLING_PHYSICS` varchar(255) DEFAULT NULL,
  `SLINGSHOT_OVERALL` varchar(255) DEFAULT NULL,
  `SLINGSHOT_GRAPHICS` varchar(255) DEFAULT NULL,
  `SLINGSHOT_PHYSICS` varchar(255) DEFAULT NULL,
  `API_OPENGL` varchar(255) DEFAULT NULL,
  `API_VULKAN` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `threedmark_result`
--

LOCK TABLES `threedmark_result` WRITE;
/*!40000 ALTER TABLE `threedmark_result` DISABLE KEYS */;
INSERT INTO `threedmark_result` VALUES (1,'5 647','6 202','4 300','5 000','5 786','3 388','7 551','9 700','4 253','533 892','834 964');
/*!40000 ALTER TABLE `threedmark_result` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tools`
--

DROP TABLE IF EXISTS `tools`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tools` (
  `NAME` varchar(255) DEFAULT NULL,
  `ID` int NOT NULL AUTO_INCREMENT,
  `CATEGORY` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tools`
--

LOCK TABLES `tools` WRITE;
/*!40000 ALTER TABLE `tools` DISABLE KEYS */;
INSERT INTO `tools` VALUES ('ANDROBENCH',1,'PERF'),('ANTUTU',2,'PERF'),('GEEKBENCH',3,'PERF'),('3DMARK',4,'PERF'),('LMBENCH',5,'PERF'),('GFXBENCH',6,'PERF');
/*!40000 ALTER TABLE `tools` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-02-20 17:30:35
