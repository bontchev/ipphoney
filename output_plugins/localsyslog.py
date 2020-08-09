
import syslog

from core import output
from core.config import CONFIG


def formatCef(logentry):
    """
    Take logentry and turn into CEF string
    """
    # Jan 18 11:07:53 host CEF:Version|Device Vendor|Device Product|
    # Device Version|Signature ID|Name|Severity|[Extension]
    cefVendor = 'Bontchev'
    cefProduct = 'IPPHoney'
    cefVersion = '1.0'
    cefSignature = logentry['eventid']
    cefName = logentry['eventid']
    cefSeverity = '5'

    cefExtensions = {
        'deviceExternalId': logentry['sensor'],
        'src': logentry['src_ip'],
        'spt': logentry['src_port'],
        'dpt': logentry['dst_port'],
        'dst': logentry['dst_ip'],
        'req': logentry['request'],
        'url': logentry['url'],
        'proto': 'tcp'
    }

    if 'operation' in logentry:
        cefExtensions['opr'] = logentry['operation']
    if 'filename' in logentry:
        cefExtensions['nam'] = logentry['filename']
        cefExtensions['siz'] = logentry['filesize']
        cefExtensions['sha'] = logentry['sha256']

    cefList = []
    for key in list(cefExtensions.keys()):
        value = str(cefExtensions[key])
        cefList.append('{}={}'.format(key, value))

    cefExtension = ' '.join(cefList)

    cefString = 'CEF:0|' + \
                cefVendor + '|' + \
                cefProduct + '|' + \
                cefVersion + '|' + \
                cefSignature + '|' + \
                cefName + '|' + \
                cefSeverity + '|' + \
                cefExtension

    return cefString


class Output(output.Output):

    def start(self):
        facilityString = CONFIG.get('output_localsyslog', 'facility', fallback='USER')
        facility = vars(syslog)['LOG_' + facilityString]
        syslog.openlog(logoption=syslog.LOG_PID, facility=facility)

    def stop(self):
        pass

    def write(self, event):
        syslog.syslog(syslog.LOG_INFO, formatCef(event))
