from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import logging
from logging.handlers import RotatingFileHandler
from owlready2 import get_ontology
import os
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

# create the andromeda application with capability to log running events to the docker container service.
def create_app():
    app = Flask(__name__)
    env = os.getenv('FLASK_ENV', 'development')
    app.config.from_object(f'config.{env.capitalize()}Config')
    
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    
    login_manager.login_view = "auth.login_page"  # specify the login view
    login_manager.login_message_category = "info"
    
    with app.app_context():
        from . import models
        from .routes import bp as main_bp
        from .auth import auth_bp
        from .api import api_bp
        from .handlers import errors_bp
        app.register_blueprint(main_bp)
        app.register_blueprint(auth_bp, url_prefix='/auth')
        app.register_blueprint(api_bp, url_prefix='/api')
        app.register_blueprint(errors_bp)
        db.create_all()
        
    configure_logging(app)
        
    return app

def configure_logging(app):
    if not app.debug:
        app.logger.setLevel(logging.INFO)
        
        file_handler = RotatingFileHandler('andromeda.log', maxBytes=10240, backupCount=1)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        console_handler.setLevel(logging.INFO)
        app.logger.addHandler(console_handler)
        
        app.logger.info('Andromeda startup')

    energyaionto = get_ontology("http://energyaiontonamespace.org/energyaionton.owl")

# create_database(app)

def create_database(app):
    if not path.exists('ontoML/' + DB_NAME):            
        db.create_all(app=app)
        print('Database created!')
