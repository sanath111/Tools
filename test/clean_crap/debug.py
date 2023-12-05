#!/usr/bin/env python2
#-*- coding: utf-8 -*-

import os

from logging import *
import tempfile

tempDir = tempfile.gettempdir()
user = os.environ['USER']

FORMAT = "%(asctime)s : %(pathname)s : %(funcName)s - %(levelname)s - %(lineno)d - %(message)s"
basicConfig(filename=tempDir + os.sep + "Clean_Crap_" + user + ".log",filemode='a', format=FORMAT, level=INFO)
