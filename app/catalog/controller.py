# Import flask dependencies
from flask import Blueprint, request, render_template, \
    flash, g, session, redirect, url_for, abort
from sqlalchemy import desc
# Import the database object from the main app module
from app import db
from flask import current_app as APP
# Import module model
from app.catalog.model import Catalog, Item
# Import module forms
from app.catalog.form import CatalogForm, ItemForm

from app.auth import controller as auth
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
    form = CatalogForm(request.form)
    form_action = url_for('catalog.create')
    if request.method == 'POST' and form.validate():
        catalog = Catalog(form.name.data)
        db.session.add(catalog)
        db.session.commit()
        return redirect('/')
    return render_template('catalog/catalog_create.html', form_action=form_action, form=form)


@catalog.route('/catalog/<catalog>/edit', methods=['GET', 'POST'])
def edit(catalog):
    this_one = db.session.query(Catalog).filter(
        Catalog.name == catalog).one()
    if not this_one:
        abort(404)

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
        redirect(request.endpoint)


@catalog.route('/catalog/<catalog>/delete', methods=['GET', 'POST'])
def delete(catalog):
    this_one = db.session.query(Catalog).filter(
        Catalog.name == catalog).one()
    if not this_one:
        abort(404)

    form_action = url_for('catalog.delete', catalog=catalog)
    if request.method == 'GET':
        return render_template('catalog/catalog_delete.html', form_action=form_action, catalog=catalog)

    if request.method == 'POST' and request.form['confirm']:
        db.session.delete(this_one)
        db.session.commit()
        return redirect('/')
    else:
        redirect(request.endpoint)


# catalog items handling


@catalog.route('/catalog/item_create', methods=['GET', 'POST'])
def item_create():
    form = ItemForm(request.form)
    form_action = url_for('catalog.item_create')
    if request.method == 'POST' and form.validate():
        item = Item(
            form.name.data, form.description.data, form.catalog_id.data)
        db.session.add(item)
        db.session.commit()
        return redirect('/')
    return render_template('catalog/item_create.html', form_action=form_action, form=form)


@catalog.route('/catalog/<catalog>/<item>/edit', methods=['GET', 'POST'])
def item_edit(catalog, item):
    this_one = db.session.query(Item).join(Catalog).filter(
        Item.name == item).filter(Catalog.name == catalog).one()

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
        redirect(request.endpoint)


@catalog.route('/catalog/<catalog>/<item>/delete', methods=['GET', 'POST'])
def item_delete(catalog, item):
    this_one = db.session.query(Item).join(Catalog).filter(
        Item.name == item).filter(Catalog.name == catalog).one()

    form_action = url_for('catalog.item_delete', catalog=catalog, item=item)
    if request.method == 'GET':
        return render_template('catalog/item_delete.html', form_action=form_action, item=item)

    if request.method == 'POST' and request.form['confirm']:
        db.session.delete(this_one)
        db.session.commit()
        return redirect('/')
    else:
        redirect(request.endpoint)
