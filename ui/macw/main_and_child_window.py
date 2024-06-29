import sys

from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication
from PyQt5 import QtCore

from ui.macw.macw_window import Ui_MainWindow
from ui.macw.macw_form import Ui_Form


class Child(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class Main(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 此处可以用单例惰性模型的
        self.child_form = Child()
        self.add_child_window_flag = 1
        self.add_child_window.triggered.connect(self.on_add_child_window_triggered)

        # self.browser = QWebEngineView()
        # self.browser.load(QUrl("https://www.dmla5.com/play/8202-1-2.html"))
        # self.setCentralWidget(self.browser)

    def on_add_child_window_triggered(self):
        self.gridLayout.addWidget(self.child_form)
        if self.add_child_window_flag == 1:
            self.child_form.show()
            self.add_child_window_flag = 0
        else:
            self.child_form.hide()
            self.add_child_window_flag = 1


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # w = Main()
    # w.show()
    c = Child()
    c.show()
    sys.exit(app.exec_())
