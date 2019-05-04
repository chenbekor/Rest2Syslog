from r2s_utils import _print
from r2s_state import State
from r2s_api_adaptor import APIAdaptor

class Paginator:
    def __init__(self,options, api_adaptor = None, state = State()):
        self.state = state
        self.reset()
        try:
            self.max_pages = int(options['max_pages'])
        except:
            _print('could not read max_pages param from config options. please reffer to the R2S wiki for more information.')
            raise
        if api_adaptor is not None:
            self.api_adaptor = api_adaptor
        else:
            self.api_adaptor = APIAdaptor(options)

    def reset(self):
        try:
            self.state.setLastRecordId(self.current_record_id)
        except: pass
        self.page_num = -1
        self.current_record_id = ''
        

    def getPage(self):
        return {'page':self.page_num}

    def next(self):
        if (self.page_num + 1) < self.max_pages:
            self.page_num += 1
            return True
        else:
            return False


    def handlePageError(self,r):
        _print('Got non 200 response code')
        if r.status_code == 401:
            _print('The Auth Token was probably expired.')
            self.auth_token = None
        else:
            _print('Error Response code: ' + str(r.status_code))
            _print('Error Response body: ' + r.text)

    def filterRecords(self,records):
        if records is None or len(records) == 0: return None
        filtered_records = []
        if self.current_record_id == '':
            self.current_record_id = records[0]['id']
        for record in records:
            if record['id'] != self.state.last_record_id:
                filtered_records.append(record)
            else:
                self.state.setLastRecordId(self.current_record_id)
                break
        if len(filtered_records) == 0:
            return None
        else:
            return filtered_records


    def fetchPage(self):
        r = self.api_adaptor.executeRequest(self.getPage())
        if r.status_code != 200:
            self.handlePageError(r)
            return None
        else:
            try:
                records = r.json()['alerts']
            except:
                records = None
            return self.filterRecords(records)
