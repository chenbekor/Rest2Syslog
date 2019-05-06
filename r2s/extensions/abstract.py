from abc import ABC,abstractmethod

class R2SFetcher(ABC):
    def __init__(self):
        super().__init__()
    
    @abstractmethod
    def fetchItems(self):
        pass

class R2SItemFormatter(ABC):
    """Abstract Item formatter - wraps a single json item. handles json parsing"""

    options = {}

    def __init__(self, item):
        self.item = item
        super().__init__()
    
    @abstractmethod
    def buildMessage(self):
        """Please implement in extension class - return string representation of item"""
        pass
    
    @staticmethod
    def jsonToItems(json_obj):
        """Please implement in extension class: input is json. output is list of item formatters"""
        pass

    @abstractmethod
    def getID(self):
        """each item should have a unique identifier"""