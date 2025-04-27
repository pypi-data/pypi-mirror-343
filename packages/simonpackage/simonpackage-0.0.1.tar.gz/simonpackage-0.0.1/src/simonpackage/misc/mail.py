from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib
def sendMail(content,
             subject=None,
             from_addr='simonzhang84@163.com',
             to_addr='304417686@qq.com',
             account='simonzhang84',
             password='love2015'):
    """
    send email automatically
    :param content: main content of the mail, string
    :param subject: the subject of the email, if None, will be content
    :param from_addr: sending email address
    :param to_addr: receiving email address
    :param account: account of the from_addr
    :param password: password of the from_addr, possibly the login password, or the verify code
    :return:
    """
    def _format_addr(s):
        # 用来处理格式化文本，将格式化的结果作为返回值传出去
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))

    smtp_domain = from_addr.split('@')[-1]
    smtp_server = f'smtp.{smtp_domain}'

    # 将发送邮箱、接收邮箱、邮件主题格式化
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['From'] = _format_addr(u'张建广 <%s>' % from_addr)

    msg['To'] = _format_addr(u'注意 <%s>' % to_addr)
    if not subject:
        subject = content
    msg['Subject'] = Header(subject, 'utf-8').encode()
    # SMTP协议加密端口是465
    server = smtplib.SMTP_SSL(smtp_server, 465)
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()


if __name__ == '__main__':
    sendMail('hello from python')