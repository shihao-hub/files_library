import sys

from PyQt5 import QtWidgets, QtCore, QtSql  # , QtGui, QtNfc, QtQml, QtSvg, QtXml
from PyQt5 import QtWebEngineWidgets

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    browser_widget = QtWidgets.QWidget()
    self = browser_widget
    self.resize(800, 800)

    self.vbox_layout = QtWidgets.QVBoxLayout()
    self.setLayout(self.vbox_layout)

    self.browser = QtWebEngineWidgets.QWebEngineView(self)
    self.browser.load(QtCore.QUrl(r"http://127.0.0.1:1060/"))

    self.vbox_layout.addWidget(self.browser)

    browser_widget.show()
    sys.exit(app.exec_())
