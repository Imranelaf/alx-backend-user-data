#!/usr/bin/env python3

'''
This module contains the main Flask app
'''

from typing import Union
from uuid import uuid4
from bcrypt import hashpw, gensalt, checkpw
from sqlalchemy.orm.exc import NoResultFound

from db import User, DB


def _hash_password(password: str) -> bytes:
    '''
    This function should use the bcrypt package to hash a password with a salt.
    Args:
        password: string type
    Returns:
        bytes: a salted hash of the input password
    '''
    return hashpw(password.encode('utf-8'), gensalt())


def _generate_uuid() -> str:
    '''
    This function should return a string representation of a new UUID
    Returns:
        str: a new UUID
    '''
    return str(uuid4())


class Auth:
    '''
    This class is the authentication system for the app
    Methods:
        register_user: registers a new user given a new password and email
        valid_login: checks if a user is valid
        create_session: creates a new session for a user
        get_user_from_session_id: gets a user from a session id
        destroy_session: destroys a session
        get_reset_password_token: gets a reset password token
        update_password: updates a user's password
    '''
    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        '''
        registers a new user given a new password and email
        Args:
            email: string type
            password: string type
        Returns:
            User: a new user object
        '''
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
        else:
            raise ValueError(f'User {email} already exists')

    def valid_login(self, email: str, password: str) -> bool:
        '''
        checks if a user is valid
        Args:
            email: string type
            password: string type
            Returns:
            bool: True if the password is valid, False otherwise
        Returns:
            bool: True if the password is valid, False otherwise
        '''
        try:
            usr = self._db.find_user_by(email=email)
            return checkpw(
                password.encode("utf-8"),
                usr.hashed_password
            )
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        '''
        creates a new session for a user
        Args:
            email: string type
        Returns:
            str: a new session ID
        '''
        try:
            usr = self._db.find_user_by(email=email)
            sessID = _generate_uuid()
            self._db.update_user(usr.id, session_id=sessID)
            return usr.session_id

        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        '''
        gets a user from a session id
        Args:
            session_id: string type
        Returns:
            Union[User, None]: a user object or None
        '''
        if session_id is None:
            return None
        try:
            return self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        '''
        destroys a session
        Args:
            user_id: integer type
        Returns:
            None
        '''
        self._db.update_user(user_id, session_id=None)
        return None

    def get_reset_password_token(self, email: str) -> str:
        '''
        gets a reset password token
        Args:
            email: string type
        '''
        try:
            usr = self._db.find_user_by(email=email)
            rsttkn = _generate_uuid()
            self._db.update_user(usr.id, reset_token=rsttkn)
            return rsttkn
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        '''
        updates a user's password
        Args:
            reset_token: string type
            password: string type
        Returns:
            None
        '''
        try:
            usr = self._db.find_user_by(reset_token=reset_token)
            hshdpasswd = _hash_password(password)
            self._db.update_user(
                usr.id, hashed_password=hshdpasswd, reset_token=None)
            return None
        except NoResultFound:
            raise ValueError
