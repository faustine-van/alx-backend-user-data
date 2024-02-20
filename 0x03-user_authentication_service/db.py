#!/usr/bin/env python3
"""DB module
"""
from typing import TypeVar
from sqlalchemy import create_engine
from sqlalchemy.exc import NoResultFound, IntegrityError, InvalidRequestError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> TypeVar('User'):
        """add user to the database"""
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        try:
            self._session.commit()   # save into databases
        except IntegrityError:
            self._session.rollback()
            raise ValueError('user with email alread exists')
        return user

    def find_user_by(self, **kwargs) -> TypeVar('User'):
        """returns the first row found in the users table as
            filtered by the method’s input arguments.
        """
        if kwargs:
            for key, value in kwargs.items():
                column = getattr(User, key, None)
                user = self._session.query(User
                                           ).filter(column == value).first()
                if not user:
                    raise NoResultFound('Not found')
                if key not in User.__table__.columns:
                    raise InvalidRequestError('Invalid')
        return user

    def update_user(self, user_id: int, **kwargs) -> TypeVar('User'):
        """update user"""
        res = self.find_user_by(id=user_id)
        if res:
            for key, val in kwargs.items():
                if hasattr(User, key):
                    setattr(res, key, val)
                else:
                    raise ValueError('Error')
            self._session.commit()
            return res
