import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidget

from books.books import Ui_MainWindow
from books.start_tab_control import Ui_StartTabControl


class StartTabControl(QtWidgets.QWidget, Ui_StartTabControl):
    tab_control_name = "Start Tab Control Test"

    def __init__(self):
        super().__init__()
        self.setupUi(self)


class BooksMainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.tab_widget.addTab(StartTabControl(), StartTabControl.tab_control_name)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = BooksMainWindow()
    w.show()
    sys.exit(app.exec())
