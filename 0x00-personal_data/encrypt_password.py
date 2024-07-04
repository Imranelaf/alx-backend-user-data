#!/usr/bin/env python3

'''
This module contains the following:
- hash_password
- is_valid
'''

import bcrypt


def hash_password(password: str) -> bytes:
    '''
    Returns a salted, hashed password, which is a byte string.
    Args:
        password: a string argument.
    Returns:
        A byte string.
    '''
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    '''
    Returns a boolean value.
    Args:
        hashed_password: a byte string argument.
        password: a string argument.
    Returns:
        A boolean value.
    '''
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)
