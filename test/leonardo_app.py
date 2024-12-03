import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PySide6.QtWebEngineCore import QWebEnginePage
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl

# class CustomWebEnginePage(QWebEnginePage):
#     def acceptNavigationRequest(self, url, nav_type, is_main_frame):
#         # Allow only navigation to the main site
#         allowed_url = QUrl("https://app.leonardo.ai/")
#         if url.host() == allowed_url.host():
#             return True
#         return False  # Block all other navigation

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the web engine view
        self.browser = QWebEngineView()

        # Set a custom web page to restrict navigation
        self.page = QWebEnginePage(self.browser)
        self.browser.setPage(self.page)

        # Load the allowed URL
        self.browser.setUrl(QUrl("https://app.leonardo.ai/"))

        # Set up the window layout
        self.setCentralWidget(self.browser)
        self.setWindowTitle("Leonardo AI App")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
