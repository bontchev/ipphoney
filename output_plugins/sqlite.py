
from core import output
from core.config import CONFIG
from core.tools import geolocate

from json import dumps
from hashlib import sha256
from geoip2.database import Reader
from sqlite3 import OperationalError, IntegrityError

from twisted.python import log
from twisted.internet import defer
from twisted.enterprise.adbapi import ConnectionPool


class Output(output.Output):

    def start(self):
        db_name = CONFIG.get('output_sqlite', 'db_file', fallback='data/ipphoney.db')
        self.debug = CONFIG.getboolean('output_sqlite', 'debug', fallback=False)
        self.geoip = CONFIG.getboolean('output_sqlite', 'geoip', fallback=True)

        try:
            self.db = ConnectionPool(
                'sqlite3',
                database=db_name,
                check_same_thread=False
            )
        except OperationalError as e:
            log.msg(e)

        self.db.start()

        if self.geoip:
            geoipdb_city_path = CONFIG.get('output_sqlite', 'geoip_citydb', fallback='data/GeoLite2-City.mmdb')
            geoipdb_asn_path = CONFIG.get('output_sqlite', 'geoip_asndb', fallback='data/GeoLite2-ASN.mmdb')

            try:
                self.reader_city = Reader(geoipdb_city_path)
            except:
                log.msg('Failed to open City GeoIP database {}'.format(geoipdb_city_path))

            try:
                self.reader_asn = Reader(geoipdb_asn_path)
            except:
                log.msg('Failed to open ASN GeoIP database {}'.format(geoipdb_asn_path))

    def stop(self):
        if self.geoip:
            if self.reader_city is not None:
                self.reader_city.close()
            if self.reader_asn is not None:
                self.reader_asn.close()

    def write(self, event):
        self.db.runInteraction(self.connect_event, event)

    def simple_query(self, txn, sql, args):
        if self.debug:
            if len(args):
                log.msg('output_sqlite: SQLite3 query: {} {}'.format(sql, repr(args)))
            else:
                log.msg('output_sqlite: SQLite3 query: {}'.format(sql))
        try:
            if len(args):
                txn.execute(sql, args)
            else:
                txn.execute(sql)
            result = txn.fetchall()
        except IntegrityError as e:
            result = None
        except Exception as e:
            log.msg('output_sqlite: SQLite3 Error: {}'.format(e))
            result = None
        return result

    def get_id(self, txn, table, column, entry):
        r = self.simple_query(txn, "SELECT `id` FROM `{}` WHERE `{}` = ?".format(table, column), (entry, ))
        if r:
            id = r[0][0]
        else:
            self.simple_query(txn, "INSERT INTO `{}` (`{}`) VALUES (?)".format(table, column), (entry, ))
            r = self.simple_query(txn, 'SELECT LAST_INSERT_ROWID()', ())
            if r:
                id = int(r[0][0])
            else:
                id = 0
        return id

    def get_hashed_id(self, txn, table, filename, filesize, shasum):
        r = self.simple_query(txn, "SELECT `id` FROM `{}` WHERE `hash` = ?".format(table), (shasum, ))
        if r:
            id = int(r[0][0])
        else:
            self.simple_query(txn, "INSERT INTO `{}` (`filename`, `filesize`, `hash`) VALUES (?, ?, ?)".format(table),
                              (filename, filesize, shasum, ))
            r = self.simple_query(txn, 'SELECT LAST_INSERT_ROWID()', ())
            if r:
                id = int(r[0][0])
            else:
                id = 0
        return id

    def connect_event(self, txn, event):
        remote_ip = event['src_ip']

        operation_id = self.get_id(txn, 'operations', 'op_name', event['operation'])
        path_id = self.get_id(txn, 'urls', 'path', event['url'])
        if 'filename' in event:
            file_id = self.get_hashed_id(txn, 'files', event['filename'], event['filesize'], event['sha256'])
        else:
            file_id = 'NULL'
        if 'query' in event:
            query_id = self.get_id(txn, 'queries', 'query', dumps(event['query']))
        else:
            query_id = 'NULL'
        if 'user_agent' in event:
            agent_id = self.get_id(txn, 'user_agents', 'user_agent', event['user_agent'])
        else:
            agent_id = 'NULL'
        sensor_id = self.get_id(txn, 'sensors', 'name', event['sensor'])

        self.simple_query(txn, """
            INSERT INTO `connections` (
                `timestamp`, `ip`, `remote_port`, `request`, `url`, `operation`,
                `file`, `query`, `user_agent`, `local_host`, `local_port`, `sensor`)
            VALUES (DATETIME(?, 'unixepoch', 'localtime'), ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (event['unixtime'], remote_ip, event['src_port'], event['request'], path_id, operation_id,
             file_id, query_id, agent_id, event['dst_ip'], event['dst_port'], sensor_id, ))

        if self.geoip:
            country, country_code, city, org, asn_num = geolocate(remote_ip, self.reader_city, self.reader_asn)
            result = self.simple_query(txn, """
                INSERT INTO `geolocation` (`ip`, `country_name`, `country_iso_code`, `city_name`, `org`, `org_asn`)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (remote_ip, country, country_code, city, org, asn_num, ))
            if result is None:
                self.simple_query(txn, """
                    UPDATE `geolocation` SET
                        `country_name` = ?,
                        `country_iso_code` = ?,
                        `city_name` = ?,
                        `org` = ?,
                        `org_asn` = ?
                    WHERE `ip` = ?
                    """,
                    (country, country_code, city, org, asn_num, remote_ip, ))
