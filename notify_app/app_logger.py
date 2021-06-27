import logging
import sys

from notify_app import config


# _log_format = config.LOG_FORMAT
_log_format = '%(asctime)s %(message)s'

logging.basicConfig(filename=config.LOG_FILENAME, level=logging.DEBUG, format=_log_format)


def get_file_handler():
    file_handler = logging.FileHandler(config.LOG_FILENAME)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(_log_format))
    return file_handler


def get_stream_handler():
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(logging.Formatter(_log_format))
    return stream_handler


def get_logger(name):
    logger = logging.getLogger(name)
    # logger.setLevel(logging.INFO)
    logger.addHandler(get_file_handler())
    logger.addHandler(get_stream_handler())
    return logger
