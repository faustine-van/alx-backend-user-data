#!/usr/bin/env python3
"""return bytes is a salted hash of the
    input password, hashed with bcrypt.hashpw.
"""
from typing import TypeVar
from uuid import uuid4
import bcrypt
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """hash password
        arg: - password
        return bytes
    """
    byte = password.encode('utf-8')
    gen_salt = bcrypt.gensalt()
    hashpass = bcrypt.hashpw(byte, gen_salt)
    return hashpass


def _generate_uuid():
    """generate unique id"""
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> TypeVar('User'):
        """register user and save the user to the databas
        """
        user_w_email = self._db._session.query(User
                                               ).filter_by(email=email).first()
        if user_w_email:
            raise ValueError(f'User {email} already exists.')
        user = self._db.add_user(email, _hash_password(password))
        return user

    def valid_login(self, email: str, password: str) -> bool:
        """validate login"""
        user = self._db._session.query(User).filter_by(email=email).first()
        if user:
            bytePass = password.encode('utf-8')
            if bcrypt.checkpw(bytePass, user.hashed_password):
                return True
            else:
                return False
        return False

    def create_session(self, email: str) -> str:
        """return session id for user corresponding to the emai
        """
        user = self._db._session.query(User).filter_by(email=email).first()
        if user:
            new_session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=new_session_id)
            return new_session_id

    def get_user_from_session_id(self, session_id: str) -> TypeVar('User'):
        """returns the corresponding User or None using session_id
        """
        user = self._db._session.query(User
                                       ).filter_by(session_id=session_id
                                                   ).first()
        if session_id is None or not user:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        """Destroy session"""
        self._db.update_user(user_id, session_id=None)
        return None