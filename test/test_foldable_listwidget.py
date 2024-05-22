import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTreeWidget, QTreeWidgetItem, QVBoxLayout

class Ui_MainWindow(QWidget):
    def __init__(self, parent=None):
        super(Ui_MainWindow, self).__init__(parent)
        self.setWindowTitle("Tree Structure with QListWidget")

        # Your list of strings
        my_list = ["Apple", "Banana", "Cherry", "Date"]

        # Create a QTreeWidget
        treeWidget = QTreeWidget()
        treeWidget.setHeaderLabels(["Items"])

        # Create parent items using the first letter of each string
        parent_items = {}
        for word in my_list:
            first_letter = word[0].upper()
            if first_letter not in parent_items:
                parent_items[first_letter] = QTreeWidgetItem(treeWidget, [first_letter])

            # Add child items (nested under parent items)
            QTreeWidgetItem(parent_items[first_letter], [word])

        # Set up the window layout
        window_layout = QVBoxLayout(self)
        window_layout.addWidget(treeWidget)
        self.setLayout(window_layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Ui_MainWindow()
    window.show()
    sys.exit(app.exec_())
