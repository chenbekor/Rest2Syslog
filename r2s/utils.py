from syslogng import Logger

logger = syslogng.Logger()

def _print(msg):
    logger.info(msg)

def _print_error(msg):
    logger.error(msg)

def _print_debug(msg):
    logger.debug(msg)
