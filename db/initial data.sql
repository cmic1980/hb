-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               10.2.12-MariaDB - mariadb.org binary distribution
-- Server OS:                    Win64
-- HeidiSQL Version:             9.4.0.5125
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

-- Dumping structure for table hb.daily_trade
CREATE TABLE IF NOT EXISTS `daily_trade` (
  `daily_trade_id` int(11) NOT NULL AUTO_INCREMENT,
  `balance` int(11) NOT NULL DEFAULT 0 COMMENT '买入数量',
  `symbol` varchar(20) NOT NULL,
  `exec_time` varchar(5) NOT NULL COMMENT '执行时间，格式为HH:mm',
  `t` float NOT NULL COMMENT '期望收益率百分数，比如期望收益率1.2%，这个值应该是1.2',
  `buy_order_id` int(11) DEFAULT NULL COMMENT '买单id，挂买单成功后更新到该字段',
  `buy_price` float DEFAULT NULL,
  `sell_order_id` int(11) DEFAULT NULL COMMENT '卖单id，挂卖单成功后更新到该字段',
  `status` int(11) NOT NULL COMMENT '当前状态',
  PRIMARY KEY (`daily_trade_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

-- Dumping data for table hb.daily_trade: ~0 rows (approximately)
DELETE FROM `daily_trade`;
/*!40000 ALTER TABLE `daily_trade` DISABLE KEYS */;
INSERT INTO `daily_trade` (`daily_trade_id`, `balance`, `symbol`, `exec_time`, `t`, `buy_order_id`, `buy_price`, `sell_order_id`, `status`) VALUES
	(3, 150, 'omg', '21:00', 1.3, NULL, NULL, NULL, 1),
	(4, 12000, 'cmt', '23:00', 1.3, NULL, NULL, NULL, 1);

/*!40000 ALTER TABLE `daily_trade` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
