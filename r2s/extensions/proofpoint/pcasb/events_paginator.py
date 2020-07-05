from r2s.utils import _print, _print_error, _print_debug, _loadClass
from r2s.extensions.abstract import R2SItemFormatter, R2SAPIPaginator
from r2s.state import State
import sys


class PCASBEventsPaginator(R2SAPIPaginator):
    def __init__(self, options, state = None, api_adaptor = None, extension_name = 'extension_name'):
        super().__init__(options, state, api_adaptor, extension_name)

    def reset(self):
        try:
            self.state.setValue(self.next_page_token)
        except: pass
        self.page_size = -1
        self.is_end = False

    def next(self):
        _print_debug('next page token for {} = {}'.format(self.extension_name,self.next_page_token))
        return self.page_size != 0
    
    def fetchPageItems(self):
        response_json = self.api_adaptor.fetchItems(self.next_page_token) 
        if response_json is not None:
            try:
                events = response_json['content']
                _print_debug('{}: about to update next page token with: {}'.format(self.extension_name,response_json['nextPageToken']))
                self.next_page_token = response_json['nextPageToken']
                self.page_size = int(response_json['size'])
                _print('got {} events.'.format(self.page_size))
                if self.page_size is 0:
                    return None
                else:
                    _print_debug('page size is: {}'.format(self.page_size))
                wrapped_events = self.formatter.wrapItems(events)
            except Exception as ex:
                _print_error(ex)
                wrapped_events = None
            return wrapped_events
        else:
            return None