# -*- coding:utf-8 -*-
"""
setup your_logger
Copyright (c) 2017 Bee Beans Technologies Co.,Ltd.
"""
import os
from logging import Formatter, StreamHandler, getLogger

LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")


def setup_logger(logger_name, log_level=LOG_LEVEL):
    """
    returns default logger for debugging.
    for logger_name , __name__ could be used as your self filename.
    ex) LOGGER = setup_logger(__name__, DEBUG)
    ex) LOGGER = setup_logger(__name__, INFO)
    """
    your_logger = getLogger(logger_name)
    if your_logger.hasHandlers():
        print("your_logger %s already has handler" % logger_name)
        return your_logger
    logger_handler = StreamHandler()
    your_formatter = Formatter(
        "%(asctime)s,%(levelname)s,%(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )
    logger_handler.setFormatter(your_formatter)

    logger_handler.setLevel(log_level)
    your_logger.setLevel(log_level)
    your_logger.addHandler(logger_handler)
    return your_logger
