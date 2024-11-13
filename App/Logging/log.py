import logging
from logging.handlers import RotatingFileHandler

def setup_logger(log_file):
    """
    Set up a logger with the specified log file.

    Parameters:
    log_file (str): The path to the log file.

    Returns:
    None
    """
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    file_handler = RotatingFileHandler(log_file, mode='a', maxBytes=5*1024*1024, backupCount=2)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

def log_debug(message:str):
    """
    Logs a debug message.

    Args:
        message (str): The message to be logged.
    """
    logging.debug(message)

def log_info(message:str):
    """
    Logs an informational message.

    Args:
        message (str): The message to be logged.
    """
    logging.info(message)

def log_warning(message:str):
    """
    Logs a warning message.

    Parameters:
    message (str): The warning message to be logged.

    Returns:
    None
    """
    logging.warning(message)

def log_error(message:str):
    """
    Logs an error message using the logging module.

    Parameters:
    - message (str): The error message to be logged.

    Returns:
    - None

    Example:
    log_error("An error occurred.")
    """
    logging.error(message)

def log_critical(message:str):
    """
    Logs a critical message.

    Args:
        message (str): The message to be logged.

    Returns:
        None
    """
    logging.critical(message)