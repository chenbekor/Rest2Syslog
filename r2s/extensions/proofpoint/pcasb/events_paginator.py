from r2s.utils import _print, _print_error, _print_debug, _loadClass
from r2s.extensions.abstract import R2SItemFormatter
from r2s.state import State
import sys


class PCASBEventsPaginator:
    def __init__(self, options, state, api_adaptor, extension_name):
        super().__init__()
        _print('init: Events Paginator')
        if(state is None):
            self.state = State(file_prefix=extension_name)
        else:
            self.state = state
        self.extension_name = extension_name
        self.reset()
        try:
            self.max_pages = int(options['max_pages'])
            _print('about to load formatters')
            self.formatter = R2SItemFormatter.loadFormatterClass(
                formatter_class_prefix = self.extension_name,
                options = options)
        except Exception as ex:
            _print_error(ex)
            _print_error('could not initialize Events Paginator.')
            raise
        if api_adaptor is not None:
            self.api_adaptor = api_adaptor
        else:
            _print('about to load api adaptor for extension ' + self.extension_name)
            type_name = 'api_adaptor'
            api_adaptor_class = _loadClass(options, extension_name,type_name)
            _print('loaded api adaptor class!!')
            self.api_adaptor = api_adaptor_class(options)

    def reset(self):
        try:
            self.state.setValue(self.next_page_token)
        except: pass
        self.next_page_token = ""
        self.page_size = -1
        self.is_end = False

    def next(self):
        return self.page_size != 0
    
    def fetchPageItems(self):
        response_json = self.api_adaptor.fetchItems(self.next_page_token) 
        if response_json is not None:
            try:
                events = response_json['content']
                self.next_page_token = response_json['nextPageToken']
                self.page_size = int(response_json['size'])
                wrapped_events = self.formatter.wrapItems(events)
            except Exception as ex:
                _print_error(ex)
                wrapped_events = None
            return wrapped_events
        else:
            return None