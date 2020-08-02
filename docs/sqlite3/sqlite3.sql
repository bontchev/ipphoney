CREATE TABLE IF NOT EXISTS `connections` (
  `id` INTEGER PRIMARY KEY,
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
  `sensor` INT(4) DEFAULT NULL
);

CREATE INDEX IF NOT EXISTS `time_idx` ON `connections` (`timestamp`);
CREATE INDEX IF NOT EXISTS `ip_idx` ON `connections` (`ip`);
CREATE INDEX IF NOT EXISTS `ip2_idx` ON `connections` (`timestamp`, `ip`);

CREATE TABLE IF NOT EXISTS `urls` (
  `id` INTEGER PRIMARY KEY,
  `path` VARCHAR(255) DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS `operations` (
  `id` INTEGER PRIMARY KEY,
  `op_name` VARCHAR(63) NOT NULL
);

CREATE TABLE IF NOT EXISTS `files` (
  `id` INTEGER PRIMARY KEY,
  `filesize` INT(11) DEFAULT NULL,
  `filename` VARCHAR(255) DEFAULT NULL,
  `hash` VARCHAR(66),
  UNIQUE (`hash`)
);

CREATE TABLE IF NOT EXISTS `queries` (
  `id` INTEGER PRIMARY KEY,
  `query` JSON
);

CREATE TABLE IF NOT EXISTS `user_agents` (
  `id` INTEGER PRIMARY KEY,
  `user_agent` VARCHAR(255) DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS `sensors` (
  `id` INTEGER PRIMARY KEY,
  `name` VARCHAR(255) DEFAULT NULL,
  UNIQUE (`name`)
);

CREATE TABLE IF NOT EXISTS `geolocation` (
  `id` INTEGER PRIMARY KEY,
  `ip` VARCHAR(15) DEFAULT NULL,
  `country_name` VARCHAR(45) DEFAULT '',
  `country_iso_code` VARCHAR(2) DEFAULT '',
  `city_name` VARCHAR(128) DEFAULT '',
  `org` VARCHAR(128) DEFAULT '',
  `org_asn` INT(11) DEFAULT NULL,
  UNIQUE(`ip`)
);

