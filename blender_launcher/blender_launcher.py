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
# import pyperclip
import time
import threading
import traceback
import pathlib
import json
from PIL import Image
from multiprocessing import Pool
from bs4 import BeautifulSoup
import urllib2
import re
from collections import OrderedDict

from PyQt5.QtWidgets import QApplication, QFileSystemModel, QListWidgetItem
from PyQt5 import QtCore, uic, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


projDir = os.sep.join(os.path.abspath(__file__).split(os.sep)[:-1])
sys.path.append(projDir)

rootDir = "/"
homeDir = os.path.expanduser("~")
assDir = homeDir + "/Documents/blender_launcher/"
if os.path.exists(assDir):
    pass
else:
    os.mkdir(assDir)

main_ui_file = os.path.join(projDir, "blender_launcher.ui")
debug.info(main_ui_file)


# confFile = homeDir+os.sep+".config"+os.sep+"files.json"



class WorkerSignals(QtCore.QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)


class Worker(QtCore.QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()
        self.kwargs['progress_callback'] = self.signals.progress

    @pyqtSlot()
    def run(self):
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)
        finally:
            self.signals.finished.emit()



class blenderLauncherWidget():
    def __init__(self):
        global listIcon
        global iconsIcon

        self.threadpool = QtCore.QThreadPool()

        self.main_ui = uic.loadUi(main_ui_file)
        self.main_ui.setWindowTitle("FILES")

        sS = open(os.path.join(projDir, "dark.qss"), "r")
        self.main_ui.setStyleSheet(sS.read())
        sS.close()

        self.initLoad()

        self.main_ui.show()
        self.main_ui.update()

        qtRectangle = self.main_ui.frameGeometry()
        centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.main_ui.move(qtRectangle.topLeft())


    def initLoad(self):
        self.loadVersions(self.main_ui.listWidget_LTS_2_9, "Blender2.93")
        self.loadVersions(self.main_ui.listWidget_LTS_2_8, "Blender2.83")


    def loadVersions(self, ui, ver):
        ui.clear()

        build_str = "https://download.blender.org/release/"+ver+"/"

        htmlPage = urllib2.urlopen(build_str)
        soup = BeautifulSoup(htmlPage, 'html.parser')

        links = OrderedDict()
        for link in soup.findAll('a', attrs={'href': re.compile("(?=.*linux)(?=.*x64)(?=.*.tar.xz)")}):
            downloadLabel = link.get('href')
            downloadLink = build_str+downloadLabel
            links[str(downloadLabel)] = str(downloadLink)

        if links:
            for key in links:

                downloadButt = QtWidgets.QPushButton()
                versionLabel = QtWidgets.QLabel()

                downloadButt.setMaximumWidth(200)

                if os.path.exists(assDir+key.strip(".tar.xz")):
                    downloadButt.setText("Launch")
                    downloadButt.clicked.connect(lambda x, path=assDir+key.strip(".tar.xz"): self.launchVersion(path))
                else:
                    downloadButt.setText("Download")
                    downloadButt.clicked.connect(lambda x, link=links[key], name=key: self.downloadVersion(link,name))

                versionLabel.setText(str(key))


                itemWidget = QtWidgets.QWidget()
                hl = QtWidgets.QHBoxLayout()
                itemWidget.setLayout(hl)
                hl.addWidget(downloadButt)
                hl.addWidget(versionLabel)

                item = QListWidgetItemSort()
                item.setSizeHint(itemWidget.sizeHint() + QtCore.QSize(10, 10))
                ui.addItem(item)
                ui.setItemWidget(item, itemWidget)



    def downloadVersion(self,link,name):
        downloadWorker = Worker(self.download,link,name)
        downloadWorker.signals.finished.connect(self.initLoad)
        self.threadpool.start(downloadWorker)


    def download(self,link,name,progress_callback):
        downCmd = "aria2c -c -s 10 -x 10 -d " + assDir+ " " + link
        debug.info(downCmd)
        subprocess.call(shlex.split(downCmd))
        untarCmd = "tar -xvf " + assDir + name + " -C " + assDir
        debug.info(untarCmd)
        subprocess.call(shlex.split(untarCmd))


    def launchVersion(self,path):
        launchWorker = Worker(self.launch,path)
        self.threadpool.start(launchWorker)


    def launch(self,path,progress_callback):
        openCmd = path+"/blender"
        debug.info(openCmd)
        subprocess.call(shlex.split(openCmd))


    # def messages(self,color,msg):
    #     self.main_ui.messages.setStyleSheet("color: %s" %color)
    #     self.main_ui.messages.setText("%s"%msg)
    #
    #
    # def setStyle(self,ui):
    #     sS = open(os.path.join(projDir, "styleSheets", "dark.qss"), "r")
    #     ui.setStyleSheet(sS.read())
    #     sS.close()


class QListWidgetItemSort(QtWidgets.QListWidgetItem):
    def __lt__(self, other):
        return self.data(QtCore.Qt.UserRole) < other.data(QtCore.Qt.UserRole)

    def __ge__(self, other):
        return self.data(QtCore.Qt.UserRole) > other.data(QtCore.Qt.UserRole)


if __name__ == '__main__':
    setproctitle.setproctitle("FILES")
    app = QtWidgets.QApplication(sys.argv)
    window = blenderLauncherWidget()
    sys.exit(app.exec_())
