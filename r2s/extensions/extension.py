from r2s.paginator import Paginator
from r2s.utils import _print

class Extension:
    def __init__(self,name,options, paginator = None, send_items_func = _print):
        self.name = name
        self.sendItems = send_items_func
        if paginator is None:    
            self.paginator = Paginator(name,options)
        else:
            self.paginator = paginator
        

    def doWork(self):
        while self.paginator.next():
            page_items = self.paginator.fetchPageItems()
            if page_items is not None:
                self.sendItems(page_items)
            else:
                _print('No new items for extension: ' + self.name)
                break