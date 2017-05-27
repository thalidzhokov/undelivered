#!/usr/bin/python
# coding: utf8

# e.g.
# */10 * * * * cd /home/PATH_TO/undelivered && /usr/bin/python Cron.py >> Cron.log

# Imports
import datetime
import imaplib
import lepl.apps.rfc3696
import pymysql
import Conf
import Functions


dateForTimestamp = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
date = (datetime.date.today() - datetime.timedelta(1)).strftime("%d-%b-%Y")
emailValidator = lepl.apps.rfc3696.Email()
server = imaplib.IMAP4_SSL(Conf.IMAP_SERVER, Conf.IMAP_PORT)
server.login(Conf.IMAP_LOGIN, Conf.IMAP_PASSWORD)
server.select(mailbox='INBOX', readonly=Conf.READONLY)
result, data = server.search(None, '(SUBJECT "Undelivered" UNSEEN SINCE "{date}")'.format(date=date))
UIDs = data[0].split()
UIDs = UIDs[:Conf.COUNT]
emails = []
errors = []

for UID in UIDs:
    body = server.fetch(UID, '(UID BODY[TEXT])')
    text = body[1][0][1]

    UID = UID.decode()
    email = Functions.get_email(text)
    diagnostic_code = Functions.get_diagnostic_code(text)

    if emailValidator(email):
        emails.append((UID, email, diagnostic_code))
    else:
        errors.append((UID, text.decode()))

query = ''

# emails
if len(emails) > 0:
    i = 0
    query += 'INSERT INTO `emails` (`uid`, `email`, `diagnostic_code`, `timestamp`) VALUES'

    for UID, email, diagnostic_code in emails:
        if i > 0:
            query += ", "
        query += "('%s', '%s', '%s', '%s')" % (UID, email, diagnostic_code, dateForTimestamp)
        i += 1

    query += ';'

# errors
if len(errors) > 0:
    i = 0
    query += 'INSERT INTO `errors` (`uid`, `timestamp`) VALUES'

    for UID, text in errors:
        if i > 0:
            query += ", "
        query += "('%s', '%s')" % (UID, dateForTimestamp)
        i += 1

    query += ';'

# sql
if query:
    db = pymysql.connect(host=Conf.DB_HOST,
                         user=Conf.DB_USER,
                         passwd=Conf.DB_PASSWORD,
                         db=Conf.DB_NAME,
                         charset='utf8')
    cursor = db.cursor()

    try:
        execute = cursor.execute(query)
    except Exception as e:
        print('################################## %s ##################################' % dateForTimestamp)
        print('QUERY: %s \nERROR: %s \n' % (query, e))
        pass

    db.commit()
    db.close()

