
from os import makedirs, linesep
from os.path import dirname, basename

from core import output
from core.config import CONFIG
from core.tools import mkdir, print_query
from core.logfile import HoneypotDailyLogFile

class Output(output.Output):

    def start(self):
        fn = CONFIG.get('output_textlog', 'logfile')
        dirs = dirname(fn)
        base = basename(fn)
        mkdir(dirs)
        self.outfile = HoneypotDailyLogFile(base, dirs, defaultMode=0o664)

    def stop(self):
        self.outfile.flush()

    def write(self, event):
        self.outfile.write('[{}] '.format(event['timestamp']))
        self.outfile.write('[{}] '.format(event['sensor']))
        self.outfile.write('{} '.format(event['request']))
        self.outfile.write('{} '.format(event['url']))
        self.outfile.write('from {}:{} '.format(event['src_ip'], event['dst_port']))
        if 'query' in event:
            self.outfile.write('{}\tIPP query:{}{} '.format(linesep, linesep, print_query(event['query'])))
        self.outfile.write(linesep)
        self.outfile.flush()
