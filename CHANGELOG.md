# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.1]

### Added in version 1.0.1

* Nothing yet

### Changed in version 1.0.1

* Fixed a typo in the `README.md` file

## [1.0.0]

### Added in version 1.0.0

* Initial release
* Implemented the honeypot using the Twisted framework
* Made the honeypot compatible with Python 3.x
* Config file support
* Various command-line options
* Log rotation
* Support for the `report_public_ip` config file option
* A script for starting, stopping, and restarting the honeypot
* Macros like `$ip`, `$now`, `$old`
* Documentation
* Emulation of the following IPP operations:
  * `Get-Printer-Attributes`
  * `Get-Jobs`
  * "get completed jobs"
  * `Print-Job`
* Output plugin support
* Output plugins for
  * CouchDB
  * Elasticsearch
  * HPFeeds
  * Influx 2.0 (Python 3 only)
  * JSON
  * MongoDB
  * MySQL
  * PostgreSQL
  * RedisDB
  * SQLite3
  * syslog
  * text
