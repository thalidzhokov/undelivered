#!/usr/bin/python
# coding: utf8

# e.g.
# */10 * * * * cd /home/PATH_TO/undelivered && /usr/bin/python Cron.py >> Cron.log

# Imports
import datetime, imaplib, re, lepl.apps.rfc3696, pymysql, Conf, Functions

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
    email = re.search(b'To: ([^\s]+)', text)
    email = email.group(1).decode()
    UID = UID.decode()
    reason = Functions.reason(text)

    if emailValidator(email):
        emails.append((UID, email, reason))
    else:
        errors.append((UID, text.decode()))

sql = ''

# emails
if len(emails) > 0:
    i = 0
    sql += 'INSERT INTO `emails` (`uid`, `email`, `reason`, `timestamp`) VALUES'

    for UID, email, reason in emails:
        if i > 0:
            sql += ", "
        sql += "('%s', '%s', '%s', '%s')" % (UID, email, reason, dateForTimestamp)
        i += 1

    sql += ';'

# errors
if len(errors) > 0:
    i = 0
    sql += 'INSERT INTO `errors` (`uid`, `timestamp`) VALUES'

    for UID, text in errors:
        if i > 0:
            sql += ", "
        sql += "('%s', '%s')" % (UID, dateForTimestamp)
        i += 1

    sql += ';'

# sql
if sql:
    db = pymysql.connect(host=Conf.DB_HOST,
                         user=Conf.DB_USER,
                         passwd=Conf.DB_PASSWORD,
                         db=Conf.DB_NAME,
                         charset='utf8')
    cursor = db.cursor()

    try:
        cursor.execute(sql)
    except:
        print('ERROR!', sql)
        pass

    db.commit()
    db.close()
else:
    print('EMPTY sql')
