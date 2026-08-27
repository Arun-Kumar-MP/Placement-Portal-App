# controllers/user_datastore.py
# This module sets up the user data store for Flask-Security using SQLAlchemy, linking the User and Role models defined in models.py.

from flask_security import SQLAlchemyUserDatastore
from .database import db
from .models import User, Role

user_datastore = SQLAlchemyUserDatastore(db, User, Role)