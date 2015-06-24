# Import Form and RecaptchaField (optional)
from flask.ext.wtf import Form  # , RecaptchaField
from wtforms import TextField, HiddenField, TextAreaField, \
    SelectField, BooleanField, FileField
from wtforms.validators import Required, EqualTo
from app import db
from model import Catalog, Item


class CatalogForm(Form):

    """ CatalogForm is for producing related fields in html
         and providing validation in submission
    """
    name = TextField(
        'Name', [Required(message='Please input the Catalog Name!')])
    id = HiddenField('ID')


class ItemForm(Form):

    """ ItemForm is for producing related fields in html
         and providing validation in submission
    """
    id = HiddenField('ID')
    name = TextField('Name', [Required(message='Please input the Item Name!')])
    description = TextAreaField('Description')
    catalog_id = SelectField('Catalog', coerce=int)
    image_file = FileField('File')

    def set_choices(self):
        self.catalog_id.choices = [(h.id, h.name)
                                   for h in db.session.query(Catalog).all()]

    def __init__(self, formdata=None, obj=None, prefix='', **kwargs):
        super(ItemForm, self).__init__(formdata, obj, prefix, **kwargs)
        self.set_choices()


class DeleteForm(Form):
    """ DeleteForm is for providing validation in submission
    """
    confirm = BooleanField('confirm')
