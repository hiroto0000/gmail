import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate

import settings

sendAddress = settings.SendAddress
mail_to = settings.Mail_to
password = settings.Pass

def mail(subject, text):




    # SMTPサーバに接続
    smtpobj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpobj.starttls()
    smtpobj.ehlo()
    smtpobj.login(sendAddress, password)

    #送信元、送信先
    # mail_from = sendAddress
    # mail_to = "h"

    #本文
    # text = "こんにちは"

    #メッセージのオブジェクト
    msg = MIMEText(text)
    msg['Subject'] = subject
    msg['From'] = sendAddress
    msg['To'] = mail_to
    msg['Date'] = formatdate(localtime=True)

    #メール送信
    smtpobj.sendmail(sendAddress, mail_to, msg.as_string())
    return 1

def reply_mail(email, subject, text):

        # SMTPサーバに接続
    smtpobj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpobj.starttls()
    smtpobj.ehlo()
    smtpobj.login(sendAddress, password)
    
    #送信元、送信先
    mail_from = sendAddress
    mail_to = email

    subjects = "re:{}".format(subject)

    #メッセージのオブジェクト
    msg = MIMEText(text)
    msg['Subject'] = subjects
    msg['From'] = mail_from
    msg['To'] = mail_to
    msg['Date'] = formatdate(localtime=True)

    #メール送信
    smtpobj.sendmail(mail_from, mail_to, msg.as_string())
    return 1