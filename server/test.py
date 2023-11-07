import json
import time
from datetime import datetime
import traceback
from flask import jsonify, request

from app.extensions.db_extension import db
from app.sensor import sensor, sock
from app.utils import preform_fft, conv_time_secs
import numpy as np
import matplotlib.pyplot as plt

import cv2
import pandas as pd

from sys import exit

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
Axc = []
Ayc = []
Azc = []
Tsc = []
Ts_freq = []
dom_x = []
dom_y = []
dom_z = []


# def create_plots(ax, ay, az, ts, t_s):
#    scaled_x, dom_x, pos_freq_x, freq_vals_x = preform_fft(ts, ax)
#    scaled_y, dom_y, pos_freq_y, freq_vals_y = preform_fft(ts, ay)
#    scaled_z, dom_z, pos_freq_z, freq_vals_z = preform_fft(ts, az)
#    print(len(scaled_x), len(t_s))
#    fig = plt.figure()
#    timer = fig.canvas.new_timer(interval=4000)
#    #timer.add_callback(plt.close)
#    timer.add_callback(plt.clf)
#    plt.title('Raw Data Plot')
#    # X-Axis Acceleration vs Time #
#    plt.subplot(3, 2, 1)
#    plt.plot(t_s, scaled_x)
#    plt.xlabel('Time (Secs)')
#    plt.ylabel('A-X (m/s^2)')
#    # Y-Axis Acceleration vs Time #
#    plt.subplot(3, 2, 3)
#    plt.plot(t_s, scaled_y)
#    plt.xlabel('Time (Secs)')
#    plt.ylabel('A-Y (m/s^2)')
#    # Z-Axis Acceleration vs Time #
#    plt.subplot(3, 2, 5)
#    plt.plot(t_s, scaled_z)
#    plt.xlabel('Time (Secs)')
#    plt.ylabel('A-Z (m/s^2)')
#    # X-Axis FFT Plot #
#    plt.subplot(3, 2, 2)
#    plt.plot(pos_freq_x, freq_vals_x)
#    plt.xlabel('Frequency (Hz)')
#    plt.ylabel('Amplitude')
#    # Y-Axis FFT Plot #
#    plt.subplot(3, 2, 4)
#    plt.plot(pos_freq_y, freq_vals_y)
#    plt.xlabel('Frequency (Hz)')
#    plt.ylabel('Amplitude')
#    # Z-Axis FFT Plot #
#    plt.subplot(3, 2, 6)
#    plt.plot(pos_freq_z, freq_vals_z)
#    plt.xlabel('Frequency (Hz)')
#    plt.ylabel('Amplitude')


