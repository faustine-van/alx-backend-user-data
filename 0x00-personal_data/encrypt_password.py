#!/usr/bin/env python3
"""
    that returns the log message obfuscated
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """hash password using bcrypt package
       to perform the hashing (with hashpw
    """
    # convert password to bytes
    byte_pass = password.encode('utf-8')
    # generate salt to add to password
    gen_salt = bcrypt.gensalt()

    hash_pass = bcrypt.hashpw(byte_pass, gen_salt)
    return hash_pass


def is_valid(hashed_password: bytes, password: str) -> bool:
    """validate that the provided password
       matches the hashed password.
    """
    # convert password to bytes
    bytes_pass = password.encode('utf-8')
    is_val = bcrypt.checkpw(bytes_pass, hashed_password)
    return is_val
