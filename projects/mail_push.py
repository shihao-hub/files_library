import os.path
import smtplib
import sys
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


class Mail:
    # 这个标记用命令行执行的时候会报错...
    # sender: str = None
    # receivers: list[str] = None
    # password: str = None

    def __init__(self, sender, receivers, password):
        self.sender = sender
        self.receivers = receivers
        self.password = password

    def send_mail(self, subject: str, content: str, attachments=None):
        if attachments is None:
            attachments = []
        message = MIMEMultipart()

        message["From"] = self.sender
        message["subject"] = subject

        text_apart = MIMEText(content, "plain", "utf-8")
        message.attach(text_apart)

        success_attachments = []
        defeat_attachments = []
        for filepath in attachments:
            try:
                filename = os.path.basename(filepath)
                if os.path.isdir(filepath):
                    raise RuntimeError("'%s' 是文件夹！" % filepath)
                file_apart = MIMEApplication(open(filepath, "rb").read())
                file_apart.add_header("Content-Disposition", "attachment", filename=filename)
                message.attach(file_apart)
                success_attachments.append("附件：'%s' 发送成功！" % filepath)
            except Exception as e:
                print(e)
                defeat_attachments.append("附件：'%s' 发送失败！" % filepath)

        try:
            smtp_obj = smtplib.SMTP_SSL("smtp.qq.com", 465)

            ehlo_ret = smtp_obj.ehlo()
            if ehlo_ret[0] != 250:
                raise RuntimeError("SMTP ehlo 失败")

            print("正在尝试登录邮箱用户: %s" % self.sender)
            login_ret = smtp_obj.login(self.sender, self.password)
            if login_ret[0] == 235:
                print("登录成功！")
            sendmail_ret = smtp_obj.sendmail(self.sender, self.receivers, message.as_string())

            if sendmail_ret != {}:
                print("传输失败的收件人有：" + str(sendmail_ret))
            if len(sendmail_ret) != len(self.receivers):
                print("发送成功！")
                for msg in success_attachments:
                    print(msg)
                for msg in defeat_attachments:
                    print(msg)
            quit_ret = smtp_obj.quit()
            if quit_ret == 221:
                print("会话结束！")
        except smtplib.SMTPException as e:
            print(e)


sys_argv_len = len(sys.argv)
mail = Mail("2958017271@qq.com", ["2958017271@qq.com"], "gzuhzbhicluldhba")

sys_argv_first = sys_argv_len > 1 and sys.argv[1] or None
if sys_argv_first == "-f":
    attachments = [sys.argv[i] for i in range(2, sys_argv_len)]
    mail.send_mail("文件传输", "文件传输", attachments)
elif sys_argv_first == "-t":
    if sys_argv_len != 4:
        raise RuntimeError("Usage: python.exe main.py 主题 正文")
    mail.send_mail(sys.argv[1], sys.argv[2])
elif sys_argv_first == "-tf":
    if sys_argv_len < 4:
        raise RuntimeError("Usage: python.exe main.py 主题 正文 文件1 文件2 ...")
    attachments = [sys.argv[i] for i in range(4, sys_argv_len)]
    mail.send_mail(sys.argv[2], sys.argv[3], attachments)
else:
    with open("mail_push.txt") as file:
        mail.send_mail("OD OD OD", "".join(file.readlines()))
