#!/usr/bin/env python3

'''
This module contains the main Flask app
'''

import requests
from auth import Auth


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"
BASE_URL = "http://127.0.0.1:5000"


def register_user(email: str, password: str) -> None:
    '''
    This function should assert the correct response to
    registering a user with a specified email and password.
    Args:
        email: string type
        password: string type
    Returns:
        None
    '''
    pass


def log_in_wrong_password(email: str, password: str) -> None:
    '''
    This function should assert the correct response to
    logging in with a specified email and password.
    Args:
        email: string type
        password: string type
    Returns:
        None
    '''
    pass


def profile_unlogged() -> None:
    '''
    This function should assert the correct response to
    the profile endpoint without a session ID.
    Returns:
        None
    '''
    pass


def log_in(email: str, password: str) -> str:
    '''
    This function should assert the correct response to
    logging in with a specified email and password.
    Args:
        email: string type
        password: string type
    Returns:
        str: the session ID
    '''
    return None


def profile_logged(session_id: str) -> None:
    '''
    This function should assert the correct response to
    the profile endpoint with a specified session ID.
    Args:
        session_id: string type
    Returns:
        None
    '''
    pass


def log_out(session_id: str) -> None:
    '''
    This function should assert the correct response to
    logging out with a specified session ID.
    Args:
        session_id: string type
    Returns:
        None
    '''
    pass


def reset_password_token(email: str) -> str:
    '''
    This function should assert the correct response to
    getting a reset password token with a specified email.
    Args:
        email: string type
    Returns:
        str: the reset token
    '''
    return None


def update_password(email: str, reset_token: str, new_password: str) -> None:
    '''
    This function should assert the correct response to
    updating a password with a specified email, reset token,
    and new password.
    Args:
        email: string type
        reset_token: string type
        new_password: string typ
    Returns:
        None
    '''
    pass


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
