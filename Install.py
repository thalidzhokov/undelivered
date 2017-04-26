#!/usr/bin/python
# coding: utf8

# Imports
import os, pymysql, Conf

# MySQL
file = open('Install.sql')
sql = file.read()

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

# Crontab
crontab = '*/10 * * * * cd %s && /usr/bin/python Cron.py >> Cron.log' % (Conf.PATH)
cmd = 'crontab -l | { cat; echo "%s"; } | crontab -' % (crontab)
os.system(cmd)
