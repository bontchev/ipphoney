
from sys import version_info
from datetime import datetime
from os import makedirs, path
from socket import socket, AF_INET, SOCK_DGRAM

from core.config import CONFIG

from twisted.python import log

try:
    from urllib.request import urlopen
    from urllib.parse import urlsplit, urlunsplit
except ImportError:
    from urllib import urlopen
    from urlparse import urlsplit, urlunsplit


if version_info[0] >= 3:
    xrange = range
    def ord(x):
        return x
    def decode(x):
        return x.decode('utf-8')
else:
    def decode(x):
        return x


def hexdump(buffer, length=16):
    theHex = lambda data: ' '.join('{:02X}'.format(ord(i)) for i in data)
    theStr = lambda data: ''.join(chr(ord(i)) if (31 < ord(i) < 127) else '.' for i in data)
    result = ''
    for offset in xrange(0, len(buffer), length):
        data = buffer[offset:offset + length]
        result += '{:08X}   {:{}}    {}\n'.format(offset, theHex(data), length * 3 - 1, theStr(data))
    return result


def get_real_ip (request):
    ip = request.getHeader('X-Real-IP')
    return request.getClientAddress().host if ip is None else ip


def get_real_port (request):
    port = request.getHeader('X-Real-Port')
    return request.getClientAddress().port if port is None else port


def get_word(data, index):
    return ord(data[index]) * 0x100 + ord(data[index + 1])


def get_dword(data, index):
    return ord(data[index]) * 0x1000000 + ord(data[index + 1]) * 0x10000 + ord(data[index + 2]) * 0x100 + ord(data[index + 3])


def get_string(data, index, length):
    return decode(data[index:index + length])


def get_utc_time(unix_time):
    return datetime.utcfromtimestamp(unix_time).isoformat() + 'Z'


def get_public_ip(ip_reporter):
    if version_info[0] < 3:
        return urlopen(ip_reporter).read().decode('latin1', errors='replace').encode('utf-8')
    else:
        return decode(urlopen(ip_reporter).read())


def get_local_ip():
    s = socket(AF_INET, SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip


def resolve_url(url):
    parts = list(urlsplit(url))
    segments = parts[2].split('/')
    segments = [segment + '/' for segment in segments[:-1]] + [segments[-1]]
    resolved = []
    for segment in segments:
        if segment in ('../', '..'):
            if resolved[1:]:
                resolved.pop()
        elif segment not in ('./', '.'):
            resolved.append(segment)
    parts[2] = ''.join(resolved)
    return urlunsplit(parts)


def write_event(event, cfg):
    output_plugins = cfg['output_plugins']
    for plugin in output_plugins:
        try:
            plugin.write(event)
        except Exception as e:
            log.msg(e)
            continue


def mkdir(dir_path):
    if not dir_path:
        return
    if path.exists(dir_path) and path.isdir(dir_path):
        return
    makedirs(dir_path)


def import_plugins(cfg):
    # Load output modules (inspired by the Cowrie honeypot)
    log.msg('Loading the plugins...')
    output_plugins = []
    general_options = cfg
    for x in CONFIG.sections():
        if not x.startswith('output_'):
            continue
        if CONFIG.getboolean(x, 'enabled') is False:
            continue
        engine = x.split('_')[1]
        try:
            output = __import__('output_plugins.{}'.format(engine),
                                globals(), locals(), ['output'], 0).Output(general_options)
            output_plugins.append(output)
            log.msg('Loaded output engine: {}'.format(engine))
        except ImportError as e:
            log.msg('Failed to load output engine: {} due to ImportError: {}'.format(engine, e))
        except Exception as e:
            log.msg('Failed to load output engine: {} {}'.format(engine, e))
    return output_plugins


def stop_plugins(cfg):
    log.msg('Stoping the plugins...')
    for plugin in cfg['output_plugins']:
        try:
            plugin.stop()
        except Exception as e:
            log.msg(e)
            continue


def geolocate(remote_ip, reader_city, reader_asn):
    try:
        response_city = reader_city.city(remote_ip)
        city = response_city.city.name
        if city is None:
            city = ''
        else:
            city = decode(city.encode('utf-8'))
        country = response_city.country.name
        if country is None:
            country = ''
            country_code = ''
        else:
            country = decode(country.encode('utf-8'))
            country_code = decode(response_city.country.iso_code.encode('utf-8'))
    except Exception as e:
        log.msg(e)
        city = ''
        country = ''
        country_code = ''

    try:
        response_asn = reader_asn.asn(remote_ip)
        if response_asn.autonomous_system_organization is None:
            org = ''
        else:
            org = decode(response_asn.autonomous_system_organization.encode('utf-8'))

        if response_asn.autonomous_system_number is not None:
            asn_num = response_asn.autonomous_system_number
        else:
            asn_num = 0
    except Exception as e:
        log.msg(e)
        org = ''
        asn_num = 0
    return country, country_code, city, org, asn_num


def print_query(query):
    def print_group(group):
        def print_attribute(attribute):
            result = '\tATTR ' + attribute['attribute_type'] + ' '
            result += attribute['attribute_name'] + ' '
            if isinstance(attribute['attribute_value'], list):
                result += ','.join(str(v) for v in attribute['attribute_value'])
            else:
                result += str(attribute['attribute_value'])
            result += '\n'
            return result

        result = ''
        if 'group_type' in group:
            result += '\tGROUP ' + group['group_type'] + '\n'
        if 'attributes' in group:
            for attribute in group['attributes']:
                result += print_attribute(attribute)
        return result

    result = '{\n'
    if 'version' in query:
        result += '\tVERSION ' + query['version'] + '\n'
    if 'request_id' in query:
        result += '\tREQUEST ' + query['request_id'] + '\n'
    if 'status' in query:
        result += '\tSTATUS ' + query['status'] + '\n'
    if 'operation' in query:
        result += '\tOPERATION ' + query['operation'] + '\n'
    if 'groups' in query:
        for group in query['groups']:
            result += print_group(group)
    result += '}'
    return result
