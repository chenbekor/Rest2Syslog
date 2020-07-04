import sys
#import syslogng

#logger = syslogng.Logger()

def _print(msg):
    print(msg)
    sys.stdout.flush() 
#    logger.info(msg)

def _print_error(msg):
    _print(msg)
#    logger.error(msg)

def _print_debug(msg):
    #return
    _print(msg)
    # #logger.debug(msg)

def _loadClass(options,class_prefix, type_name):
    _print('about to load {} class...'.format(type_name))
    module_name = options['{}.{}_module'.format(class_prefix, type_name)]
    class_name =  options['{}.{}_class'.format(class_prefix, type_name)]
    _print('about to load class {}.{}'.format(module_name,class_name))
    try:
        module = __import__(module_name, fromlist =[class_name])
    except:
        _print('loading of class failed with reason: {}'.format(sys.exc_info()))
        raise
    _print('class {}.{} imported!!'.format(module_name,class_name))
    _class = getattr(module, class_name)
    return _class