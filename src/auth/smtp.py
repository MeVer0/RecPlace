from smtplib import SMTP_SSL as SMTP
import sys
from email.mime.text import MIMEText
from src.auth.config import smtp_username, smtp_password, smtp_server


def send_mail(destination, subject, content, text_subtype='plain'):
    """
    :param destination email адресата
    :param subject тема письма

    Отправляет письмо на email
    """

    sender = "RecPlace"

    try:
        msg = MIMEText(content, text_subtype)
        msg['Subject'] = subject
        msg['From'] = "RecPlace"

        conn = SMTP(smtp_server)
        conn.set_debuglevel(False)
        conn.login(smtp_username, smtp_password)
        try:
            conn.sendmail(sender, destination, msg.as_string())
        finally:
            conn.quit()
    except:
        sys.exit("mail failed; %s" % "CUSTOM_ERROR")
