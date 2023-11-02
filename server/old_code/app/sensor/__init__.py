from flask import Blueprint
from flask_sock import Sock

sensor = Blueprint('sensor', __name__)
sock = Sock(sensor)
