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
import layouts
import time

try:
    from PyQt5.QtWidgets import QApplication, QFileSystemModel, QListWidgetItem
    from PyQt5 import QtCore, uic, QtGui, QtWidgets
    from PyQt5.QtCore import *
    from PyQt5.QtWidgets import *
    from PyQt5.QtGui import *
except:
    pass

# import sys
# from PyQt5.QtCore import *
# from PyQt5.QtGui import *
# # from PyQt5.QtWidget import *
#
# def main():
#     app = QApplication(sys.argv)
#     w = MyWindow()
#     w.show()
#     sys.exit(app.exec_())
#
# class MyWindow(QWidget):
#     def __init__(self, *args):
#         QWidget.__init__(self, *args)
#
#         self.la = QLabel("Press tab in this box:")
#         # self.le = MyLineEdit()
#         self.le = QKeySequenceEdit()
#         layout = QVBoxLayout()
#         layout.addWidget(self.la)
#         layout.addWidget(self.le)
#         self.setLayout(layout)
#
#     #     self.le.keyPressed.connect(self.update)
#     #
#     # def update(self, text):
#     #     self.le.setText(text)
#
# # MOD_MASK = (Qt.CTRL | Qt.ALT | Qt.SHIFT | Qt.META)
#
# # class MyLineEdit(QLineEdit):
# #     keyPressed = pyqtSignal(str)
#
#     # def keyPressEvent(self, event):
#     #     keyname = ''
#     #     key = event.key()
#     #     print (key)
#     #     # modifiers = int(event.modifiers())
#     #     # if (modifiers and modifiers & MOD_MASK == modifiers and
#     #     #     key > 0 and key != Qt.Key_Shift and key != Qt.Key_Alt and
#     #     #     key != Qt.Key_Control and key != Qt.Key_Meta):
#     #     #
#     #     #     keyname = QKeySequence(modifiers + key).toString()
#     #     #
#     #     keyname = QKeySequence(key).toString()
#     #     if key == PyQt4.QtCore.Qt.CTRL:
#     #         print("ctrl pressed")
#     #     print('event.text(): %r' % event.text())
#     #     print('event.key(): %d, %#x, %s' % (key, key, keyname))
#     #     self.keyPressed.emit(keyname)
#
# if __name__ == "__main__":
#     main()

projDir = os.sep.join(os.path.abspath(__file__).split(os.sep)[:-2])
sys.path.append(projDir)
print (projDir)
main_ui_file = os.path.join(projDir, "test", "test01.ui")

keyCombs = ['a', 'alt','alt a', 'ctrl', 'ctrl l', 'ctrl s', 'ctrl shift z', 'ctrl t', 'ctrl tab', 'ctrl z', 'd', 'e', 'enter',
            'esc', 'g', 'l', 'left', 'n', 'r', 'right', 's', 'shift', 'shift s', 't', 'tab', 'tab', 'v', 'x', 'z', '~']
keyCombs.sort()
# print (keyCombs)
# def key(self, main_ui):
#     print(main_ui.keySequenceEdit.keySequence().toString())

device = "HID 256c:006e Pad pad"

# def setOrient(main_ui,orient):
#     lay = {}
#     if orient == "left":
#         main_ui.left.show()
#         main_ui.left.setLayout(layouts.Huion())
#     if orient == "up":
#         main_ui.up.show()
#         main_ui.up.setLayout(layouts.Huion())
#     if orient == "right":
#         main_ui.right.show()
#         main_ui.right.setLayout(layouts.Huion())


def mainGui(main_ui):
    main_ui.setWindowTitle("Key Mapper")

    # qssFile = os.path.join(projDir, "styleSheet", "stylesheetTest.qss")
    # with open(qssFile, "r") as fh:
    #     main_ui.setStyleSheet(fh.read())

    # main_ui.folderName.setText(dirPath+"/")
    # main_ui.folderName.setEnabled(False)
    # main_ui.input.setText(videoName)
    # main_ui.input.setReadOnly(True)
    # main_ui.output.setToolTip("New Name for the file. Don't put extensions")
    #
    # main_ui.convertButton.clicked.connect(lambda self, main_ui = main_ui : convert(self, main_ui))
    # main_ui.keySequenceEdit.keySequenceChanged.connect(lambda self, main_ui = main_ui : key(self, main_ui))
    # button = QComboBox()
    # button.addItems(keyCombs)
    # hbox = QHBoxLayout()
    # hbox.addWidget(button)
    # main_ui.left.hide()
    # main_ui.up.hide()
    # main_ui.right.hide()

    # orient = layouts.getButtOrient(device)
    # print (orient)
    # setOrient(main_ui,orient)
    # main_ui.frame_side.setLayout(layouts.Huion())
    # main_ui.frame_up.hide()
    # main_ui.pushButton1.addItems(keyCombs)
    # main_ui.Button1.addItems(keyCombs)
    # widget = main_ui.findChild(QComboBox)
    # print (widget.objectName())
    main_ui.deviceName.setText(device)
    widgets = main_ui.findChildren(QComboBox)
    # widgets.addItems(keyCombs)
    # print (widgets)
    for widget in widgets:
        widget.addItems(keyCombs)
    main_ui.update()
    main_ui.show()
    # time.sleep(1)
    # main_ui.Button8.addItems(keyCombs)

def mainfunc():
    global app
    app = QApplication(sys.argv)
    main_ui = uic.loadUi(main_ui_file)
    mainGui(main_ui)
    sys.exit(app.exec_())

if __name__ == '__main__':
    setproctitle.setproctitle("KEY_MAPPER")
    mainfunc()
