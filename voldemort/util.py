# -*- coding: utf-8 -*-
#
# Common utility functions
#
# @author: Sreejith K
# Created On 19th Sep 2011


import sys
import traceback
import logging
import logging.handlers


def setup_logging(path, level):
    """Setup application logging.
    """
    log_handler = logging.handlers.RotatingFileHandler(
        path,
        maxBytes=1024 * 1024,
        backupCount=2)
    root_logger = logging.getLogger('')
    root_logger.setLevel(level)
    format = '%(name)s - %(message)s'
    formatter = logging.Formatter(format)
    log_handler.setFormatter(formatter)
    root_logger.addHandler(log_handler)
    # add console logger
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('--> %(message)s')
    ch.setFormatter(formatter)
    root_logger.addHandler(ch)


def print_traceback():
    """Get the exception traceback.
    """
    exc_type, exc_value, exc_traceback = sys.exc_info()
    return ''.join(
        traceback.format_exception(
            exc_type,
            exc_value,
            exc_traceback))
