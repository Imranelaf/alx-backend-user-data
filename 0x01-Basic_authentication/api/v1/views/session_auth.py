#!/usr/bin/env python3
""" Module of Session views
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session() -> str:
    """ GET /api/v1/status
    Return:
      - the status of the API
    """
    user_email = request.form.get("email")
    user_pwd = request.form.get("password")
    if not user_email or user_email == '':
        return (jsonify({"error": "email missing"}), 400)
    if not user_pwd or user_pwd == "":
        return (jsonify({"error": "password missing"}), 400)

    user = User.search({'email': user_email})
    if not user:
        return jsonify({"error": "no user found for this email"}), 404
    if (User.search({'email': user_email})):
        users = User.search({'email': user_email})
        for user in users:
            if user.is_valid_password(user_pwd):

                from api.v1.app import auth

                session_id = auth.create_session(user.id)
                # jsonify returns a Response object, so capture it
                # before returning from your view and add the cookie
                # then with Response.set_cookie.
                resp = jsonify(user.to_json())
                session_name = getenv('SESSION_NAME')
                resp.set_cookie(session_name, session_id)
                return resp

        return jsonify({"error": "wrong password"}), 401


@app_views.route('/auth_session/logout', methods=["DELETE"],
                 strict_slashes=False)
def logout_session():
    """ delete the Session ID contained in the request as cookie
    """
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
