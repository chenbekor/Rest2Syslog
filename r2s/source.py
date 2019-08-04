from syslogng import LogSource
from syslogng import LogMessage
import time
from r2s.extensions.extension import Extension
from r2s.utils import _print, _print_error
import sys

class REST2SyslogSource(LogSource):

    def init(self, options): # optional
        _print("REST2Syslog Source init")
        _print("running python version:{}.{}".format(sys.version_info[0],sys.version_info[1]))
        try:
            self.interval = int(options['interval'])
            self.extensions = []
            for extension_name in options['extensions'].split(','):
                _print('found extension: ' + extension_name)
                self.extensions.append(Extension(name = extension_name,options = options, send_items_func = self.sendItems))
            self.exit = False
            return True
        except:
            _print_error('configuration of REST2Syslog Source (R2S) is incomplete or malformed. Please reffer to the R2S Wiki for more details.')
            return False

    def request_exit(self): # mandatory
        _print("R2S Source exit")
        self.exit = True

    def run(self): # mandatory
        while not self.exit:
            try:
                time.sleep(self.interval)
                self.doWork()
            except Exception as e:
                _print_error('Error while trying to fetch alerts.')
                _print_error(e)

    def sendItems(self,items):
        for item in items:            
            msg = LogMessage(item.buildMessage())
            self.post_message(msg)

    def doWork(self):
        while not self.exit:
            for extension in self.extensions:
                extension.doWork()
            break