#    timer.start()
#    plt.show()
def create_plots(AX, AY, AZ, TS, ax, ay, az, ts, t_s, fft_ts, d_x, d_y, d_z):

    scaled_x, dom_x, pos_freq_x, freq_vals_x = preform_fft(ts, ax)
    scaled_y, dom_y, pos_freq_y, freq_vals_y = preform_fft(ts, ay)
    scaled_z, dom_z, pos_freq_z, freq_vals_z = preform_fft(ts, az)

    scaled_xc, dom_xc, pos_freq_xc, freq_vals_xc = preform_fft(TS, AX)  # chunks
    scaled_yc, dom_yc, pos_freq_yc, freq_vals_yc = preform_fft(TS, AY)
    scaled_zc, dom_zc, pos_freq_zc, freq_vals_zc = preform_fft(TS, AZ)

    print("Dominant Frequencies")
    print(f'X - {round(dom_xc, 3)} Hz, Y - {round(dom_yc, 3)} Hz, Z - {round(dom_zc, 3)} Hz')
    plt.figure(figsize=(12, 7))
    plt.clf()
    # X-Axis Acceleration vs Time #
    plt.subplot(3, 3, 1)
    plt.title("Raw Data")
    plt.plot(t_s, scaled_x)
    plt.xlabel('Time (Secs)')
    plt.ylabel('A-X (m/s^2)')
    #    # Y-Axis Acceleration vs Time #
    plt.subplot(3, 3, 4)
    plt.plot(t_s, scaled_y)
    plt.xlabel('Time (Secs)')
    plt.ylabel('A-Y (m/s^2)')
    # Z-Axis Acceleration vs Time #
    plt.subplot(3, 3, 7)
    plt.plot(t_s, scaled_z)
    plt.xlabel('Time (Secs)')
    plt.ylabel('A-Z (m/s^2)')
    # FFT Plot for Complete data chunk #
    # X-Axis FFT Plot #
    plt.subplot(3, 3, 2)
    plt.title("Complete FFT Plot")
    plt.plot(fft_ts, d_x)
    plt.xlabel('Timestamp')
    plt.ylabel('Frequency (Hz)')
    # Y-Axis FFT Plot #
    plt.subplot(3, 3, 5)
    plt.plot(fft_ts, d_y)
    plt.xlabel('Timestamp')
    plt.ylabel('Frequency (Hz)')
    # Z-Axis FFT Plot #
    plt.subplot(3, 3, 8)
    plt.plot(fft_ts, d_z)
    plt.xlabel('Timestamp')
    plt.ylabel('Frequency (Hz)')
    # FFT Plot for current Data Chunks #
    # X-Axis FFT Plot #
    plt.subplot(3, 3, 3)
    plt.title("Current FFT Plot")
    plt.plot(pos_freq_xc, freq_vals_xc)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')
    # Y-Axis FFT Plot #
    plt.subplot(3, 3, 6)
    plt.plot(pos_freq_yc, freq_vals_yc)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')
    # Z-Axis FFT Plot #
    plt.subplot(3, 3, 9)
    plt.plot(pos_freq_zc, freq_vals_zc)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')

    fig = plt.gcf()
    fig.canvas.draw()

    img_np = np.array(fig.canvas.renderer.buffer_rgba())
    img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGBA2BGR)
    cv2.imshow('output', img_bgr)
    # time.sleep(0.001)

    # key = cv2.waitKey(4000)
    key = cv2.waitKey(10)
    if key == ord('q'):
        cv2.destroyAllWindows()
        exit(-1)
    plt.close()


def on_values_pushed():
    data_freq, time_step, time_secs = conv_time_secs(Ts)
    data_freqc, time_stepc, time_secsc = conv_time_secs(Tsc)
    print("Data Rate: ", data_freqc, " Hz")
    plt.rcParams["figure.figsize"] = [12.50, 7.50]
    plt.rcParams["figure.autolayout"] = True
    plt.close('all')
    create_plots(Axc, Ayc, Azc, time_stepc, Ax, Ay, Az, time_step, time_secs, Ts_freq, dom_x, dom_y, dom_z)
    # print("Dominant Frequency: ", ax_fft[0])




@sock.route('/ws_push_data')
def ws_push_data(ws):
    global Axc, Ayc, Azc, Tsc
    try:
        while True:
            ws_data = ws.receive()
            data = json.loads(ws_data)
            print(data)
            if "name" in data and "values" in data:
                name = str(data['name'])
                values = data['values']

                for i in range(len(values) - 1):
                    Ax.append(values[i]['Ax'])
                    Ay.append(values[i]['Ay'])
                    Az.append(values[i]['Az'])
                    Ts.append(values[i]['ts'])
                    Axc.append(values[i]['Ax'])
                    Ayc.append(values[i]['Ay'])
                    Azc.append(values[i]['Az'])
                    Tsc.append(values[i]['ts'])

                Ts_freq.append(values[-1]['ts_fft'])
                dom_x.append(values[-1]['dom_freq_X'])
                dom_y.append(values[-1]['dom_freq_Y'])
                dom_z.append(values[-1]['dom_freq_Z'])

                print(Ts_freq, dom_y)
                on_values_pushed()

                Axc, Ayc, Azc, Tsc = [], [], [], []

                # insert into mongodb
                db.sensors.insert_one({
                    'name': name,
                    'values': values,
                    'ts': datetime.now(),
                })

    except Exception as e:
        ws.send(f"Error! {e} ")
        print("Error push_data_ws", e)
        error = traceback.format_exc()
        print(error)
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


