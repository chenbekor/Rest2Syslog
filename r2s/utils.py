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
    #_print(msg)
#    logger.debug(msg)
