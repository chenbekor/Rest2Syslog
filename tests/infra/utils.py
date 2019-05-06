import os
from r2s.state import DEFAULT_PERSIST_PATH

def teardown_function(function):
    try:
        os.remove(DEFAULT_PERSIST_PATH)
    except Exception as e:
        print(e)

def unwrap(item_formatters):
    if item_formatters is None:
        return None
    else:
        return list(map(lambda x:x.item,item_formatters))