# Import flask dependencies
from flask import Blueprint, request, render_template, \
    flash, g, session, redirect, url_for, make_response
from oauth2client.client import OAuth2WebServerFlow, Credentials
import httplib2
import json
import random
import requests
import string
import urllib
from pprint import pprint
from flask import session as login_session
from .. import db, google_secret
from model import User

# Define goolge oauth login


# Defind links and vars related to goolge oauth login
google_oauth = {
    'oauth_uri': 'https://accounts.google.com/o/oauth2/auth',
    'scope': 'openid email',
    'exchange_uri': 'https://www.googleapis.com/oauth2/v3/token',
    'userinfo_uri': 'https://www.googleapis.com/oauth2/v2/userinfo',
    'validate_uri': 'https://www.googleapis.com/oauth2/v1/tokeninfo'
}


# Define the blueprint: 'auth', set its url prefix: app.url/auth
auth = Blueprint('auth', __name__, url_prefix="/auth")


def make_state():
    """ Generate a random string for anti csrf
    """
    login_session['state'] = ''.join(
        random.choice(string.ascii_uppercase
                      + string.digits) for x in xrange(32))
    return login_session['state']


def delete_state():
    """ Reset the randome string for anti csrf
    """
    del login_session['state']


def get_user_info(user_id):
    """ Get user info by user id
    """
    user = db.session.query(User).filter(User.id == user_id).first()
    return user


def get_user_id(email):
    """ Get user's id by email
    """
    user = db.session.query(User).filter(User.email == email).first()
    pprint(user)
    if user is not None:
        return user.id
    else:
        return None


def create_user():
    """ For Creating user
    """
    try:
        user = User(name=login_session['username'], picture=login_session[
                    'picture'], email=login_session['email'])
        db.session.add(user)
        db.session.commit()
        flash('User created successfully!')
    except:
        db.session.rollback()
        flash('Failed to creat this user!', 'error')
    return get_user_id(login_session['email'])


def get_current_user():
    """ Get current user id
    """
    if login_session['user_id'] is not None:
        return get_user_id(login_session['user_id'])
    return None


@auth.route('/login')
def login():
    """ The endpoint for user to login
    """
    login_session['origin'] = request.referrer
    auth_params = {
        'response_type': 'code',
        'client_id': google_secret['client_id'],
        'redirect_uri': url_for('auth.callback', _external=True),
        'scope': google_oauth['scope'],
        'state': make_state()}
    auth_uri = google_oauth['oauth_uri']+'?' + urllib.urlencode(auth_params)
    return redirect(auth_uri)


@auth.route('/oauth2callback', methods=['POST', 'GET'])
def callback():
    """ For Google oauth login to call back and to process login process
    """
    pprint(login_session)
    # check data
    error = request.args.get('error')
    code = request.args.get('code').decode('utf-8')
    if (error is not None) or (code is None):
        return redirect('/')

    # check cross side attack
    if request.args.get('state') != login_session.get('state'):
        response = make_response(
            json.dumps('Unauthorized access.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

     # Upgrade the authorization code into a credentials object
    flow = OAuth2WebServerFlow(client_id=google_secret['client_id'],
                               client_secret=google_secret['client_secret'],
                               scope='openid email',
                               redirect_uri=url_for(
        'auth.callback', _external=True))

    try:
        credentials = flow.step2_exchange(code)
        access_token = credentials.access_token
    except:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # check access token is valid
    params = {'access_token': access_token}
    response = requests.get(google_oauth['validate_uri'], params=params)
    data = response.json()

    # 1.check error
    if data.get('error') is not None:
        response = make_response(
            json.dumps('Failed to validate access token.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # 2.check client id
    if data['issued_to'] != google_secret['client_id']:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # 3.check user id
    gplus_id = credentials.id_token['sub']
    if data['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # get user info
    params = {'access_token': access_token, 'alt': 'json'}
    answer = requests.get(google_oauth['userinfo_uri'], params=params)
    userinfo = answer.json()

    login_session['access_token'] = access_token
    login_session['gplus_id'] = gplus_id
    login_session['username'] = userinfo['name']
    login_session['picture'] = userinfo['picture']
    login_session['email'] = userinfo['email']

    # see if user exists, if it doesn't make a new one
    user_id = get_user_id(login_session['email'])
    if not user_id:
        user_id = create_user()
    login_session['user_id'] = user_id
    flash('You were successfully logged in.')

    pprint(userinfo)
    pprint(login_session)
    return redirect(login_session.get('origin'))


@auth.route('/logout')
def logout():
    """ For user to log out
    """
    login_session['origin'] = request.referrer
    #delete all user data
    del login_session['access_token']
    del login_session['gplus_id']
    del login_session['username']
    del login_session['picture']
    del login_session['email']
    del login_session['state']
    del login_session['user_id']
    flash('You were successfully logged out.')
    return redirect(login_session.get('origin'))
