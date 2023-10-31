import os


# class Config:
#     db_uri = "mysql+mysqlconnector://root:@127.0.0.1:3306/mpu"
#

class ConfigProduction:
    FLASK_ENV = 'production'
    FLASK_SECRET_KEY = os.environ.get('FLASK_SECRET_KEY') or "ABCD123456"
    # SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:@127.0.0.1:3306/mpu"
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    MONGO_URI = "mongodb://localhost:27017/alima_rpi"


class ConfigDevelopment:
    FLASK_ENV = 'development'
    FLASK_SECRET_KEY = os.environ.get('FLASK_SECRET_KEY') or "WXYZ654321"
    # SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:@127.0.0.1:3306/mpu"
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    MONGO_URI = "mongodb://localhost:27017/alima_rpi"


config = {
    'development': ConfigDevelopment,
    'production': ConfigProduction,
}
