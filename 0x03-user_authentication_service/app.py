#!/usr/bin/env python3

'''
This module contains the main Flask app
'''

from flask import abort, redirect, Flask, jsonify, request

from auth import Auth


app = Flask(__name__)
app.url_map.strict_slashes = False

AUTH = Auth()


@app.route('/')
def hello():
    '''
    basepath: GET /
    Return: a welcome message
    '''
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users():
    '''
    basepath: POST /users
    Return: a message
    '''
    mail = request.form.get('email')
    passwd = request.form.get('password')
    try:
        AUTH.register_user(mail, passwd)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400
    return jsonify({"email": mail, "message": "user created"}), 200


@app.route('/sessions', methods=['POST'])
def login():
    '''
    basepath: POST /sessions
    Return: a message
    '''
    mail = request.form.get('email')
    psswd = request.form.get('password')
    if not AUTH.valid_login(mail, psswd):
        abort(401)
    session_id = AUTH.create_session(mail)
    resp = jsonify({"email": mail, "message": "logged in"})
    resp.set_cookie("session_id", session_id)
    return resp, 200


@app.route('/sessions', methods=['DELETE'])
def logout():
    '''
    basepath: DELETE /sessions
    Return: a message
    '''
    sessID = request.cookies.get('session_id')
    hmhle = AUTH.get_user_from_session_id(session_id=sessID)
    if hmhle:
        AUTH.destroy_session(hmhle.id)
        return redirect('/')
    abort(403)


@app.route('/profile', methods=['GET'])
def profile():
    '''
    basepath: GET /profile
    Return: a message
    '''
    sessID = request.cookies.get('session_id')
    usr = AUTH.get_user_from_session_id(session_id=sessID)
    if usr:
        return jsonify({"email": usr.email})
    abort(403)


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token():
    '''
    basepath: POST /reset_password
    Return: a message
    '''
    mail = request.form.get('email')
    try:
        tkn = AUTH.get_reset_password_token(mail)
    except ValueError:
        abort(403)
    return jsonify(
        {"email": mail, "reset_token": tkn}
        ), 200


@app.route('/reset_password', methods=['PUT'])
def update_password():
    '''
    basepath: PUT /reset_password
    Return: a message
    '''
    mail = request.form.get('email')
    rst_tkn = request.form.get('reset_token')
    npass = request.form.get('new_password')
    try:
        AUTH.update_password(rst_tkn, npass)
    except ValueError:
        abort(403)
    return jsonify({"email": mail, "message": "Password updated"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
