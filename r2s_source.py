from syslogng import LogSource
import time
from r2s_paginator import Paginator
from r2s_parser import Parser
from r2s_utils import _print

class REST2SyslogSource(LogSource):

    def init(self, options, paginator = None): # optional
        _print("REST2Syslog Source init")
        try:
            self.interval = int(options['interval'])
            if paginator is None:    
                self.paginator = Paginator(options)
            else:
                self.paginator = paginator
            self.parser = Parser(options)
            self.exit = False
            return True
        except:
            _print('configuration of REST2Syslog Source (R2S) is incomplete or malformed. Please reffer to the R2S Wiki for more details.')
            return False

    def request_exit(self): # mandatory
        _print("R2S Source exit")
        self.exit = True

    def run(self): # mandatory
        while not self.exit:
            try:
                time.sleep(5)
                self.fetchPages()
            except Exception as e:
                _print('Error while trying to fetch alerts.')
                _print(e)

    def sendItems(self,items):
        for item in items:            
            msg = self.parser.buildMessage(item)
            self.post_message(msg)

    def fetchPages(self):
        while not self.exit and self.paginator.next():
            page_items = self.paginator.fetchPage()
            if page_items is not None:
                self.sendItems(page_items)
            else:
                _print('No new items')
                break
