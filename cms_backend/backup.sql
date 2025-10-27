-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: localhost    Database: clinic_django_db
-- ------------------------------------------------------
-- Server version	8.0.43

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
-- Table structure for table `adminbackendapi_doctor`
--

DROP TABLE IF EXISTS `adminbackendapi_doctor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `adminbackendapi_doctor` (
  `DoctorId` int NOT NULL AUTO_INCREMENT,
  `ConsultationFee` decimal(10,2) NOT NULL,
  `availability` varchar(100) NOT NULL,
  `YearsOfExperience` int unsigned NOT NULL,
  `Specialization_id` int DEFAULT NULL,
  `Staff_id` int NOT NULL,
  PRIMARY KEY (`DoctorId`),
  KEY `adminbackendapi_doct_Specialization_id_42d7ed91_fk_adminback` (`Specialization_id`),
  KEY `adminbackendapi_doct_Staff_id_0ed59129_fk_adminback` (`Staff_id`),
  CONSTRAINT `adminbackendapi_doct_Specialization_id_42d7ed91_fk_adminback` FOREIGN KEY (`Specialization_id`) REFERENCES `adminbackendapi_specialization` (`SpecializationId`),
  CONSTRAINT `adminbackendapi_doct_Staff_id_0ed59129_fk_adminback` FOREIGN KEY (`Staff_id`) REFERENCES `adminbackendapi_staff` (`StaffId`),
  CONSTRAINT `adminbackendapi_doctor_chk_1` CHECK ((`YearsOfExperience` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `adminbackendapi_doctor`
--

LOCK TABLES `adminbackendapi_doctor` WRITE;
/*!40000 ALTER TABLE `adminbackendapi_doctor` DISABLE KEYS */;
INSERT INTO `adminbackendapi_doctor` VALUES (1,300.00,'Available',10,1,1);
/*!40000 ALTER TABLE `adminbackendapi_doctor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `adminbackendapi_role`
--

DROP TABLE IF EXISTS `adminbackendapi_role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `adminbackendapi_role` (
  `RoleId` int NOT NULL AUTO_INCREMENT,
  `RoleName` varchar(100) NOT NULL,
  `Description` longtext,
  PRIMARY KEY (`RoleId`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `adminbackendapi_role`
--

LOCK TABLES `adminbackendapi_role` WRITE;
/*!40000 ALTER TABLE `adminbackendapi_role` DISABLE KEYS */;
INSERT INTO `adminbackendapi_role` VALUES (1,'doctor','consult Patients'),(2,'receptionist','manage the patients'),(3,'admin','manage staffs');
/*!40000 ALTER TABLE `adminbackendapi_role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `adminbackendapi_specialization`
--

