#!/usr/bin/python2
# *-* coding: utf-8 *-*
__author__ = "Sanath Shetty K"
__license__ = "GPL"
__email__ = "sanathshetty111@gmail.com"

import os
import sys
# import psutil
from PyQt5 import QtGui, QtWidgets, uic, QtCore, QtSvg
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtCore import QProcess, QThread, pyqtSignal
import dbInv
# import zmq
# import socket
import debug
# import subprocess
# from Utils_Gui import *
import time
import setproctitle
# import tempfile
# import xml.dom.minidom
# import glob
import datetime
import json
# from collections import OrderedDict
# import argparse
import types

filePath = os.path.abspath(__file__)
projDir = os.sep.join(filePath.split(os.sep)[:-1])
# uiDir = os.path.join(projDir,"GUI","uiFiles")
# imageDir = os.path.join(projDir, "GUI","imageFiles")
# fileDir = os.path.join(projDir, "GUI")

# sys.path.append(uiDir)
# sys.path.append(imageDir)
# sys.path.append(fileDir)

username = os.environ['USER']

authUsers = None

currUser = username

# parser = argparse.ArgumentParser(description="Utility to repair items")
# parser.add_argument("-i","--item",dest="item",help="name of item")
# parser.add_argument("-n","--index",dest="index",help="index of tab")
# args = parser.parse_args()

class dailyReportWidget():

    db = dbInv.dbGrantha()

    def __init__(self):
        self.ui = uic.loadUi(os.path.join(projDir,"daily_report.ui"))

        # self.loadJson()
        self.ui.calendar.setMaximumDate(QtCore.QDate.currentDate())
        self.ui.calendar.clicked.connect(self.loadText)

        self.loadVars()
        self.loadUsers()
        self.loadText()
        self.center()
        self.ui.setWindowTitle('DAILY REPORT')
        self.ui.show()

        qssFile = os.path.join(projDir, "light.qss")
        with open(qssFile, "r") as sS:
            self.ui.setStyleSheet(sS.read())

    def loadVars(self):
        global authUsers
        getAuthUsers = "SELECT * FROM AUTH_USERS"
        aU = self.db.execute(getAuthUsers, dictionary=True)
        authUsers = [x['auth_users'] for x in aU]

    def loadUsers(self):
        Users = []
        getUsers = "SELECT * FROM USER"
        users = self.db.execute(getUsers, dictionary=True)
        for x in users:
            Users.append(x['user'])

        while ("" in Users):
            Users.remove("")

        layV = QtWidgets.QVBoxLayout()
        self.ui.usersFrame.setLayout(layV)

        for user in Users:
            butt = QtWidgets.QRadioButton(user)
            butt.setText(user)
            if username in authUsers:
                layV.addWidget(butt)
            else:
                if user == username:
                    butt.setEnabled(False)
                    layV.addWidget(butt)
            if user == username:
                butt.setChecked(True)

            butt.clicked.connect(lambda x, butt=butt: self.buttClick(butt))

    def buttClick(self,butt):
        global currUser
        debug.info("butt clicked!")
        currUser = butt.text()

        self.loadText()

    def loadText(self):
        date = self.ui.calendar.selectedDate().toString(QtCore.Qt.ISODate)
        dT = datetime.datetime.strptime(date, "%Y-%m-%d").strftime("%A, %b %d, %Y")
        self.ui.titleBox.setText(dT)
        self.loadJson(date)

    def loadJson(self,date):
        try:
            with open("/crap/crap.server/Sanath_Shetty/tests/daily_reports/"+currUser+".json") as f:
                data = json.load(f)
                try:
                    text = (data['entries'][date]['text'])
                    self.ui.textBox.setText(text)
                except:
                    debug.info(str(sys.exc_info()))
                    self.ui.textBox.clear()
        except:
            debug.info(str(sys.exc_info()))


    def center(self):
        qr = self.ui.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.ui.move(qr.topLeft())


if __name__ == '__main__':
    setproctitle.setproctitle("DAILY_REPORT")
    app = QtWidgets.QApplication(sys.argv)
    window = dailyReportWidget()
    sys.exit(app.exec_())

