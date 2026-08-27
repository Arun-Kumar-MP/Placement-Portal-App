# controllers/config.py
# This module defines the configuration settings for the Flask application, including database URI and security settings.

class Config:
    SECRET_KEY = 'super-secret-key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///ppa.db'
    
    # Flask-Security configurations
    SECURITY_PASSWORD_SALT = 'djhaskdvado98y29bcrypt'

