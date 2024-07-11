#!/usr/bin/env python3from typing import Optional, Tuple, TypeVar

"""
Basic authentication module
"""
import binascii
from base64 import b64decode
from models.user import User
from typing import Optional, Tuple, TypeVar
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    '''
    BasicAuth class
    '''
    def extract_base64_authorization_header(self,
                                            authorization_header: str) \
            -> Optional[str]:
        '''
        Extracts base64 authorization string
        Returns:
            - Base64 authorization string
        '''
        if authorization_header is None or \
            type(authorization_header) is not str or \
                not authorization_header.startswith("Basic "):
            return None
        return authorization_header.split()[1]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str) \
            -> Optional[str]:
        '''
        Decodes base64 authorization string
        Returns:
            - Decoded authorization string
        '''
        if not base64_authorization_header or \
                type(base64_authorization_header) is not str:
            return None
        try:
            authenstr = b64decode(base64_authorization_header, validate=True)
        except binascii.Error:
            return None
        else:
            return authenstr.decode('utf-8')

    def extract_user_credentials(self,
                                 decode_base64_authorization_header: str) \
            -> Tuple[Optional[str], Optional[str]]:
        '''
        Extracts user credentials
        Returns:
            - Tuple of user email and password
        '''
        if not decode_base64_authorization_header or \
                type(decode_base64_authorization_header) is not str or \
                ":" not in decode_base64_authorization_header:
            return None, None
        eml, passwd = decode_base64_authorization_header.split(":", maxsplit=1)
        return eml, passwd

    def user_object_from_credentials(self, user_email: str, user_pwd: str) \
            -> TypeVar('User'):
        '''
        Gets user object from credentials
        Returns:
            - User object
        '''
        if not user_email or type(user_email) is not str:
            return None
        if not user_pwd or type(user_pwd) is not str:
            return None

        try:
            all_usrs = User.search(attributes={"email": user_email})
        # Exception from passing unknown s_class to DATA
        # Check module base.py lines 12 and 125-137(instance method
        # 'search')
        except KeyError:
            return None

        if not all_usrs:
            return None
        for user in all_usrs:
            if user.is_valid_password(user_pwd):
                return user

    def current_user(self, request=None) -> TypeVar('User'):
        '''
        Gets current user
        Args:
            request (TypeVar('Request')): request object
        Returns:
            TypeVar('User'): current user
        '''
        auheader = self.authorization_header(request)
        b64str = self.extract_base64_authorization_header(auheader)
        dcd64 = self.decode_base64_authorization_header(b64str)
        ml, passwd = self.extract_user_credentials(dcd64)
        usr = self.user_object_from_credentials(ml, passwd)
        return usr
