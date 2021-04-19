#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys

from job import Job
from notifier import MailNotifier, PrintNotifier, DBNotifier

if __name__ == '__main__':
    args_len = len(sys.argv)
    if args_len < 3:
        print("Missing enough arguments, at least 2: user, pass")
        exit(1)
    if 4 < args_len < 8:
        print(
            "Missing enough arguments, expect 7: user, pass, ip, mail_host, mail_user, mail_pass, mail_receiver")
        exit(1)
    if 8 < args_len < 12:
        print(
            "Missing enough arguments, expect 12: user, pass, ip, mail_host, mail_user, mail_pass, mail_receiver, "
            "db_host, db_user, db_pass, db_name")
        exit(1)
    if args_len > 12:
        print("Too many arguments")
        exit(1)

    job = Job(sys.argv[1], sys.argv[2], sys.argv[3] if args_len > 3 else '')

    if args_len <= 4 or "" in sys.argv[4:8]:
        print("running without sending email")
        job.do(PrintNotifier())
    elif args_len <= 8 or "" in sys.argv[8:12]:
        print("running with sending email")
        job.do(MailNotifier(sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7]))
    else:
        print("running with saving to db")
        job.do(DBNotifier(sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7],
                          sys.argv[8], sys.argv[9], sys.argv[10], sys.argv[11]))
