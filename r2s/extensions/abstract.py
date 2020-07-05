from abc import ABC,abstractmethod
from r2s.utils import _print, _print_error, _print_debug, _loadClass
from r2s.state import State

class R2SAPIAdaptor(ABC):
    def __init__(self):
        super().__init__()
    
    @abstractmethod
    def fetchItems(self, page_num):
        """Implement a call to a specific API to fetch items (single page)
        Return value should be a touple of: isFull, response_json where:
        is
        """
        pass

class R2SItemFormatter(ABC):
    """Abstract Item formatter - wraps a single json item. handles json parsing"""

    options = {}

    def __init__(self, item):
        self.item = item
        super().__init__()
    
    @abstractmethod
    def buildMessage(self):
        """Return a string representation of the item, formatted as a syslog message."""
        pass
    
    @staticmethod
    def wrapItems(items_as_json_array):
        """Input is json array of items. output is list of item formatters (each formatter instance wraps a single item)"""
        pass

    @staticmethod
    def loadFormatterClass(formatter_class_prefix, options):
        _print('about to load formatter ' + str(formatter_class_prefix))
        formatter_class = _loadClass(options, formatter_class_prefix,'formatter')
        formatter_class.options = options
        return formatter_class

    @abstractmethod
    def getID(self):
        """each item should have a unique identifier"""


class R2SAPIPaginator(ABC):
    def __init__(self, options, state = None, api_adaptor = None, extension_name = 'extension_name'):
        _print('initializing {} Paginator'.format(extension_name))
        if(state is None):
            self.state = State(file_prefix=extension_name)
        else:
            _print('initializing state for {} with value: {}'.format(extension_name,state.value))
            self.state = state
        self.extension_name = extension_name
        self.next_page_token = state.value
        _print('paginator {} next page token is: {}'.format(extension_name,state.value))
        self.is_end = False
        self.reset()
        try:
            self.max_pages = int(options['max_pages'])
            _print_debug('about to load formatters')
            self.formatter = R2SItemFormatter.loadFormatterClass(
                formatter_class_prefix = self.extension_name,
                options = options)
        except Exception as ex:
            _print_error(ex)
            _print_error('could not initialize {} Paginator.'.format(extension_name))
            raise
        if api_adaptor is not None:
            self.api_adaptor = api_adaptor
        else:
            _print_debug('about to load api adaptor for extension ' + self.extension_name)
            type_name = 'api_adaptor'
            api_adaptor_class = _loadClass(options, extension_name,type_name)
            _print('loaded api adaptor class!!')
            self.api_adaptor = api_adaptor_class(options)    

    @abstractmethod
    def reset(self):
        """reset pagination state. could be used to persist pagination state - such as last known item id or last known page token etc"""
        pass

    @abstractmethod
    def next(self):
        """check if more items are available for fetching."""
        pass

    @abstractmethod
    def fetchPageItems(self):
        """return a set of items wrapped in a R2SItemFormatter."""
        pass