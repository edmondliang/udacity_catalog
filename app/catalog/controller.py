# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for

# Import the database object from the main app module
from app import db

# Define the blueprint: 'auth', set its url prefix: app.url/auth
catalog = Blueprint('catalog', __name__)
# Set the route and accepted methods
@catalog.route('/')
def index():
    return "Home page!"

@catalog.route('/catalog/')
def show():
    return "Catalog list page!"

@catalog.route('/catalog/<catalog>')
def detail(catalog):
    return "Catalog %s show " % (catalog,)

@catalog.route('/catalog/create')
def create():
    return "Catalog create!"

@catalog.route('/catalog/<catalog>/edit')
def edit(catalog):
        return "Catalog edit %s!" % (catalog,)

@catalog.route('/catalog/<catalog>/delete')
def delete(catalog):
    return "Catalog delete %s !" %(catalog,)



#catalog items handling
@catalog.route('/catalog/<catalog>/items')
def items(catalog):
    return "Catalog %s items show " % (catalog,)

@catalog.route('/catalog/<catalog>/<item>')
def item_detail(catalog,item):
    return "Catalog (%s) items <%s> show " % (catalog,item,)

@catalog.route('/catalog/<catalog>/create')
def item_create():
    return "Catalog create!"

@catalog.route('/catalog/<catalog>/<item>/edit')
def item_edit(catalog,item):
    return "Catalog(%s) edit %s!" % (catalog,item,)

@catalog.route('/catalog/<catalog>/<item>/delete')
def item_delete(catalog,item):
    return "Catalog(%s) delete %s !" %(catalog,item,)
