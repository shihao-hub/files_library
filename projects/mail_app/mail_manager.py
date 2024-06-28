import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class MailManager:
    def __init__(self, receivers):
        self.receivers = receivers
        self.sender = "2958017271@qq.com"
        self.password = "gzuhzbhicluldhba"

    def send(self, subject: str, content: str, attachments=None):
        attachments = attachments or []

        mime_multipart = MIMEMultipart()
        mime_multipart["From"] = self.sender
        mime_multipart["subject"] = subject

        text_apart = MIMEText(content, "plain", "utf-8")
        mime_multipart.attach(text_apart)

        msg = ""
        try:
            smtp_obj = smtplib.SMTP_SSL("smtp.qq.com", 465)

            ehlo_ret = smtp_obj.ehlo()
            if ehlo_ret[0] != 250:
                raise Exception("SMTP ehlo 失败")

            print(f"正在尝试登录邮箱用户: {self.sender}")

            login_ret = smtp_obj.login(self.sender, self.password)
            if login_ret[0] == 235:
                print("登录成功！")

            sendmail_ret = smtp_obj.sendmail(self.sender, self.receivers, mime_multipart.as_string())

            if sendmail_ret:
                print(f"传输失败的收件人有：{sendmail_ret}")
            if len(sendmail_ret) != len(self.receivers):
                print("发送成功！")

            quit_ret = smtp_obj.quit()
            if quit_ret == 221:
                print("会话结束")

            msg += f"发送成功\n"
            if sendmail_ret:
                msg += f"传输失败的收件人有：{sendmail_ret}\n"
        except smtplib.SMTPException as e:
            print(e)
            msg += f"发送失败，原因：{e}\n"
            return False, msg
        return True, msg


if __name__ == '__main__':
    main_manager = MailManager(["2958017271@qq.com"])
    main_manager.send("这是一个主题", "这是一个正文")
