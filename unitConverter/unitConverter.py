#!/usr/bin/python2
# *-* coding: utf-8 *-*
__author__ = "Sanath Shetty K"
__license__ = "GPL"
__email__ = "sanathshetty111@gmail.com"


import debug
import argparse
import glob
import os
import sys
import re
import pexpect
import setproctitle
import subprocess
import shlex
from collections import OrderedDict
import time
import threading
import traceback
import pathlib

from PyQt5.QtWidgets import QApplication, QFileSystemModel, QListWidgetItem
from PyQt5 import QtCore, uic, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

projDir = os.sep.join(os.path.abspath(__file__).split(os.sep)[:-1])
sys.path.append(projDir)

main_ui_file = os.path.join(projDir, "unitConverter.ui")
debug.info(main_ui_file)


def mainGui(main_ui):
    main_ui.setWindowTitle("UNIT CONVERTER")

    # sS = open(os.path.join(projDir, "styleSheets", "dark.qss"), "r")
    # main_ui.setStyleSheet(sS.read())
    # sS.close()

    main_ui.box1.textChanged.connect(lambda self, main_ui=main_ui: convertUnits(self, main_ui))
    main_ui.comboBox1.currentIndexChanged.connect(lambda self, main_ui=main_ui: convertUnits(self, main_ui))
    # main_ui.meterBox.textChanged.connect(lambda self, main_ui=main_ui: convertToFeet(self, main_ui))
    # main_ui.feetBox.textChanged.connect(lambda self, main_ui=main_ui: convertToMeter(self, main_ui))

    main_ui.show()
    main_ui.update()

    qtRectangle = main_ui.frameGeometry()
    centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
    qtRectangle.moveCenter(centerPoint)
    main_ui.move(qtRectangle.topLeft())


def convertUnits(self, main_ui):
    u1 = main_ui.box1.text()
    debug.info(u1)
    unit1 = main_ui.comboBox1.currentText()
    debug.info(unit1)
    # unit2 = main_ui.comboBox2.currentText()
    # debug.info(unit2)

    if u1:
        if unit1 == "meter":
            try:
                main_ui.label.setText("Ft")
                u2 = float(u1) * 3.28084
                debug.info(u2)
                main_ui.box2.setText(str(u2))
            except:
                debug.info("Enter numbers only")

        if unit1 == "foot":
            try:
                main_ui.label.setText("m")
                u2 = float(u1) * 0.3048
                debug.info(u2)
                main_ui.box2.setText(str(u2))
            except:
                debug.info("Enter numbers only")
    else:
        main_ui.box2.clear()


def closeEvent(self, main_ui):
    main_ui.close()
    sys.exit()


def mainFunc():
    global app
    app = QApplication(sys.argv)
    main_ui = uic.loadUi(main_ui_file)
    mainGui(main_ui)
    sys.exit(app.exec_())


if __name__ == '__main__':
    setproctitle.setproctitle("UNIT_CONVERTER")
    mainFunc()
