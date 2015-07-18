# Import the database object (db) from the main application module
from .. import db
from sqlalchemy.orm import relationship, backref
from sqlalchemy import desc, UniqueConstraint
# Define model


class User(db.Model):

    """ The User Model is for storing user information
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False, unique=True)
    picture = db.Column(db.String(250))
    date_created = db.Column(
        db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,
                              default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

    def __repr__(self):
        """ Provide information when access instance
        """
        return '<Catalog %s,%s,%s,%s,%s,%s>' % (self.id,
                                                self.name,
                                                self.email,
                                                self.picture,
                                                self.date_created,
                                                self.date_modified)
