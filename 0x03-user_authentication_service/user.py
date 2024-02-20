#!/usr/bin/env python3
"""User models database table named users
"""
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """Create tables called users"""
    __tablename__ = 'users'

    id = Column(Integer,  primary_key=True)
    email = Column(String(250), nullable=True)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)