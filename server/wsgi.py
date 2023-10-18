import waitress
from app import create_app
from app.config import config
import os

config_name = os.environ.get('config_name', "production")

app = create_app(config[config_name])

if __name__ == '__main__':
    host = os.environ.get('HOST', "0.0.0.0")
    port = os.environ.get('PORT', 8888)
    print(f"Starting server on {host}:{port}")
    waitress.serve(app, host=host, port=port)
