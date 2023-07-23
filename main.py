import os
import imaplib
import email
from email.header import decode_header

# 邮箱的登录信息
username = "your email username"
password = "your email password"

# 邮箱的IMAP服务器地址，比如：imap.gmail.com
imap_url = "your imap server"

# 邮件的文件夹，INBOX是默认的收件箱
mail_folder = "INBOX"

# 附件保存的目录
attachment_dir = "path to save attachments"

# 连接到邮箱服务器
mail = imaplib.IMAP4_SSL(imap_url)

# 登录邮箱
mail.login(username, password)

# 选择邮件文件夹
mail.select(mail_folder)

# 搜索邮件
resp, items = mail.search(None, "ALL")
items = items[0].split()

# 遍历邮件
for emailid in items:
    resp, data = mail.fetch(emailid, "(BODY.PEEK[])")
    raw_email = data[0][1]
    email_message = email.message_from_bytes(raw_email)

    # 遍历邮件的每一个部分
    for part in email_message.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue

        filename = part.get_filename()
        
        # 解码文件名
        dh = decode_header(filename)
        filename = dh[0][0]
        charset = dh[0][1]
        if charset is not None:
            filename = filename.decode(charset)
        
        if bool(filename):
            filepath = os.path.join(attachment_dir, filename)
            with open(filepath, "wb") as f:
                f.write(part.get_payload(decode=True))

    print('Attachment saved at: ' + filepath)
