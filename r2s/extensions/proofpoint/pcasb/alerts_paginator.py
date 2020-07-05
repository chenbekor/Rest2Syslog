from r2s.utils import _print, _print_error, _print_debug, _loadClass
from r2s.extensions.abstract import R2SItemFormatter, R2SAPIPaginator
from r2s.state import State
import sys


class PCASBAlertsPaginator(R2SAPIPaginator):
    def __init__(self, options, state = None, api_adaptor = None, extension_name = 'extension_name'):
        super().__init__(options, state, api_adaptor, extension_name)

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
        _print_debug("inside next!!")
        if self.isNextAvailable():
            _print_debug("is next available!!")
            self.next_page_token += 1
            _print('next page token for {} = {}'.format(self.extension_name,self.next_page_token))
            return True
        else:
            return False

    def filterItems(self,items):
        _print_debug('filtering items...')
        if items is None or len(items) == 0: 
            _print_debug('nothing to filter - aborting filtration.')
            return None
        filtered_items = []
        if self.current_item_id == '':
            _print_debug('current item id == "" assigning new value: {}'.format(items[0].getID()))
            self.current_item_id = items[0].getID()
        for item in items:
            _print('filtration: checking item {}'.format(item.getID()))
            if item.getID() != self.state.value:
                _print_debug('item {} is good - adding to filtered list.'.format(item))
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
            _print_debug('Reached stream end. Aborting.')
            return None

        _print_debug('fetching items==>')
        response_json = self.api_adaptor.fetchItems(self.next_page_token) 
        _print_debug('got those items: {}'.format(response_json))
        if response_json is not None:
            try:
                items = self.formatter.wrapItems(response_json)
            except Exception as ex:
                _print_error(ex)
                items = None
            return self.filterItems(items)
        else:
            return None