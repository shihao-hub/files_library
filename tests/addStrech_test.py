import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget

from PyQt5 import QtWidgets, QtCore

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = QWidget()
    # w.setGeometry(QtCore.QRect(0, 0, 500, 500))
    w.hbox_layout = QtWidgets.QHBoxLayout()

    w.hbox_layout.addStretch(1)

    btn = QtWidgets.QPushButton(w)
    btn.setText("1")
    w.hbox_layout.addWidget(btn)

    w.hbox_layout.addStretch(1)

    btn = QtWidgets.QPushButton(w)
    btn.setText("2")
    w.hbox_layout.addWidget(btn)

    w.hbox_layout.addStretch(1)

    btn = QtWidgets.QPushButton(w)
    btn.setText("3")
    w.hbox_layout.addWidget(btn)

    w.hbox_layout.addStretch(1)
    w.setLayout(w.hbox_layout)

    w.show()
    sys.exit(app.exec_())
