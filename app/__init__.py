from flask import Flask, render_template
import os
# Import SQLAlchemy
from flask.ext.sqlalchemy import SQLAlchemy

import json
# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(APP_ROOT,'../','client_secret.json')) as data_file:
    data = json.load(data_file)
    google_secret = data.get('web')


# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

# Import a module / component using its blueprint handler variable (mod_auth)
from .auth.controller import auth
from .catalog.controller import catalog

# Register blueprint(s)
app.register_blueprint(auth)
app.register_blueprint(catalog)

# app.register_blueprint(xyz_module)
# ..

# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()
