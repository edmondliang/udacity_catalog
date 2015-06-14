# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for

# Import the database object from the main app module
from app import db

# Define the blueprint: 'auth', set its url prefix: app.url/auth
auth = Blueprint('auth', __name__,url_prefix="/auth")
# Set the route and accepted methods
@auth.route('/login')
def index():
    return "Login!"

@auth.route('/logout')
def show():
    return "Logout!"




