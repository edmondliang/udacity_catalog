# Import Form and RecaptchaField (optional)
from flask.ext.wtf import Form  # , RecaptchaField

# Import Form elements such as TextField and BooleanField (optional)
# BooleanField
from wtforms import TextField, HiddenField, TextAreaField, SelectField, BooleanField

# Import Form validators
from wtforms.validators import Required, EqualTo

from app import db
from model import Catalog, Item

# Define the login form (WTForms)


class CatalogForm(Form):
    name = TextField(
        'Name', [Required(message='Please input the Catalog Name!')])
    id = HiddenField('ID')


class ItemForm(Form):
    id = HiddenField('ID')
    name = TextField('Name', [Required(message='Please input the Item Name!')])
    description = TextAreaField('Description')
    catalog_id = SelectField('Catalog', coerce=int)

    def set_choices(self):
        self.catalog_id.choices = [(h.id, h.name)
                                   for h in db.session.query(Catalog).all()]

    def __init__(self, formdata=None, obj=None, prefix='', **kwargs):
        super(ItemForm, self).__init__(formdata, obj, prefix, **kwargs)
        self.set_choices()


class DeleteForm(Form):
    confirm = BooleanField('confirm')

