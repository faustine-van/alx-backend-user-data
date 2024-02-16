#!/usr/bin/env python3
""" Module of Auth the API authentication
"""
from datetime import datetime, timedelta
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """class inherits from SessionAuth class
        for storing user session a Session ID in database.
    """
    def create_session(self, user_id=None):
        """creates and stores new instance of UserSession
            and returns the Session ID
        """
        # doesn’t return a Session ID and don’t create any UserSession
        # record in DB if user_id = None
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = super().create_session(user_id)
        new_user_session = UserSession()
        new_user_session.user_id = user_id
        new_user_session.session_id = session_id
        new_user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Returns a user ID based on a session ID
        Args:
            session_id (str): session ID
        Return:
            user id or None if session_id is None or not a string
        """
        user_id = UserSession.search({"session_id": session_id})
        if user_id:
            return user_id
        return None

    def destroy_session(self, request=None):
        """destroys the UserSession based on the Session
            ID from the request cookie
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        # check if request doesn’t contain the Session ID cookie
        if not session_id:
            return False
        user_session = UserSession.search({'session_id': session_id})
        # If the Session ID of the request is not linked to any User ID
        if not user_session:
            return False
        user_session[0].remove()
        return True
