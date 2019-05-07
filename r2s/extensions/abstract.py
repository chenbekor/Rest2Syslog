from abc import ABC,abstractmethod

class R2SAPIAdaptor(ABC):
    def __init__(self):
        super().__init__()
    
    @abstractmethod
    def fetchItems(self, page_num):
        """Implement a call to a specific API to fetch items (single page)"""
        pass

class R2SItemFormatter(ABC):
    """Abstract Item formatter - wraps a single json item. handles json parsing"""

    options = {}

    def __init__(self, item):
        self.item = item
        super().__init__()
    
    @abstractmethod
    def buildMessage(self):
        """Return a string representation of an item - this will be sent to syslog"""
        pass
    
    @staticmethod
    def wrapItems(items_as_json_array):
        """Input is json array of items. output is list of item formatters (each formatter wraps a single item)"""
        pass

    @abstractmethod
    def getID(self):
        """each item should have a unique identifier"""