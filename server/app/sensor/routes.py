import json
import time

from flask import jsonify, request

from app.extensions.db_extension import db
from app.sensor import sensor, sock

'''
The mongodb schema is as follows:
{
    "name": "MPU_8050",
    "values": "[1,2,3,4,5]",
    "ts": 1234567890
}
'''


@sensor.route('/', methods=['GET'])
def list_sensors():
    try:
        distinct_sensors = list(db.sensors.distinct('name'))
        return jsonify(distinct_sensors), 200

    except Exception as e:
        print("Error list_sensors", e)
        return jsonify({'error': 'somthing went wrong'}), 500


@sensor.route('/<sensor_name>', methods=['GET'])
def get_specific_sensor(sensor_name):
    try:
        time_frame_minute = request.args.get('time_frame_minute')
        if time_frame_minute:
            try:
                end_time = int(time.time())
                start_time = end_time - (int(time_frame_minute) * 60 * 1000)
                values = db.sensors.find(
                    {"name": sensor_name, "ts": {"$and": [{"$lt": end_time}, {"$gt": start_time}]}}).sort('ts')
            except ValueError:
                return jsonify({'error': 'Invalid time_frame format'}), 400
        else:
            # If time_frame is not specified, return the last added values
            limit = int(request.args.get('limit', 100))
            values = db.sensors.find({"name": sensor_name}).sort('ts').limit(limit)

        return jsonify([{'name': item['name'], 'values': item['values']} for item in list(values)]), 200

    except Exception as e:
        print("Error get_specific_sensor", e)
        return jsonify({'error': 'somthing went wrong'}), 500


@sensor.route('/<sensor_name>', methods=['POST'])
def post_specific_sensor(sensor_name):
    try:
        data = request.get_json()
        sensor_values = data.get('values', None)
        sensor_doc = {
            'name': sensor_name,
            'values': sensor_values,
            'ts': int(time.time()),
        }
        db.sensors.insert_one(sensor_doc)
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
                db.sensors.insert_one({
                    'name': name,
                    'values': values,
                    'ts': int(time.time()),
                })
                # ws.send('ok')

    except Exception as e:
        ws.send(f"Error! {e} ")
        print("Error push_data_ws", e)
        return jsonify({'error': 'somthing went wrong'}), 500
