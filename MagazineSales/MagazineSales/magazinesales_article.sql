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
-- Table structure for table `article`
--

DROP TABLE IF EXISTS `article`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `article` (
  `articleTitle` varchar(100) NOT NULL,
  `authorID` int NOT NULL,
  `magID2` int NOT NULL,
  `volID2` int NOT NULL,
  `issueID` int NOT NULL,
  `topic` varchar(50) NOT NULL,
  PRIMARY KEY (`articleTitle`),
  KEY `authorID_idx` (`authorID`),
  KEY `issueID_idx` (`issueID`),
  KEY `magID2_idx` (`magID2`),
  KEY `volID2_idx` (`volID2`),
  CONSTRAINT `authorID` FOREIGN KEY (`authorID`) REFERENCES `author` (`authorID`),
  CONSTRAINT `issueID` FOREIGN KEY (`issueID`) REFERENCES `issue` (`issueID`),
  CONSTRAINT `magID2` FOREIGN KEY (`magID2`) REFERENCES `magazine` (`magazineID`),
  CONSTRAINT `volID2` FOREIGN KEY (`volID2`) REFERENCES `volume` (`volID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `article`
--

LOCK TABLES `article` WRITE;
/*!40000 ALTER TABLE `article` DISABLE KEYS */;
INSERT INTO `article` VALUES ('10 March 1917',378154,2,3,1,'Operations'),('1st Dogger Bank',378156,2,1,4,'Operations'),('1st Heligoland Bight',378957,2,1,1,'Operations'),('1st Yarmouth',378264,2,1,2,'Operations'),('22 September 1914',378264,2,1,2,'Operations'),('29 February 1916',378264,2,2,1,'Operations'),('2nd Durazzo',378156,2,4,4,'Operations'),('8 June 1915',378957,2,4,1,'Operations'),('Action of 24 July 1945',378954,3,2,3,'Battles'),('Action of 27 March 1942',378456,3,1,2,'Battles'),('Action of 6 June 1942',378654,3,3,1,'Battles'),('Action off Bougainville',378261,3,3,3,'Battles'),('Action off Cape Bougaroun',378261,3,1,2,'Battles'),('Adriatic Campaign',378154,2,3,3,'Operations'),('Allied Naval Bombardments of Japan',378378,3,2,3,'Battles'),('American Carrier Raids of 1942',378843,3,3,1,'Battles'),('Antivari',378565,2,3,4,'Operations'),('Attack on Aruba',378456,3,2,3,'Battles'),('Bakar',378264,2,4,4,'Operations'),('Baralong',378565,2,2,4,'Operations'),('Battle of Aquia Creek',378565,1,1,3,'Battles'),('Battle of Badung Strait',378456,3,3,2,'Battles'),('Battle of Balikpapan (1942)',378456,3,1,4,'Battles'),('Battle of Blackett Strait',378954,3,1,3,'Battles'),('Battle of Cape Esperance',378378,3,2,1,'Battles'),('Battle of Chrismas Island',378378,3,3,4,'Battles'),('Battle of Cockle Creek',378156,1,2,1,'Battles'),('Battle of Cockpit Point',378264,1,2,3,'Battles'),('Battle of Coronel',378154,2,1,1,'Battles'),('Battle of Dogger Bank',378156,2,3,1,'Battles'),('Battle of Drewry\'s Bluff',378154,1,3,3,'Battles'),('Battle of Elizabeth City',378264,1,2,4,'Battles'),('Battle of Fort Henry',378957,1,2,4,'Battles'),('Battle of Forts Jackson and St. Philips',378957,1,3,1,'Battles'),('Battle of Gela',378421,3,2,3,'Battles'),('Battle of Gloucester Point',378264,1,1,2,'Battles'),('Battle of Hampton Roads',378951,1,3,1,'Battles'),('Battle of Hatteras Inlet Batteries',378345,1,1,4,'Battles'),('Battle of Imbros',378264,2,4,3,'Battles'),('Battle of Island Number Ten',378162,1,3,2,'Battles'),('Battle of Jutland',378156,2,4,2,'Battles'),('Battle of La Ciotat',378954,3,1,4,'Battles'),('Battle of Leyte Gulf',378654,3,3,2,'Battles'),('Battle of Lucas Bend',378345,1,2,3,'Battles'),('Battle of Mathias Point',378154,1,1,4,'Battles'),('Battle of Midway',378456,3,2,2,'Battles'),('Battle of Pig Point',378957,1,1,3,'Battles'),('Battle of Plum Point Bend',378156,1,3,2,'Battles'),('Battle of Port Royal',378162,1,2,2,'Battles'),('Battle of Sewell\'s Point',378345,1,1,2,'Battles'),('Battle of the Atlantic',378421,3,1,2,'Battles'),('Battle of the Eastern Solomons',378843,3,2,3,'Battles'),('Battle of the Falkland Islands',378156,2,2,2,'Battles'),('Battle of the Head of Passes',378162,1,2,1,'Battles'),('Battle of the Java Sea',378456,3,2,3,'Battles'),('Battle of the Santa Cruz Islands',378954,3,3,1,'Battles'),('Blockade',378565,2,2,1,'Operations'),('Bombardment of Ellwood',378843,3,3,2,'Battles'),('Bombardment of Fort Stevens',378421,3,1,4,'Battles'),('Carolina',378264,2,3,1,'Operations'),('Convoy Faith',378378,3,2,2,'Battles'),('Convoy Hi-71',378421,3,3,2,'Battles'),('Convoys',378565,2,2,1,'Operations'),('Convoys SG-6/LN-6',378843,3,3,1,'Battles'),('CSS Florida',378345,1,1,2,'Warships'),('CSS Tennessee',378162,1,2,4,'Warships'),('Cuxhaven',378162,2,1,3,'Operations'),('Dardanelles',378162,2,3,3,'Operations'),('Falkland Islands',378565,2,3,1,'Operations'),('First Battle of Fort Sumter',378156,1,1,1,'Battles'),('First Battle of Memphis',378957,1,3,4,'Battles'),('Gallipoli Campaign',378162,2,2,3,'Battles'),('Goeben and Breslau',378156,2,3,2,'Operations'),('Gulflight',378951,2,2,3,'Operations'),('H.L. Hunley',378951,1,1,4,'Warships'),('Imbros',378951,2,4,3,'Operations'),('Invasion of Salamaua',378654,3,2,1,'Battles'),('Kaiser Wilhelm der Grosse',378162,2,2,2,'Operations'),('Northern Patrol',378264,2,2,1,'Operations'),('Operation Cleanslate',378378,3,1,3,'Battles'),('Operation Desecrate One',378843,3,1,4,'Battles'),('Operation I-Go',378421,3,1,1,'Battles'),('Operation Kita',378954,3,3,2,'Battles'),('Patrol Torpedo Boat PT-109',378954,3,2,4,'Battles'),('Raid on Algiers',378261,3,1,2,'Battles'),('Road on Porto Buso',378951,2,4,1,'Operations'),('Scarborough/Hartlepool/Whitby',378957,2,1,3,'Operations'),('Sinking of the Pretrel',378264,1,1,4,'Battles'),('Strait of Otranto',378264,2,4,2,'Operations'),('Texel',378951,2,1,2,'Operations'),('U-Boat Campaign',378951,2,1,1,'Operations'),('USN Operations',378345,2,4,2,'Operations'),('USS Cairo',378345,1,1,1,'Warships'),('USS Cumberland',378957,1,1,1,'Warships'),('USS Hartford',378951,1,3,3,'Warships'),('USS Miami',378154,1,2,2,'Warships'),('USS Nantucket',378156,1,2,3,'Warships'),('USS Wachusett',378565,1,3,1,'Warships'),('Vieste',378951,2,4,1,'Operations');
/*!40000 ALTER TABLE `article` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-03-31 13:33:40
