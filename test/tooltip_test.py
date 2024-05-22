from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QApplication, QToolTip

class CustomTooltipFilter(QtCore.QObject):
    def __init__(self, widget):
        super(CustomTooltipFilter, self).__init__(widget)
        self.widget = widget

    def eventFilter(self, obj, event):
        if obj == self.widget and event.type() == QtCore.QEvent.Enter:
            # Calculate tooltip position (here, 10px below and to the right)
            pos = event.globalPos() + QPoint(10, 10)
            # Set tooltip text and position
            QToolTip.showText(pos, self.widget.toolTip())
        return super(CustomTooltipFilter, self).eventFilter(obj, event)

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super(MyWidget, self).__init__()
        self.layout = QtWidgets.QVBoxLayout(self)

        # Create list widget and add items
        self.listWidget = QtWidgets.QListWidget()
        self.listWidget.addItem("Item 1 - This is a tooltip")
        self.listWidget.addItem("Item 2 - Another tooltip!")
        self.listWidget.addItem("Item 3 - You can customize tooltips!")

        self.layout.addWidget(self.listWidget)

        self.setFont(QFont("Arial", 10))
        self.setToolTip("This is a custom tooltip!")
        # Install event filter
        self.filter = CustomTooltipFilter(self)
        self.installEventFilter(self.filter)

if __name__ == '__main__':
    app = QApplication([])
    widget = MyWidget()
    widget.show()
    app.exec_()
