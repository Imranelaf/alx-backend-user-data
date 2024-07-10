#!/usr/bin/env python3

'''
This module contains the BasicAuth class
'''

from typing import TypeVar
from models.user import User
from .auth import Auth
import base64


class BasicAuth(Auth):
    '''
    BasicAuth class
    Methods:
        - extract_base64_authorization_header: returns None
        - decode_base64_authorization_header: returns None
        - extract_user_credentials: returns None
        - user_object_from_credentials: returns None
        - current_user: returns None
    '''
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        '''
        returns the Base64 part of the Authorization header for a Basic
        Args:
            authorization_header (str): [description]
        Returns:
            str: [description]
        '''
        if (authorization_header is None or
            type(authorization_header) is not str or
                not authorization_header.startswith("Basic ")):
            # print(authorization_header)
            return None
        return (authorization_header[6:])

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        '''
        returns the decoded value of a Base64 string
        Args:
            base64_authorization_header (str): [description]
        Returns:
            str: [description]
        '''
        if (base64_authorization_header is None or
                type(base64_authorization_header) is not str):
            return None
        try:
            return base64.b64decode(base64_authorization_header).decode()
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        '''
        returns the user email and password from the Base64 decoded value
        Args:
            decoded_base64_authorization_header (str): [description]
        Returns:
            (str, str): [description]
        '''
        if (decoded_base64_authorization_header is None or
            type(decoded_base64_authorization_header) is not str or
                ":" not in decoded_base64_authorization_header):
            return None, None
        return decoded_base64_authorization_header.split(':', 1)

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        '''
        returns the User instance based on his email and password
        Args:
            user_email (str): [description]
            user_pwd (str): [description]
        Returns:
            TypeVar('User'): [description]
        '''
        if (user_email is None or
            type(user_email) is not str or
                type(user_pwd) is not str):
            return None
        if (User.search({'email': user_email})):
            all_usrs = User.search({'email': user_email})
            for usr in all_usrs:
                if usr.is_valid_password(user_pwd):
                    return usr
                return None

    def current_user(self, request=None) -> TypeVar('User'):
        '''
        returns the User instance based on his email and password
        Args:
            request ([type], optional): [description]. Defaults to None.
        Returns:
            TypeVar('User'): [description]
        '''
        rw_hdr = self.authorization_header(request)
        bs_64 = self.extract_base64_authorization_header(rw_hdr)
        dcdd = self.decode_base64_authorization_header(bs_64)
        ready_data = self.extract_user_credentials(dcdd)
        return self.user_object_from_credentials(*ready_data)
