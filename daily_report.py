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
currUserDict = {"entries": {}}

jsonPath = "/blueprod/STOR2/stor2/grantha/share/dailyReports/"

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
        self.ui.saveButton.clicked.connect(self.saveReport)

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

        # cal = CalendarWidget()
        # cal.setMaximumDate(QtCore.QDate.currentDate())
        # layV.addWidget(cal)

    def buttClick(self,butt):
        global currUser
        # debug.info("butt clicked!")
        currUser = butt.text()
        self.loadText()

    def loadText(self):
        date = self.ui.calendar.selectedDate().toString(QtCore.Qt.ISODate)
        dT = datetime.datetime.strptime(date, "%Y-%m-%d").strftime("%A, %b %d, %Y")
        self.ui.titleBox.setText(dT)
        self.loadJson(date)

    def loadJson(self,date):
        global currUser
        global currUserDict
        try:
            f = open(jsonPath+currUser+".json")
            data = json.load(f)
            # debug.info(data)
            currUserDict = data
            try:
                text = (data['entries'][date]['text'])
                self.ui.textBox.setText(text)
            except (KeyError):
                debug.info("key error")
                self.ui.textBox.clear()
            except:
                debug.info(str(sys.exc_info()))
                self.ui.textBox.clear()
        except (IOError):
            debug.info("io error")
            with open(jsonPath+currUser+".json", 'w') as outfile:
                json.dump(currUserDict, outfile, sort_keys=True, indent=4)

        except:
            debug.info(str(sys.exc_info()))

    def saveReport(self):
        global currUser
        global currUserDict
        date = self.ui.calendar.selectedDate().toString(QtCore.Qt.ISODate)
        dT = str(datetime.datetime.strptime(date, "%Y-%m-%d").date())
        debug.info(dT)
        # debug.info(date)
        text = self.ui.textBox.toPlainText()
        # debug.info(text)
        if text:
            debug.info("saving")
            currUserDict['entries'][dT] = {"text" : text}
            # debug.info(currUserDict)
            with open(jsonPath+currUser+".json", 'w') as outfile:
                json.dump(currUserDict, outfile, sort_keys=True, indent=4)


    def center(self):
        qr = self.ui.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.ui.move(qr.topLeft())

# class CalendarWidget(QtWidgets.QCalendarWidget):
#     def __init__(self, parent=None):
#         super(CalendarWidget, self).__init__(parent,
#             verticalHeaderFormat=QtWidgets.QCalendarWidget.NoVerticalHeader,gridVisible=False)
#
#         for d in (QtCore.Qt.Saturday, QtCore.Qt.Sunday,):
#             fmt = self.weekdayTextFormat(d)
#             fmt.setForeground(QtCore.Qt.darkGray)
#             self.setWeekdayTextFormat(d, fmt)
#
#     def paintCell(self, painter, rect, date):
#         if date == self.selectedDate():
#             painter.save()
#             painter.fillRect(rect, QtGui.QColor("white"))
#             painter.setPen(QtCore.Qt.NoPen)
#             painter.setBrush(QtGui.QColor("#76797C"))
#             r = QtCore.QRect(QtCore.QPoint(), min(rect.width(), rect.height())*QtCore.QSize(1, 1))
#             r.moveCenter(rect.center())
#             painter.drawEllipse(r)
#             painter.setPen(QtGui.QPen(QtGui.QColor("white")))
#             painter.drawText(rect, QtCore.Qt.AlignCenter, str(date.day()))
#             painter.restore()
#         else:
#             super(CalendarWidget, self).paintCell(painter, rect, date)

if __name__ == '__main__':
    setproctitle.setproctitle("DAILY_REPORT")
    app = QtWidgets.QApplication(sys.argv)
    window = dailyReportWidget()
    sys.exit(app.exec_())

