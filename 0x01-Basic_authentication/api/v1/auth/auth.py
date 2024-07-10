#!/usr/bin/env python3

'''
This module contains the Auth class
'''

from api.v1.views import app_views
from typing import TypeVar, List
from flask import jsonify, abort, request


class Auth:
    '''
    Auth class

    Methods:
        - require_auth: returns False
        - authorization_header: returns None
        - current_user: returns None
    '''
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        '''
        This function returns False
        Args:
            path (str): [description]
            excluded_paths (List[str]): [description]
        '''
        if not path or not excluded_paths or excluded_paths == []:
            return True

        if not path.endswith('/'):
            path = path + '/'

        for exc in excluded_paths:
            if exc == path or path.startswith(exc.split('*')[0]):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        '''
        This function returns None
        Args:
            request ([type], optional): [description]. Defaults to None.
        Returns:
            str: [description]
        '''
        if not request:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        '''
        This function returns None
        Args:
            request ([type], optional): [description]. Defaults to None.
        Returns:
            TypeVar('User'): [description]
        '''
        return None
