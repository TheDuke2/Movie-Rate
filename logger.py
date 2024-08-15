import logging
import logging.handlers


PAPERTRAIL_HOST = 'logs4.papertrailapp.com'
PAPERTRAIL_PORT = 15688

# handler = logging.handlers.SysLogHandler(address=(PAPERTRAIL_HOST, PAPERTRAIL_PORT))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s"
)

# logging.getLogger().addHandler(handler)

def get_logger(name):
    logger = logging.getLogger(name)
    return logger
