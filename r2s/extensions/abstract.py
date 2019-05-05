from abc import ABC,abstractmethod

class R2SFetcher(ABC):
    def __init__(self):
        super().__init__()
    
    @abstractmethod
    def fetchItems(self):
        pass

class R2SItemFormatter(ABC):
    def __init__(self,options):
        super().__init__()
    
    @abstractmethod
    def buildMessage(self):
        pass