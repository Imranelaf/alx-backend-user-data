#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os

app = Flask(__name__)
app.register_blueprint(app_views)
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None
# Check authentication type
auth_type = getenv('AUTH_TYPE')
if auth_type == 'auth':
    from api.v1.auth.auth import Auth
    auth = Auth()
if auth_type == 'basic_auth':
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()
if auth_type == 'session_auth':
    from api.v1.auth.session_auth import SessionAuth
    auth = SessionAuth()
if auth_type == 'session_exp_auth':
    from api.v1.auth.session_exp_auth import SessionExpAuth
    auth = SessionExpAuth()
if auth_type == 'session_db_auth':
    from api.v1.auth.session_db_auth import SessionDBAuth
    auth = SessionDBAuth()


@app.errorhandler(404)
def not_found(error) -> str:
    '''
    This function returns a JSON-formatted 404 status code response.
    Returns:
        str: JSON-formatted 404 status code response.
    '''
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    '''
    This function returns a JSON-formatted 401 status code response.
    Returns:
        str: JSON-formatted 401 status code response.
    '''
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error):
    '''
    This function returns a JSON-formatted 403 status code response.
    Returns:
        str: JSON-formatted 403 status code response.
    '''
    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def before_request():
    '''
    This function checks if a request is authorized to access a route.
    Returns:
        None
    '''
    if not auth:
        return
    if not auth.require_auth(request.path, ['/api/v1/status/',
                                            '/api/v1/unauthorized/',
                                            '/api/v1/forbidden/',
                                            '/api/v1/auth_session/login/']):
        return

    sess_coo = auth.session_cookie(request)
    authen_hdr = auth.authorization_header(request)
    if not sess_coo and not authen_hdr:
        abort(401)

    # Check if current user is authorized to access the route
    currUser = auth.current_user(request)
    if not currUser:
        abort(403)
    setattr(request, "current_user", currUser)


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port, debug=True)
