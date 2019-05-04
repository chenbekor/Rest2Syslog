import pickle
from r2s_utils import _print

DEFAULT_PERSIST_PATH = '/tmp/r2s-state.obj'

class State:
    def __init__(self, last_record_id = '', persit_path = DEFAULT_PERSIST_PATH):
        self.persist_path = persit_path
        try:
            with open(self.persist_path, 'rb') as f:
                restored_state = pickle.load(f)
                self.last_record_id = restored_state.last_record_id
        except Exception as e:
            _print('No REST2Syslog State. Creating a new instance.'+ str(e))
            self.last_record_id = last_record_id

    def setLastRecordId(self,last_record_id):
        if(last_record_id != ''):
            _print('storing new last record id:' + last_record_id)
            self.last_record_id = last_record_id
            self.persist()

    def persist(self):
        try:
            with open(self.persist_path, 'wb') as f:
                pickle.dump(self, f)
        except Exception as e:
            _print('Error while trying to store REST2Syslog State: ' + str(e))



