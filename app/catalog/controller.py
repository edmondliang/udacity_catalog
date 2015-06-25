# Import flask dependencies
from flask import Blueprint, request, render_template, \
    flash, g, session, redirect, url_for, abort, make_response, jsonify
from sqlalchemy import desc
from sqlalchemy.ext.serializer import loads, dumps
import os
import json
from werkzeug.contrib.atom import AtomFeed
from werkzeug import secure_filename
from app import db
from flask import session as login_session
from flask import current_app as APP
# Import module model
from app.catalog.model import Catalog, Item
from app.catalog.form import CatalogForm, ItemForm, DeleteForm

from app.auth import controller as auth
from pprint import pprint
from functools import wraps

# Define the blueprint:
catalog = Blueprint('catalog', __name__)


def allowed_image_file(filename):
    """ Define accepted file formats """
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def upload_file(file):
    """ Upload process
        arguments:
        file= request.files['file_field']
    """
    if file and allowed_image_file(file.filename):
        pprint('end checking.')
        filename = secure_filename(file.filename)
        file.save(os.path.join(APP.config['UPLOAD_FOLDER'], filename))
        return url_for('static', filename='upload/'+filename)


def login_require(f):
    """ Login decorator for login process  """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = login_session.get('user_id')
        if user_id is None:
            abort(401)
        return f(*args, **kwargs)
    return decorated_function


@catalog.route('/')
@catalog.route('/catalog/')
def index():
    """ Index page for website entrance """

    catalog_list = db.session.query(Catalog).all()
    item_list = db.session.query(Item.name.label('name'), Catalog.name.label(
        'catalog_name')).join(Catalog).order_by(desc(Item.date_modified)).all()
    return render_template('catalog/main_list.html',
                           catalog=catalog_list, items=item_list)


@catalog.route('/catalog/<string:catalog>/items')
def detail(catalog):
    """ Catalog page for managing catalog infomation
        arguments:
        catalog :  catalog name

    """

    catalog_list = db.session.query(Catalog).all()
    this_one = db.session.query(Catalog).filter(Catalog.name == catalog).one()
    return render_template('catalog/list.html',
                           catalog=catalog_list, this_one=this_one)


@catalog.route('/catalog/<string:catalog>/<string:item>')
def item_detail(catalog, item):
    """ Items in Catalog page for managing item infomation
        arguments:
        catalog :  catalog name
        item    :  item name

    """
    this_one = db.session.query(Item).join(Catalog).filter(
        Item.name == item).filter(Catalog.name == catalog).one()
    return render_template('catalog/item.html',
                           item=this_one, catalog_name=catalog)


@catalog.route('/catalog/create', methods=['GET', 'POST'])
@login_require
def create():
    """ For creating catalog
    """
    user_id = login_session.get('user_id')
    form = CatalogForm(request.form)
    form_action = url_for('catalog.create')
    if request.method == 'POST' and form.validate():
        try:
            catalog = Catalog(name=form.name.data, user_id=user_id)
            db.session.add(catalog)
            db.session.commit()
            flash('Catalog created successfully!')
        except:
            db.session.rollback()
            flash('Failed to create this catalog.', 'error')
        return redirect('/')
    return render_template('catalog/catalog_create.html',
                           form_action=form_action, form=form)


@catalog.route('/catalog/<string:catalog>/edit', methods=['GET', 'POST'])
@login_require
def edit(catalog):
    """ For modifying catalog
        arguments:
        catalog : catalog name
    """
    user_id = login_session.get('user_id')
    this_one = db.session.query(Catalog).filter(
        Catalog.name == catalog).one()
    if not this_one:
        abort(404)

    if this_one.user_id != user_id:
        abort(401)

    form_action = url_for('catalog.edit', catalog=catalog)

    if request.method == 'GET':
        form = CatalogForm(obj=this_one)
        return render_template('catalog/catalog_edit.html',
                               form_action=form_action, form=form)

    form = CatalogForm(request.form)
    if request.method == 'POST' and form.validate():
        try:
            form.populate_obj(this_one)
            db.session.merge(this_one)
            db.session.commit()
            flash('Catalog updated successfully!')
        except:
            db.session.rollback()
            flash('Failed to updated this catalog!', 'error')
        return redirect('/')
    else:
        return redirect(request.path)


