# Import the database object (db) from the main application module
from app import db
from sqlalchemy.orm import relationship, backref
from sqlalchemy import desc, UniqueConstraint
# Define model


class Item(db.Model):

    """ The Item model is for storing item information
    """
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text())
    filename = db.Column(db.String(255))
    catalog_id = db.Column(
        db.Integer, db.ForeignKey("catalogs.id",
                                  ondelete=u"CASCADE"), nullable=False)
    catalog = relationship("Catalog")
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = relationship("User")
    date_created = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,
                              default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

    def __repr__(self):
        """ Provide information when access instance
        """
        return '<Item %s,%s,%s,%s>' % (self.id, self.name,
                                       self.filename, self.catalog_id)

    # for making JSON
    @property
    def serialize(self):
        """ Provide data for producing JSON format
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }


class Catalog(db.Model):

    """The Catalog model is for storing catalog information
    """
    __tablename__ = 'catalogs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    items = relationship(
        "Item", cascade="delete, delete-orphan", backref="Catalog")
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = relationship("User")
    date_created = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,
                              default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

    def __repr__(self):
        """ Provide information when access instance
        """
        return '<Catalog %s,%s,%s,%s>' % (self.id, self.name,
                                          self.date_created,
                                          self.date_modified)
    # for making JSON

    @property
    def serialize(self):
        """ Provide data for producing JSON format
        """
        return {
            'id': self.id,
            'name': self.name,
            'items': [i.serialize for i in self.items]
        }
