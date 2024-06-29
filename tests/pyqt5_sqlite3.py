import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel


def test_open_database_and_query_exec():
    app = QtWidgets.QApplication(sys.argv)

    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName(r"db.pyqt5_sqlite3")
    print("db.open...")
    if not db.open():
        raise Exception("sqlite3 数据库打开失败")

    # 这些操作显然不应该在这里执行吧，MVC
    query = QSqlQuery()
    commands = [
        # "create table people(id int primary key ,name varchar(20),address varchar(30))",
        "insert into people values(3,'zhangsan','shanghai2')",
        "insert into people values(4,'lisi','anhui2')",
    ]
    for e in commands:
        query.exec_(e)
    db.close()

    sys.exit(app.exec_())


def test_QSqlTableModel_and_QTableView():
    app = QtWidgets.QApplication(sys.argv)

    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName(r"db.pyqt5_sqlite3")

    model = QSqlTableModel()
    model.setTable("people")
    model.setEditStrategy(QSqlTableModel.OnManualSubmit)
    model.select()
    model.setHeaderData(0, Qt.Horizontal, "ID")
    model.setHeaderData(1, Qt.Horizontal, "name")
    model.setHeaderData(2, Qt.Horizontal, "address")

    dlg = QtWidgets.QDialog()
    dlg.resize(430, 450)

    def on_add_button_clicked():
        model.insertRows(model.rowCount(), 1)

    def on_delete_button_clicked():
        model.removeRow(dlg.table_view.currentIndex().row())

    dlg.table_view = QtWidgets.QTableView(dlg)
    dlg.table_view.setModel(model)
    dlg.table_view.setWindowTitle("Table View (View 1)")

    dlg.add_button = QtWidgets.QPushButton(dlg)
    dlg.add_button.setText("添加一行")
    dlg.add_button.clicked.connect(on_add_button_clicked)

    dlg.delete_button = QtWidgets.QPushButton(dlg)
    dlg.delete_button.setText("删除一行")
    dlg.delete_button.clicked.connect(on_delete_button_clicked)

    vbox_layout = QtWidgets.QVBoxLayout()
    vbox_layout.addWidget(dlg.table_view)
    vbox_layout.addWidget(dlg.add_button)
    vbox_layout.addWidget(dlg.delete_button)

    dlg.setLayout(vbox_layout)
    dlg.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    # test_open_database_and_query_exec()
    test_QSqlTableModel_and_QTableView()
