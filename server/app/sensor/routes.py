import json
import time

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
            "ts": 1698823310 # this is epoch timestamp (in seconds) when the sensor is read
        },
        {
            "Ax": 11,
            "Ay": 22,
            "Az": 11,
            "ts": 1698823312
        },
        {
            "Ax": 12,
            "Ay": 14,
            "Az": 13,
            "ts": 1698823514
        }
    ],
    "ts": 1234567890 # this is epoch timestamp (in seconds) at when data is pushed to db
}
'''


Ax = []
Ay = []
Az = []
Ts = []


def on_values_pushed():
    # this runs every time new values are pushed
    # we can generate the plots here
    pass


@sensor.route('/', methods=['GET'])
def list_sensors():
    try:
        distinct_sensors = list(db.sensors.distinct('name'))
        return jsonify(distinct_sensors), 200

    except Exception as e:
        print("Error list_sensors", e)
        return jsonify({'error': 'somthing went wrong'}), 500


@sensor.route('/fft', methods=['GET'])
def sensor_fft():
    try:
        # FFTs are not working, need some help here
        data_freq, time_step = conv_time_secs(Ts)
        ax_fft = preform_fft(Ax, Ts)  # or preform_fft(Ax, time_step) ??
        ay_fft = preform_fft(Ay, Ts)
        az_fft = preform_fft(Az, Ts)
        return jsonify({'ax_fft': ax_fft, 'ay_fft': ay_fft, 'az_fft': az_fft}), 200

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
                    'ts': int(time.time()),
                })

    except Exception as e:
        ws.send(f"Error! {e} ")
        print("Error push_data_ws", e)
        return jsonify({'error': 'somthing went wrong'}), 500


# extra code commented for now..
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

# @sensor.route('/<sensor_name>', methods=['GET'])
# def get_specific_sensor(sensor_name):
#     try:
#         time_frame_minute = request.args.get('time_frame_minute')
#         if time_frame_minute:
#             try:
#                 end_time = int(time.time())
#                 start_time = end_time - (int(time_frame_minute) * 60 * 1000)
#                 values = db.sensors.find(
#                     {"name": sensor_name, "ts": {"$and": [{"$lt": end_time}, {"$gt": start_time}]}}).sort('ts')
#             except ValueError:
#                 return jsonify({'error': 'Invalid time_frame format'}), 400
#         else:
#             # If time_frame is not specified, return the last added values
#             limit = int(request.args.get('limit', 100))
#             values = db.sensors.find({"name": sensor_name}).sort('ts').limit(limit)
#
#         return jsonify([{'name': item['name'], 'values': item['values']} for item in list(values)]), 200
#
#     except Exception as e:
#         print("Error get_specific_sensor", e)
#         return jsonify({'error': 'somthing went wrong'}), 500
