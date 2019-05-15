from syslogng import Logger

logger = syslogng.Logger()

def _print(msg):
    logger.info(msg)
