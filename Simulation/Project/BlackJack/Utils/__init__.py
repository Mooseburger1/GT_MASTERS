from os import sys, path

sys.path.append(path.dirname(__file__))
from CustomLogger import makeLogger
from utils import strategy_parser
from dashboard import Dapp, open_browser