# coding:utf-8
from email.mime.text import MIMEText
from email.header import Header
from email.utils import parseaddr, formataddr

import smtplib, base64

def send_mail(host):
    # 发件人 地址
    addresser_address = 'taokunliang@wanmagroup.com'
    # 收件人 地址
    recipients_address = 'taokunliang@wanmagroup.com'
    # SMTP服务器地址
    smtp_server = 'smtp.exmail.qq.com'
    # 邮箱密码
    mailbox_password = "V20wNDE1MTI3"
    mailbox_password = base64.b64decode(mailbox_password.encode('utf-8')).decode('utf-8')
    # mail.mime的MIMEText 类来实现支持HTML格式的邮件
    # 邮件内容
    msg = MIMEText('Someone is using the log viewer. selected: ' + host, 'plain', 'utf-8')
    # 格式化 邮件地址： 邮件 (发件人/收件人) 名称 <邮件地址>
    msg['From'] = format_address('taokunliang <%s>' % addresser_address)
    msg['To'] = format_address('taokunliang <%s>' % recipients_address)
    # 邮件主题：
    msg['Subject'] = Header('Someone is using the SEELOG.', 'utf-8').encode()

    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(1)
    server.login(addresser_address, mailbox_password)
    # 抄送 和 发送 邮件是一样的，只要在 收件地址里里面(是list) 添加地址即可：像下面 [recipients_address,carbon_copy,carbon_copy2]
    server.sendmail(addresser_address, [recipients_address], msg.as_string())
    server.quit()

# 格式化 邮件地址
def format_address(address):
    (email_owner_name, email_owner_address) = parseaddr(address)
    # isinstance()  函数来判断一个对象是否是一个已知的类型
    # python3中的str/bytes 对应python2中的unicode, 所以python3中没有unicode
    formatted_address = formataddr((Header(email_owner_name, 'utf-8').encode(), email_owner_address.encode('utf-8')
    if isinstance(email_owner_address, bytes) else email_owner_address))

    return formatted_address




