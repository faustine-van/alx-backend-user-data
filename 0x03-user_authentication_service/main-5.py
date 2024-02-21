#!/usr/bin/env python3
"""
Main file
"""
from auth import Auth

email = 'tom@sugi.com'
password = 'MyPwdOfBob'
auth = Auth()


auth.register_user(email, password)

print(auth.valid_login(email, password))

print(auth.valid_login(email, "WrongPwd"))

print(auth.valid_login("unknown@email", password))