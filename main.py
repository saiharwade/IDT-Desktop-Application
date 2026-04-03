import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget

from pages.login_page import LoginPage
from pages.home_page import HomePage
from pages.history_page import HistoryPage
from pages.result_page import ResultPage
from pages.compare_page import ComparePage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("IDT Desktop Application")
        self.setGeometry(100, 100, 1200, 700)

        self.stack = QStackedWidget()

        self.login_page = LoginPage()
        self.home_page = HomePage(self.stack)
        self.history_page = HistoryPage()
        self.result_page = ResultPage()
        self.compare_page = ComparePage(self.stack)

        self.stack.addWidget(self.login_page)    # index 0
        self.stack.addWidget(self.home_page)     # index 1
        self.stack.addWidget(self.history_page)  # index 2
        self.stack.addWidget(self.result_page)   # index 3
        self.stack.addWidget(self.compare_page)  # index 4

        self.setCentralWidget(self.stack)
        self.stack.setCurrentIndex(0)

        self.login_page.login_button.clicked.connect(self.show_home_page)

    def show_home_page(self):
        self.stack.setCurrentIndex(1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec_())