DROP TABLE IF EXISTS `adminbackendapi_specialization`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `adminbackendapi_specialization` (
  `SpecializationId` int NOT NULL AUTO_INCREMENT,
  `SpecializationName` varchar(100) NOT NULL,
  `Description` longtext,
  PRIMARY KEY (`SpecializationId`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `adminbackendapi_specialization`
--

LOCK TABLES `adminbackendapi_specialization` WRITE;
/*!40000 ALTER TABLE `adminbackendapi_specialization` DISABLE KEYS */;
INSERT INTO `adminbackendapi_specialization` VALUES (1,'cardiology',''),(2,'NeuroSurgeon','');
/*!40000 ALTER TABLE `adminbackendapi_specialization` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `adminbackendapi_staff`
--

DROP TABLE IF EXISTS `adminbackendapi_staff`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `adminbackendapi_staff` (
  `StaffId` int NOT NULL AUTO_INCREMENT,
  `FirstName` varchar(100) NOT NULL,
  `LastName` varchar(100) NOT NULL,
  `DOB` date NOT NULL,
  `Gender` varchar(10) NOT NULL,
  `Email` varchar(254) NOT NULL,
  `PhoneNumber` varchar(15) NOT NULL,
  `Address` longtext NOT NULL,
  `HireDate` date NOT NULL,
  `IsActive` tinyint(1) NOT NULL,
  `Role_id` int DEFAULT NULL,
  PRIMARY KEY (`StaffId`),
  UNIQUE KEY `Email` (`Email`),
  KEY `adminbackendapi_staff_Role_id_dab56e2a_fk_auth_group_id` (`Role_id`),
  CONSTRAINT `adminbackendapi_staff_Role_id_dab56e2a_fk_auth_group_id` FOREIGN KEY (`Role_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `adminbackendapi_staff`
--

LOCK TABLES `adminbackendapi_staff` WRITE;
/*!40000 ALTER TABLE `adminbackendapi_staff` DISABLE KEYS */;
INSERT INTO `adminbackendapi_staff` VALUES (1,'Doni','G','1990-10-01','Male','thahseelchullikulavan@gmail.com','09539722714','Thiruvananthapuram','2025-10-23',1,3);
/*!40000 ALTER TABLE `adminbackendapi_staff` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
INSERT INTO `auth_group` VALUES (1,'admin'),(3,'doctor'),(2,'receptionist');
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=158 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
INSERT INTO `auth_group_permissions` VALUES (1,1,1),(2,1,2),(3,1,3),(4,1,4),(5,1,5),(6,1,6),(7,1,7),(8,1,8),(9,1,9),(10,1,10),(11,1,11),(12,1,12),(13,1,13),(14,1,14),(15,1,15),(16,1,16),(17,1,17),(18,1,18),(19,1,19),(20,1,20),(21,1,21),(22,1,22),(23,1,23),(24,1,24),(25,1,25),(26,1,26),(27,1,27),(28,1,28),(29,1,29),(30,1,30),(31,1,31),(32,1,32),(33,1,33),(34,1,34),(35,1,35),(36,1,36),(37,1,37),(38,1,38),(39,1,39),(40,1,40),(41,1,41),(42,1,42),(43,1,43),(44,1,44),(45,1,45),(46,1,46),(47,1,47),(48,1,48),(49,1,49),(50,1,50),(51,1,51),(52,1,52),(53,1,53),(54,1,54),(55,1,55),(56,1,56),(57,1,57),(58,1,58),(59,1,59),(60,1,60),(61,1,61),(62,1,62),(63,1,63),(64,1,64),(65,1,65),(66,1,66),(67,1,67),(68,1,68),(69,1,69),(70,1,70),(71,1,71),(72,1,72),(73,1,73),(74,1,74),(75,1,75),(76,1,76),(77,1,77),(78,1,78),(79,1,79),(80,1,80),(81,1,81),(82,1,82),(83,1,83),(84,1,84),(85,1,85),(86,1,86),(87,1,87),(88,1,88),(89,1,89),(90,1,90),(91,1,91),(92,1,92),(93,1,93),(94,1,94),(95,1,95),(96,1,96),(129,2,5),(130,2,6),(131,2,7),(132,2,8),(133,2,9),(134,2,10),(135,2,11),(136,2,12),(137,2,13),(138,2,14),(139,2,15),(140,2,16),(141,2,17),(142,2,18),(143,2,19),(144,2,20),(145,2,21),(146,2,22),(147,2,23),(148,2,24),(149,2,41),(97,2,45),(98,2,46),(99,2,47),(100,2,48),(101,2,49),(102,2,50),(103,2,51),(104,2,52),(105,2,61),(106,2,62),(107,2,63),(108,2,64),(109,2,65),(110,2,66),(111,2,67),(112,2,68),(113,2,69),(114,2,70),(115,2,71),(116,2,72),(150,2,89),(151,2,90),(152,2,91),(153,2,92),(154,2,93),(155,2,94),(156,2,95),(157,2,96),(117,3,41),(118,3,42),(119,3,43),(120,3,44),(121,3,45),(122,3,46),(123,3,47),(124,3,48),(125,3,49),(126,3,50),(127,3,51),(128,3,52);
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=97 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add role',7,'add_role'),(26,'Can change role',7,'change_role'),(27,'Can delete role',7,'delete_role'),(28,'Can view role',7,'view_role'),(29,'Can add specialization',8,'add_specialization'),(30,'Can change specialization',8,'change_specialization'),(31,'Can delete specialization',8,'delete_specialization'),(32,'Can view specialization',8,'view_specialization'),(33,'Can add staff',9,'add_staff'),(34,'Can change staff',9,'change_staff'),(35,'Can delete staff',9,'delete_staff'),(36,'Can view staff',9,'view_staff'),(37,'Can add doctor',10,'add_doctor'),(38,'Can change doctor',10,'change_doctor'),(39,'Can delete doctor',10,'delete_doctor'),(40,'Can view doctor',10,'view_doctor'),(41,'Can add consultation',11,'add_consultation'),(42,'Can change consultation',11,'change_consultation'),(43,'Can delete consultation',11,'delete_consultation'),(44,'Can view consultation',11,'view_consultation'),(45,'Can add lab prescription',12,'add_labprescription'),(46,'Can change lab prescription',12,'change_labprescription'),(47,'Can delete lab prescription',12,'delete_labprescription'),(48,'Can view lab prescription',12,'view_labprescription'),(49,'Can add prescription',13,'add_prescription'),(50,'Can change prescription',13,'change_prescription'),(51,'Can delete prescription',13,'delete_prescription'),(52,'Can view prescription',13,'view_prescription'),(53,'Can add Medicine',14,'add_medicine'),(54,'Can change Medicine',14,'change_medicine'),(55,'Can delete Medicine',14,'delete_medicine'),(56,'Can view Medicine',14,'view_medicine'),(57,'Can add Bill',15,'add_bill'),(58,'Can change Bill',15,'change_bill'),(59,'Can delete Bill',15,'delete_bill'),(60,'Can view Bill',15,'view_bill'),(61,'Can add patient',16,'add_patient'),(62,'Can change patient',16,'change_patient'),(63,'Can delete patient',16,'delete_patient'),(64,'Can view patient',16,'view_patient'),(65,'Can add appointment',17,'add_appointment'),(66,'Can change appointment',17,'change_appointment'),(67,'Can delete appointment',17,'delete_appointment'),(68,'Can view appointment',17,'view_appointment'),(69,'Can add reception bill',18,'add_receptionbill'),(70,'Can change reception bill',18,'change_receptionbill'),(71,'Can delete reception bill',18,'delete_receptionbill'),(72,'Can view reception bill',18,'view_receptionbill'),(73,'Can add labtest',19,'add_labtest'),(74,'Can change labtest',19,'change_labtest'),(75,'Can delete labtest',19,'delete_labtest'),(76,'Can view labtest',19,'view_labtest'),(77,'Can add labrecord',20,'add_labrecord'),(78,'Can change labrecord',20,'change_labrecord'),(79,'Can delete labrecord',20,'delete_labrecord'),(80,'Can view labrecord',20,'view_labrecord'),(81,'Can add lab bill',21,'add_labbill'),(82,'Can change lab bill',21,'change_labbill'),(83,'Can delete lab bill',21,'delete_labbill'),(84,'Can view lab bill',21,'view_labbill'),(85,'Can add lab test request',22,'add_labtestrequest'),(86,'Can change lab test request',22,'change_labtestrequest'),(87,'Can delete lab test request',22,'delete_labtestrequest'),(88,'Can view lab test request',22,'view_labtestrequest'),(89,'Can add Token',23,'add_token'),(90,'Can change Token',23,'change_token'),(91,'Can delete Token',23,'delete_token'),(92,'Can view Token',23,'view_token'),(93,'Can add Token',24,'add_tokenproxy'),(94,'Can change Token',24,'change_tokenproxy'),(95,'Can delete Token',24,'delete_tokenproxy'),(96,'Can view Token',24,'view_tokenproxy');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$1000000$YoLhttVV8MWQhFKJJKPGIg$a4XAmU5A3b9KxJtjm5B09QYiWNOTg+XA/JNa1xA6MBA=','2025-10-23 05:49:51.211633',1,'thahseel','','','thah123@gmail.com',1,1,'2025-10-23 05:48:33.373350'),(3,'pbkdf2_sha256$1000000$F1ZbYDtWblR3zOZDRUA65T$MKNLglJ2cT1l9n7WDvZQkp0x3oRBNMJyWEJmLTPvAkE=',NULL,0,'recept','','','recept@gmail.com',0,1,'2025-10-23 06:38:59.000000'),(4,'pbkdf2_sha256$1000000$x6Ex6NOQ7to5PIgvFNFemL$8JUvJREsY0zfT0XAmB3jerSB+bCF7X60mbFY2JCugCg=',NULL,0,'reception','recept','ion','recept@gmail.com',0,1,'2025-10-01 06:56:32.000000');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
INSERT INTO `auth_user_groups` VALUES (2,3,2),(3,4,2);
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
INSERT INTO `auth_user_user_permissions` VALUES (30,3,61),(31,3,62),(32,3,63),(21,3,64),(22,3,65),(23,3,66),(24,3,67),(25,3,68),(26,3,69),(27,3,70),(28,3,71),(29,3,72),(1,4,45),(2,4,46),(3,4,47),(4,4,48),(5,4,49),(6,4,50),(7,4,51),(8,4,52),(9,4,61),(10,4,62),(11,4,63),(12,4,64),(13,4,65),(14,4,66),(15,4,67),(16,4,68),(17,4,69),(18,4,70),(19,4,71),(20,4,72);
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `authtoken_token`
--

DROP TABLE IF EXISTS `authtoken_token`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `authtoken_token` (
  `key` varchar(40) NOT NULL,
  `created` datetime(6) NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`key`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `authtoken_token_user_id_35299eff_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `authtoken_token`
--

LOCK TABLES `authtoken_token` WRITE;
/*!40000 ALTER TABLE `authtoken_token` DISABLE KEYS */;
/*!40000 ALTER TABLE `authtoken_token` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2025-10-23 05:50:20.878868','1','admin',1,'[{\"added\": {}}]',3,1),(2,'2025-10-23 05:50:39.939931','2','receptionist',1,'[{\"added\": {}}]',3,1),(3,'2025-10-23 05:51:17.966662','3','doctor',1,'[{\"added\": {}}]',3,1),(4,'2025-10-23 05:53:04.982705','1','doctor',1,'[{\"added\": {}}]',7,1),(5,'2025-10-23 05:53:18.053366','2','receptionist',1,'[{\"added\": {}}]',7,1),(6,'2025-10-23 05:53:29.507274','3','admin',1,'[{\"added\": {}}]',7,1),(7,'2025-10-23 05:53:48.276536','1','cardiology',1,'[{\"added\": {}}]',8,1),(8,'2025-10-23 05:53:57.977090','2','NeuroSurgeon',1,'[{\"added\": {}}]',8,1),(9,'2025-10-23 05:55:08.852514','1','Doni G',1,'[{\"added\": {}}]',9,1),(10,'2025-10-23 05:55:28.981618','1','Dr. Doni G - cardiology',1,'[{\"added\": {}}]',10,1),(11,'2025-10-23 06:55:31.608225','2','recep',3,'',4,1),(12,'2025-10-23 06:56:33.005915','4','reception',1,'[{\"added\": {}}]',4,1),(13,'2025-10-23 06:58:02.490687','4','reception',2,'[{\"changed\": {\"fields\": [\"First name\", \"Last name\", \"Email address\", \"Groups\", \"User permissions\", \"Date joined\"]}}]',4,1),(14,'2025-10-24 06:37:23.157272','2','receptionist',2,'[{\"changed\": {\"fields\": [\"Permissions\"]}}]',3,1),(15,'2025-10-24 06:38:30.687865','3','recept',2,'[{\"changed\": {\"fields\": [\"User permissions\"]}}]',4,1),(16,'2025-10-24 09:59:11.126989','1','1 - John Doe',1,'[{\"added\": {}}]',17,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(10,'adminbackendapi','doctor'),(7,'adminbackendapi','role'),(8,'adminbackendapi','specialization'),(9,'adminbackendapi','staff'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(23,'authtoken','token'),(24,'authtoken','tokenproxy'),(5,'contenttypes','contenttype'),(11,'doctorbackendapi','consultation'),(12,'doctorbackendapi','labprescription'),(13,'doctorbackendapi','prescription'),(21,'labtechbackendapi','labbill'),(20,'labtechbackendapi','labrecord'),(19,'labtechbackendapi','labtest'),(22,'labtechbackendapi','labtestrequest'),(15,'pharmasistbackendapi','bill'),(14,'pharmasistbackendapi','medicine'),(17,'reseptionistbackendapi','appointment'),(16,'reseptionistbackendapi','patient'),(18,'reseptionistbackendapi','receptionbill'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-10-23 05:46:53.838454'),(2,'auth','0001_initial','2025-10-23 05:46:54.597051'),(3,'admin','0001_initial','2025-10-23 05:46:54.760539'),(4,'admin','0002_logentry_remove_auto_add','2025-10-23 05:46:54.767698'),(5,'admin','0003_logentry_add_action_flag_choices','2025-10-23 05:46:54.775440'),(6,'contenttypes','0002_remove_content_type_name','2025-10-23 05:46:54.903121'),(7,'auth','0002_alter_permission_name_max_length','2025-10-23 05:46:54.984487'),(8,'auth','0003_alter_user_email_max_length','2025-10-23 05:46:55.007483'),(9,'auth','0004_alter_user_username_opts','2025-10-23 05:46:55.016457'),(10,'auth','0005_alter_user_last_login_null','2025-10-23 05:46:55.087872'),(11,'auth','0006_require_contenttypes_0002','2025-10-23 05:46:55.091759'),(12,'auth','0007_alter_validators_add_error_messages','2025-10-23 05:46:55.098081'),(13,'auth','0008_alter_user_username_max_length','2025-10-23 05:46:55.175030'),(14,'auth','0009_alter_user_last_name_max_length','2025-10-23 05:46:55.250142'),(15,'auth','0010_alter_group_name_max_length','2025-10-23 05:46:55.267405'),(16,'auth','0011_update_proxy_permissions','2025-10-23 05:46:55.274120'),(17,'auth','0012_alter_user_first_name_max_length','2025-10-23 05:46:55.351248'),(18,'adminbackendapi','0001_initial','2025-10-23 05:46:55.660188'),(19,'adminbackendapi','0002_alter_staff_role','2025-10-23 05:46:55.770439'),(20,'authtoken','0001_initial','2025-10-23 05:46:55.884776'),(21,'authtoken','0002_auto_20160226_1747','2025-10-23 05:46:55.901875'),(22,'authtoken','0003_tokenproxy','2025-10-23 05:46:55.906248'),(23,'authtoken','0004_alter_tokenproxy_options','2025-10-23 05:46:55.911902'),(24,'reseptionistbackendapi','0001_initial','2025-10-23 05:46:56.336668'),(25,'reseptionistbackendapi','0002_patient_age_receptionbill_date_and_more','2025-10-23 05:46:56.707060'),(26,'doctorbackendapi','0001_initial','2025-10-23 05:46:56.984686'),(27,'labtechbackendapi','0001_initial','2025-10-23 05:46:57.501054'),(28,'pharmasistbackendapi','0001_initial','2025-10-23 05:46:57.970450'),(29,'sessions','0001_initial','2025-10-23 05:46:58.012672');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('li4nufmi8l4gn6crns1z2y1y5htuzash','.eJxVjDsOwjAQBe_iGln-20tJnzNYu_aCAyiR4qRC3B0ipYD2zcx7iYzb2vLWecljFWehxel3IywPnnZQ7zjdZlnmaV1GkrsiD9rlMFd-Xg7376Bhb98aSvImIcHVFQeaqkWPxAxcUkBLHGykYAzp4BxDicF6rdBDBJWssuL9AfTUN34:1vBoCt:iQVlEfSCgSjCcAI8-12_FiSr6I7kghD3BHIP85-W4UA','2025-11-06 05:49:51.216164');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `doctorbackendapi_consultation`
--

DROP TABLE IF EXISTS `doctorbackendapi_consultation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `doctorbackendapi_consultation` (
  `consultation_id` int NOT NULL AUTO_INCREMENT,
  `symptoms` longtext NOT NULL,
  `notes` longtext,
  `diagnosis` longtext NOT NULL,
  `appointment_id` int NOT NULL,
  PRIMARY KEY (`consultation_id`),
  KEY `doctorbackendapi_con_appointment_id_ed5a8e36_fk_reseption` (`appointment_id`),
  CONSTRAINT `doctorbackendapi_con_appointment_id_ed5a8e36_fk_reseption` FOREIGN KEY (`appointment_id`) REFERENCES `reseptionistbackendapi_appointment` (`appointment_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `doctorbackendapi_consultation`
--

LOCK TABLES `doctorbackendapi_consultation` WRITE;
/*!40000 ALTER TABLE `doctorbackendapi_consultation` DISABLE KEYS */;
/*!40000 ALTER TABLE `doctorbackendapi_consultation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `doctorbackendapi_labprescription`
--

DROP TABLE IF EXISTS `doctorbackendapi_labprescription`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `doctorbackendapi_labprescription` (
  `lab_pid` int NOT NULL AUTO_INCREMENT,
  `testname` varchar(200) NOT NULL,
  `consultation_id` int NOT NULL,
  PRIMARY KEY (`lab_pid`),
  KEY `doctorbackendapi_lab_consultation_id_ccd8ec80_fk_doctorbac` (`consultation_id`),
  CONSTRAINT `doctorbackendapi_lab_consultation_id_ccd8ec80_fk_doctorbac` FOREIGN KEY (`consultation_id`) REFERENCES `doctorbackendapi_consultation` (`consultation_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `doctorbackendapi_labprescription`
--

LOCK TABLES `doctorbackendapi_labprescription` WRITE;
/*!40000 ALTER TABLE `doctorbackendapi_labprescription` DISABLE KEYS */;
/*!40000 ALTER TABLE `doctorbackendapi_labprescription` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `doctorbackendapi_prescription`
--

DROP TABLE IF EXISTS `doctorbackendapi_prescription`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `doctorbackendapi_prescription` (
  `pid` int NOT NULL AUTO_INCREMENT,
  `medicine` varchar(200) NOT NULL,
  `dosage` varchar(100) NOT NULL,
  `consultation_id` int NOT NULL,
  PRIMARY KEY (`pid`),
  KEY `doctorbackendapi_pre_consultation_id_d51d593c_fk_doctorbac` (`consultation_id`),
  CONSTRAINT `doctorbackendapi_pre_consultation_id_d51d593c_fk_doctorbac` FOREIGN KEY (`consultation_id`) REFERENCES `doctorbackendapi_consultation` (`consultation_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `doctorbackendapi_prescription`
--

LOCK TABLES `doctorbackendapi_prescription` WRITE;
/*!40000 ALTER TABLE `doctorbackendapi_prescription` DISABLE KEYS */;
/*!40000 ALTER TABLE `doctorbackendapi_prescription` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `labtechbackendapi_labbill`
--

DROP TABLE IF EXISTS `labtechbackendapi_labbill`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `labtechbackendapi_labbill` (
  `bill_id` int NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `address` longtext,
  `sex` varchar(10) DEFAULT NULL,
  `test_rate` decimal(10,2) NOT NULL,
  `total_amount` decimal(10,2) NOT NULL,
  `payment_status` varchar(20) NOT NULL,
  `patient_id` int DEFAULT NULL,
  `test_id` int DEFAULT NULL,
  PRIMARY KEY (`bill_id`),
  KEY `labtechbackendapi_la_patient_id_44a09376_fk_reseption` (`patient_id`),
  KEY `labtechbackendapi_la_test_id_a880161c_fk_labtechba` (`test_id`),
  CONSTRAINT `labtechbackendapi_la_patient_id_44a09376_fk_reseption` FOREIGN KEY (`patient_id`) REFERENCES `reseptionistbackendapi_patient` (`Patient_id`),
  CONSTRAINT `labtechbackendapi_la_test_id_a880161c_fk_labtechba` FOREIGN KEY (`test_id`) REFERENCES `labtechbackendapi_labtest` (`test_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `labtechbackendapi_labbill`
--

LOCK TABLES `labtechbackendapi_labbill` WRITE;
/*!40000 ALTER TABLE `labtechbackendapi_labbill` DISABLE KEYS */;
/*!40000 ALTER TABLE `labtechbackendapi_labbill` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `labtechbackendapi_labrecord`
--

DROP TABLE IF EXISTS `labtechbackendapi_labrecord`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `labtechbackendapi_labrecord` (
  `rec_id` int NOT NULL AUTO_INCREMENT,
  `result` longtext NOT NULL,
  `test_date` date NOT NULL,
  `patient_id_id` int DEFAULT NULL,
  `test_id` int NOT NULL,
  PRIMARY KEY (`rec_id`),
  KEY `labtechbackendapi_la_patient_id_id_cc69d75a_fk_reseption` (`patient_id_id`),
  KEY `labtechbackendapi_la_test_id_139deba5_fk_labtechba` (`test_id`),
  CONSTRAINT `labtechbackendapi_la_patient_id_id_cc69d75a_fk_reseption` FOREIGN KEY (`patient_id_id`) REFERENCES `reseptionistbackendapi_patient` (`Patient_id`),
  CONSTRAINT `labtechbackendapi_la_test_id_139deba5_fk_labtechba` FOREIGN KEY (`test_id`) REFERENCES `labtechbackendapi_labtest` (`test_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `labtechbackendapi_labrecord`
--

LOCK TABLES `labtechbackendapi_labrecord` WRITE;
/*!40000 ALTER TABLE `labtechbackendapi_labrecord` DISABLE KEYS */;
/*!40000 ALTER TABLE `labtechbackendapi_labrecord` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `labtechbackendapi_labtest`
--

DROP TABLE IF EXISTS `labtechbackendapi_labtest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `labtechbackendapi_labtest` (
  `test_id` int NOT NULL AUTO_INCREMENT,
  `test_name` varchar(255) NOT NULL,
  `description` longtext NOT NULL,
  `cost` decimal(10,2) NOT NULL,
  `sample_required` varchar(255) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`test_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `labtechbackendapi_labtest`
--

LOCK TABLES `labtechbackendapi_labtest` WRITE;
/*!40000 ALTER TABLE `labtechbackendapi_labtest` DISABLE KEYS */;
/*!40000 ALTER TABLE `labtechbackendapi_labtest` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `labtechbackendapi_labtestrequest`
--

DROP TABLE IF EXISTS `labtechbackendapi_labtestrequest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `labtechbackendapi_labtestrequest` (
  `request_id` int NOT NULL AUTO_INCREMENT,
  `requested_date` date NOT NULL,
  `status` varchar(20) NOT NULL,
  `remarks` longtext,
  `patient_id` int DEFAULT NULL,
  `test_id` int NOT NULL,
  PRIMARY KEY (`request_id`),
  KEY `labtechbackendapi_la_patient_id_43038bf2_fk_reseption` (`patient_id`),
  KEY `labtechbackendapi_la_test_id_bed93b3f_fk_labtechba` (`test_id`),
  CONSTRAINT `labtechbackendapi_la_patient_id_43038bf2_fk_reseption` FOREIGN KEY (`patient_id`) REFERENCES `reseptionistbackendapi_patient` (`Patient_id`),
  CONSTRAINT `labtechbackendapi_la_test_id_bed93b3f_fk_labtechba` FOREIGN KEY (`test_id`) REFERENCES `labtechbackendapi_labtest` (`test_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `labtechbackendapi_labtestrequest`
--

LOCK TABLES `labtechbackendapi_labtestrequest` WRITE;
/*!40000 ALTER TABLE `labtechbackendapi_labtestrequest` DISABLE KEYS */;
/*!40000 ALTER TABLE `labtechbackendapi_labtestrequest` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pharmacy_bill`
--

DROP TABLE IF EXISTS `pharmacy_bill`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pharmacy_bill` (
  `bill_id` int NOT NULL AUTO_INCREMENT,
  `serial_number` varchar(20) NOT NULL,
  `bill_type` varchar(20) NOT NULL,
  `ref_id` int unsigned NOT NULL,
  `total_amount` decimal(10,2) NOT NULL,
  `paid_amount` decimal(10,2) NOT NULL,
  `status` varchar(20) NOT NULL,
  `bill_date` datetime(6) NOT NULL,
  `due_date` date DEFAULT NULL,
  `notes` longtext,
  `created_by_id` int NOT NULL,
  `patient_id_id` int DEFAULT NULL,
  PRIMARY KEY (`bill_id`),
  UNIQUE KEY `serial_number` (`serial_number`),
  KEY `pharmacy_bill_created_by_id_5dd9defe_fk_auth_user_id` (`created_by_id`),
  KEY `pharmacy_bill_ref_id_6f4a7352` (`ref_id`),
  KEY `pharmacy_bill_bill_date_39ee3a5a` (`bill_date`),
  KEY `patient_id_idx` (`patient_id_id`),
  KEY `bill_status_idx` (`status`),
  KEY `bill_type_idx` (`bill_type`),
  KEY `bill_date_idx` (`bill_date`),
  CONSTRAINT `pharmacy_bill_created_by_id_5dd9defe_fk_auth_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `pharmacy_bill_patient_id_id_32b64a65_fk_reseption` FOREIGN KEY (`patient_id_id`) REFERENCES `reseptionistbackendapi_patient` (`Patient_id`),
  CONSTRAINT `pharmacy_bill_chk_1` CHECK ((`ref_id` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pharmacy_bill`
--

LOCK TABLES `pharmacy_bill` WRITE;
/*!40000 ALTER TABLE `pharmacy_bill` DISABLE KEYS */;
/*!40000 ALTER TABLE `pharmacy_bill` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pharmacy_medicine`
--

DROP TABLE IF EXISTS `pharmacy_medicine`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pharmacy_medicine` (
  `med_id` int NOT NULL AUTO_INCREMENT,
  `serial_number` varchar(20) NOT NULL,
  `med_code` varchar(50) NOT NULL,
  `name` varchar(200) NOT NULL,
  `manufacturer` varchar(100) NOT NULL,
  `unit_rate` decimal(10,2) NOT NULL,
  `stock` int unsigned NOT NULL,
  `expiry_date` date NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`med_id`),
  UNIQUE KEY `serial_number` (`serial_number`),
  UNIQUE KEY `med_code` (`med_code`),
  KEY `pharmacy_medicine_name_de5baaf9` (`name`),
  KEY `pharmacy_medicine_manufacturer_2842a98e` (`manufacturer`),
  KEY `pharmacy_medicine_expiry_date_8d85cc6a` (`expiry_date`),
  KEY `med_code_idx` (`med_code`),
  KEY `med_name_idx` (`name`),
  KEY `manufacturer_idx` (`manufacturer`),
  KEY `expiry_date_idx` (`expiry_date`),
  CONSTRAINT `pharmacy_medicine_chk_1` CHECK ((`stock` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pharmacy_medicine`
--

LOCK TABLES `pharmacy_medicine` WRITE;
/*!40000 ALTER TABLE `pharmacy_medicine` DISABLE KEYS */;
/*!40000 ALTER TABLE `pharmacy_medicine` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reseptionistbackendapi_appointment`
--

DROP TABLE IF EXISTS `reseptionistbackendapi_appointment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reseptionistbackendapi_appointment` (
  `appointment_id` int NOT NULL AUTO_INCREMENT,
  `token_number` int DEFAULT NULL,
  `appointment_date` date NOT NULL,
  `appointment_time` time(6) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `doc_id_id` int NOT NULL,
  `patient_id` int NOT NULL,
  PRIMARY KEY (`appointment_id`),
  KEY `reseptionistbackenda_doc_id_id_af37ceef_fk_adminback` (`doc_id_id`),
  KEY `reseptionistbackenda_patient_id_012c8798_fk_reseption` (`patient_id`),
  CONSTRAINT `reseptionistbackenda_doc_id_id_af37ceef_fk_adminback` FOREIGN KEY (`doc_id_id`) REFERENCES `adminbackendapi_doctor` (`DoctorId`),
  CONSTRAINT `reseptionistbackenda_patient_id_012c8798_fk_reseption` FOREIGN KEY (`patient_id`) REFERENCES `reseptionistbackendapi_patient` (`Patient_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reseptionistbackendapi_appointment`
--

LOCK TABLES `reseptionistbackendapi_appointment` WRITE;
/*!40000 ALTER TABLE `reseptionistbackendapi_appointment` DISABLE KEYS */;
INSERT INTO `reseptionistbackendapi_appointment` VALUES (1,2,'2025-10-30','12:00:00.000000','2025-10-24 09:59:11.104412',1,1);
/*!40000 ALTER TABLE `reseptionistbackendapi_appointment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reseptionistbackendapi_patient`
--

DROP TABLE IF EXISTS `reseptionistbackendapi_patient`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reseptionistbackendapi_patient` (
  `Patient_id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(100) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  `dob` date NOT NULL,
  `blood_group` varchar(3) NOT NULL,
  `gender` varchar(10) NOT NULL,
  `phone_no` varchar(15) NOT NULL,
  `address` longtext NOT NULL,
  `email` varchar(254) DEFAULT NULL,
  `reg_date` date NOT NULL,
  `age` int DEFAULT NULL,
  PRIMARY KEY (`Patient_id`),
  UNIQUE KEY `phone_no` (`phone_no`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reseptionistbackendapi_patient`
--

LOCK TABLES `reseptionistbackendapi_patient` WRITE;
/*!40000 ALTER TABLE `reseptionistbackendapi_patient` DISABLE KEYS */;
INSERT INTO `reseptionistbackendapi_patient` VALUES (1,'John','Doe','1990-05-15','O+','Male','+919876543210','123 Main Street, Kochi, Kerala','john.doe@example.com','2025-10-23',NULL),(2,'Vishnu','Kala','1990-10-08','A+','Male','8796756453','Thiruvananthapuram','vishnu@gmail.com','2025-10-23',NULL),(3,'uihiu','ffghuhur','2000-05-25','A-','Male','9876567876','Sreekaryam, Thiruvananthapuram','thahs@gmail.com','2025-10-23',NULL),(4,'uihiu','ffghuhur','2000-05-25','B+','Male','8898766756','Neyyattinkara,\ntrivandrum','tha76@gmail.com','2025-10-23',NULL),(5,'recept','ion','2001-10-25','A-','Male','08796756453','Sreekaryam, Thiruvananthapuram','recept@gmail.com','2025-10-23',NULL),(6,'ffgh','fghfdh','2000-10-20','A+','Male','9539722710','cdacsaadsfdsaGHFDSA','thahseelch123van@gmail.com','2025-10-24',NULL),(7,'anzel','r','1997-02-25','A+','Male','9622824094','Thiruvananthapuram','thahseelchullikulavan@gmail.com','2025-10-24',NULL),(8,'anu','chris','1999-12-17','A+','Female','9877656432','sgewgwgewg','anu@gmail.com','2025-10-24',NULL),(9,'ngfdjrtd','rhtrheyre','2009-11-27','','','8798675654','cdacsaadsfdsaGHFDSA','fdyr@gmail.com','2025-10-24',NULL),(10,'Thahseel','Rahman','2025-10-24','','','9539722711','Thiruvananthapuram','thahseelchul123van@gmail.com','2025-10-24',NULL);
/*!40000 ALTER TABLE `reseptionistbackendapi_patient` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reseptionistbackendapi_receptionbill`
--

DROP TABLE IF EXISTS `reseptionistbackendapi_receptionbill`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reseptionistbackendapi_receptionbill` (
  `bill_id` int NOT NULL AUTO_INCREMENT,
  `reg_fee` decimal(8,2) NOT NULL,
  `doc_fee` decimal(8,2) NOT NULL,
  `total` decimal(8,2) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `appointment_id` int NOT NULL,
  `patient_id` int NOT NULL,
  `date` date NOT NULL,
  `payment_mode` varchar(20) NOT NULL,
  PRIMARY KEY (`bill_id`),
  KEY `reseptionistbackenda_appointment_id_78283f82_fk_reseption` (`appointment_id`),
  KEY `reseptionistbackenda_patient_id_7494cd51_fk_reseption` (`patient_id`),
  CONSTRAINT `reseptionistbackenda_appointment_id_78283f82_fk_reseption` FOREIGN KEY (`appointment_id`) REFERENCES `reseptionistbackendapi_appointment` (`appointment_id`),
  CONSTRAINT `reseptionistbackenda_patient_id_7494cd51_fk_reseption` FOREIGN KEY (`patient_id`) REFERENCES `reseptionistbackendapi_patient` (`Patient_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reseptionistbackendapi_receptionbill`
--

LOCK TABLES `reseptionistbackendapi_receptionbill` WRITE;
/*!40000 ALTER TABLE `reseptionistbackendapi_receptionbill` DISABLE KEYS */;
/*!40000 ALTER TABLE `reseptionistbackendapi_receptionbill` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-10-24 23:24:40
