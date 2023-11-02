import os
from app import create_app
from app.config.configuration import config

config_name = os.environ.get('config_name', "development")

app = create_app(config[config_name])

if __name__ == '__main__':
    host = os.environ.get('HOST', "0.0.0.0")
    port = os.environ.get('PORT', 5000)
    print(f"Starting server on {host}:{port}")
    app.run(host=host, port=port, debug=True)
