# from flask_sqlalchemy import SQLAlchemy
# db = SQLAlchemy()
from flask_pymongo import PyMongo
from flask import current_app, g
from werkzeug.local import LocalProxy

mongo = PyMongo()


def get_db():
    """
    This method is According to Docs : https://www.mongodb.com/compatibility/setting-up-flask-with-mongodb
    Configuration method to return global db instance
    """
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = PyMongo(current_app).db
    return db


# Use LocalProxy to read the global db instance with just `db`
db = LocalProxy(get_db)
