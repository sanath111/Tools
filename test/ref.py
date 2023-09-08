import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class PureRef(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PureRef")
        self.resize(600, 400)

        self.images = []

        self.add_image_button = QPushButton("Add Image")
        self.add_image_button.clicked.connect(self.add_image)
        self.add_image_button.setGeometry(10, 10, 100, 30)

        self.image_label = QLabel()
        self.image_label.setGeometry(10, 50, 500, 300)

    def add_image(self):
        file_path = QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.jpg *.png)")[0]
        image = QImage(file_path)
        image = image.scaled(self.image_label.size(), Qt.KeepAspectRatio)
        self.image_label.setPixmap(QPixmap.fromImage(image))
        self.images.append(image)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PureRef()
    window.show()
    app.exec_()
