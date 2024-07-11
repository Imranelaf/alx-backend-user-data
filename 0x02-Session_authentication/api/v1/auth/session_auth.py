#!/usr/bin/env python3
"""
Session authentication module
"""
from api.v1.auth.auth import Auth
from typing import Dict, TypeVar
from uuid import uuid4
from os import getenv
from models.user import User


class SessionAuth(Auth):
    '''
    SessionAuth class
    Attributes:
        user_id_by_session_id (dict): user id by session id
    Methods:
        create_session(self, user_id: str = None): Creates user session_id
        user_id_for_session_id(self, session_id: str = None): Gets user id
        current_user(self, request=None): Gets current user
        destroy_session(self, request=None): Destroys session
    '''
    user_id_by_session_id: Dict = {}

    def create_session(self, user_id: str = None) -> str:
        """ Creates user session_id and adds to session dictionary
            Return:
                - nrw session id
        """
        if user_id and type(user_id) is str:
            session_id = str(uuid4())
            SessionAuth.user_id_by_session_id[session_id] = user_id
            return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Gets user id associated with passed session id
            Return:
                - user's id
        """
        if session_id and type(session_id) is str:
            return SessionAuth.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> TypeVar('User'):
        '''
        Gets current user
        Args:
            request (TypeVar('Request')): request object
        Returns:
            TypeVar('User'): current user
        '''
        if not request:
            return None
        sessId = self.session_cookie(request)
        usrId = self.user_id_for_session_id(sessId)
        currUsr = User.get(usrId)
        return currUsr

    def destroy_session(self, request=None) -> bool:
        '''
        Destroys session
        Args:
            request (TypeVar('Request')): request object
        Returns:
            bool: True if session is destroyed, False otherwise
        '''
        if not request:
            return False
        sessId = request.cookies.get(getenv('SESSION_NAME'))
        if not sessId:
            return False
        usrId = self.user_id_for_session_id(sessId)
        if not usrId:
            return False
        SessionAuth.user_id_by_session_id.pop(sessId)
        return True
