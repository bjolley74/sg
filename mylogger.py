#mylogger
import logging

def set_up(log_name='app_log.log', log_set_level='DEBUG'):
    log_level = 'logging.' + log_set_level
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)
    format = '%(asctime)s: %(levelname)s: %(name)s: %(funcName)s: %(message)s'
    formatter = logging.Formatter(format)
    file_handler = logging.FileHandler(log_name)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

def log(message,level):
    if level == 'debug':
        logger.info(message)
    elif level == 'info':
        logger.info(message)
    elif level == 'warning':
        logging.warning(message)
    elif level == 'error':
        logging.error(message)
    elif level == 'critical':
        logging.critical(message

