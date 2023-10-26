import json
from datetime import datetime, timedelta
from flask import jsonify, request
from app.extensions.db_extension import db
from app.sensor import sensor, sock
from app.sensor.models import Sensor


@sensor.route('/', methods=['GET'])
def list_sensors():
    try:
        sensors = db.session.query(Sensor.name).distinct().all()
        unique_sensor_names = [name for (name,) in sensors]
        return jsonify(unique_sensor_names), 200

    except Exception as e:
        print("Error list_sensors", e)
        return jsonify({'error': 'somthing went wrong'}), 500


@sensor.route('/<sensor_name>', methods=['GET'])
def get_specific_sensor(sensor_name):
    try:
        time_frame = request.args.get('time_frame')
        if time_frame:
            try:
                end_time = datetime.now()
                start_time = end_time - timedelta(minutes=int(time_frame))
                query = db.session.query(Sensor).filter(Sensor.timestamp >= start_time,
                                                        Sensor.timestamp <= end_time,
                                                        Sensor.name == sensor_name)
            except ValueError:
                return jsonify({'error': 'Invalid time_frame format'}), 400
        else:
            # If time_frame is not specified, return the last added values
            limit = int(request.args.get('limit', 100))
            query = db.session.query(Sensor).filter(Sensor.name == sensor_name).order_by(Sensor.timestamp.desc()).limit(limit)

        sensor_values = [_sensor.serialize() for _sensor in query.all()]
        return jsonify(sensor_values), 200

    except Exception as e:
        print("Error get_specific_sensor", e)
        return jsonify({'error': 'somthing went wrong'}), 500


@sensor.route('/<sensor_name>', methods=['POST'])
def post_specific_sensor(sensor_name):
    try:
        data = request.get_json()
        values = data.get('values', None)
        new_sensor = Sensor(name=sensor_name, values=values)
        db.session.add(new_sensor)
        db.session.commit()

        return jsonify({"msg": "ok"}), 200

    except Exception as e:
        print("Error post_specific_sensor", e)
        return jsonify({'error': 'somthing went wrong'}), 500


@sock.route('/ws_push_data')
def ws_push_data(ws):
    try:
        while True:
            ws_data = ws.receive()
            data = json.loads(ws_data)
            if "name" in data and "values" in data:
                name = str(data['name'])
                values = str(data['values'])
                new_sensor_values = Sensor(name=name, values=values)
                db.session.add(new_sensor_values)
                db.session.commit()
                ws.send('ok')

    except Exception as e:
        ws.send(f"Error! {e} ")
        print("Error push_data_ws", e)
        return jsonify({'error': 'somthing went wrong'}), 500
