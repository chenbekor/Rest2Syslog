from syslogng import LogSource
import time
import pickle
from paginator import Paginator
import pfpt-parser
from pfpt-state import State
import pfpt-utils

class ProofpointSyslogSource(LogSource):

    def init(self, options): # optional
        _print("Proofpoint Syslog Source init")
        try:
            self.interval = int(options['interval'])
            self.paginator = Paginator(options)
            self.exit = False
            try:
                self.state = _read_state()
            except Exception as e:
                _print(type(e).__name__)
                _print('Error while trying to read Proofpoint Syslog State: '+ str(e))
                self.state = State('')
            return True
        except:
            _print('configuration of Proofpoint Syslog Source (PSS) is incomplete or malformed. Please reffer to the PSS documentation for more details.')
            return False

    def request_exit(self): # mandatory
        _print("Proofpoint Syslog Source exit")
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
            if item['id'] != self.state.last_record_id
                msg = buildMessage(item)
                self.post_message(msg)
                self.state.last_record_id = item['id']
            else:
                return True
        return False

    def fetchPages(self):
        while not self.exit:
            page_items = self.paginator.fetchPage()
            if page_items is not None && len(page_items) != 0:
                is_last_page = self.sendItems(page_items)
                if is_last_page: break    
                self.paginator.next()
            else:
                _print('No more pages to fetch')
                break
        self.state.persist()
        self.paginator.reset()
