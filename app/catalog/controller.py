# Import flask dependencies
from flask import Blueprint, request, render_template, \
    flash, g, session, redirect, url_for, abort

# Import the database object from the main app module
from app import db
from flask import current_app as APP
# Import module model
import app.catalog.model

# Define the blueprint:
catalog = Blueprint('catalog', __name__)

# fake data
catalog_list = [{'id': 1, 'name': 'catalog1', 'text': "321432"}, {
    'id': 2, 'name': 'catalog2', 'text': "321432"}]
catalog1 = {'id': 1, 'name': 'catalog1', 'text': "321432"}
items_array = [{'id': 1, 'name': 'item1', 'catalog_name': 'catalog1', 'text': '43214321421342314231'}, {
    'id': 2, 'name': 'item2', 'catalog_name': 'catalog1', 'text': '43214321421342314231'}]
item1 = {'id': 1, 'name': 'item1', 'catalog_name': 'catalog1',"catalog_id":1,
         'text': '43214321421342314231'}

items_array2 = [{'id': 1, 'name': '1111', 'catalog_name': 'catalog1', 'text': '43214321421342314231'}, {
    'id': 2, 'name': '2222', 'catalog_name': 'catalog1', 'text': '43214321421342314231'}]

# Make option list for catalog
def get_option():
    items=[]
    for item in catalog_list:
        items.append({'value':item['id'],'name':item['name']})
    return items

# Set the route and accepted methods
@catalog.route('/')
@catalog.route('/catalog/')
def index():
    return render_template('catalog/main_list.html', catalog=catalog_list, items=items_array)
    # try:
    #     return render_template('catalog/list.html',catalog=catalog_list)
    # except Exception, e:
    #     abort(404)


@catalog.route('/catalog/<catalog>/items')
def detail(catalog):
    return render_template('catalog/list.html', catalog=catalog_list, catalog_name='abc catalog', items=items_array2)


@catalog.route('/catalog/<catalog>/<item>')
def item_detail(catalog, item):
    return render_template('catalog/item.html', item=item1)


@catalog.route('/catalog/create')
def create():
    return render_template('catalog/catalog_create.html')


@catalog.route('/catalog/<catalog>/edit')
def edit(catalog):
    return render_template('catalog/catalog_edit.html', item=catalog1)


@catalog.route('/catalog/<catalog>/delete')
def delete(catalog):
    return render_template('catalog/catalog_delete.html', catalog=catalog1)


# catalog items handling


@catalog.route('/catalog/item_create')
def item_create():
    return render_template('catalog/item_create.html',option=get_option())


@catalog.route('/catalog/<catalog>/<item>/edit')
def item_edit(catalog, item):
    return render_template('catalog/item_edit.html',option=get_option(),catalog=catalog,item=item1)


@catalog.route('/catalog/<catalog>/<item>/delete')
def item_delete(catalog, item):
    return render_template('catalog/item_delete.html',catalog=catalog,item=item1)
