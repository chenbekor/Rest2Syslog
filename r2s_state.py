import pickle
from r2s_utils import _print

fp = None

def _get_file_handler():
    global fp
    if fp is None:
        fp = open('/tmp/pfpf-syslog-state.obj', 'wb+')
    return fp

class State:
    def __init__(self, last_record_id = ''):
        _print('init State')
        try:
            fp = _get_file_handler()
            state = pickle.load(fp)
            self.last_record_id = state.last_record_id
        except Exception as e:
            _print('No REST2Syslog State. Creating a new instance.'+ str(e))
            self.last_record_id = last_record_id

    def setLastRecordId(self,last_record_id):
        if(last_record_id != ''):
            _print('storing new last record id:' + last_record_id)
            self.last_record_id = last_record_id

    def persist(self):
        try:
            fp = _get_file_handler()
            pickle.dump(self, fp)
        except Exception as e:
            _print('Error while trying to store REST2Syslog State: ' + str(e))



