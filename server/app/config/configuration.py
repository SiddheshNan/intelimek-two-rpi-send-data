import os
from datetime import timedelta


class ConfigProduction:
    FLASK_ENV = 'production'
    FLASK_SECRET_KEY = os.environ.get('FLASK_SECRET_KEY') or "ABCD123456"


class ConfigDevelopment:
    FLASK_ENV = 'development'
    FLASK_SECRET_KEY = os.environ.get('FLASK_SECRET_KEY') or "WXYZ654321"


config = {
    'development': ConfigDevelopment,
    'production': ConfigProduction,
}
