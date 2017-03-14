
import logging
import logging.handlers


def get_logger():
    return logging.getLogger('broadlink-http')

def add_file_handler(log_file):
    logger = get_logger()
    logger.setLevel(logging.INFO)
    log_file = log_file
    handler = logging.handlers.RotatingFileHandler(
        log_file, maxBytes=1024*1024, backupCount=5)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

def add_console_handler():
    logger = get_logger()
    logger.addHandler(logging.StreamHandler())
    return logger
