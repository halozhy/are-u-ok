#!/usr/bin/python
# -*- coding: UTF-8 -*-
import datetime
import smtplib
import time
import traceback
import pymysql
from email.mime.text import MIMEText
from email.header import Header


class Notifier:
    def send(self, subject: str, content: str):
        pass


class DBNotifier(Notifier):
    def __init__(self, mail_host: str, mail_username: str, mail_password: str, mail_receiver: str,
                 db_host: str, db_username: str, db_password: str, db_name: str):
        self._mail_host: str = mail_host
        self._mail_user: str = mail_username
        self._mail_pass: str = mail_password
        self._mail_receiver: str = mail_receiver
        self._db_host: str = db_host
        self._db_user: str = db_username
        self._db_pass: str = db_password
        self._db_name: str = db_name

    def send(self, subject: str, content: str):
        try:
            conn = pymysql.connect(host=self._db_host, user=self._db_user, password=self._db_pass,
                                   database=self._db_name)
            cursor = conn.cursor()
            sql = "INSERT INTO ARE_YOU_OK_LOG (date, msg) VALUES (%s, %s)"
            now_time = datetime.datetime.now().astimezone(datetime.timezone(datetime.timedelta(hours=8)))
            cursor.execute(sql, (now_time.strftime("%Y-%m-%d %H:%M:%S"), f'{subject}:\n{content}'))
            conn.commit()
            conn.close()
            print("save to db successfully")
        except (pymysql.Error, RuntimeError) as e:
            traceback.print_exc()
            print("Fail to save to db, try sending mail...")
            mail_notifier = MailNotifier(self._mail_host, self._mail_user, self._mail_pass, self._mail_receiver)
            content = content + "\n注意：写入数据库存在异常，故改用邮件提醒"
            mail_notifier.send(subject, content)


class MailNotifier(Notifier):
    _from: Header = Header("自动打卡小助手", 'utf-8')
    _to: Header = Header("小主", 'utf-8')

    def __init__(self, host: str, username: str, password: str, receiver: str):
        self._host: str = host
        self._user: str = username
        self._pass: str = password
        self._receiver: str = receiver

    def _make_content(self, subject: str, content: str) -> MIMEText:
        message = MIMEText(content, 'plain', 'utf-8')
        message['Subject'] = Header(subject, 'utf-8')
        message['From'] = self._from
        message['To'] = self._to
        return message

    def send(self, subject: str, content: str):
        try:
            svr = smtplib.SMTP()
            svr.connect(self._host)
            svr.login(self._user, self._pass)
            message = self._make_content(subject, content)
            svr.sendmail(self._user, self._receiver, message.as_string())
            print("send mail successfully")
        except Exception as e:
            print("fail to send mail")
            print(e)
            traceback.print_exc()


class PrintNotifier(Notifier):
    def send(self, subject: str, content: str):
        print(f'{subject}:\n{content}')
