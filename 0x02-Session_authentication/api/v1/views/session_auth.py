#!/usr/bin/env python3
""" Session authentication route module
"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'],
                 strict_slashes=False)
def login():
    """ Session authentication route
        POST parameters:
            - email: user's email
            - password: user's password
        Returns - response with user details and session cookie
    """
    eml = request.form.get('email')
    passwd = request.form.get('password')
    if not eml:
        return jsonify({"error": "email missing"}), 400
    if not passwd:
        return jsonify({"error": "password missing"}), 400
    all_users = User.search({"email": eml})
    if not all_users:
        return jsonify({"error": "no user found for this email"}), 404
    current_user = None
    for usR in all_users:
        if usR.is_valid_password(passwd):
            current_user = usR
            break
    if not current_user:
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth
    sess_id = auth.create_session(usR.id)
    res = make_response(jsonify(usR.to_json()), 200)
    res.set_cookie(getenv('SESSION_NAME'), sess_id)
    return res


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def logout():
    '''
    This function logs out a user by destroying their session.
    Returns:
        JSON-formatted 200 status code response.
    '''
    from api.v1.app import auth
    sts = auth.destroy_session(request)
    if not sts:
        abort(404)
    return jsonify({}), 200
