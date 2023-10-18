from flask import jsonify, request
from app.sensor import sensor

SENSORS = {}


@sensor.route('/', methods=['GET'])
def list_sensors():
    try:
        return jsonify(SENSORS), 200
    except Exception as e:
        print("Error list_sensors", e)
        return jsonify({'error': 'somthing went wrong'}), 500


@sensor.route('/<sensor_name>', methods=['GET'])
def get_specific_sensor(sensor_name):
    try:
        if sensor_name not in SENSORS:
            return jsonify({"error": "Sensor not found"}), 404

        return jsonify({"sensor_value": SENSORS[sensor_name]}), 200

    except Exception as e:
        print("Error get_specific_sensor", e)
        return jsonify({'error': 'somthing went wrong'}), 500


@sensor.route('/<sensor_name>', methods=['POST'])
def post_specific_sensor(sensor_name):
    try:
        data = request.get_json()
        value = data.get('value', None)

        SENSORS[sensor_name] = value

        print(f"Data Received! {sensor_name} = {value}")

        return jsonify({"msg": "ok"}), 200

    except Exception as e:
        print("Error post_specific_sensor", e)
        return jsonify({'error': 'somthing went wrong'}), 500

