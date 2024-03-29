#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
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

    def add_user(self, email: str, hashed_password: str) -> User:
        """add user to the database"""
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
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

    def update_user(self, user_id: int, **kwargs) -> None:
        """updated user and save in databases

        Args:
            user_id (str): The password to hash
            kwargs: arbitrary argument
        Returns:
            User Objects
        """
        res = self.find_user_by(id=user_id)
        if res:
            for key, val in kwargs.items():
                if hasattr(User, key):
                    setattr(res, key, val)
                else:
                    raise ValueError('Error')
            self._session.commit()
            return None
