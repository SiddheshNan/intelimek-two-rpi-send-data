from flask import Flask
from flask_cors import CORS
import click
from werkzeug.exceptions import HTTPException
from app.utils import http_exception_handler


def create_app(app_configuration):
    app = Flask(__name__)
    app.config.from_object(app_configuration)

    # Initialize Flask extensions here
    CORS(app)

    # Register blueprints here
    from app.sensor.routes import sensor as sensor_routes
    app.register_blueprint(sensor_routes, url_prefix='/api/sensor')

    # Register the http exception handler
    app.register_error_handler(HTTPException, http_exception_handler)

    # print all the registered routes
    sorted_rules = sorted(app.url_map.iter_rules(), key=lambda x: x.rule)

    max_rule = max(len(rule.rule) for rule in sorted_rules)
    max_ep = max(len(rule.endpoint) for rule in sorted_rules)
    max_meth = max(len(', '.join(rule.methods)) for rule in sorted_rules)

    column_format = '{:<%s}  {:<%s}  {:<%s}' % (max_rule, max_ep, max_meth)
    click.echo(column_format.format('Route', 'Endpoint', 'Methods'))
    under_count = max_rule + max_ep + max_meth + 4
    click.echo('-' * under_count)

    for rule in sorted_rules:
        methods = ', '.join(rule.methods)
        click.echo(column_format.format(rule.rule, rule.endpoint, methods))

    # with app.app_context():
    #     db.create_all()

    return app
