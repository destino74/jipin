import logging
import logging.handlers


def setup_logger(logfile):
    handler = logging.handlers.RotatingFileHandler(logfile, maxBytes=1024 * 1024, backupCount=5)
    fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'

    formatter = logging.Formatter(fmt)
    handler.setFormatter(formatter)

    logger = logging.getLogger(logfile)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger
