
from time import time
from struct import pack
from hashlib import sha256
from sys import version_info
from datetime import datetime
from os.path import join, exists
from os import SEEK_SET, SEEK_END

from core.compile import compile_line
from core.tools import (
    mkdir,
    decode,
    hexdump,
    get_word,
    get_dword,
    get_string,
    get_real_ip,
    get_local_ip,
    get_real_port,
    get_utc_time,
    print_query,
    resolve_url,
    write_event
)

from twisted.python import log
from twisted.web.resource import Resource

try:
    from urllib.parse import unquote
except ImportError:
    from urlparse import unquote


if version_info[0] >= 3:
    def ord(x):
        return x


class Index(Resource):
    isLeaf = True
    page_cache = {
        'getattr.ipp': b'',
        'getjobs.ipp': b'',
        'printjob.ipp': b''
    }

    def __init__(self, options):
        self.cfg = options

    def render_HEAD(self, request):
        self.log_request(request)
        self.report_event(request)
        return self.send_response(request)

    def render_GET(self, request):
        self.log_request(request)
        self.report_event(request)
        return self.send_response(request)

    def render_POST(self, request):
        self.log_request(request)
        if request.getHeader('Content-Length'):
            content_length = int(request.getHeader('Content-Length'))
        else:
            old_pos = request.content.tell()
            request.content.seek(0, SEEK_END)
            content_length = request.content.tell()
            request.content.seek(old_pos, SEEK_SET)
        #log.msg('Content length: {}'.format(content_length))
        if content_length:
            post_data = request.content.read()
            answer = self.process_request(request, post_data)
            return self.send_response(request, answer)
        return self.send_response(request)

    def log_request(self, request):
        ip = request.getClientAddress().host
        path = unquote(decode(request.uri))
        method = decode(request.method)
        log.msg('[INFO] {}: {} {}'.format(ip, method, path))

    def process_request(self, request, data):
        from core.data import (
            operations_code,
            attributes_code,
            groups_code,
            operations,
            attributes,
            groups
        )

        def error(query, answer):
            log.msg('\n' + print_query(query))
            return answer

        answer = b''
        if len(data) < 9:
            return compile_line('VERSION 1.1', self.cfg) + compile_line('STATUS successful-ok', self.cfg)
        request_id = 0
        query = {}
        index = 0
        version_major = ord(data[index])
        index += 1
        version_minor = ord(data[index])
        index += 1
        answer += compile_line('VERSION {}.{}'.format(version_major, version_minor), self.cfg)
        answer += compile_line('STATUS successful-ok', self.cfg)
        query['version'] = '{}.{}'.format(version_major, version_minor)
        operation = get_word(data, index)
        index += 2
        request_id = get_dword(data, index)
        index += 4
        answer += compile_line('REQUEST-ID {:08X}'.format(request_id), self.cfg)
        query['request_id'] = '{:08X}'.format(request_id)
        if operation not in operations_code:
            return error(query, answer)
        query['operation'] = operations_code[operation]
        # begin-attribute-group-tag must follow:
        group_id = ord(data[index])
        if group_id not in groups_code:
            return error(query, answer)
        index += 1
        query['groups'] = []
        group = {}
        group['group_type'] = groups_code[group_id]
        group['attributes'] = []
        query['groups'].append(group)
        data_len = len(data)
        col_value = b''
        in_collection = 0
        in_list = False
        while index < data_len:
            attr = ord(data[index])
            index += 1
            if attr == groups['end-of-attributes-tag']:
                # end-of-attributes-tag
                break
            elif attr in groups_code:
                group = {}
                group['group_type'] = groups_code[attr]
                group['attributes'] = []
                query['groups'].append(group)
                continue
            if attr not in attributes_code:
                return error(query, answer)
            if index + 2 >= data_len:
                break
            name_len = get_word(data, index)
            index += 2
            if name_len:
                if index + name_len >= data_len:
                    break
                name = get_string(data, index, name_len)
                index += name_len
            elif attr != attributes['memberattrname'] and in_collection == 0:
                in_list = True
            if index + 2 >= data_len:
                break
            value_len = get_word(data, index)
            index += 2
            if index + value_len >= data_len:
                break
            if attr == attributes['boolean']:
                value = 'true' if ord(data[index]) else 'false'
                index += 1
            elif attr == attributes['integer']:
                # integer
                value = get_dword(data, index)
                index += 4
            elif attr == attributes['rangeofinteger']:
                # rangeOfInteger
                lower_limit = get_dword(data, index)
                index += 4
                upper_imit = get_dword(data, index)
                index += 4
                value = str(lower_limit) + '-' + str(upper_imit)
            elif attr in [attributes['unknown'], attributes['no-value']]:
                # unknown, no-value
                value = attributes_code[attr]
            elif attr == attributes['resolution']:
                # resolution
                value = str(get_dword(data, index))
                index += 8
                value += 'dpi' if ord(data[index]) == 0x03 else 'dpcm'
                index += 1
            elif attr == attributes['enum']:
                # enum
                enum_code = get_dword(data, index)
                index += 4
                if enum_code in operations_code:
                    value = operations_code[enum_code]
                else:
                    value = '{:04X}'.format(enum_code)
            elif attr == attributes['datetime']:
                # dateTime
                year = get_word(data, index)
                month = ord(data[index + 2])
                day = ord(data[index + 3])
                hour = ord(data[index + 4])
                minute = ord(data[index + 5])
                second = ord(data[index + 6])
                value = datetime.strftime(datetime(year, month, day, hour, minute, second), '%Y-%m-%dT%H:%M:%SZ')
                index += 11
            elif attr == attributes['collection']:
                # begCollection
                if in_collection:
                    col_value += b'{'
                else:
                    col_value = b'{'
                    in_collection += 1
                value = ''
            elif attr == attributes['memberattrname']:
                # memberAttrName
                member_name_len = value_len
                member_name = get_string(data, index, member_name_len)
                col_value += b' ' + member_name + b'='
                value = ''
                index += member_name_len
            elif attr == attributes['endcollection']:
                # endCollection
                col_value += b' }'
                in_collection -= 1
                if in_collection:
                    value = ''
                else:
                    value = col_value.replace('{ ', '{').replace(' }', '}')
                    value_len = len(value)
                    attr = attributes['collection']
            else:
                # deleteAttribute
                # adminDefine
                # octetString
                # textWithLanguage
                # nameWithLanguage
                # textWithoutLanguage
                # nameWithoutLanguage
                # uri
                # uriScheme
                # charset
                # naturalLanguage
                # mimeMediaType
                value = get_string(data, index, value_len)
                if not value:
                    value = "''"
                index += value_len
            if in_collection:
                col_value += str(value)
            elif in_list:
                query['groups'][-1]['attributes'][-1]['attribute_value'].append(value)
                in_list = False
            else:
                attribute = {}
                attribute['attribute_type'] = attributes_code[attr]
                attribute['attribute_name'] = name
                attribute['attribute_value'] = [value]
                query['groups'][-1]['attributes'].append(attribute)
        if operation == operations['print-job']:
            document = data[index:]
            hash = sha256(document).hexdigest()
            filename = join(self.cfg['download_dir'], hash)
            mkdir(self.cfg['download_dir'])
            if not exists(filename):
                with open(filename, 'wb') as f:
                    f.write(document)
            file_info = {}
            file_info['filename'] = filename
            file_info['filesize'] = len(document)
            file_info['hash'] = hash
            self.report_event(request, query, file_info)
        else:
            self.report_event(request, query)
        answer += self.process_operation(data, query)
        return answer

    def process_operation(self, data, query):
        answer = b''
        operation = query['operation']
        log.msg('[INFO] Operation: {}'.format(operation))
        if operation == 'Get-Printer-Attributes':
            # get-printer-attributes
            answer += self.get_page('getattr.ipp')
        elif operation == 'Get-Jobs':
            # get-jobs
            answer += self.get_page('getjobs.ipp')
        elif operation == 'Print-Job':
            # print-job
            answer += self.get_page('printjob.ipp')
        else:
            log.msg('[INFO] POST body:\n{}'.format(hexdump(data)))
        log.msg('\n' + print_query(query))
        return answer

    def report_event(self, request, query=None, file_info=None):
        unix_time = time()
        event = {}
        if query is None or 'operation' not in query:
            event['eventid'] = 'ipphoney.connect'
        else:
            event['eventid'] = 'ipphoney.' + query['operation'].lower()
        event['timestamp'] = get_utc_time(unix_time)
        event['unixtime'] = unix_time
        event['url'] = unquote(decode(request.uri))
        event['src_ip'] = get_real_ip(request)
        event['src_port'] = get_real_port(request)
        event['dst_port'] = self.cfg['port']
        event['sensor'] = self.cfg['sensor']
        event['request'] = decode(request.method)
        event['operation'] = query['operation']
        if file_info is not None:
            event['filename'] = file_info['filename']
            event['filesize'] = file_info['filesize']
            event['sha256'] = file_info['hash']
        if query is not None:
            event['query'] = query
        user_agent = request.getHeader('User-Agent')
        if user_agent:
            event['user_agent'] = user_agent
        event['dst_ip'] = self.cfg['public_ip'] if self.cfg['report_public_ip'] else get_local_ip()
        write_event(event, self.cfg)

    # a simple wrapper to cache files from "responses" folder
    def get_page(self, page):
        if page not in self.page_cache:
            log.msg('Missing file: "{}".'.format(page))
            return ''
        # if page is not in cache, load it from file
        if self.page_cache[page] == b'':
            with open(join(self.cfg['responses_dir'], page), 'r') as f:
                lines = f.readlines()
                for line in lines:
                    line = line.strip()
                    if not line or line[0] == '#':
                        continue
                    self.page_cache[page] += compile_line(line, self.cfg)
        return self.page_cache[page]

    def send_response(self, request, page=''):
        request.setHeader('Date', datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT'))
        request.setHeader('Server', 'Lexmark_Web_Server')
        request.setHeader('Cache-Control', 'no-cache')
        request.setHeader('X-Frame-Options', 'SAMEORIGIN')
        request.setHeader('Upgrade', 'TLS/1.0, HTTP/1.1')
        request.setHeader('Connection', 'upgrade')
        request.setHeader('Content-Length', str(len(page)))
        request.setHeader('X-XSS-Protection', '1; mode=block')
        request.setHeader('Content-Security-Policy', "frame-ancestors 'none'")
        request.setHeader('X-Content-Type-Options', 'nosniff')
        request.setHeader('Content-type', 'application/ipp')
        return page
