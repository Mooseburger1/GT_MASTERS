import logging
import os
import sys
from colorlog import ColoredFormatter


def makeLogger(name):
    ############### Logging Configuration ###############
    streamFormatter = "%(asctime)3s  %(log_color)s%(levelname)-3s%(reset)s %(white)s | %(message)s%(reset)s"
    streamFormatter = ColoredFormatter(streamFormatter)

    #register logging stream
    streamLogger = logging.getLogger(name)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(streamFormatter)
    consoleHandler.setLevel(logging.INFO)

    streamLogger.addHandler(consoleHandler)
    streamLogger.setLevel(logging.INFO)

    return streamLogger