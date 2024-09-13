from email import encoders
from email.mime.base import MIMEBase
from django.conf import settings

import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

from email.mime.multipart import MIMEMultipart


def sendEmail(email, user, html_msg,msg_subject,filename):
    port = settings.STMP_PORT
    smtp_server = settings.STMP_SERVER
    login = settings.STMP_LOGIN
    password = settings.STMP_PWD

    sender_email = settings.STMP_LOGIN
    receiver_email = email
    message = MIMEMultipart("alternative")
    message["Subject"] = msg_subject
    message["From"] = sender_email
    message["To"] = receiver_email


    part = MIMEText(html_msg, "html")
    message.attach(part)

    fp = open("./static/img/logo.png", "rb")
    image = MIMEImage(fp.read())
    fp.close()

    image.add_header("Content-ID", "<ZesstaLogo>")
    message.attach(image)
    context = ssl.create_default_context()
    # send your email
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls(context=context)
        server.login(login, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
    return True

