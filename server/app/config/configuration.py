import os

db_uri = "mysql+mysqlconnector://root:@127.0.0.1:3306/mpu"


class ConfigProduction:
    FLASK_ENV = 'production'
    FLASK_SECRET_KEY = os.environ.get('FLASK_SECRET_KEY') or "ABCD123456"
    SQLALCHEMY_DATABASE_URI = db_uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ConfigDevelopment:
    FLASK_ENV = 'development'
    FLASK_SECRET_KEY = os.environ.get('FLASK_SECRET_KEY') or "WXYZ654321"
    SQLALCHEMY_DATABASE_URI = db_uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False


config = {
    'development': ConfigDevelopment,
    'production': ConfigProduction,
}
