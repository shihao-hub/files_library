import imapclient
import pyperclip
import pyzmail

imap_obj = imapclient.IMAPClient("imap.qq.com", ssl=True)
imap_obj.login("2958017271@qq.com", "gzuhzbhicluldhba")  # 993
imap_obj.select_folder("INBOX", readonly=True)
uids = imap_obj.search("SINCE 05-May-2024")
# print(uids)
raw_msgs = imap_obj.fetch(uids[-1], ["BODY[]"])
msg = pyzmail.PzMessage.factory(raw_msgs[uids[-1]][b"BODY[]"])

res = str(msg.text_part.get_payload(), encoding="utf-8")
pyperclip.copy(res)

imap_obj.logout()

