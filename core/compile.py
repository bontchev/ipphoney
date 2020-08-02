
from re import compile
from struct import pack
from random import randrange
from datetime import datetime, timedelta

from twisted.python import log


def compile_line(source, cfg):
    from core.data import (
        operations,
        attributes,
        statuses,
        groups,
        finishings,
        orientations,
        qualities,
        job_states,
        printer_states
    )

    def error(message, bad_arg):
        log.msg('Compile error: {} "{}".'.format(message, bad_arg))

    def merge_dicts(*dict_args):
        result = {}
        for dictionary in dict_args:
            result.update(dictionary)
        return result

    def compile_res(value):
        def compile_res_item(value):
            parts = reg_ex.match(value).groups()
            if len(parts) < 2:
                error('bad resolution', value)
                return b''
            result = pack('>H', 9)
            number = parts[0]
            measurement = parts[1]
            result += pack('>L', int(number))
            result += pack('>L', int(number))
            if measurement.lower() == 'dpi':
                result += pack('B', 3)
            else:
                result += pack('B', 4)
            return result

        if ',' not in value:
            return compile_res_item(value)
        sub_args = value.split(',')
        result = compile_res_item(sub_args[0])
        for sub_arg in sub_args[1:]:
            result += pack('B', attributes['resolution'])
            result += pack('>H', 0x0000)        # value-length
            result += compile_res_item(sub_arg) # value
        return result

    def compile_enum(value):
        def compile_enum_item(value):
            result = b''
            value = value.lower()
            if value in all_enums:
                result += pack('>H', 4)                 # value-length
                result += pack('>L', all_enums[value])  # value
            else:
                error('bad enum', value)
            return result

        if ',' not in value:
            return compile_enum_item(value)
        sub_args = value.split(',')
        result = compile_enum_item(sub_args[0])
        for sub_arg in sub_args[1:]:
            result += pack('B', attributes['enum'])
            result += pack('>H', 0x0000)            # value-length
            result += compile_enum_item(sub_arg)    # value
        return result

    def compile_bool(value):
        result = pack('>H', 1)
        result += pack('B', 1 if value == 'true' else 0)
        return result

    def compile_int(value):
        result = b''
        if value.isdigit():
            result += pack('>H', 4)
            result += pack('>L', int(value))
        else:
            error('bad integer', value)
        return result

    def compile_range(value):
        result = b''
        values = value.split('-')
        if values[0].isdigit() and values[1].isdigit():
            result += pack('>H', 8)
            result += pack('>L', int(values[0]))
            result += pack('>L', int(values[1]))
        else:
            error('bad range', value)
        return result

    def compile_collection(value, cfg):
        def compile_collection_item(value, cfg):
            def compile_value(value, cfg):
                result = b''
                if value.isdigit():
                    # x = integer
                    result += pack('B', attributes['integer'])
                    result += pack('>H', 0) # unnamed-value
                    result += compile_int(value)
                elif '://' in value:
                    # x = uri
                    result += pack('B', attributes['uri'])
                    result += pack('>H', 0) # unnamed-value
                    result += pack('>H', len(value))
                    result += value # TO-DO: replace $ip
                elif value[0] == '{':
                    # x = collection
                    result += pack('B', attributes['collection'])
                    result += pack('>H', 0) # unnamed-value
                    result += compile_collection(value, cfg)
                else:
                    # Is boolean, rangeOfInteger, resolution, etc. possible?
                    # x = keyword
                    result += pack('B', attributes['keyword'])
                    result += pack('>H', 0) # unnamed-value
                    result += pack('>H', len(value))
                    result += value
                return result

            result = b''
            result += pack('>H', 0) # unnamed-value
            value = value.lstrip('{').rstrip('}')
            while value:
                result += pack('B', attributes['memberattrname'])
                result += pack('>H', 0) # unnamed-value
                parts = value.split('=', 1)
                var_name = parts[0]
                if len(parts) < 2:
                    error('bad collection member', var_name)
                    return b''
                result += pack('>H', len(var_name))
                result += var_name
                rest = parts[1]
                if rest[0] == '{':
                    level = 0
                    index = 0
                    for ch in rest:
                        if ch == '{':
                            level += 1
                        elif ch == '}':
                            level -= 1
                        index += 1
                        if level == 0:
                            break
                    var_value = rest[:index]
                    result += compile_value(var_value, cfg)
                    value = rest[index:].strip()
                else:
                    parts = rest.split(' ', 1)
                    var_value = parts[0]
                    result += compile_value(var_value, cfg)
                    if len(parts) < 2:
                        value = ''
                    else:
                        value = parts[1]
            result += pack('B', attributes['endcollection'])
            result += pack('>H', 0x0000)
            result += pack('>H', 0x0000)
            return result

        result = b''
        if value[0] != '{' or value[-1] != '}':
            error('bad collection', value)
            return result
        if ',' not in value:
            result += compile_collection_item(value, cfg)
        else:
            # Warning: This will break if collection members can be 1SetOf
            sub_args = value.split(',')
            result += compile_collection_item(sub_args[0], cfg)
            for sub_arg in sub_args[1:]:
                result += pack('B', attributes['collection'])
                result += pack('>H', 0x0000)    # unnamed-value
                result += compile_collection_item(sub_arg, cfg)  # value
        return result

    def compile_date(value):
        result = b''
        if '$now' in value.lower():
            timestamp = datetime.utcnow()
        elif '$old' in value.lower():
            timestamp = datetime.utcnow() - timedelta(
                days=randrange(30),
                hours=randrange(24),
                minutes=randrange(60),
                seconds=randrange(60)
            )
        else:
            timestamp = datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ')
        result += pack('>H', 11)
        result += pack('>H', timestamp.year)
        result += pack('B', timestamp.month)
        result += pack('B', timestamp.day)
        result += pack('B', timestamp.hour)
        result += pack('B', timestamp.minute)
        result += pack('B', timestamp.second)
        result += pack('>H', 0x002B)
        result += pack('>H', 0x0000)
        return result

    def compile_keyword(value, keyword_type):
        result = b''
        if ',' not in value:
            if value in ['no-value', 'unknown', 'unsupported']:
                result += pack('>H', 0)
            else:
                result += pack('>H', len(value))    # value-length
                result += value.encode('utf-8')     # value
        else:
            sub_args = value.split(',')
            result += pack('>H', len(sub_args[0]))  # value-length
            result += sub_args[0].encode('utf-8')   # value
            for sub_arg in sub_args[1:]:
                result += pack('B', attributes[keyword_type])
                result += pack('>H', 0x0000)        # unnamed-value
                result += pack('>H', len(sub_arg))  # value-length
                result += sub_arg.encode('utf-8')   # value
        return result

    reg_ex = compile('([0-9]+)([a-zA-Z]+)')
    all_enums = merge_dicts(
        operations,
        finishings,
        orientations,
        qualities,
        job_states,
        printer_states
    )
    tokens = source.split()
    keyword = tokens[0].lower()
    if len(tokens) > 1:
        keyword_type = tokens[1].lower()
        arguments = tokens[2:]
    if keyword == 'version':
        version = keyword_type.split('.')
        result = pack('B', int(version[0])) + pack('B', int(version[1]))
    elif keyword == 'request-id':
        if len(keyword_type) == 8 and set(keyword_type) <= set('0123456789abcdef'):
            result = pack('>L', int(keyword_type, 16))
        else:
            error('bad hex number', keyword_type)
            result = b''
    elif keyword == 'status':
        if keyword_type in statuses:
            result = pack('>H', statuses[keyword_type])
        else:
            error('uknown status', keyword_type)
            result = b''
    elif keyword == 'operation':
        if keyword_type in operations:
            result = pack('>H', operations[keyword_type])
        else:
            error('unknown operation', keyword_type)
            result = b''
    elif keyword == 'group':
        if keyword_type in groups:
            result = pack('B', groups[keyword_type])
        else:
            error('unknown group type', keyword_type)
            result = b''
    elif keyword == 'attr':
        if keyword_type not in attributes:
            error('unknown attribute type', keyword_type)
            result = b''
        elif len(arguments) < 2:
            error('too few arguments of ATTR', ' '.join(arguments))
            result = b''
        else:
            result = pack('B', attributes[keyword_type])
            result += pack('>H', len(arguments[0])) # name-length
            result += arguments[0].encode('utf-8')  # name
            long_args = [
                'textwithoutlanguage',
                'namewithoutlanguage',
                'textwithlanguage',
                'namewithlanguage',
                'collection'
            ]
            if keyword_type in long_args:
                value = ' '.join(arguments[1:])
            else:
                value = arguments[1]
            value = value.replace("''", '')
            value = value.replace('$ip', cfg['public_ip'])
            if keyword_type == 'boolean':
                result += compile_bool(value)
            elif keyword_type == 'integer':
                if arguments[0].lower() == 'printer-up-time':
                    value = str(randrange(2500000))
                result += compile_int(value)
            elif keyword_type == 'rangeofinteger':
                result += compile_range(value)
            elif keyword_type == 'resolution':
                result += compile_res(value)
            elif keyword_type == 'collection':
                result += compile_collection(value, cfg)
            elif keyword_type == 'enum':
                result += compile_enum(value)
            elif keyword_type == 'datetime':
                result += compile_date(value)
            else:
                result += compile_keyword(value, keyword_type)
    else:
        error('unknown keyword', keyword)
        result = b''
    return result
