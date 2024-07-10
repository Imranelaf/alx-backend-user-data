#!/usr/bin/env python3
"""add an expiration date to a Session ID"""

from datetime import datetime, timedelta
from os import getenv
from .session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """add an expiration date to a Session ID"""

    def __init__(self) -> None:
        # super().__init__()
        self.session_duration = int(getenv("SESSION_DURATION", 0))

    def create_session(self, user_id=None):
        """Return the Session ID created"""
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        session_dictionary = {}
        session_dictionary['user_id'] = user_id
        session_dictionary['created_at'] = datetime.now()

        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Overload method from parent class"""
        if not session_id or not self.user_id_by_session_id.get(session_id):
            return None

        session_dict = self.user_id_by_session_id.get(session_id)
        if not session_dict:
            return None

        if self.session_duration <= 0:
            return session_dict.get("user_id")

        if not session_dict.get("created_at"):
            return None
        expInSeconds = timedelta(seconds=self.session_duration)
        if (expInSeconds + session_dict.get("created_at") < datetime.now()):
            return None
        return session_dict.get("user_id")
