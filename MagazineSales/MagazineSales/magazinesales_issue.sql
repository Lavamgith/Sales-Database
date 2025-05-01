-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: magazinesales
-- ------------------------------------------------------
-- Server version	9.2.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `issue`
--

DROP TABLE IF EXISTS `issue`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `issue` (
  `issueID` int NOT NULL,
  `volID` int NOT NULL,
  `issNum` int NOT NULL,
  `season` varchar(6) NOT NULL,
  `issueCost` decimal(5,2) NOT NULL,
  `backCopiesSold` int NOT NULL,
  PRIMARY KEY (`issueID`),
  UNIQUE KEY `issueID_UNIQUE` (`issueID`),
  KEY `volID_idx` (`volID`),
  CONSTRAINT `volID` FOREIGN KEY (`volID`) REFERENCES `volume` (`volID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `issue`
--

LOCK TABLES `issue` WRITE;
/*!40000 ALTER TABLE `issue` DISABLE KEYS */;
INSERT INTO `issue` VALUES (1,1,1,'Winter',10.00,162),(2,1,2,'Spring',10.00,156),(3,1,3,'Summer',10.00,123),(4,1,4,'Fall',10.00,154),(5,2,1,'Winter',10.00,146),(6,2,2,'Spring',10.00,165),(7,2,3,'Summer',10.00,132),(8,2,4,'Fall',10.00,165),(9,3,1,'Winter',10.00,145),(10,3,2,'Spring',10.00,195),(11,3,3,'Summer',10.00,174),(12,3,4,'Fall',10.00,145),(13,4,1,'Winter',10.00,135),(14,4,2,'Spring',10.00,165),(15,4,3,'Summer',10.00,148),(16,4,4,'Fall',10.00,174),(17,5,1,'Winter',10.00,165),(18,5,2,'Spring',10.00,136),(19,5,3,'Summer',10.00,125),(20,5,4,'Fall',10.00,145),(21,6,1,'Winter',10.00,135),(22,6,2,'Spring',10.00,135),(23,6,3,'Summer',10.00,201),(24,6,4,'Fall',10.00,99),(25,7,1,'Winter',10.00,152),(26,7,2,'Spring',10.00,156),(27,7,3,'Summer',10.00,174),(28,7,4,'Fall',10.00,193),(29,8,1,'Winter',10.00,186),(30,8,2,'Spring',10.00,105),(31,8,3,'Summer',10.00,106),(32,8,4,'Fall',10.00,201),(33,9,1,'Winter',10.00,135),(34,9,2,'Spring',10.00,145),(35,9,3,'Summer',10.00,123),(36,9,4,'Fall',10.00,165),(37,10,1,'Winter',10.00,148),(38,10,2,'Spring',10.00,102),(39,10,3,'Summer',10.00,195),(40,10,4,'Fall',10.00,187);
/*!40000 ALTER TABLE `issue` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-03-31 13:33:39
