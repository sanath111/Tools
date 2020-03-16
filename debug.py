#!/usr/bin/env python2.7
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import sys
import os

import logging
from logging import *
import tempfile

# tempDir = tempfile.gettempdir()
# user = os.environ['USER']

FORMAT = "%(asctime)s : %(pathname)s : %(funcName)s - %(levelname)s - %(lineno)d - %(message)s"
basicConfig(format=FORMAT, level=INFO)
# basicConfig(filename=tempDir + os.sep + "Grantha_" + user + ".log",filemode='a', format=FORMAT, level=INFO)

# logger = logging.getLogger()
# logger.addHandler(logging.FileHandler(tempDir + os.sep + "Grantha_" + user + ".log", 'a'))

# import inspect
# def getLineInfo():
#     return (str(inspect.stack()[1][1]) + " : " + str(inspect.stack()[1][2]) + " : " + str(inspect.stack()[1][3]))
