import functools
import json
import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox

from mail_app.mail_manager import MailManager
from ui.mail import Ui_Mail


def send_button_exit(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        res = func(self, *args, **kwargs)
        self.send_button.setEnabled(True)
        return res

    return wrapper


class Mail(QMainWindow, Ui_Mail):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.json_data_path = r"mail_app/mail_app_draft.json"

        self.setupUi(self)  # 传入自己

        self._on_load()

    def _messagebox_notice(self, msg):
        QMessageBox.information(self, "通知", msg)

    def _on_load(self):
        data = None
        with open(self.json_data_path, "r", encoding="utf-8") as file:
            try:
                data = json.load(file)
            except json.decoder.JSONDecodeError as e:
                print(f"load error: {e}")
        if not data:
            return
        draft = data["drafts"][0]
        self.subject_line_edit.setText(draft["subject"])
        self.receiver_line_edit.setText(draft["receivers"])
        self.body_text_edit.setPlainText(draft["body"])
        print("初始化数据结束")

    @QtCore.pyqtSlot()
    def on_test_button_clicked(self):
        self.subject_line_edit.setText("这是一个主题")
        self.receiver_line_edit.setText("chang123456789zsh@163.com")
        self.body_text_edit.setPlainText("这是一个正文")

    @QtCore.pyqtSlot()
    @send_button_exit
    def on_send_button_clicked(self):
        self.send_button.setEnabled(False)
        subject = self.subject_line_edit.text()
        receivers = self.receiver_line_edit.text().split(";")
        body = self.body_text_edit.toPlainText()

        if not subject or not receivers or not body:
            self._messagebox_notice("主题、发送人、正文不可为空！")
            return

        mail_manager = MailManager(receivers)
        res, msg = mail_manager.send(subject, body)
        self._messagebox_notice(msg)

    @QtCore.pyqtSlot()
    def on_draft_save_button_clicked(self):
        # TODO: 后面改成 sqlite3 这个轻量级数据库！
        with open(self.json_data_path, "w", encoding="utf-8") as file:
            json.dump({
                "drafts": [
                    {
                        "receivers": self.receiver_line_edit.text(),
                        "subject": self.subject_line_edit.text(),
                        "body": self.body_text_edit.toPlainText()
                    }
                ]
            }, file)
        print("存草稿成功")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Mail()
    w.show()
    sys.exit(app.exec_())
