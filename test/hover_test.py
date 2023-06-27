# import sys
# from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout, QCheckBox, QLabel, QDesktopWidget
# from PyQt5.QtCore import Qt, QEvent, QPoint


# class CheckBoxWidget(QWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint)
#         # self.setAttribute(Qt.WA_TranslucentBackground)
#         self.installEventFilter(self)

#         layout = QVBoxLayout()
#         label = QLabel("Checkbox Widget")
#         layout.addWidget(label)

#         checkbox = QCheckBox("Check me!")
#         layout.addWidget(checkbox)

#         self.setLayout(layout)

#     def eventFilter(self, obj, event):
#         if event.type() == QEvent.Leave:
#             self.close()
#             return True
#         return super().eventFilter(obj, event)


# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()

#         self.setWindowTitle("Main Window")
#         self.setFixedSize(300, 200)

#         button = QPushButton("Open CheckBox Widget", self)
#         button.move(100, 80)
#         button.clicked.connect(self.open_checkbox_widget)

#     def open_checkbox_widget(self):
#         checkbox_widget = CheckBoxWidget(self)
#         position = self.mapToGlobal(QPoint(0, 0))
#         checkbox_widget.move(position.x() + 150, position.y() + 100)
#         checkbox_widget.show()


# if __name__ == "__main__":
#     app = QApplication(sys.argv)

#     main_window = MainWindow()
#     main_window.show()

#     sys.exit(app.exec_())




from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QCheckBox, QVBoxLayout, QFrame
from PyQt5.QtCore import Qt, QEvent

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 300, 220)
        self.setWindowTitle('Checkbox')

        self.btn = QPushButton('Show popup', self)
        self.btn.move(20, 20)
        self.btn.clicked.connect(self.showPopup)

        self.popup = QWidget(self)
        self.popup.setGeometry(20, 50, 100, 100)
        self.popup.hide()
        self.popup.setWindowFlags(Qt.Popup)

        layout = QVBoxLayout()
        frame = QFrame()
        frame.setFrameShape(QFrame.Box)
        layout.addWidget(frame)

        self.checkbox = QCheckBox('Checkbox', frame)
        self.checkbox.move(20, 20)

        self.popup.setLayout(layout)

    def showPopup(self):
        if not self.popup.isVisible():
            pos = self.mapToGlobal(self.btn.pos())
            x = pos.x() + self.btn.width()
            y = pos.y()
            self.popup.move(x, y)
            self.popup.show()
            self.popup.setFocus(Qt.PopupFocusReason)
            self.popup.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Leave:
            obj.hide()
            return True
        return super().eventFilter(obj, event)

if __name__ == '__main__':
    app = QApplication([])
    ex = Example()
    ex.show()
    app.exec_()
