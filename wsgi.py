# -*- coding: utf-8 -*-

from sys import path
from sys import stderr
from logging import basicConfig as loggingBasic
from settings import *


loggingBasic(stream = stderr)


path.insert(0, BASE_DIR)


from run import app as application
