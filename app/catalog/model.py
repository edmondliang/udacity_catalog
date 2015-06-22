# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from app import db
from sqlalchemy.orm import relationship, backref
from sqlalchemy import desc, UniqueConstraint
# Define model


class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text())
    catalog_id = db.Column(
        db.Integer, db.ForeignKey("catalogs.id", ondelete=u"CASCADE"), nullable=False)
    catalog = relationship("Catalog")
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = relationship("User")
    date_created = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,
                              default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

    def __repr__(self):
        return '<Item %s,%s,%s>' % (self.id, self.name, self.catalog_id)


class Catalog(db.Model):
    __tablename__ = 'catalogs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    items = relationship("Item", cascade="delete, delete-orphan", backref="Catalog")
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = relationship("User")
    date_created = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,
                              default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

    def __repr__(self):
        return '<Catalog %s,%s,%s,%s>' % (self.id, self.name, self.date_created, self.date_modified)
