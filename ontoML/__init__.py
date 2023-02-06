from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from os import path
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "appl.db"
# create the app; configure the SQLite database, relative to the app instance folder; create the
# extension; and initialize the app with the extension by passing the app to the extension
# def create_app():
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' # ///-Rel path; ////-Abs. path
app.config['SECRET_KEY'] = os.urandom(12).hex()  #create a secret key required for CSRF to display the form for session and cookies
db.init_app(app)
bcrypt = Bcrypt(app)
loging_manager = LoginManager(app)
loging_manager.login_view = "login_page"
loging_manager.login_message_category = "info"
# return app


import ontoML.models

from ontoML import auth
from . import routes


# create_database(app)

def create_database(app):
    if not path.exists('ontoML/' + DB_NAME):            
        #db.create_all((app=app))
        print('Database created!')
