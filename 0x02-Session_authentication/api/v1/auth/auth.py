#!/usr/bin/env python3
"""
Authentication module for API
"""
from typing import Any, List, TypeVar, Optional
from os import getenv
from flask import request


class Auth:
    '''
    Auth class
    '''
    def require_auth(self, pth: str, excluded_paths: List[str]) -> bool:
        '''
        Requires authentication
        Args:
            path (str): path
            excluded_paths (List[str]): excluded paths
        Returns:
            bool: True if authentication is required, False otherwise
        '''
        if not excluded_paths or not pth:
            return True
        pth = pth if pth.endswith('/') else pth + '/'
        for exl_pth in excluded_paths:
            if pth.startswith(exl_pth.strip("*")):
                return False
        return True

    def authorization_header(self, request=None) -> Optional[str]:
        '''
        Gets authorization header
        Args:
            request (TypeVar('Request')): request object
        Returns:
            Optional[str]: authorization header
        '''
        if not request or 'Authorization' not in request.headers:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        '''
        Gets current user
        Args:
            request (TypeVar('Request')): request object
        Returns:
            TypeVar('User'): current user
        '''
        return None

    def session_cookie(self, request=None) -> Any:
        '''
        Gets session cookie
        Args:
            request (TypeVar('Request')): request object
        Returns:
            Any: session cookie
        '''
        if not request:
            return None
        sess_coo = request.cookies.get(getenv('SESSION_NAME'))
        return sess_coo
