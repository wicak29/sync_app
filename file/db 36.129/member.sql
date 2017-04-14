-- --------------------------------------------------------
-- Host:                         10.151.36.129
-- Versi server:                 5.5.54-0ubuntu0.14.04.1-log - (Ubuntu)
-- OS Server:                    debian-linux-gnu
-- HeidiSQL Versi:               9.3.0.4984
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

-- Dumping database structure for emp
CREATE DATABASE IF NOT EXISTS `emp` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `emp`;


-- Dumping structure for table emp.member
CREATE TABLE IF NOT EXISTS `member` (
  `id_member` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) DEFAULT NULL,
  `salary` double DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `change_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id_member`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=latin1;

-- Dumping data for table emp.member: ~13 rows (approximately)
DELETE FROM `member`;
/*!40000 ALTER TABLE `member` DISABLE KEYS */;
INSERT INTO `member` (`id_member`, `name`, `salary`, `email`, `change_date`) VALUES
	(5, 'Adi Wicaksan', 80000, 'wicak@gmail.com', '2017-04-05 06:28:41'),
	(6, 'Nabilah', 90000, NULL, '2017-04-05 16:29:10'),
	(7, 'Faradilla', 88000, 'faradilla@ymail.com', '2017-04-05 06:28:41'),
	(9, 'Ronaldo', 90000, 'ronaldo@gmail.com', '2017-04-05 16:29:11'),
	(10, 'Lionel Mess', 90000, 'mesi@mail.com', '2017-04-05 16:29:10'),
	(11, 'Coutinho', 90000, 'coutinho@mail.com', '2017-04-05 06:28:41'),
	(13, 'Roberto Firmino', 87000, 'rfirmino@mail.com', '2017-04-05 16:29:10'),
	(14, 'Daniel Sturidge', 80000, 'da.struridge@mail.com', '2017-04-05 06:28:41'),
	(15, 'Adam Lallana', 80000, 'da.struridge@mail.com', '2017-04-05 06:28:41'),
	(16, 'Daniel Bintar', 80000, 'bintar@mail.com', '2017-04-05 06:28:41'),
	(17, 'Daniel Fablius', 80000, 'df@mail.com', '2017-04-05 06:28:41'),
	(18, 'Jordan Henderson', 80000, 'jordan@mail.com', '2017-04-05 06:28:41'),
	(19, 'Steven Gerrad', 80000, 'steveg@mail.com', '2017-04-05 16:29:12');
/*!40000 ALTER TABLE `member` ENABLE KEYS */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
