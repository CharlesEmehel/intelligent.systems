from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import logging
from logging.handlers import RotatingFileHandler
from owlready2 import get_ontology


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()


def create_app():
    
    # create the app; configure the SQLite database, relative to the app instance folder; create the
    # extension; and initialize the app with the extension by passing the app to the extension

    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    
    login_manager.login_view = "main.login_page" # specify the login view
    login_manager.login_message_category = "info"
    
    
    with app.app_context():
        from . import models
        from .routes import bp as main_bp
        app.register_blueprint(main_bp)
        db.create_all()
        
    # Set up logging
    configure_logging(app)
        
    return app


def configure_logging(app):
    if not app.debug:
        #set the log level
        app.logger.setLevel(logging.INFO) 
        
        
        # Create a file handler for logging  
        file_handler = RotatingFileHandler('andromeda.log', maxBytes=10240, backupCount=1)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        # Add the file handler to the app's logger.
        app.logger.addHandler(file_handler)
        
        
        #Create a console handler for logging.
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        console_handler.setLevel(logging.INFO) 
        # Add the console handler to the app's logger.
        app.logger.addHandler(console_handler)
        
        app.logger.info('Andromeda startup')
        

    energyaionto = get_ontology("http://energyaiontonamespace.org/energyaionton.owl")


# create_database(app)

def create_database(app):
    if not path.exists('ontoML/' + DB_NAME):            
        #db.create_all((app=app))
        print('Database created!')
