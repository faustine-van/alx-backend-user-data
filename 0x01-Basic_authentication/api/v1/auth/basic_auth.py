#!/usr/bin/env python3
""" Module of Auth the API authentication
"""
from typing import TypeVar
import base64
import binascii
from api.v1.auth.auth import Auth
from models.user import User


class BasicAuth(Auth):
    """class inherits from Auth class"""
    def extract_base64_authorization_header(self, authorization_header: str
                                            ) -> str:
        """extract base 64"""
        if authorization_header is None or not isinstance(authorization_header,
                                                          str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header.lstrip('Basic ')

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """extract base 64"""
        if base64_authorization_header is None or not isinstance(
                base64_authorization_header,
                str):
            return None
        try:
            base64.b64decode(base64_authorization_header, validate=True)
        except binascii.Error:
            return None
        # converts base64_authorization_header into bytes using UTF-8 encoding
        bytes_64 = base64_authorization_header.encode('utf-8')
        # decodes the Base64-encoded bytes obtained
        decode_64 = base64.b64decode(bytes_64)
        # converts the decoded bytes back to a string using UTF-8 decoding
        res = decode_64.decode('utf-8')
        return res

    def extract_user_credentials(self, decoded_base64_authorization_header: str
                                 ) -> str:
        """extract user email and password"""
        if decoded_base64_authorization_header is None or not isinstance(
                decoded_base64_authorization_header,
                str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        return tuple(decoded_base64_authorization_header.split(':'))

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """eturns the User instance based on his email and password."""
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        # search user matching  with email
        users_with_email = User.search({'email': user_email})
        # check if user exists or not
        if not users_with_email or users_with_email is None:
            return None
        # check if password match
        for user in users_with_email:
            if user.is_valid_password(user_pwd):
                return user
        # If no user found with matching password
        return None
