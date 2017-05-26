#!/usr/bin/python
# coding: utf8


import re


def get_email(text=''):
    text = text.decode()
    email = re.search('To: ([^\s]+)', text)
    email = email.group(1)
    print('To:', email)
    return email


def get_diagnostic_code(text=''):
    text = text.decode()
    diagnostic_code = re.search('Diagnostic-Code: (.+(\s.+\n){0,5})', text)
    diagnostic_code = diagnostic_code.group(1)
    print('Diagnostic-Code:', diagnostic_code)
    return diagnostic_code
