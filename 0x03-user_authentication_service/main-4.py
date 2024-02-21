#!/usr/bin/env python3
"""
Main file
"""
from auth import Auth
from db import DB

email = 'br@no.com'
password = 'mySePwd'

auth = Auth()

try:
    user = auth.register_user(email, password)
    print(f"successfully created a new user!")
except ValueError as err:
    print("could not create a new user: {}".format(err))

try:
    user = auth.register_user(email, password)
    print("successfully created a new user!")
except ValueError as err:
    print("could not create a new user: {}".format(err))
