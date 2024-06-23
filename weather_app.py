import pprint
import sys

from PyQt5.QtWidgets import QApplication, QWidget

from ui.weather_app_ui import Form



if __name__ == '__main__':
    app  = QApplication(sys.argv)

    w = QWidget()

    f = Form(w)

    w.show()
    sys.exit(app.exec_())
