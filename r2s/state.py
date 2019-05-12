import pickle
from r2s.utils import _print

DEFAULT_PERSIST_PATH = '/tmp/r2s-state.obj'

class State:
    def __init__(self, last_item_id = '', persit_path = DEFAULT_PERSIST_PATH):
        _print('initializing State')
        self.persist_path = persit_path
        try:
            with open(self.persist_path, 'rb') as f:
                restored_state = pickle.load(f)
                if restored_state is not None:
                    _print('loaded from disk the following last record: ' + restored_state.last_item_id)
                    self.last_item_id = restored_state.last_item_id
                else
                    _print('restored state was empty.')
        except Exception as e:
            _print('No REST2Syslog State. Creating a new instance.'+ str(e))
            self.last_item_id = last_item_id

    def setLastItemId(self,last_item_id):
        if(last_item_id != ''):
            _print('storing new last item id:' + last_item_id)
            self.last_item_id = last_item_id
            self.persist()

    def persist(self):
        try:
            with open(self.persist_path, 'wb') as f:
                pickle.dump(self, f)
        except Exception as e:
            _print('Error while trying to store REST2Syslog State: ' + str(e))



