-- MySQL dump 10.13  Distrib 8.0.22, for Win64 (x86_64)
--
-- Host: localhost    Database: miniamazon
-- ------------------------------------------------------
-- Server version	8.0.22

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
-- Table structure for table `cart`
--

DROP TABLE IF EXISTS `cart`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cart` (
  `item_id` int NOT NULL AUTO_INCREMENT,
  `product_email` varchar(80) DEFAULT NULL,
  `item_name` varchar(80) DEFAULT NULL,
  `img` varchar(20) DEFAULT NULL,
  `cart_holder` varchar(80) DEFAULT NULL,
  PRIMARY KEY (`item_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cart`
--

LOCK TABLES `cart` WRITE;
/*!40000 ALTER TABLE `cart` DISABLE KEYS */;
INSERT INTO `cart` VALUES (1,'yelaiyugandhar@gmail.com','ciso drafter','7.jpg','nikita.potdar15@gmail.com'),(6,'yelaiyugandhar@gmail.com','book sepm','4.jpg','sakship1920@gmail.com'),(7,'sakship1920@gmail.com','big drafter','6.jpg','yelaiyugandhar@gmail.com'),(8,'sakship1920@gmail.com','trial','7.jpg','yelaiyugandhar@gmail.com'),(9,'yelaiyugandhar@gmail.com','yugandhar','8.jpg','nikita.potdar15@gmail.com'),(10,'yelaiyugandhar@gmail.com','cello drafter','7.jpg','sakship1920@gmail.com');
/*!40000 ALTER TABLE `cart` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `items`
--

DROP TABLE IF EXISTS `items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `items` (
  `item_id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(50) NOT NULL,
  `item_name` varchar(50) NOT NULL,
  `price` float NOT NULL,
  `item_type` varchar(10) NOT NULL,
  `img` varchar(50) NOT NULL,
  `sold` tinyint(1) NOT NULL,
  PRIMARY KEY (`item_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `items`
--

LOCK TABLES `items` WRITE;
/*!40000 ALTER TABLE `items` DISABLE KEYS */;
INSERT INTO `items` VALUES (1,'yelaiyugandhar@gmail.com','drafter',10,'sell','1.jpg',0),(2,'yelaiyugandhar@gmail.com','ciso drafter',20,'sell','2.jpg',0),(3,'yelaiyugandhar@gmail.com','cello drafter',40,'sell','3.jpg',0),(4,'yelaiyugandhar@gmail.com','book sepm',200,'sell','4.jpg',0),(5,'yelaiyugandhar@gmail.com','toc book',150,'sell','5.jpg',0),(6,'sakship1920@gmail.com','big drafter',200,'sell','6.jpg',0),(7,'sakship1920@gmail.com','trial',20,'sell','7.jpg',0),(8,'yelaiyugandhar@gmail.com','yugandhar',0,'sell','8.jpg',0);
/*!40000 ALTER TABLE `items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders` (
  `order_id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(50) NOT NULL,
  `item_name` varchar(50) NOT NULL,
  `price` float NOT NULL,
  `seller` varchar(50) NOT NULL,
  PRIMARY KEY (`order_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders`
--

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
INSERT INTO `orders` VALUES (1,'nikita.potdar008@gmail.com','drafter',0,'nikita.potdar15@gmail.com'),(2,'nikita.potdar008@gmail.com','drafter',0,'nikita.potdar15@gmail.com'),(3,'nikita.potdar008@gmail.com','drafter',0,'nikita.potdar15@gmail.com'),(4,'nikita.potdar008@gmail.com','drafter',0,'nikita.potdar15@gmail.com'),(5,'nikita.potdar008@gmail.com','drafter',0,'nikita.potdar15@gmail.com'),(6,'nikita.potdar008@gmail.com','drafter',0,'nikita.potdar15@gmail.com');
/*!40000 ALTER TABLE `orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `registration`
--

DROP TABLE IF EXISTS `registration`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `registration` (
  `email` varchar(50) DEFAULT NULL,
  `branch` varchar(36) DEFAULT NULL,
  `year` varchar(3) DEFAULT NULL,
  `password` varchar(50) DEFAULT NULL,
  `user_id` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `registration`
--

LOCK TABLES `registration` WRITE;
/*!40000 ALTER TABLE `registration` DISABLE KEYS */;
INSERT INTO `registration` VALUES ('yelaiyugandhar@gmail.com','Computer','TE','pass',1),('sakship1920@gmail.com','Computer','TE','ppp',3),('nikita.potdar15@gmail.com','Computer','TE','1234',4),('123@123.com','Mechanical','TE','1111',5),('nikita.potdar008@gmail.com','Computer','TE','0000',6),('test@gmail.com','It','FE','password123',7),('hello@gmail.com','IT','SE','helloworld',8);
/*!40000 ALTER TABLE `registration` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-12-04 22:54:29
