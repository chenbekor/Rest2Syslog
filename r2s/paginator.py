from r2s.utils import _print
from r2s.state import State

class Paginator:
    def __init__(self,options, api_adaptor = None, state = State(), extension_name = 'extension_name'):
        _print('init: Paginator')
        self.state = state
        self.extension_name = extension_name
        self.reset()
        try:
            self.max_pages = int(options['max_pages'])
            _print('about to load formatters')
            self.formatter = self.loadFormatter(options)
        except Exception as ex:
            _print(ex)
            _print('could not initialize Paginator.')
            raise
        if api_adaptor is not None:
            self.api_adaptor = api_adaptor
        else:
            _print('about to load api adaptor for extension ' + self.extension_name)
            api_adaptor_class = self.loadClass(options,'api_adaptor')
            self.api_adaptor = api_adaptor_class(options)

    def loadClass(self,options,type_name):
        _print('about to load ' + type_name + ' class...')
        module_name = options[self.extension_name + '.' + type_name + '_module']
        class_name = options[self.extension_name + '.' + type_name + '_class']
        _print('about to load from module:' + module_name)
        _print('about to load class:' + class_name)
        module = __import__(module_name, fromlist =[class_name])
        _class = getattr(module, class_name)
        return _class

    def loadFormatter(self,options):
        _print('about to load formatter for extension ' + self.extension_name)
        formatter_class = self.loadClass(options,'formatter')
        formatter_class.options = options
        return formatter_class

    def reset(self):
        try:
            self.state.setLastItemId(self.current_item_id)
        except: pass
        self.page_num = -1
        self.current_item_id = ''

    def next(self):
        if self.max_pages >= 0 and (self.max_pages == 0 or (self.page_num + 1) <= self.max_pages):
            self.page_num += 1
            return True
        else:
            return False

    def filterItems(self,items):
        if items is None or len(items) == 0: return None
        filtered_items = []
        if self.current_item_id == '':
            self.current_item_id = items[0].getID()
        for item in items:
            if item.getID() != self.state.last_item_id:
                filtered_items.append(item)
            else:
                _print('Current Record ID: ' + item.getID() + ' matched last record id from state: ' + self.state.last_item_id )
                self.state.setLastItemId(self.current_item_id)
                break
        if len(filtered_items) == 0:
            return None
        else:
            return filtered_items

    def fetchPageItems(self):
        response_json = self.api_adaptor.fetchItems(self.page_num) 
        try:
            items = self.formatter.wrapItems(response_json)
        except Exception as ex:
            _print(ex)
            items = None
        return self.filterItems(items)
