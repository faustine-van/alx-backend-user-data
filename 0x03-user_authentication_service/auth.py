#!/usr/bin/env python3
"""return bytes is a salted hash of the
    input password, hashed with bcrypt.hashpw.
"""
from typing import TypeVar
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
import bcrypt
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """Hashes the input password using bcrypt.hashpw

    Args:
        password (str): The password to hash

    Returns:
        bytes: Salted hash of the input password
    """
    byte = password.encode('utf-8')
    gen_salt = bcrypt.gensalt()
    hashpass = bcrypt.hashpw(byte, gen_salt)
    return hashpass


def _generate_uuid() -> str:
    """generate unique id
    Args: nothing
    Returns:
        str: return a string representation
        of a new UUID
    """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user.

        Args:
            email (str): Email of the user.
            password (str): Password of the user.

        Returns:
            User: User object.
        """
        try:
            # Check if user with email already exists
            user_with_email = self._db.find_user_by(email=email)
            raise ValueError(f'User {email} already exists')
        except NoResultFound:
            # Hash the password
            hashed_pass = _hash_password(password)
            new_user = self._db.add_user(email, hashed_pass)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """Validate login credentials.

        Args:
            email (str): Email of the user.
            password (str): Password of the user.

        Returns:
            bool: True if login is valid, False otherwise.
        """
        user = self._db._session.query(User).filter_by(email=email).first()
        if user:
            bytepass = password.encode('utf-8')
            if bcrypt.checkpw(bytepass, user.hashed_password):
                return True
        return False

    def create_session(self, email: str) -> str:
        """return session id for user corresponding to the emai
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                new_session_id = _generate_uuid()
                self._db.update_user(user.id, session_id=new_session_id)
                return new_session_id
        except NoResultFound:
            pass

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
