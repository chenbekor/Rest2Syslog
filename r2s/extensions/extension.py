from r2s.utils import _print, _loadClass

class Extension:
    def __init__(self, name, options, paginator = None, send_items_func = _print):
        _print('init Extension ' + name)
        self.name = name
        self.sendItems = send_items_func
        if paginator is None:
            _print('about to load paginator for extension ' + name)
            paginator_class = _loadClass(options, name,'api_paginator')
            self.paginator = paginator_class(options = options, extension_name = name)
        else:
            self.paginator = paginator
    


    def doWork(self):
        while self.paginator.next():
            page_items = self.paginator.fetchPageItems()
            if page_items is not None:
                if len(page_items) > 0:
                    self.sendItems(page_items)
                    _print('Extension: ' + self.name + ' returned ' + str(len(page_items)) + ' new items.')
                else:
                    _print('Extension: ' + self.name + ' finished pagination.')
            else:
                _print('Extension: ' + self.name + ' finished pagination.')
                break
        self.paginator.reset()