@catalog.route('/catalog/<string:catalog>/delete', methods=['GET', 'POST'])
@login_require
def delete(catalog):
    """ For deleting catalog
        arguments:
        catalog : catalog name
    """
    user_id = login_session.get('user_id')
    this_one = db.session.query(Catalog).filter(
        Catalog.name == catalog).one()
    if not this_one:
        abort(404)

    if this_one.user_id != user_id:
        abort(401)

    other_items_count = db.session.query(Item).join(Catalog).filter(
        Catalog.name == catalog).filter(Item.user_id != user_id).count()

    if other_items_count > 0:
        response = make_response(
            json.dumps("""Forbidden to delete this catalog. Because there 
                are some items created by other user included."""), 403)
        response.headers['Content-Type'] = 'application/json'
        return response

    form = DeleteForm(request.form)
    form_action = url_for('catalog.delete', catalog=catalog)
    if request.method == 'GET':
        return render_template('catalog/catalog_delete.html',
                               form_action=form_action,
                               form=form,
                               catalog=catalog)

    if request.method == 'POST' and form.validate():
        pprint('begin delete')
        try:
            db.session.delete(this_one)
            db.session.commit()
            flash('Catalog deleted successfully!')
        except:
            db.session.rollback()
            flash('Failed to delete this catalog!', 'error')
        return redirect('/')
    else:
        return redirect(request.path)


@catalog.route('/catalog/item_create', methods=['GET', 'POST'])
@login_require
def item_create():
    """ For creating item
    """

    user_id = login_session.get('user_id')
    form = ItemForm(request.form)
    form_action = url_for('catalog.item_create')
    if request.method == 'POST' and form.validate():
        try:
            filename = upload_file(request.files['image_file'])
            pprint(form.image_file)
            item = Item(name=form.name.data,
                        description=form.description.data,
                        catalog_id=form.catalog_id.data,
                        user_id=user_id,
                        filename=filename)
            db.session.add(item)
            db.session.commit()
            flash('Item created successfully!')
        except:
            db.session.rollback()
            flash('Failed to create this item!', 'error')
        return redirect('/')
    return render_template('catalog/item_create.html',
                           form_action=form_action, form=form)

# Modify item


@catalog.route('/catalog/<string:catalog>/<string:item>/edit',
               methods=['GET', 'POST'])
@login_require
def item_edit(catalog, item):
    """ For modifying item
        arguments:
        catalog : catalog name
        item    : item name
    """
    user_id = login_session.get('user_id')
    this_one = db.session.query(Item).join(Catalog).filter(
        Item.name == item).filter(Catalog.name == catalog).one()

    if not this_one:
        abort(404)

    if this_one.user_id != user_id:
        abort(401)

    form_action = url_for('catalog.item_edit', catalog=catalog, item=item)

    if request.method == 'GET':
        form = ItemForm(obj=this_one)
        return render_template('catalog/item_edit.html',
                               form_action=form_action, form=form)

    form = ItemForm(request.form)
    if request.method == 'POST' and form.validate():
        try:
            filename = upload_file(request.files['image_file'])
            form.populate_obj(this_one)
            this_one.filename = filename
            db.session.merge(this_one)
            db.session.commit()
            flash('Item updated successfully!')
        except:
            db.session.rollback()
            flash('Failed to update this item!', 'error')
        return redirect('/')
    else:
        return redirect(request.path)


@catalog.route('/catalog/<string:catalog>/<string:item>/delete',
               methods=['GET', 'POST'])
@login_require
def item_delete(catalog, item):
    """ for deleting item
        arguments:
        catalog : catalog name
        item    : item name
    """
    user_id = login_session.get('user_id')
    this_one = db.session.query(Item).join(Catalog).filter(
        Item.name == item).filter(Catalog.name == catalog).one()

    if not this_one:
        abort(404)

    if this_one.user_id != user_id:
        abort(401)

    form = DeleteForm(request.form)
    form_action = url_for('catalog.item_delete', catalog=catalog, item=item)
    if request.method == 'GET':
        return render_template('catalog/item_delete.html',
                               form_action=form_action, form=form, item=item)

    if request.method == 'POST' and form.validate():
        try:
            db.session.delete(this_one)
            db.session.commit()
            flash('Item deleted successfully!')
        except:
            db.session.rollback()
            flash('Failed to delete this item!', 'error')
        return redirect('/')
    else:
        return redirect(request.path)


@catalog.route('/catalog/json')
def json():
    """ For providing JSON data to user
    """
    json_data = db.session.query(Catalog).all()
    return jsonify(json_list=[i.serialize for i in json_data])


@catalog.route('/catalog/rss')
def rss():
    """ For providing RSS data to user
    """
    feed = AtomFeed('Recent Articles',
                    feed_url=request.url, url=request.url_root)
    items = db.session.query(Item.name,
                             Item.description,
                             Item.date_modified,
                             Catalog.name.label('catalog_name')) \
        .join(Catalog).order_by(Item.date_modified.desc()).limit(15).all()
    for item in items:
        feed.add(item.name, unicode(item.description),
                 content_type='html',
                 url=url_for(
                     'catalog.item_detail',
                     catalog=item.catalog_name,
                     item=item.name),
                 updated=item.date_modified
                 )
    return feed.get_response()
