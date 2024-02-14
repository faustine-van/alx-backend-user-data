#!/usr/bin/env python3
""" Module of Auth the API authentication
"""
from api.v1.auth.session_auth import SessionAuth
import os
from datetime import datetime, timedelta
from models.user import User


class SessionExpAuth(SessionAuth):
    """class inherits from SessionAuth class
        for an expiration date to a Session ID.
    """
    def __init__(self):
        """initialize variables"""
        self.session_duration = int(os.environ.get('SESSION_DURATION'))

    def create_session(self, user_id=None):
        """create session_id with expiration data"""
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        session_dictionary = {'user_id': user_id, 'created_at': datetime.now()}
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """returns a User ID based on a Session ID
            with expiration id
        """
        # doesn’t contain any key equals to session_id or none
        if session_id is None \
                or session_id not in self.user_id_by_session_id.keys():
            return None
        session_dict = self.user_id_by_session_id.get(session_id)
        if 'created_at' not in session_dict.keys():
            return None
        user_id = self.user_id_by_session_id.get(session_id).get('user_id')
        if self.session_duration == 0 or self.session_duration < 0:
            return user_id
        created_at = self.user_id_by_session_id.get(session_id
                                                    ).get('created_at')
        date_after_sec = created_at + timedelta(seconds=self.session_duration)
        if date_after_sec < datetime.now():
            return None
        return user_id
