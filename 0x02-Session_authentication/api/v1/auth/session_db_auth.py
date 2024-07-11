#!/usr/bin/env python3
"""
Session storage module
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    '''
    SessionDBAuth class

    Attributes:
        user_id_by_session_id (dict): user id by session id

    Methods:
        create_session(self, user_id: str = None): Creates session object
        user_id_for_session_id(self, session_id: str = None): Get user
        destroy_session(self, request=None): Destroy session object
    '''
    def create_session(self, user_id: str = None) -> str:
        '''
        Creates session object
        Args:
            user_id (str): user's id

        Returns:
            str: session id
        '''
        if not user_id or type(user_id) is not str:
            return None

        sess = UserSession(**{"user_id": user_id})
        sess.save()
        SessionDBAuth.user_id_by_session_id[sess.session_id] =\
            sess.user_id
        return sess.session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        '''
        Get user by session id
        Args:
            session_id (str): session id
        Returns:
            str: user id
        '''
        if not session_id or type(session_id) is not str:
            return None
        try:
            sessns = UserSession.search({"session_id": session_id})
        except KeyError:
            return None
        if not sessns:
            return None
        sess = sessns[0]

        if self.session_duration <= 0:
            return sess.user_id

        expData = sess.updated_at \
            + timedelta(seconds=self.session_duration)
        if datetime.utcnow() < expData:
            return sess.user_id
        SessionDBAuth.user_id_by_session_id.pop(session_id)
        sess.remove()
        return None

    def destroy_session(self, request=None) -> bool:
        '''
        Destroy session object
        Args:
            request (obj): request object
        Returns:
            bool: True if session is destroyed, False otherwise
        '''
        if not request:
            return False
        sessId = self.session_cookie(request)
        try:
            sessins = UserSession.search({"session_id": sessId})
        except KeyError:
            return False

        if sessins:
            sess = sessins[0]
            SessionDBAuth.user_id_by_session_id.pop(sess.session_id)
            sess.remove()
            return True
        return False
