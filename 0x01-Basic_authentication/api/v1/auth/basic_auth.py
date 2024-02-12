#!/usr/bin/env python3
""" Module of Auth the API authentication
"""
import base64
import binascii
from api.v1.auth.auth import Auth


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
