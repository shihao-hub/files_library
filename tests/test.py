import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QPushButton, QLineEdit


class CalculatorWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 设置窗口属性
        self.setWindowTitle("Calculator")
        self.setFixedSize(300, 300)

        # 设置中心窗口
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # 创建布局
        grid_layout = QGridLayout()
        central_widget.setLayout(grid_layout)

        # 添加文本框
        self.result_line_edit = QLineEdit()
        self.result_line_edit.setAlignment(Qt.AlignRight)
        self.result_line_edit.setReadOnly(True)
        # row: int, column: int, rowSpan: int, columnSpan: int
        # grid_layout.addWidget(self.result_line_edit, 0, 0, 1, 4)
        grid_layout.addWidget(self.result_line_edit, 0, 0, 1, 4)

        # 添加按钮
        buttons = [
            "7", "8", "9", "/",
            "4", "5", "6", "*",
            "1", "2", "3", "-",
            "0", ".", "=", "+"
        ]
        positions = [(i, j) for i in range(1, 5) for j in range(4)]
        for position, button_label in zip(positions, buttons):
            button = QPushButton(button_label)
            button.setMaximumWidth(50)
            button.clicked.connect(self.on_button_clicked)
            grid_layout.addWidget(button, *position)

    def on_button_clicked(self):
        print(111)
        button = self.sender()
        button_label = button.text()

        if button_label == "=":
            try:
                result = str(eval(self.result_line_edit.text()))
            except (SyntaxError, ZeroDivisionError):
                result = "Error"
            self.result_line_edit.setText(result)
        else:
            self.result_line_edit.setText(self.result_line_edit.text() + button_label)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    calculator = CalculatorWindow()
    calculator.show()
    sys.exit(app.exec_())
