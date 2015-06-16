# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for,abort

# Import the database object from the main app module
from app import db
from flask import current_app as APP
# Import module model
import app.catalog.model

# Define the blueprint: 
catalog = Blueprint('catalog', __name__)

#fake data
catalog_list= [{'id':1, 'name':'catalog1', 'text':"321432"},{'id':2, 'name':'catalog2', 'text':"321432"}]
catalog1={'id':1, 'name':'catalog1', 'text':"321432"}
items_array=[{'id':1,'name':'item1','catalog_name':'catalog1','text':'43214321421342314231'},{'id':2,'name':'item2','catalog_name':'catalog1','text':'43214321421342314231'}]
item1={'id':1,'name':'item1','catalog_name':'catalog1','text':'43214321421342314231'}

items_array2=[{'id':1,'name':'1111','catalog_name':'catalog1','text':'43214321421342314231'},{'id':2,'name':'2222','catalog_name':'catalog1','text':'43214321421342314231'}]


# Set the route and accepted methods
@catalog.route('/')
@catalog.route('/catalog/')
def index():
    return render_template('catalog/main_list.html',catalog=catalog_list,items=items_array)
    # try:
    #     return render_template('catalog/list.html',catalog=catalog_list)
    # except Exception, e:
    #     abort(404)

@catalog.route('/catalog/<catalog>/items')
def detail(catalog):
    return render_template('catalog/list.html',catalog=catalog_list,catalog_name='abc catalog',items=items_array2)

@catalog.route('/catalog/<catalog>/<item>')
def item_detail(catalog,item):
    return render_template('catalog/item.html',item=item1)


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



@catalog.route('/catalog/<catalog>/create')
def item_create():
    return "Catalog create!"

@catalog.route('/catalog/<catalog>/<item>/edit')
def item_edit(catalog,item):
    return "Catalog(%s) edit %s!" % (catalog,item,)

@catalog.route('/catalog/<catalog>/<item>/delete')
def item_delete(catalog,item):
    return "Catalog(%s) delete %s !" %(catalog,item,)
