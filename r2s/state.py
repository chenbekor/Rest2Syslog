import pickle
from r2s.utils import _print, _print_debug, _print_error

DEFAULT_PREFIX = 'default'
STATE_FILE_NAME = '-r2s-state.obj'
DEFAULT_PERSIST_PATH = '/tmp/'

class State:
    def __init__(self, value = '', persist_path = DEFAULT_PERSIST_PATH, file_prefix = DEFAULT_PREFIX):
        _print('initializing State')
        self.persist_path = persist_path
        self.file_prefix = file_prefix
        self.full_path = self.persist_path + self.file_prefix + STATE_FILE_NAME
        if(value is not ''):
            self.value = value
        else:
            try:
                with open(self.full_path, 'rb') as f:
                    restored_state = pickle.load(f)
                    if restored_state is not None:
                        _print('loaded from disk the following last record: ' + restored_state.value)
                        self.value = restored_state.value
                    else:
                        _print('restored state was empty.')
            except Exception as e:
                _print_error('No REST2Syslog State. Creating a new instance.'+ str(e))
                self.value = value

    def setValue(self,value):
        if(value != ''):
            _print_debug('persisting new value:' + value)
            self.value = value
            self.persist()

    def persist(self):
        try:
            with open(self.full_path, 'wb') as f:
                pickle.dump(self, f)
        except Exception as e:
            _print_error('Error while trying to store REST2Syslog State: ' + str(e))



