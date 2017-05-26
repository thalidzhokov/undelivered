#!/usr/bin/python
# coding: utf8


import re


def get_email(text=''):
    email = re.search(b'To: ([^\s]+)', text)
    email = email.group(1).decode()
    print(email)
    return email


def get_diagnostic_code(text=''):
    diagnostic_code = re.search(b'Diagnostic-Code: ([^\r\n]+)', text)
    diagnostic_code = diagnostic_code.group(1).decode()
    print(diagnostic_code)
    return diagnostic_code
