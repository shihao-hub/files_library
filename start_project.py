import sys
from contextlib import contextmanager

from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow

from ui.demo import Ui_MainWindow


# NOTE: 开发第一个基于 PyQt5 的桌面应用，必须使用两个类: QApplication 和 QWidget。都在 PyQt5.QtWidgets。


@contextmanager
def context_app():
    app = QApplication(sys.argv)
    try:
        yield
    finally:
        sys.exit(app.exec_())


if __name__ == '__main__':
    with context_app():
        w = QMainWindow()

        umw = Ui_MainWindow()
        umw.setupUi(w)
        umw.retranslateUi(w)


        w.show()
