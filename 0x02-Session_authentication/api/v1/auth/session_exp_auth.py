#!/usr/bin/env python3
"""
Expiring session module
"""
from datetime import datetime, timedelta
from os import getenv
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    '''
    SessionExpAuth class
    Attributes:
        session_duration (int): session duration
    Methods:
        __init__(self): Initializes SessionExpAuth instance
        create_session(self, user_id: str = None): Creates session id
        user_id_for_session_id(self, session_id: str = None): Gets user id
    '''
    def __init__(self) -> None:
        '''
        Initializes SessionExpAuth instance
        '''
        super().__init__()
        dur = getenv('SESSION_DURATION')
        if not dur:
            self.session_duration = 0
        else:
            try:
                dur = int(dur)
                self.session_duration = dur
            except ValueError:
                self.session_duration = 0

    def create_session(self, usrId: str = None) -> str:
        '''
        Creates session id
        Args:
            user_id (str): user's id
        Returns:
            str: session id
        '''
        sess_id = super().create_session(usrId)
        if not sess_id:
            return None
        usrId = SessionExpAuth.user_id_by_session_id.get(sess_id)
        crtd_at = datetime.now()
        sess_dict = {"user_id": usrId, "created_at": crtd_at}
        SessionExpAuth.user_id_by_session_id.update({sess_id: sess_dict})
        return sess_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        '''
        Gets user id
        Args:
            session_id (str): session id
        Returns:
            str: user id
        '''
        if not session_id and type(session_id) is not str:
            return None
        sess_info = SessionExpAuth.user_id_by_session_id.get(session_id)
        if not sess_info:
            return None
        usrId = sess_info.get("user_id")
        ctd_at = sess_info.get("created_at")

        if self.session_duration <= 0:
            return usrId

        if not ctd_at:
            return None
        exp_data = ctd_at + timedelta(seconds=self.session_duration)
        if datetime.now() > exp_data:
            return None
        return usrId
