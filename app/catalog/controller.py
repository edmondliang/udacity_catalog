# Import flask dependencies
from flask import Blueprint, request, render_template, \
    flash, g, session, redirect, url_for, abort, make_response, jsonify
from sqlalchemy import desc
from sqlalchemy.ext.serializer import loads, dumps
import json
from werkzeug.contrib.atom import AtomFeed
# Import the database object from the main app module
from app import db
from flask import session as login_session
from flask import current_app as APP
# Import module model
from app.catalog.model import Catalog, Item
# Import module forms
from app.catalog.form import CatalogForm, ItemForm, DeleteForm

from app.auth import controller as auth
from pprint import pprint

# Define the blueprint:
catalog = Blueprint('catalog', __name__)


# Make option list for catalog
def get_option():
    items = []
    for item in db.session.query(Catalog).all():
        items.append({'value': item.id, 'name': item.name})
    return items

# Set the route and accepted methods


@catalog.route('/')
@catalog.route('/catalog/')
def index():
    catalog_list = db.session.query(Catalog).all()
    item_list = db.session.query(Item.name.label('name'), Catalog.name.label(
        'catalog_name')).join(Catalog).order_by(desc(Item.date_modified)).all()
    return render_template('catalog/main_list.html', catalog=catalog_list, items=item_list)
    # try:
    #     return render_template('catalog/list.html',catalog=catalog_list)
    # except Exception, e:
    #     abort(404)


@catalog.route('/catalog/<catalog>/items')
def detail(catalog):
    catalog_list = db.session.query(Catalog).all()
    this_one = db.session.query(Catalog).filter(Catalog.name == catalog).one()
    return render_template('catalog/list.html', catalog=catalog_list, this_one=this_one)


@catalog.route('/catalog/<catalog>/<item>')
def item_detail(catalog, item):
    this_one = db.session.query(Item).join(Catalog).filter(
        Item.name == item).filter(Catalog.name == catalog).one()
    return render_template('catalog/item.html', item=this_one, catalog_name=catalog)


@catalog.route('/catalog/create', methods=['GET', 'POST'])
def create():
    user_id = login_session.get('user_id')
    if user_id is None:
        return redirect('/')
    form = CatalogForm(request.form)
    form_action = url_for('catalog.create')
    if request.method == 'POST' and form.validate():
        catalog = Catalog(name=form.name.data, user_id=user_id)
        db.session.add(catalog)
        db.session.commit()
        return redirect('/')
    return render_template('catalog/catalog_create.html', form_action=form_action, form=form)


@catalog.route('/catalog/<catalog>/edit', methods=['GET', 'POST'])
def edit(catalog):
    user_id = login_session.get('user_id')
    if user_id is None:
        return redirect('catalog.detail', catalog=catalog)
    this_one = db.session.query(Catalog).filter(
        Catalog.name == catalog).one()
    if not this_one:
        abort(404)

    if this_one.user_id != user_id:
        abort(401)

    form_action = url_for('catalog.edit', catalog=catalog)

    if request.method == 'GET':
        form = CatalogForm(obj=this_one)
        return render_template('catalog/catalog_edit.html', form_action=form_action, form=form)

    form = CatalogForm(request.form)
    if request.method == 'POST' and form.validate():
        form.populate_obj(this_one)
        db.session.merge(this_one)
        db.session.commit()
        return redirect('/')
    else:
        return redirect(request.path)


@catalog.route('/catalog/<catalog>/delete', methods=['GET', 'POST'])
def delete(catalog):
    user_id = login_session.get('user_id')
    if user_id is None:
        return redirect(url_for('catalog.detail', catalog=catalog))
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
            json.dumps('Forbidden to delete this catalog. Because there are some items created by other user included.'), 403)
        response.headers['Content-Type'] = 'application/json'
        return response

    form = DeleteForm(request.form)
    form_action = url_for('catalog.delete', catalog=catalog)
    if request.method == 'GET':
        return render_template('catalog/catalog_delete.html', form_action=form_action, form=form, catalog=catalog)

    if request.method == 'POST' and form.validate():
        pprint('begin delete')
        db.session.delete(this_one)
        db.session.commit()
        return redirect('/')
    else:
        return redirect(request.path)


# catalog items handling


@catalog.route('/catalog/item_create', methods=['GET', 'POST'])
def item_create():
    user_id = login_session.get('user_id')
    if user_id is None:
        return redirect('catalog.detail', catalog=catalog)

    form = ItemForm(request.form)
    form_action = url_for('catalog.item_create')
    if request.method == 'POST' and form.validate():
        item = Item(name=form.name.data, description=form.description.data,
                    catalog_id=form.catalog_id.data, user_id=user_id)
        db.session.add(item)
        db.session.commit()
        return redirect('/')
    return render_template('catalog/item_create.html', form_action=form_action, form=form)


@catalog.route('/catalog/<catalog>/<item>/edit', methods=['GET', 'POST'])
def item_edit(catalog, item):
    user_id = login_session.get('user_id')
    if user_id is None:
        return redirect('catalog.item_detail', catalog=catalog, item=item)

    this_one = db.session.query(Item).join(Catalog).filter(
        Item.name == item).filter(Catalog.name == catalog).one()

    if not this_one:
        abort(404)

    if this_one.user_id != user_id:
        abort(401)

    form_action = url_for('catalog.item_edit', catalog=catalog, item=item)

    if request.method == 'GET':
        form = ItemForm(obj=this_one)
        return render_template('catalog/item_edit.html', form_action=form_action, form=form)

    form = ItemForm(request.form)
    if request.method == 'POST' and form.validate():
        form.populate_obj(this_one)
        db.session.merge(this_one)
        db.session.commit()
        return redirect('/')
    else:
        return redirect(request.path)


@catalog.route('/catalog/<catalog>/<item>/delete', methods=['GET', 'POST'])
def item_delete(catalog, item):
    user_id = login_session.get('user_id')
    if user_id is None:
        return redirect('catalog.item_detail', catalog=catalog, item=item)

    this_one = db.session.query(Item).join(Catalog).filter(
        Item.name == item).filter(Catalog.name == catalog).one()

    if not this_one:
        abort(404)

    if this_one.user_id != user_id:
        abort(401)

    form = DeleteForm(request.form)
    form_action = url_for('catalog.item_delete', catalog=catalog, item=item)
    if request.method == 'GET':
        return render_template('catalog/item_delete.html', form_action=form_action, form=form, item=item)

    if request.method == 'POST' and form.validate():
        db.session.delete(this_one)
        db.session.commit()
        return redirect('/')
    else:
        return redirect(request.path)


@catalog.route('/catalog/json')
def json():
    return jsonify(json_list=[i.serialize for i in db.session.query(Catalog).all()])


@catalog.route('/catalog/rss')
def rss():
    feed = AtomFeed('Recent Articles',
                    feed_url=request.url, url=request.url_root)
    items = db.session.query(Item.name, Item.description,Item.date_modified, Catalog.name.label('catalog_name')).join(Catalog).order_by(Item.date_modified.desc()) \
                      .limit(15).all()
    for item in items:
        feed.add(item.name, unicode(item.description),
                 content_type='html',
                 url=url_for(
                     'catalog.item_detail', catalog=item.catalog_name, item=item.name),
                 updated=item.date_modified
                 )
    return feed.get_response()
