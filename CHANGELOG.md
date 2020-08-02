# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0]

### Added in version 1.0.0

* Initial release
* Wrote documentation
* Implemented the honeypot using the Twisted framework
* Config file support
* Various command-line options
* Log rotation
* Support for the `report_public_ip` config file option
* Implemented macros like `$ip`, `$now`, `$old`
* Implemented emulation of the following IPP operations:
  * `Get-Printer-Attributes`
  * `Get-Jobs`
  * "get completed jobs"
  * `Print-Job`
* Output plugin support
* Implemented output plugins for
  * JSON
  * MySQL
  * SQLite3
  * text