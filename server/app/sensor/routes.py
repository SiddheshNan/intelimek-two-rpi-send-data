import json
import time
from datetime import datetime

from flask import jsonify, request

from app.extensions.db_extension import db
from app.sensor import sensor, sock
from app.utils import preform_fft, conv_time_secs

'''
The mongodb schema is as follows:
{
    "name": "MPU_8050",
    "values": [
        {
            "Ax": 10,
            "Ay": 9,
            "Az": 11,
            "ts": '2023-11-01 13:20:43.836119'
        },
        {
            "Ax": 11,
            "Ay": 22,
            "Az": 11,
            "ts":'2023-11-01 13:20:43.836119'
        },
        {
            "Ax": 12,
            "Ay": 14,
            "Az": 13,
            "ts": '2023-11-01 13:20:43.836119'
        }
    ],
    "ts": 2023-11-01 13:20:43.836119 # this is Datetime object at when data is pushed to db
}
'''

Ax = []
Ay = []
Az = []
Ts = []


def on_values_pushed():
    # this runs every time new values are pushed
    # we can generate and save the plots here
    pass


@sensor.route('/values', methods=['GET'])
def get_sensor_values():
    return jsonify({'ax': Ax, 'ay': Ay, 'az': Az, "Ts": Ts}), 200


@sensor.route('/fft', methods=['GET'])
def sensor_fft():
    try:
        data_freq, time_step = conv_time_secs(Ts)
        print(data_freq, time_step)
        print(Ax, Ay, Az)
        ax_fft = preform_fft(Ax, time_step)
        ay_fft = preform_fft(Ay, time_step)
        az_fft = preform_fft(Az, time_step)
        return jsonify({'ax_fft': ax_fft, 'ay_fft': ay_fft,
                        'az_fft': az_fft, 'data_freq': data_freq}), 200

    except Exception as e:
        print("Error sensor_fft", e)
        return jsonify({'error': 'somthing went wrong'}), 500


@sock.route('/ws_push_data')
def ws_push_data(ws):
    try:
        while True:
            ws_data = ws.receive()
            data = json.loads(ws_data)
            if "name" in data and "values" in data:
                name = str(data['name'])
                values = data['values']

                for value in values:
                    Ax.append(value['Ax'])
                    Ay.append(value['Ay'])
                    Az.append(value['Az'])
                    Ts.append(value['ts'])

                on_values_pushed()

                # insert into mongodb
                db.sensors.insert_one({
                    'name': name,
                    'values': values,
                    'ts': datetime.now(),
                })

    except Exception as e:
        ws.send(f"Error! {e} ")
        print("Error push_data_ws", e)
        return jsonify({'error': 'somthing went wrong'}), 500

# extra code commented for now..
# @sensor.route('/', methods=['GET'])
# def list_sensors():
#     try:
#         distinct_sensors = list(db.sensors.distinct('name'))
#         return jsonify(distinct_sensors), 200
#
#     except Exception as e:
#         print("Error list_sensors", e)
#         return jsonify({'error': 'somthing went wrong'}), 500
#
# @sensor.route('/<sensor_name>', methods=['POST'])
# def post_specific_sensor(sensor_name):
#     try:
#         data = request.get_json()
#         sensor_values = data.get('values', None)
#         sensor_doc = {
#             'name': sensor_name,
#             'values': sensor_values,
#             'ts': int(time.time()),
#         }
#         db.sensors.insert_one(sensor_doc)
#         return jsonify({"msg": "ok"}), 200
#
#     except Exception as e:
#         print("Error post_specific_sensor", e)
#         return jsonify({'error': 'somthing went wrong'}), 500
