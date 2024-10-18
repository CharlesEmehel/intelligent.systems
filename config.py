import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(12).hex())  # Default to a random generated value if not provided
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///../db/appl.db') # Default to appl.db if not provided
    DEBUG = os.getenv('DEBUG', 'False').lower() in ['true', '1', 't']
    OIDC_CLIENT_SECRETS = os.getenv('OIDC_CLIENT_SECRETS', 'client_secrets.json')
    OIDC_COOKIE_SECURE = os.getenv('OIDC_COOKIE_SECURE', 'False')
    OIDC_CALLBACK_ROUTE = os.getenv('OIDC_CALLBACK_ROUTE', '/oidc/callback')
    # OIDC_REQUIRE_VERIFIED_EMAIL = os.getenv('OIDC_REQUIRE_VERIFIED_EMAIL', 'False')
    OIDC_USER_INFO_ENABLED = os.getenv('OIDC_USER_INFO_ENABLED', 'True')
    OIDC_OPENID_REALM = os.getenv('OIDC_OPENID_REALM', 'flask-demo')
    OIDC_SCOPES = os.getenv('OIDC_SCOPES', ['openid', 'email', 'profile'])
    OIDC_INTROSPECTION_AUTH_METHOD = os.getenv('OIDC_INTROSPECTION_AUTH_METHOD', 'client_secret_post')
    OIDC_SSL_VERIFY = False  # Disable SSL verification
class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../db/test.db'
    TESTING = True
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
