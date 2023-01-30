from . import db
from ontoML import bcrypt
from datetime import datetime

# Define users model and tables
class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=1000)
    items = db.relationship('Item', backref='owned_user', lazy=True)

    def __repr__(self):
        return f'User {self.username}'

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')



# Define Entity model and tables
class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    entityname = db.Column(db.String(length=30), nullable=False, unique=True)
    type = db.Column(db.String(length=30), nullable=False)
    locatedat = db.Column(db.String(length=25), nullable=False)
    datecreated = db.Column(db.String(length=25), nullable=False)
    # datecreated = db.Column(db.DateTime, default=datetime.utcnow)
    modifiedat = db.Column(db.String(length=25), nullable=False)
    entityversion = db.Column(db.Integer(), nullable=False)
    devicecategory = db.Column(db.String(length=15), nullable=False)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))
    # description = db.Column(db.String(length=1024), nullable=False, unique=True)

    def __repr__(self):
        return f'Item {self.entityname}'

# Define Entity model and tables
class Query(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    namespace = db.Column(db.String(length=50), nullable=False, unique=True)
    querytext = db.Column(db.String(length=200), nullable=False)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))
    # description = db.Column(db.String(length=1024), nullable=False, unique=True)

    def __repr__(self):
        return f'Item {self.namespace}'
