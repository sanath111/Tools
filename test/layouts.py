#!/usr/bin/python2
# *-* coding: utf-8 *-*
__author__ = "Sanath Shetty K"
__license__ = "GPL"
__email__ = "sanathshetty111@gmail.com"

# import debug
# import argparse
# import glob
import os
import sys
import setproctitle
# import subprocess

try:
    from PyQt5.QtWidgets import QApplication, QFileSystemModel, QListWidgetItem
    from PyQt5 import QtCore, uic, QtGui, QtWidgets
    from PyQt5.QtCore import *
    from PyQt5.QtWidgets import *
    from PyQt5.QtGui import *
except:
    pass

projDir = os.sep.join(os.path.abspath(__file__).split(os.sep)[:-2])
sys.path.append(projDir)
print (projDir)

def getButtOrient(device):
    deviceButtOrient = {"HID 256c:006e Pad pad":('left',),"Wacom Cintiq 22HD Pad pad":('left', 'right'),"Wacom Intuos PT S Pad pad":('up',)}
    if device in deviceButtOrient.keys():
        return deviceButtOrient[device]

def Huion():
    # buttons = {}
    # frame = QFrame()
    vbox1 = QVBoxLayout()
    # vbox2 = QVBoxLayout()
    # hbox1 =QHBoxLayout()
    Abutton = QComboBox()
    Bbutton = QComboBox()
    Cbutton = QComboBox()
    Dbutton = QComboBox()
    Ebutton = QComboBox()
    Fbutton = QComboBox()
    Gbutton = QComboBox()
    Hbutton = QComboBox()

    butts = [Abutton,Bbutton,Cbutton,Dbutton,Ebutton,Fbutton,Gbutton,Hbutton]
    i =1
    for b in butts:
        b.setObjectName("Button{}".format(i))
        # print ("pushButton{}".format(i))
        print (b.objectName())
        vbox1.addWidget(b)
        i+=1

    # buttons = {"abutton" = Abutton, "bbutton" = Bbutton}
    # print (buttons)
    # for k in buttons.keys():
    #     vbox1.addWidget(k)
    # frame.setLayout(vbox1)
    # vbox2.addWidget(frame)
    # hbox = QHBoxLayout()
    # hbox.addWidget(button)
    horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

    # hbox1.addWidget(vbox1)
    # hbox1.addWidget(horizontalSpacer)
    return vbox1
