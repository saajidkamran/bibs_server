-- MySQL dump 10.13  Distrib 8.0.41, for Linux (x86_64)
--
-- Host: localhost    Database: bibs_server_db
-- ------------------------------------------------------
-- Server version	8.0.41-0ubuntu0.24.04.1

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
-- Table structure for table `M_trs_items_metals`
--

DROP TABLE IF EXISTS `M_trs_items_metals`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `M_trs_items_metals` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `seq_no` int NOT NULL,
  `it_id` varchar(10) COLLATE utf8mb4_general_ci NOT NULL,
  `met_id` varchar(10) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `M_trs_items_metals_it_id_met_id_3ac1f1a5_uniq` (`it_id`,`met_id`),
  KEY `M_trs_items_metals_met_id_6ddc6f5e_fk_nmetals_met_id` (`met_id`),
  CONSTRAINT `M_trs_items_metals_it_id_babbbdbe_fk_nitems_it_id` FOREIGN KEY (`it_id`) REFERENCES `nitems` (`it_id`),
  CONSTRAINT `M_trs_items_metals_met_id_6ddc6f5e_fk_nmetals_met_id` FOREIGN KEY (`met_id`) REFERENCES `nmetals` (`met_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `M_trs_items_metals`
--

LOCK TABLES `M_trs_items_metals` WRITE;
/*!40000 ALTER TABLE `M_trs_items_metals` DISABLE KEYS */;
INSERT INTO `M_trs_items_metals` VALUES (2,0,'ITM00002','MET00001');
/*!40000 ALTER TABLE `M_trs_items_metals` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `M_trs_metals_metalprocess`
--

DROP TABLE IF EXISTS `M_trs_metals_metalprocess`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `M_trs_metals_metalprocess` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `seq_no` int NOT NULL,
  `met_id` varchar(10) COLLATE utf8mb4_general_ci NOT NULL,
  `mepr_id` varchar(10) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `M_trs_metals_metalprocess_mepr_id_met_id_c842477e_uniq` (`mepr_id`,`met_id`),
  KEY `M_trs_metals_metalprocess_met_id_e83f2eb9_fk_nmetals_met_id` (`met_id`),
  CONSTRAINT `M_trs_metals_metalpr_mepr_id_40acd45c_fk_nmetalpro` FOREIGN KEY (`mepr_id`) REFERENCES `nmetalprocess` (`mepr_id`),
  CONSTRAINT `M_trs_metals_metalprocess_met_id_e83f2eb9_fk_nmetals_met_id` FOREIGN KEY (`met_id`) REFERENCES `nmetals` (`met_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `M_trs_metals_metalprocess`
--

LOCK TABLES `M_trs_metals_metalprocess` WRITE;
/*!40000 ALTER TABLE `M_trs_metals_metalprocess` DISABLE KEYS */;
INSERT INTO `M_trs_metals_metalprocess` VALUES (1,0,'MET00001','MPR00001');
/*!40000 ALTER TABLE `M_trs_metals_metalprocess` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `M_trs_process`
--

DROP TABLE IF EXISTS `M_trs_process`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `M_trs_process` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `seq_no` int NOT NULL,
  `mepr_id` varchar(10) COLLATE utf8mb4_general_ci NOT NULL,
  `pr_id` varchar(10) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `M_trs_process_mepr_id_pr_id_f1cac6f0_uniq` (`mepr_id`,`pr_id`),
  KEY `M_trs_process_pr_id_4581389e_fk_nprocess_pr_id` (`pr_id`),
  CONSTRAINT `M_trs_process_mepr_id_72cc8355_fk_nmetalprocess_mepr_id` FOREIGN KEY (`mepr_id`) REFERENCES `nmetalprocess` (`mepr_id`),
  CONSTRAINT `M_trs_process_pr_id_4581389e_fk_nprocess_pr_id` FOREIGN KEY (`pr_id`) REFERENCES `nprocess` (`pr_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `M_trs_process`
--

LOCK TABLES `M_trs_process` WRITE;
/*!40000 ALTER TABLE `M_trs_process` DISABLE KEYS */;
/*!40000 ALTER TABLE `M_trs_process` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `M_trs_process_type`
--

DROP TABLE IF EXISTS `M_trs_process_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `M_trs_process_type` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `seq_no` int NOT NULL,
  `pr_id` varchar(10) COLLATE utf8mb4_general_ci NOT NULL,
  `pt_id` varchar(10) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `M_trs_process_type_pt_id_pr_id_d36bfad7_uniq` (`pt_id`,`pr_id`),
  KEY `M_trs_process_type_pr_id_7e87a8f0_fk_nprocess_pr_id` (`pr_id`),
  CONSTRAINT `M_trs_process_type_pr_id_7e87a8f0_fk_nprocess_pr_id` FOREIGN KEY (`pr_id`) REFERENCES `nprocess` (`pr_id`),
  CONSTRAINT `M_trs_process_type_pt_id_34285654_fk_nprocesstype_pt_id` FOREIGN KEY (`pt_id`) REFERENCES `nprocesstype` (`pt_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `M_trs_process_type`
--

LOCK TABLES `M_trs_process_type` WRITE;
/*!40000 ALTER TABLE `M_trs_process_type` DISABLE KEYS */;
/*!40000 ALTER TABLE `M_trs_process_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `access_rights`
--

DROP TABLE IF EXISTS `access_rights`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `access_rights` (
  `access_right_id` int NOT NULL AUTO_INCREMENT,
  `add` tinyint(1) NOT NULL,
  `edit` tinyint(1) NOT NULL,
  `delete` tinyint(1) NOT NULL,
  `update` tinyint(1) NOT NULL,
  `menu_id` int NOT NULL,
  `user_group_id` int NOT NULL,
  PRIMARY KEY (`access_right_id`),
  UNIQUE KEY `access_rights_user_group_id_menu_id_b2d729c5_uniq` (`user_group_id`,`menu_id`),
  KEY `access_rights_menu_id_49db8536_fk_menu_menu_id` (`menu_id`),
  CONSTRAINT `access_rights_menu_id_49db8536_fk_menu_menu_id` FOREIGN KEY (`menu_id`) REFERENCES `menu` (`menu_id`),
  CONSTRAINT `access_rights_user_group_id_52dcd82a_fk_user_grou` FOREIGN KEY (`user_group_id`) REFERENCES `user_groups` (`user_group_id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `access_rights`
--

LOCK TABLES `access_rights` WRITE;
/*!40000 ALTER TABLE `access_rights` DISABLE KEYS */;
INSERT INTO `access_rights` VALUES (2,1,1,1,1,1,1),(3,1,1,1,1,2,1),(4,1,1,1,1,3,1),(5,1,1,1,1,4,1),(6,1,1,1,1,5,1),(7,1,1,1,1,6,1),(8,1,1,1,1,7,1),(9,1,1,1,1,8,1),(10,1,1,1,1,9,1),(11,1,1,1,1,10,1),(12,1,1,1,1,11,1);
/*!40000 ALTER TABLE `access_rights` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
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
  `name` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=129 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add customer',7,'add_customer'),(26,'Can change customer',7,'change_customer'),(27,'Can delete customer',7,'delete_customer'),(28,'Can view customer',7,'view_customer'),(29,'Can add employee',8,'add_employee'),(30,'Can change employee',8,'change_employee'),(31,'Can delete employee',8,'delete_employee'),(32,'Can view employee',8,'view_employee'),(33,'Can add job',9,'add_job'),(34,'Can change job',9,'change_job'),(35,'Can delete job',9,'delete_job'),(36,'Can view job',9,'view_job'),(37,'Can add menu',10,'add_menu'),(38,'Can change menu',10,'change_menu'),(39,'Can delete menu',10,'delete_menu'),(40,'Can view menu',10,'view_menu'),(41,'Can add m item',11,'add_mitem'),(42,'Can change m item',11,'change_mitem'),(43,'Can delete m item',11,'delete_mitem'),(44,'Can view m item',11,'view_mitem'),(45,'Can add m metal',12,'add_mmetal'),(46,'Can change m metal',12,'change_mmetal'),(47,'Can delete m metal',12,'delete_mmetal'),(48,'Can view m metal',12,'view_mmetal'),(49,'Can add m metal process',13,'add_mmetalprocess'),(50,'Can change m metal process',13,'change_mmetalprocess'),(51,'Can delete m metal process',13,'delete_mmetalprocess'),(52,'Can view m metal process',13,'view_mmetalprocess'),(53,'Can add m process',14,'add_mprocess'),(54,'Can change m process',14,'change_mprocess'),(55,'Can delete m process',14,'delete_mprocess'),(56,'Can view m process',14,'view_mprocess'),(57,'Can add n account summary',15,'add_naccountsummary'),(58,'Can change n account summary',15,'change_naccountsummary'),(59,'Can delete n account summary',15,'delete_naccountsummary'),(60,'Can view n account summary',15,'view_naccountsummary'),(61,'Can add n item resize type',16,'add_nitemresizetype'),(62,'Can change n item resize type',16,'change_nitemresizetype'),(63,'Can delete n item resize type',16,'delete_nitemresizetype'),(64,'Can view n item resize type',16,'view_nitemresizetype'),(65,'Can add n process pipe type',17,'add_nprocesspipetype'),(66,'Can change n process pipe type',17,'change_nprocesspipetype'),(67,'Can delete n process pipe type',17,'delete_nprocesspipetype'),(68,'Can view n process pipe type',17,'view_nprocesspipetype'),(69,'Can add n process type',18,'add_nprocesstype'),(70,'Can change n process type',18,'change_nprocesstype'),(71,'Can delete n process type',18,'delete_nprocesstype'),(72,'Can view n process type',18,'view_nprocesstype'),(73,'Can add serial table',19,'add_serialtable'),(74,'Can change serial table',19,'change_serialtable'),(75,'Can delete serial table',19,'delete_serialtable'),(76,'Can view serial table',19,'view_serialtable'),(77,'Can add setup company',20,'add_setupcompany'),(78,'Can change setup company',20,'change_setupcompany'),(79,'Can delete setup company',20,'delete_setupcompany'),(80,'Can view setup company',20,'view_setupcompany'),(81,'Can add user group',21,'add_usergroup'),(82,'Can change user group',21,'change_usergroup'),(83,'Can delete user group',21,'delete_usergroup'),(84,'Can view user group',21,'view_usergroup'),(85,'Can add job image',22,'add_jobimage'),(86,'Can change job image',22,'change_jobimage'),(87,'Can delete job image',22,'delete_jobimage'),(88,'Can view job image',22,'view_jobimage'),(89,'Can add ticket',23,'add_ticket'),(90,'Can change ticket',23,'change_ticket'),(91,'Can delete ticket',23,'delete_ticket'),(92,'Can view ticket',23,'view_ticket'),(93,'Can add menu access visibility',24,'add_menuaccessvisibility'),(94,'Can change menu access visibility',24,'change_menuaccessvisibility'),(95,'Can delete menu access visibility',24,'delete_menuaccessvisibility'),(96,'Can view menu access visibility',24,'view_menuaccessvisibility'),(97,'Can add m trs items metals',25,'add_mtrsitemsmetals'),(98,'Can change m trs items metals',25,'change_mtrsitemsmetals'),(99,'Can delete m trs items metals',25,'delete_mtrsitemsmetals'),(100,'Can view m trs items metals',25,'view_mtrsitemsmetals'),(101,'Can add m trs metal metal process',26,'add_mtrsmetalmetalprocess'),(102,'Can change m trs metal metal process',26,'change_mtrsmetalmetalprocess'),(103,'Can delete m trs metal metal process',26,'delete_mtrsmetalmetalprocess'),(104,'Can view m trs metal metal process',26,'view_mtrsmetalmetalprocess'),(105,'Can add m trs process',27,'add_mtrsprocess'),(106,'Can change m trs process',27,'change_mtrsprocess'),(107,'Can delete m trs process',27,'delete_mtrsprocess'),(108,'Can view m trs process',27,'view_mtrsprocess'),(109,'Can add m trs process type',28,'add_mtrsprocesstype'),(110,'Can change m trs process type',28,'change_mtrsprocesstype'),(111,'Can delete m trs process type',28,'delete_mtrsprocesstype'),(112,'Can view m trs process type',28,'view_mtrsprocesstype'),(113,'Can add access rights',29,'add_accessrights'),(114,'Can change access rights',29,'change_accessrights'),(115,'Can delete access rights',29,'delete_accessrights'),(116,'Can view access rights',29,'view_accessrights'),(117,'Can add n payment type',30,'add_npaymenttype'),(118,'Can change n payment type',30,'change_npaymenttype'),(119,'Can delete n payment type',30,'delete_npaymenttype'),(120,'Can view n payment type',30,'view_npaymenttype'),(121,'Can add n payment',31,'add_npayment'),(122,'Can change n payment',31,'change_npayment'),(123,'Can delete n payment',31,'delete_npayment'),(124,'Can view n payment',31,'view_npayment'),(125,'Can add cash customer',32,'add_cashcustomer'),(126,'Can change cash customer',32,'change_cashcustomer'),(127,'Can delete cash customer',32,'delete_cashcustomer'),(128,'Can view cash customer',32,'view_cashcustomer');
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
  `password` varchar(128) COLLATE utf8mb4_general_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) COLLATE utf8mb4_general_ci NOT NULL,
  `first_name` varchar(150) COLLATE utf8mb4_general_ci NOT NULL,
  `last_name` varchar(150) COLLATE utf8mb4_general_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_general_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bibs_customer`
--

DROP TABLE IF EXISTS `bibs_customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bibs_customer` (
  `nCUSCODE` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `nCTId` int DEFAULT NULL,
  `nActive` tinyint(1) NOT NULL,
  `nComName` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `nSurName` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `nFirstName` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `nAddress1` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `nAddress2` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `nAddress3` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `nCity` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `nState` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `nPostCode` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `nPhone1` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `nPhone2` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `nMobile` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `nFax` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `nEmail` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `nWebsite` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `nCreditLimit` decimal(15,2) NOT NULL,
  `nVAT` tinyint(1) NOT NULL,
  `nCreatedDate` datetime(6) NOT NULL,
  `nUpdatedDate` datetime(6) NOT NULL,
  `created_by` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `updated_by` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `nSMS` tinyint(1) NOT NULL,
  PRIMARY KEY (`nCUSCODE`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bibs_customer`
--

LOCK TABLES `bibs_customer` WRITE;
/*!40000 ALTER TABLE `bibs_customer` DISABLE KEYS */;
INSERT INTO `bibs_customer` VALUES ('CUS00001',NULL,1,'sad','asd','asdasd','123qw','qweqwe','qwe','ewq',NULL,'qwe','213123','2q123123','123123','','qwewqe@asd.com','',0.00,1,'2025-05-03 09:32:32.752839','2025-05-03 09:32:32.752874','EMP00005',NULL,1);
/*!40000 ALTER TABLE `bibs_customer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bibs_employee`
--

DROP TABLE IF EXISTS `bibs_employee`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bibs_employee` (
  `nId` int NOT NULL AUTO_INCREMENT,
  `nEMPCODE` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `nUserRole` int DEFAULT NULL,
  `nActive` tinyint(1) NOT NULL,
  `nFirstName` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `nSurName` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `nAddress1` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `nAddress2` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `nAddress3` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `nTown` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `nPostCode` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `nPhone` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `nMobile` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `nEmail` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `nBasicSal` decimal(15,2) NOT NULL,
  `nOverTime` decimal(15,2) NOT NULL,
  `nNoOfAppLeave` int NOT NULL,
  `nLeaveTaken` int NOT NULL,
  `nCreatedDate` datetime(6) NOT NULL,
  `nUpdatedDate` datetime(6) NOT NULL,
  `created_by` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `updated_by` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `nFSID` char(32) COLLATE utf8mb4_general_ci NOT NULL,
  `nImage` longtext COLLATE utf8mb4_general_ci,
  `nPwdHash` varchar(256) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `nPwdSalt` varchar(256) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `is_first_login` tinyint(1) NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `password` varchar(128) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`nId`),
  UNIQUE KEY `nEMPCODE` (`nEMPCODE`),
  UNIQUE KEY `nFSID` (`nFSID`),
  UNIQUE KEY `bibs_employee_nEmail_17949a3d_uniq` (`nEmail`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bibs_employee`
--

LOCK TABLES `bibs_employee` WRITE;
/*!40000 ALTER TABLE `bibs_employee` DISABLE KEYS */;
INSERT INTO `bibs_employee` VALUES (1,'EMP00005',1,1,'Saajids','asd','asdasdsa213213',NULL,NULL,'adssad','123213','123123213','213213','sk@bibs.com',222.00,3.00,2323,0,'2025-05-03 07:27:34.754413','2025-05-03 09:31:54.786644',NULL,NULL,'9dc8adbe10ae48f2b03a590cca4fb81f',NULL,NULL,NULL,1,0,NULL,'pbkdf2_sha256$1000000$sYPnC7bNBzqpGjPeyToAPx$kLyDC/6nHnxQHdfThgM3Ttt7VshhzQ+xM0QQyvYwJwo=');
/*!40000 ALTER TABLE `bibs_employee` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bibs_employee_groups`
--

DROP TABLE IF EXISTS `bibs_employee_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bibs_employee_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `employee_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `bibs_employee_groups_employee_id_group_id_6974176e_uniq` (`employee_id`,`group_id`),
  KEY `bibs_employee_groups_group_id_f064a8da_fk_auth_group_id` (`group_id`),
  CONSTRAINT `bibs_employee_groups_employee_id_ff8a6994_fk_bibs_employee_nId` FOREIGN KEY (`employee_id`) REFERENCES `bibs_employee` (`nId`),
  CONSTRAINT `bibs_employee_groups_group_id_f064a8da_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bibs_employee_groups`
--

LOCK TABLES `bibs_employee_groups` WRITE;
/*!40000 ALTER TABLE `bibs_employee_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `bibs_employee_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bibs_employee_user_permissions`
--

DROP TABLE IF EXISTS `bibs_employee_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bibs_employee_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `employee_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `bibs_employee_user_permi_employee_id_permission_i_22357421_uniq` (`employee_id`,`permission_id`),
  KEY `bibs_employee_user_p_permission_id_b6ed6558_fk_auth_perm` (`permission_id`),
  CONSTRAINT `bibs_employee_user_p_employee_id_a2fae16d_fk_bibs_empl` FOREIGN KEY (`employee_id`) REFERENCES `bibs_employee` (`nId`),
  CONSTRAINT `bibs_employee_user_p_permission_id_b6ed6558_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bibs_employee_user_permissions`
--

LOCK TABLES `bibs_employee_user_permissions` WRITE;
/*!40000 ALTER TABLE `bibs_employee_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `bibs_employee_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bibs_nprocesspipetype`
--

DROP TABLE IF EXISTS `bibs_nprocesspipetype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bibs_nprocesspipetype` (
  `nPTId` int NOT NULL AUTO_INCREMENT,
  `nProType` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`nPTId`),
  UNIQUE KEY `nProType` (`nProType`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bibs_nprocesspipetype`
--

LOCK TABLES `bibs_nprocesspipetype` WRITE;
/*!40000 ALTER TABLE `bibs_nprocesspipetype` DISABLE KEYS */;
/*!40000 ALTER TABLE `bibs_nprocesspipetype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cash_customer`
--

DROP TABLE IF EXISTS `cash_customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cash_customer` (
  `cashCusID` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `Name` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `Address` longtext COLLATE utf8mb4_general_ci,
  `CreatedDate` datetime(6) NOT NULL,
  `created_by` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `TicketID` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `vat` tinyint(1) NOT NULL,
  PRIMARY KEY (`cashCusID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cash_customer`
--

LOCK TABLES `cash_customer` WRITE;
/*!40000 ALTER TABLE `cash_customer` DISABLE KEYS */;
/*!40000 ALTER TABLE `cash_customer` ENABLE KEYS */;
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
  `object_id` longtext COLLATE utf8mb4_general_ci,
  `object_repr` varchar(200) COLLATE utf8mb4_general_ci NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext COLLATE utf8mb4_general_ci NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
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
  `app_label` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `model` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(29,'bibs','accessrights'),(32,'bibs','cashcustomer'),(7,'bibs','customer'),(8,'bibs','employee'),(9,'bibs','job'),(22,'bibs','jobimage'),(10,'bibs','menu'),(24,'bibs','menuaccessvisibility'),(11,'bibs','mitem'),(12,'bibs','mmetal'),(13,'bibs','mmetalprocess'),(14,'bibs','mprocess'),(25,'bibs','mtrsitemsmetals'),(26,'bibs','mtrsmetalmetalprocess'),(27,'bibs','mtrsprocess'),(28,'bibs','mtrsprocesstype'),(15,'bibs','naccountsummary'),(16,'bibs','nitemresizetype'),(31,'bibs','npayment'),(30,'bibs','npaymenttype'),(17,'bibs','nprocesspipetype'),(18,'bibs','nprocesstype'),(19,'bibs','serialtable'),(20,'bibs','setupcompany'),(23,'bibs','ticket'),(21,'bibs','usergroup'),(5,'contenttypes','contenttype'),(6,'sessions','session');
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
  `app` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-04-30 18:20:31.874218'),(2,'auth','0001_initial','2025-04-30 18:20:32.184265'),(3,'admin','0001_initial','2025-04-30 18:20:32.254830'),(4,'admin','0002_logentry_remove_auto_add','2025-04-30 18:20:32.261232'),(5,'admin','0003_logentry_add_action_flag_choices','2025-04-30 18:20:32.267404'),(6,'contenttypes','0002_remove_content_type_name','2025-04-30 18:20:32.327500'),(7,'auth','0002_alter_permission_name_max_length','2025-04-30 18:20:32.372102'),(8,'auth','0003_alter_user_email_max_length','2025-04-30 18:20:32.404714'),(9,'auth','0004_alter_user_username_opts','2025-04-30 18:20:32.417426'),(10,'auth','0005_alter_user_last_login_null','2025-04-30 18:20:32.460374'),(11,'auth','0006_require_contenttypes_0002','2025-04-30 18:20:32.462599'),(12,'auth','0007_alter_validators_add_error_messages','2025-04-30 18:20:32.471840'),(13,'auth','0008_alter_user_username_max_length','2025-04-30 18:20:32.517293'),(14,'auth','0009_alter_user_last_name_max_length','2025-04-30 18:20:32.564579'),(15,'auth','0010_alter_group_name_max_length','2025-04-30 18:20:32.590000'),(16,'auth','0011_update_proxy_permissions','2025-04-30 18:20:32.600436'),(17,'auth','0012_alter_user_first_name_max_length','2025-04-30 18:20:32.651223'),(18,'bibs','0001_initial','2025-04-30 18:20:33.340324'),(19,'bibs','0002_alter_setupcompany_vat_no','2025-04-30 18:20:33.368214'),(20,'bibs','0003_alter_setupcompany_vat_no','2025-04-30 18:20:33.425181'),(21,'bibs','0004_alter_ticket_iscusnotsigned_alter_ticket_nstatid','2025-04-30 18:20:33.479868'),(22,'bibs','0005_alter_ticket_nfsid','2025-04-30 18:20:33.583277'),(23,'bibs','0006_alter_ticket_iscashcustomer','2025-04-30 18:20:33.623035'),(24,'bibs','0007_update_ntdue','2025-04-30 18:20:33.645915'),(25,'bibs','0008_npaymenttype','2025-04-30 18:20:33.663973'),(26,'bibs','0009_alter_npaymenttype_table','2025-04-30 18:20:33.677231'),(27,'bibs','0010_npayment','2025-04-30 18:20:33.697131'),(28,'bibs','0011_cashcustomer','2025-04-30 18:20:33.709044'),(29,'bibs','0012_cashcustomer_vat','2025-04-30 18:20:33.734559'),(30,'bibs','0013_alter_cashcustomer_cashcusid','2025-04-30 18:20:33.764202'),(31,'bibs','0014_rename_createdby_cashcustomer_created_by','2025-04-30 18:20:33.781969'),(32,'bibs','0015_remove_jobimage_img_id_remove_jobimage_ntktcode','2025-04-30 18:20:33.831491'),(33,'sessions','0001_initial','2025-04-30 18:20:33.856474'),(34,'bibs','0016_employee_is_first_login','2025-05-03 06:20:32.437495'),(35,'bibs','0017_employee_groups_employee_is_superuser_and_more','2025-05-03 07:13:26.592101');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) COLLATE utf8mb4_general_ci NOT NULL,
  `session_data` longtext COLLATE utf8mb4_general_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `menu`
--

DROP TABLE IF EXISTS `menu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `menu` (
  `menu_id` int NOT NULL AUTO_INCREMENT,
  `menu_name` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`menu_id`),
  UNIQUE KEY `menu_name` (`menu_name`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `menu`
--

LOCK TABLES `menu` WRITE;
/*!40000 ALTER TABLE `menu` DISABLE KEYS */;
INSERT INTO `menu` VALUES (10,'customers'),(7,'employees'),(6,'m-item-resize'),(11,'m-items'),(3,'m-metalprocesslist'),(2,'m-metals'),(8,'mp-leave-details'),(9,'Payment'),(1,'POS'),(4,'process'),(5,'type-of-process');
/*!40000 ALTER TABLE `menu` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `menu_access_visibility`
--

DROP TABLE IF EXISTS `menu_access_visibility`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `menu_access_visibility` (
  `menu_id` int NOT NULL AUTO_INCREMENT,
  `menu_name` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `visible_no` varchar(10) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `user_group_id` int NOT NULL,
  PRIMARY KEY (`menu_id`),
  KEY `menu_access_visibili_user_group_id_13989100_fk_user_grou` (`user_group_id`),
  CONSTRAINT `menu_access_visibili_user_group_id_13989100_fk_user_grou` FOREIGN KEY (`user_group_id`) REFERENCES `user_groups` (`user_group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `menu_access_visibility`
--

LOCK TABLES `menu_access_visibility` WRITE;
/*!40000 ALTER TABLE `menu_access_visibility` DISABLE KEYS */;
/*!40000 ALTER TABLE `menu_access_visibility` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `nAccountSummary`
--

DROP TABLE IF EXISTS `nAccountSummary`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `nAccountSummary` (
  `nID` bigint NOT NULL AUTO_INCREMENT,
  `nACUSID` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `nTickets` decimal(20,10) NOT NULL,
  `nPayment` decimal(20,2) NOT NULL,
  `nTotOutStand` decimal(20,4) NOT NULL,
  `nCreatedDate` datetime(6) NOT NULL,
  `created_by` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `nUpdatedDate` datetime(6) NOT NULL,
  `updated_by` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`nID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nAccountSummary`
--

LOCK TABLES `nAccountSummary` WRITE;
/*!40000 ALTER TABLE `nAccountSummary` DISABLE KEYS */;
INSERT INTO `nAccountSummary` VALUES (1,'CUS00001',15.0000000000,0.00,15.0000,'2025-05-03 09:32:32.758573','EMP00005','2025-05-05 18:01:48.364466',NULL);
/*!40000 ALTER TABLE `nAccountSummary` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `nPayment`
--

DROP TABLE IF EXISTS `nPayment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `nPayment` (
  `nId` int NOT NULL AUTO_INCREMENT,
  `nCusID` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `nMonWeek` int NOT NULL,
  `nPaidAmount` decimal(10,2) NOT NULL,
  `nPayType` int NOT NULL,
  `paymentDetail` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `nComments` longtext COLLATE utf8mb4_general_ci,
  `nCreatedDate` datetime(6) NOT NULL,
  `nCreatedBy` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`nId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nPayment`
--

LOCK TABLES `nPayment` WRITE;
/*!40000 ALTER TABLE `nPayment` DISABLE KEYS */;
/*!40000 ALTER TABLE `nPayment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `nPaymentType`
--

DROP TABLE IF EXISTS `nPaymentType`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `nPaymentType` (
  `nId` int NOT NULL AUTO_INCREMENT,
  `nType` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`nId`),
  UNIQUE KEY `nType` (`nType`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nPaymentType`
--

LOCK TABLES `nPaymentType` WRITE;
/*!40000 ALTER TABLE `nPaymentType` DISABLE KEYS */;
/*!40000 ALTER TABLE `nPaymentType` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `nitemresizetype`
--

DROP TABLE IF EXISTS `nitemresizetype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `nitemresizetype` (
  `itmrz_id` varchar(10) COLLATE utf8mb4_general_ci NOT NULL,
  `nType` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `nSeqNo` int NOT NULL,
  `nActive` tinyint(1) NOT NULL,
  `nCreatedDate` datetime(6) NOT NULL,
  `nUpdatedDate` datetime(6) NOT NULL,
  `created_by` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `updated_by` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`itmrz_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nitemresizetype`
--

LOCK TABLES `nitemresizetype` WRITE;
/*!40000 ALTER TABLE `nitemresizetype` DISABLE KEYS */;
/*!40000 ALTER TABLE `nitemresizetype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `nitems`
--

DROP TABLE IF EXISTS `nitems`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `nitems` (
  `it_id` varchar(10) COLLATE utf8mb4_general_ci NOT NULL,
  `desc` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `seq_no` varchar(10) COLLATE utf8mb4_general_ci NOT NULL,
  `nActive` tinyint(1) NOT NULL,
  `created_date` datetime(6) NOT NULL,
  `updated_date` datetime(6) NOT NULL,
  `created_by` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `updated_by` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`it_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nitems`
--

LOCK TABLES `nitems` WRITE;
/*!40000 ALTER TABLE `nitems` DISABLE KEYS */;
INSERT INTO `nitems` VALUES ('ITM00002','asd','1',1,'2025-05-03 09:31:34.596577','2025-05-03 09:31:34.596615','EMP00005',NULL);
/*!40000 ALTER TABLE `nitems` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `nmetalprocess`
--

DROP TABLE IF EXISTS `nmetalprocess`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `nmetalprocess` (
  `mepr_id` varchar(10) COLLATE utf8mb4_general_ci NOT NULL,
  `desc` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `nActive` tinyint(1) NOT NULL,
  `created_date` datetime(6) NOT NULL,
  `updated_date` datetime(6) NOT NULL,
  `created_by` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `updated_by` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`mepr_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nmetalprocess`
--

LOCK TABLES `nmetalprocess` WRITE;
/*!40000 ALTER TABLE `nmetalprocess` DISABLE KEYS */;
INSERT INTO `nmetalprocess` VALUES ('MPR00001','metal process',1,'2025-05-05 16:21:01.296067','2025-05-05 16:21:01.296084',NULL,NULL);
/*!40000 ALTER TABLE `nmetalprocess` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `nmetals`
--

DROP TABLE IF EXISTS `nmetals`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `nmetals` (
  `met_id` varchar(10) COLLATE utf8mb4_general_ci NOT NULL,
  `desc` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `nActive` tinyint(1) NOT NULL,
  `created_date` datetime(6) NOT NULL,
  `updated_date` datetime(6) NOT NULL,
  `created_by` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `updated_by` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`met_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nmetals`
--

LOCK TABLES `nmetals` WRITE;
/*!40000 ALTER TABLE `nmetals` DISABLE KEYS */;
INSERT INTO `nmetals` VALUES ('MET00001','metal',1,'2025-05-05 16:20:37.367522','2025-05-05 16:20:37.367546','EMP00005',NULL);
/*!40000 ALTER TABLE `nmetals` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `nprocess`
--

DROP TABLE IF EXISTS `nprocess`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `nprocess` (
  `pr_id` varchar(10) COLLATE utf8mb4_general_ci NOT NULL,
  `desc` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `pipe` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `nActive` tinyint(1) NOT NULL,
  `created_date` datetime(6) NOT NULL,
  `updated_date` datetime(6) NOT NULL,
  `created_by` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `updated_by` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`pr_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nprocess`
--

LOCK TABLES `nprocess` WRITE;
/*!40000 ALTER TABLE `nprocess` DISABLE KEYS */;
/*!40000 ALTER TABLE `nprocess` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `nprocesstype`
--

DROP TABLE IF EXISTS `nprocesstype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `nprocesstype` (
  `pt_id` varchar(10) COLLATE utf8mb4_general_ci NOT NULL,
  `processName` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `processPipe` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `nActive` tinyint(1) NOT NULL,
  `created_by` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `updated_by` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `nCreatedDate` datetime(6) NOT NULL,
  `nUpdatedDate` datetime(6) NOT NULL,
  PRIMARY KEY (`pt_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nprocesstype`
--

LOCK TABLES `nprocesstype` WRITE;
/*!40000 ALTER TABLE `nprocesstype` DISABLE KEYS */;
/*!40000 ALTER TABLE `nprocesstype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `serial_table`
--

DROP TABLE IF EXISTS `serial_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `serial_table` (
  `sr_code` varchar(10) COLLATE utf8mb4_general_ci NOT NULL,
  `count` int unsigned NOT NULL,
  `description` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`sr_code`),
  CONSTRAINT `serial_table_chk_1` CHECK ((`count` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `serial_table`
--

LOCK TABLES `serial_table` WRITE;
/*!40000 ALTER TABLE `serial_table` DISABLE KEYS */;
INSERT INTO `serial_table` VALUES ('cus',3,'cus Serial Count'),('emp',5,'emp Serial Count'),('itm',2,'itm Serial Count'),('job',1,'job Serial Count'),('mepr',1,''),('met',1,'met Serial Count'),('mpr',1,'mpr Serial Count'),('tkt',1,'tkt Serial Count');
/*!40000 ALTER TABLE `serial_table` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `setup_company`
--

DROP TABLE IF EXISTS `setup_company`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `setup_company` (
  `company_name` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `phone_no` varchar(15) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `email` varchar(254) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `web` varchar(200) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `address` longtext COLLATE utf8mb4_general_ci,
  `vat_no` decimal(5,2) NOT NULL,
  `logo` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `bank_name` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `account_no` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `sort_code` varchar(10) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `created_date` datetime(6) NOT NULL,
  `updated_date` datetime(6) NOT NULL,
  `created_by` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `updated_by` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`company_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `setup_company`
--

LOCK TABLES `setup_company` WRITE;
/*!40000 ALTER TABLE `setup_company` DISABLE KEYS */;
INSERT INTO `setup_company` VALUES ('bibs','0771234567','info@bibs.com','https://bibs.com','123 Main Street, Colombo, Sri Lanka',15.00,NULL,'Commercial Bank','1234567890','701122','2025-05-05 23:30:12.000000','2025-05-05 23:30:12.000000','admin','admin');
/*!40000 ALTER TABLE `setup_company` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tb_jobs`
--

DROP TABLE IF EXISTS `tb_jobs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tb_jobs` (
  `nId` int NOT NULL AUTO_INCREMENT,
  `nJOBCODE` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `nJStatID` int NOT NULL,
  `nIQty` int NOT NULL,
  `nPrice` decimal(10,2) NOT NULL,
  `nFSID` char(32) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `nImage` longtext COLLATE utf8mb4_general_ci,
  `nItem` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `nMetal` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `nJobDesc` longtext COLLATE utf8mb4_general_ci,
  `nJobDescHTML` longtext COLLATE utf8mb4_general_ci,
  `nActive` tinyint(1) NOT NULL,
  `nTKTCODE` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`nId`),
  UNIQUE KEY `nJOBCODE` (`nJOBCODE`),
  KEY `tb_jobs_nTKTCODE_f049f352_fk_tb_tickets_nTKTCODE` (`nTKTCODE`),
  CONSTRAINT `tb_jobs_nTKTCODE_f049f352_fk_tb_tickets_nTKTCODE` FOREIGN KEY (`nTKTCODE`) REFERENCES `tb_tickets` (`nTKTCODE`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_jobs`
--

LOCK TABLES `tb_jobs` WRITE;
/*!40000 ALTER TABLE `tb_jobs` DISABLE KEYS */;
INSERT INTO `tb_jobs` VALUES (1,'JOB00001',1,3,0.00,'00000000000000000000000000000001',NULL,'asd','metal','{Comment: }',NULL,1,'TKT00001');
/*!40000 ALTER TABLE `tb_jobs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tb_jobs_images`
--

DROP TABLE IF EXISTS `tb_jobs_images`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tb_jobs_images` (
  `nId` int NOT NULL AUTO_INCREMENT,
  `nJOBCODE` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `img_location` longtext COLLATE utf8mb4_general_ci NOT NULL,
  `job_id` int NOT NULL,
  PRIMARY KEY (`nId`),
  KEY `tb_jobs_images_job_id_509e2f55_fk_tb_jobs_nId` (`job_id`),
  CONSTRAINT `tb_jobs_images_job_id_509e2f55_fk_tb_jobs_nId` FOREIGN KEY (`job_id`) REFERENCES `tb_jobs` (`nId`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_jobs_images`
--

LOCK TABLES `tb_jobs_images` WRITE;
/*!40000 ALTER TABLE `tb_jobs_images` DISABLE KEYS */;
INSERT INTO `tb_jobs_images` VALUES (1,'JOB00001','[{\"raw\": \"http://127.0.0.1:8000/media/images/uploads/RAW_20250505180148_JOB00001.png\", \"thumb\": \"http://127.0.0.1:8000/media/images/uploads/THUMB_20250505180148_JOB00001.png\", \"600\": \"http://127.0.0.1:8000/media/images/uploads/600_20250505180148_JOB00001.png\"}, {\"raw\": \"http://127.0.0.1:8000/media/images/uploads/RAW_20250505180148_JOB00001.png\", \"thumb\": \"http://127.0.0.1:8000/media/images/uploads/THUMB_20250505180148_JOB00001.png\", \"600\": \"http://127.0.0.1:8000/media/images/uploads/600_20250505180148_JOB00001.png\"}, {\"raw\": \"http://127.0.0.1:8000/media/images/uploads/RAW_20250505180148_JOB00001.png\", \"thumb\": \"http://127.0.0.1:8000/media/images/uploads/THUMB_20250505180148_JOB00001.png\", \"600\": \"http://127.0.0.1:8000/media/images/uploads/600_20250505180148_JOB00001.png\"}]',1);
/*!40000 ALTER TABLE `tb_jobs_images` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tb_tickets`
--

DROP TABLE IF EXISTS `tb_tickets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tb_tickets` (
  `nTKTCODE` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `nStatID` int NOT NULL,
  `nDocNo` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `nDueDate` date NOT NULL,
  `nDueTime` time(6) NOT NULL,
  `nTItems` int NOT NULL,
  `nCalVat` decimal(10,2) NOT NULL,
  `nCostNoVAT` decimal(10,2) NOT NULL,
  `nTCost` decimal(10,2) NOT NULL,
  `nTPaid` decimal(10,2) NOT NULL,
  `nTDue` decimal(10,2) NOT NULL,
  `multipleImages` tinyint(1) NOT NULL,
  `isCashCustomer` int NOT NULL,
  `isCusNotSigned` int NOT NULL,
  `nFSID` int NOT NULL,
  `nCusSignImage` longtext COLLATE utf8mb4_general_ci,
  `nComments` longtext COLLATE utf8mb4_general_ci,
  `nActive` tinyint(1) NOT NULL,
  `nInvoice` tinyint(1) NOT NULL,
  `nAcceptedDate` datetime(6) NOT NULL,
  `nReadyDate` datetime(6) DEFAULT NULL,
  `nReleasedDate` datetime(6) DEFAULT NULL,
  `nAcceptedBy` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `nReadyBy` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `nReleasedBy` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `nCUSCODE` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`nTKTCODE`),
  KEY `tb_tickets_nCUSCODE_76da8f41_fk_bibs_customer_nCUSCODE` (`nCUSCODE`),
  CONSTRAINT `tb_tickets_nCUSCODE_76da8f41_fk_bibs_customer_nCUSCODE` FOREIGN KEY (`nCUSCODE`) REFERENCES `bibs_customer` (`nCUSCODE`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_tickets`
--

LOCK TABLES `tb_tickets` WRITE;
/*!40000 ALTER TABLE `tb_tickets` DISABLE KEYS */;
INSERT INTO `tb_tickets` VALUES ('TKT00001',1,'22','2025-05-20','22:22:00.000000',3,15.00,0.00,15.00,0.00,15.00,1,2,0,1,NULL,'ticket Comment',1,0,'2025-05-05 18:01:48.372262',NULL,NULL,NULL,NULL,NULL,'CUS00001');
/*!40000 ALTER TABLE `tb_tickets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_groups`
--

DROP TABLE IF EXISTS `user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_groups` (
  `user_group_id` int NOT NULL AUTO_INCREMENT,
  `group_name` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`user_group_id`),
  UNIQUE KEY `group_name` (`group_name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_groups`
--

LOCK TABLES `user_groups` WRITE;
/*!40000 ALTER TABLE `user_groups` DISABLE KEYS */;
INSERT INTO `user_groups` VALUES (1,'ADMIN'),(2,'EDITOR');
/*!40000 ALTER TABLE `user_groups` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-05 23:39:38
