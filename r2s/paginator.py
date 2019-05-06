from r2s.utils import _print
from r2s.state import State
from r2s.api_adaptor import APIAdaptor

class Paginator:
    def __init__(self,options, api_adaptor = None, state = State(), extension_name = 'extension_name'):
        self.state = state
        self.extension_name = extension_name
        self.reset()
        try:
            self.max_pages = int(options['max_pages'])
            self.formatter = self.loadFormatter(options)
        except Exception as ex:
            _print(ex)
            _print('could not initialize Paginator.')
            raise
        if api_adaptor is not None:
            self.api_adaptor = api_adaptor
        else:
            self.api_adaptor = APIAdaptor(options)

    def loadFormatter(self,options):
        formatter_module = options[self.extension_name + '.formatter_module']
        formatter_class_name = options[self.extension_name + '.formatter_class']
        module = __import__(formatter_module, fromlist =[formatter_class_name])
        formatter_class = getattr(module, formatter_class_name)
        formatter_class.options = options
        return formatter_class

    def reset(self):
        try:
            self.state.setLastItemId(self.current_item_id)
        except: pass
        self.page_num = -1
        self.current_item_id = ''

    def getPage(self):
        return {'page':self.page_num}

    def next(self):
        if (self.page_num + 1) < self.max_pages:
            self.page_num += 1
            return True
        else:
            return False


    def handlePageError(self,r):
        _print('Got non 200 response code')
        if r.status_code == 401:
            _print('The Auth Token was probably expired.')
            self.auth_token = None
        else:
            _print('Error Response code: ' + str(r.status_code))
            _print('Error Response body: ' + r.text)

    def filterItems(self,items):
        if items is None or len(items) == 0: return None
        filtered_items = []
        if self.current_item_id == '':
            self.current_item_id = items[0].getID()
        for item in items:
            if item.getID() != self.state.last_item_id:
                filtered_items.append(item)
            else:
                self.state.setLastItemId(self.current_item_id)
                break
        if len(filtered_items) == 0:
            return None
        else:
            return filtered_items


    def fetchPageItems(self):
        r = self.api_adaptor.fetchItems(self.getPage())
        if r.status_code != 200:
            self.handlePageError(r)
            return None
        else:
            try:
                items = self.formatter.jsonToItemFormatters(r.json())
            except Exception as ex:
                _print(ex)
                items = None
            return self.filterItems(items)
