# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'demo.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(804, 593)
        MainWindow.setFocusPolicy(QtCore.Qt.NoFocus)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(340, 30, 121, 241))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.pushButton_3 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout.addWidget(self.pushButton_3)
        self.pushButton_5 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.pushButton_5.setFont(font)
        self.pushButton_5.setObjectName("pushButton_5")
        self.verticalLayout.addWidget(self.pushButton_5)
        self.pushButton_4 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.pushButton_4.setFont(font)
        self.pushButton_4.setObjectName("pushButton_4")
        self.verticalLayout.addWidget(self.pushButton_4)
        self.pushButton_2 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout.addWidget(self.pushButton_2)
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setGeometry(QtCore.QRect(10, 30, 321, 241))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.plainTextEdit.setFont(font)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.plainTextEdit_2 = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_2.setGeometry(QtCore.QRect(470, 30, 321, 241))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.plainTextEdit_2.setFont(font)
        self.plainTextEdit_2.setObjectName("plainTextEdit_2")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 510, 801, 31))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(7)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_4 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_4.setText("")
        self.label_4.setObjectName("label_4")
        self.horizontalLayout.addWidget(self.label_4)
        self.label_3 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label.setText("")
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(9)
        self.label_2.setFont(font)
        self.label_2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.plainTextEdit_3 = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_3.setGeometry(QtCore.QRect(10, 340, 321, 161))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.plainTextEdit_3.setFont(font)
        self.plainTextEdit_3.setObjectName("plainTextEdit_3")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(20, 10, 72, 15))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(480, 10, 72, 15))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.label_6.setFont(font)
        self.label_6.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(20, 320, 72, 15))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.label_7.setFont(font)
        self.label_7.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_7.setObjectName("label_7")
        self.plainTextEdit.raise_()
        self.plainTextEdit_2.raise_()
        self.verticalLayoutWidget.raise_()
        self.horizontalLayoutWidget.raise_()
        self.plainTextEdit_3.raise_()
        self.label_5.raise_()
        self.label_6.raise_()
        self.label_7.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 804, 26))
        self.menubar.setObjectName("menubar")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuPaste = QtWidgets.QMenu(self.menuEdit)
        self.menuPaste.setObjectName("menuPaste")
        self.menuTools = QtWidgets.QMenu(self.menubar)
        self.menuTools.setObjectName("menuTools")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionText_Collation = QtWidgets.QAction(MainWindow)
        self.actionText_Collation.setObjectName("actionText_Collation")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionopen = QtWidgets.QAction(MainWindow)
        self.actionopen.setObjectName("actionopen")
        self.actionText_Remove_Dupl = QtWidgets.QAction(MainWindow)
        self.actionText_Remove_Dupl.setObjectName("actionText_Remove_Dupl")
        self.actionShow_Calendar = QtWidgets.QAction(MainWindow)
        self.actionShow_Calendar.setObjectName("actionShow_Calendar")
        self.actionUndo_Ctrl_Z = QtWidgets.QAction(MainWindow)
        self.actionUndo_Ctrl_Z.setObjectName("actionUndo_Ctrl_Z")
        self.actionCut_Ctrl_X = QtWidgets.QAction(MainWindow)
        self.actionCut_Ctrl_X.setObjectName("actionCut_Ctrl_X")
        self.actionCopy_Ctrl_C = QtWidgets.QAction(MainWindow)
        self.actionCopy_Ctrl_C.setObjectName("actionCopy_Ctrl_C")
        self.actionPaste_2 = QtWidgets.QAction(MainWindow)
        self.actionPaste_2.setObjectName("actionPaste_2")
        self.actionPaste_as_Plain_Text_Ctrl_Alt_Shift_V = QtWidgets.QAction(MainWindow)
        self.actionPaste_as_Plain_Text_Ctrl_Alt_Shift_V.setObjectName("actionPaste_as_Plain_Text_Ctrl_Alt_Shift_V")
        self.actionDelete_Delete = QtWidgets.QAction(MainWindow)
        self.actionDelete_Delete.setObjectName("actionDelete_Delete")
        self.menuPaste.addAction(self.actionPaste_2)
        self.menuPaste.addAction(self.actionPaste_as_Plain_Text_Ctrl_Alt_Shift_V)
        self.menuEdit.addAction(self.actionUndo_Ctrl_Z)
        self.menuEdit.addAction(self.actionCut_Ctrl_X)
        self.menuEdit.addAction(self.actionCopy_Ctrl_C)
        self.menuEdit.addAction(self.menuPaste.menuAction())
        self.menuEdit.addAction(self.actionDelete_Delete)
        self.menuTools.addAction(self.actionText_Collation)
        self.menuTools.addAction(self.actionText_Remove_Dupl)
        self.menuTools.addAction(self.actionShow_Calendar)
        self.menuHelp.addAction(self.actionAbout)
        self.menuFile.addAction(self.actionopen)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "文本整理"))
        self.pushButton_3.setText(_translate("MainWindow", "文本去重"))
        self.pushButton_5.setText(_translate("MainWindow", "PushButton"))
        self.pushButton_4.setText(_translate("MainWindow", "PushButton"))
        self.pushButton_2.setText(_translate("MainWindow", "PushButton"))
        self.label_2.setText(_translate("MainWindow", "TextLabel"))
        self.label_5.setText(_translate("MainWindow", "输入"))
        self.label_6.setText(_translate("MainWindow", "输出"))
        self.label_7.setText(_translate("MainWindow", "日志"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.menuPaste.setTitle(_translate("MainWindow", "Paste"))
        self.menuTools.setTitle(_translate("MainWindow", "Tools"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionText_Collation.setText(_translate("MainWindow", "Text Collation"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionopen.setText(_translate("MainWindow", "Open"))
        self.actionText_Remove_Dupl.setText(_translate("MainWindow", "Text Remove Duplicate"))
        self.actionShow_Calendar.setText(_translate("MainWindow", "Show Calendar"))
        self.actionUndo_Ctrl_Z.setText(_translate("MainWindow", "Undo (Ctrl+Z )"))
        self.actionCut_Ctrl_X.setText(_translate("MainWindow", "Cut (Ctrl+X)"))
        self.actionCopy_Ctrl_C.setText(_translate("MainWindow", "Copy (Ctrl+C)"))
        self.actionPaste_2.setText(_translate("MainWindow", "Paste (Ctrl+V)"))
        self.actionPaste_as_Plain_Text_Ctrl_Alt_Shift_V.setText(_translate("MainWindow", "Paste as Plain Text (Ctrl+Alt+Shift+V)"))
        self.actionDelete_Delete.setText(_translate("MainWindow", "Delete (Delete)"))
