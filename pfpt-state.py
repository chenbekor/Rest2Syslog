import pfpt-utils

fp = None

def _get_file_handler():
    global fp
    if fp is None:
        fp = open('/tmp/pfpf-syslog-state.obj', 'wb+')
    return fp

class State:
    def __init__(self, last_record_id):
        try:
            fp = _get_file_handler()
            state = pickle.load(fp)
            self.last_record_id = state.last_record_id
        except Exception as e:
            _print(type(e).__name__)
            _print('Error while trying to read Proofpoint Syslog State: '+ str(e))
            self.last_record_id = ''

    def persist(self):
        try:
            fp = _get_file_handler()
            pickle.dump(self, fp)
        except Exception as e:
            _print('Error while trying to store Proofpoint Syslog State: ' + str(e))



