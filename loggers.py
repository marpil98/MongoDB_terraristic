import logging
from logging.handlers import TimedRotatingFileHandler

def basic_logger(name, backup):
    
    """Logger which note information about general running of app

    Returns
    -------
    logging.logger
        logger
    """
    logger = logging.getLogger(name)
    handler = TimedRotatingFileHandler(
        filename=f"logs/{name}.log",
        when='D',
        interval=1,
        backupCount=backup,
        encoding='utf-8'
        )
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(funcName)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    
    return logger


def db_conn_logger():
    """Logger which note information about database connection

    Returns
    -------
    logging.logger
        logger
    """
    logger = basic_logger("db_conn", 30)
    
    return logger

def main_logger():
    
    """Logger which note information about general running of app

    Returns
    -------
    logging.logger
        logger
    """
    logger = basic_logger("main", 10)
    
    return logger

