import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow


class Calculator(object):
    def __init__(self, main_window):
        self.grid_layout = None
        self.grid_layout_widget = None
        self.result_line_edit = None

        self.font = QtGui.QFont()
        self.font.setFamily("微软雅黑")

        self.main_window = main_window

        self.setup()

    def on_button_clicked(self):
        button = self.main_window.sender()
        text = button.text()
        if text == "=":
            try:
                result = str(eval(self.result_line_edit.text()))
            except (SyntaxError, ZeroDivisionError):
                result = "Error"
            self.result_line_edit.setText(result)
        else:
            self.result_line_edit.setText(self.result_line_edit.text() + text)

    def _add_button(self, text, row, column, row_span, column_span, on_clicked=None):
        button = QtWidgets.QPushButton(self.grid_layout_widget)
        button.setText(text)
        button.setMaximumSize(QtCore.QSize(50, 16777215))
        button.setFont(self.font)
        button.setFlat(False)
        button.setObjectName("button")
        button.clicked.connect(on_clicked or (lambda: self.on_button_clicked()))
        self.grid_layout.addWidget(button, row, column, row_span, column_span)

    def setup(self):
        self.main_window.setObjectName("form")
        self.main_window.resize(321, 292)
        self.main_window.setWindowFlags(self.main_window.windowFlags() & ~Qt.WindowMaximizeButtonHint)
        self.main_window.setFocusPolicy(QtCore.Qt.NoFocus)

        # self.centralwidget = QtWidgets.QWidget(self.main_window)
        # self.centralwidget.setObjectName("centralwidget")

        self.grid_layout_widget = QtWidgets.QWidget(self.main_window)
        self.grid_layout_widget.setGeometry(QtCore.QRect(0, 0, 321, 291))
        self.grid_layout_widget.setObjectName("grid_layout_widget")

        self.grid_layout = QtWidgets.QGridLayout(self.grid_layout_widget)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setObjectName("grid_layout")

        self.result_line_edit = QtWidgets.QLineEdit(self.grid_layout_widget)
        self.result_line_edit.setFont(self.font)
        self.result_line_edit.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.result_line_edit.setReadOnly(True)
        self.result_line_edit.setClearButtonEnabled(False)
        self.result_line_edit.setObjectName("result_line_edit")
        self.grid_layout.addWidget(self.result_line_edit, 0, 0, 1, 4)

        buttons_text = [
            ["", "", "", "bsp"],
            ["7", "8", "9", "/"],
            ["4", "5", "6", "*"],
            ["1", "2", "3", "-"],
            ["0", ".", "=", "+"]
        ]
        for i in range(0, len(buttons_text)):
            for j in range(0, len(buttons_text[0])):
                if buttons_text[i][j] == "bsp":
                    self._add_button(buttons_text[i][j], i + 1, j, 1, 1,
                                     lambda: self.result_line_edit.setText(self.result_line_edit.text()[:-2]))
                else:
                    self._add_button(buttons_text[i][j], i + 1, j, 1, 1)

        QtCore.QMetaObject.connectSlotsByName(self.main_window)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = QMainWindow()
    Calculator(w)
    w.show()
    sys.exit(app.exec_())
