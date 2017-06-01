#!/usr/bin/python
# coding: utf8

# Imports
import os
import pymysql
import datetime
import Conf

dateForTimestamp = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())

# MySQL
file = open('Install.sql')
query = file.read()

db = pymysql.connect(host=Conf.DB_HOST,
                     user=Conf.DB_USER,
                     passwd=Conf.DB_PASSWORD,
                     db=Conf.DB_NAME,
                     charset='utf8')
cursor = db.cursor()

try:
    cursor.execute(query)
except Exception as e:
    print('################################## %s ##################################' % dateForTimestamp)
    print('QUERY: %s \nERROR: %s \n' % (query, e))
    pass

db.commit()
db.close()

# Crontab
crontab = '*/10 * * * * cd %s && /usr/bin/python Cron.py >> Cron.log' % Conf.PATH
cmd = 'crontab -l | { cat; echo "%s"; } | crontab -' % crontab
os.system(cmd)
