import sys

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QTableWidget

# from books.books import Ui_MainWindow
from books.test_ui import Ui_MainWindow
from books.start_tab_control import Ui_StartTabControl


class CustomDockWidget(QtWidgets.QDockWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _resize_based_on_scale(self, size, old_size, src_size):
        # 小于零代表刚刚启动，呃，为什么刚刚启动小于 0 ？
        if old_size.width() < 0:
            return src_size
        w_scale = size.width() / old_size.width()
        h_scale = size.height() / old_size.height()
        print(w_scale, h_scale)
        return QtCore.QSize(src_size.width() * w_scale, src_size.height() * h_scale)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        for child in self.findChildren(QtWidgets.QWidget):
            child.resize(self._resize_based_on_scale(
                event.size(),
                event.oldSize(),
                child.size()
            ))


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

        if self.dockWidget_2:
            # 可以实现最小值，但是... 拉伸的时候变化比例就不对了 ...
            # 子控件根据拉伸变化大小，好像只用比例不太对。。。哎呀，桌面开发好麻烦，怎么办...
            #   感觉只能写出凑活的，不能那么完美呀... 唉...
            # self.dockWidget_2.setMinimumWidth(self.size().width()/4.5)
            print(self.dockWidget_2.size())


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = BooksMainWindow()
    w.show()
    sys.exit(app.exec())
