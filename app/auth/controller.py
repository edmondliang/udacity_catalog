# Import flask dependencies
from flask import Blueprint, request, render_template, \
    flash, g, session, redirect, url_for, make_response
import httplib2
from oauth2client.client import OAuth2WebServerFlow, Credentials, \
    FlowExchangeError

import json
import requests
from pprint import pprint

# Import the database object from the main app module
from app import db,google_secret



flow = OAuth2WebServerFlow(client_id=google_secret[u'web'][u'client_id'],
    client_secret = google_secret[u'web'][u'client_secret'],
    scope = u'https://www.googleapis.com/auth/userinfo.profile',
    redirect_uri = u'http://127.0.0.1:5000/auth/oauth2callback')



# Define the blueprint: 'auth', set its url prefix: app.url/auth
auth = Blueprint('auth', __name__, url_prefix="/auth")
# Set the route and accepted methods


@auth.route('/login')
def login():
    auth_uri = flow.step1_get_authorize_url()
    return redirect(auth_uri)


@auth.route('/oauth2callback')
def callback():
    print request.args.get('code')
    cred = flow.step2_exchange(request.args.get('code'), httplib2.Http())
    access_token = cred.access_token

    userinfo_url = "https://www.googleapis.com/oauth2/v2/userinfo"
    params = {'access_token': cred.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = answer.json()
    return data['name']


@auth.route('/logout')
def show():
    return "Logout!"
