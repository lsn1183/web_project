# -*- coding: UTF-8 -*-
"""
Created on 2017-9-14

@author: hcz
"""
# from flask_mail import Message
# import json
# from celery import task
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import time
COMMASPACE = ', '
EMAIL_HOST = "mail.security.suntec.net"
EMAIL_PORT = 25
EMAIL_USER = "hongcz"
EMAIL_PASSWD = "111111Aa"


# @task
# def send_async_email(from_user, recipients, arl_ids):
#     from Source.spec2db_server.spec_server_if import app, mail
#     print 'Start Send Mail:', time.strftime("%Y-%m-%d %H:%M:%S")
#     subject = 'ARL Transfer'
#     recipients = json.loads(recipients)
#     msg = Message(subject=subject,
#                   sender="hongcz@security.suntec.net",  # app.config.get("MAIL_USERNAME"),
#                   recipients=recipients,
#                   )
#     msg.body = 'Test'
#     msg.body = '%s transfer ARL [%s] to you.' % (from_user, arl_ids)
#     msg.html = '测试html'
#     with app.app_context():
#         mail.send(msg)
#     print 'End Send Mail:', time.strftime("%Y-%m-%d %H:%M:%S")
#
# # def send_async_email(app, msg):
# #     from Source.spec2db_server.spec_server_if import mail
# #     # print 'sub thread:', time.strftime("%Y-%m-%d %H:%M:%S")
# #     print 'sub process:', time.strftime("%Y-%m-%d %H:%M:%S")
# #     with app.app_context():
# #         mail.send(msg)
# #     return
#
#
# def send_email(from_username, recipients, arl_list):
#     arl_ids = ', '.join(arl_list)
#     recipients = json.dumps(recipients)
#     send_async_email.delay(from_username, recipients, arl_ids)
#     # p = Process(target=send_async_email, args=(app, msg))
#     # p.start()
#     # thr = Thread(target=send_async_email(app, msg), args=[app, msg])
#     # thr.setDaemon(True)
#     # thr.start()
#     print 'main process:', time.strftime("%Y-%m-%d %H:%M:%S")
#     return


class ArlMail(object):
    """"""
    def __init__(self, _from="hongcz@security.suntec.net", to_list=None):
        self._from = _from
        self._to_list = to_list

    def send_mail(self, subject, massage):
        to_addrs = COMMASPACE.join(self._to_list)
        msg = MIMEText(massage)
        msg["Subject"] = Header(subject, 'utf-8')
        msg["From"] = self._from
        msg["To"] = to_addrs
        # Send the mail via SMTP server.
        try:
            # s = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
            s = smtplib.SMTP()
            s.connect(EMAIL_HOST, EMAIL_PORT)
            s.login(EMAIL_USER, EMAIL_PASSWD)
            s.sendmail(self._from, self._to_list, msg.as_string())
            s.quit()
            print "邮件发送成功!"
            return True
        except:
            print "邮件发送失败!"
            return False

    def send_tranfer(self, from_username, arl_list):
        subject = '[ARL Transfer]'
        massage = 'XXX transfer ARL [%s] to you.' % ', '.join(arl_list)
        self.send_mail(subject, massage)


if __name__ == '__main__':
    mail_obj = ArlMail("hongcz@security.suntec.net", ["hongcz@security.suntec.net",
                                                      "zhangkairan@security.suntec.net",
                                                      "liuxiaodong@security.suntec.net",
                                                      "shaosichen@security.suntec.net",
                                                      "wangwenjiee@security.suntec.net"])
    mail_obj.send_tranfer('hcz', ['1.10.1'])


