from r2s.utils import _print, _print_error, _print_debug, _loadClass
from r2s.extensions.abstract import R2SItemFormatter, R2SAPIPaginator
from r2s.state import State
import sys


class PCASBAlertsPaginator(R2SAPIPaginator):
    def __init__(self, options, state = None, api_adaptor = None, extension_name = 'extension_name'):
        super().__init__()
        _print('init: Alerts Paginator')
        if(state is None):
            self.state = State(file_prefix=extension_name)
        else:
            _print_debug('initializing state with value: {}'.format(state.value))
            self.state = state
        self.extension_name = extension_name
        self.next_page_token = -1
        self.is_end = False
        self.reset()
        try:
            self.max_pages = int(options['max_pages'])
            _print('about to load formatters')
            self.formatter = R2SItemFormatter.loadFormatterClass(
                formatter_class_prefix = self.extension_name,
                options = options)
        except Exception as ex:
            _print_error(ex)
            _print_error('could not initialize Alerts Paginator.')
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
            self.state.setValue(self.current_item_id)
        except: pass
        self.next_page_token = -1
        self.current_item_id = ''
        self.is_end = False
    
    def isNextAvailable(self):
        is_not_maxed = self.max_pages >= 0 and (self.max_pages == 0 or (self.next_page_token + 1) < self.max_pages)
        is_not_reached_end = not self.is_end
        return  is_not_reached_end and is_not_maxed

    def next(self):
        _print("inside next!!")
        if self.isNextAvailable():
            _print("is next available!!")
            self.next_page_token += 1
            _print('next page token = {}'.format(self.next_page_token))
            return True
        else:
            return False

    def filterItems(self,items):
        _print('filtering items...')
        if items is None or len(items) == 0: 
            _print('nothing to filter - aborting filtration.')
            return None
        filtered_items = []
        if self.current_item_id == '':
            _print('current item id == "" assigning new value: {}'.format(items[0].getID()))
            self.current_item_id = items[0].getID()
        for item in items:
            _print('filtration: checking item {}'.format(item.getID()))
            if item.getID() != self.state.value:
                _print('item {} is good - adding to filtered list.'.format(item))
                filtered_items.append(item)
            else:
                _print_debug('Current Record ID: ' + item.getID() + ' matched last record id from state: ' + self.state.value)
                self.state.setValue(self.current_item_id)
                self.is_end = True
                break
        if len(filtered_items) == 0:
            return None
        else:
            return filtered_items
    
    def fetchPageItems(self):
        if self.is_end:
            _print('Reached stream end. Aborting.')
            return None

        _print('fetching items==>')
        response_json = self.api_adaptor.fetchItems(self.next_page_token) 
        _print('got those items: {}'.format(response_json))
        if response_json is not None:
            try:
                items = self.formatter.wrapItems(response_json)
            except Exception as ex:
                _print_error(ex)
                items = None
            return self.filterItems(items)
        else:
            return None