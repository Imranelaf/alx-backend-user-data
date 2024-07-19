#!/usr/bin/env python3

'''
This module contains the main Flask app
'''

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    '''
    This class is the user model
    Attributes:
        id: an integer that is the primary key
        email: a string that is not nullable
        hashed_password: a string that is not nullable
        session_id: a string that is nullable
        reset_token: a string that is nullable
    '''

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
