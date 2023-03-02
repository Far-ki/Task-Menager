from flask import Blueprint

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return "<p>Login</p>"

@auth.route('/logout')
def sign_up():
    return "<p>Sign up </p>"