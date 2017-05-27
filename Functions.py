#!/usr/bin/python
# coding: utf8


import re


def get_email(text=''):
    email = re.search(b'To: ([^\s]+)', text)
    email = email.group(1).decode()
    email = str(email)
    return email


def get_diagnostic_code(text=''):
    diagnostic_code = re.search(b'Diagnostic-Code: (.+(\s.+\n){0,5})', text)
    diagnostic_code = diagnostic_code.group(1).decode()
    diagnostic_code = str(diagnostic_code)

    edits = [('\r\n', ''),
             ('\n', ''),
             ('\s', '')]

    for search, replace in edits:
        diagnostic_code = diagnostic_code.replace(search, replace)

    diagnostic_code = re.sub(' +', ' ', diagnostic_code)
    return diagnostic_code
