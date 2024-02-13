#!/usr/bin/env python3
""" Module of Auth the API authentication
"""
import re
from typing import List, TypeVar


class Auth:
    """Class Auth"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """require auth"""
        if path is None or excluded_paths is None or not excluded_paths:
            return True
        for p in excluded_paths:
            match = re.match(rf'{p}', path)
            if path == p or path == p.rstrip('/'):
                return False
            if match:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """authorization header"""
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """current user"""
        return None
