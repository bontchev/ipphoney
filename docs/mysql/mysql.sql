CREATE TABLE IF NOT EXISTS `connections` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `timestamp` DATETIME DEFAULT NULL,
  `ip` VARCHAR(15) DEFAULT NULL,
  `remote_port` INT(11) DEFAULT NULL,
  `request` VARCHAR(6) DEFAULT NULL,
  `url` INT(4) DEFAULT NULL,
  `operation` INT(4) DEFAULT NULL,
  `file` INT(4) DEFAULT NULL,
  `query` INT(4) DEFAULT NULL,
  `user_agent` INT(4) DEFAULT NULL,
  `local_host` VARCHAR(15) DEFAULT NULL,
  `local_port` INT(11) DEFAULT NULL,
  `sensor` INT(4) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `time_idx` (`timestamp`),
  KEY `ip_idx` (`ip`),
  KEY `ip2_idx` (`timestamp`, `ip`)
);

CREATE TABLE IF NOT EXISTS `urls` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `path` VARCHAR(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `operations` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `op_name` VARCHAR(63) DEFAULT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `files` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `filesize` INT(11) DEFAULT NULL,
  `filename` VARCHAR(255),
  `hash` VARCHAR(66),
  PRIMARY KEY (`id`),
  UNIQUE (`hash`)
);

CREATE TABLE IF NOT EXISTS `queries` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `query` JSON,
  PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `user_agents` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `user_agent` VARCHAR(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `content_types` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `content_type` VARCHAR(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `accept_languages` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `accept_language` VARCHAR(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `sensors` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE (`name`)
);

CREATE TABLE IF NOT EXISTS `geolocation` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `ip` VARCHAR(15) DEFAULT NULL,
  `country_name` VARCHAR(45) DEFAULT '',
  `country_iso_code` VARCHAR(2) DEFAULT '',
  `city_name` VARCHAR(128) DEFAULT '',
  `org` VARCHAR(128) DEFAULT '',
  `org_asn` INT(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE(`ip`)
);

