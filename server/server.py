import io
import json
import os
from datetime import datetime

import matplotlib.pyplot as plt
from flask import Flask, current_app, g, jsonify, Response, render_template, send_from_directory
from flask_cors import CORS
from flask_pymongo import PyMongo
from flask_sock import Sock
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from werkzeug.local import LocalProxy

from fft import preform_fft, conv_time_secs

plt.switch_backend('agg')

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/alima_rpi"
static_path = os.path.join(os.path.dirname(__file__), 'static')

sock = Sock(app)
CORS(app)
mongo = PyMongo()


def get_db():
    """
    This method is According to Docs : https://www.mongodb.com/compatibility/setting-up-flask-with-mongodb
    Configuration method to return global db instance
    """
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = PyMongo(current_app).db
    return db


db = LocalProxy(get_db)


@app.route('/matplotlib_graph.png')
def get_matplotlib_graph():
    try:
        with app.app_context():
            values_db = list(db.sensors.find())  # get values from mongodb
            ax = []
            ay = []
            az = []
            Ts = []

            for item in values_db:
                ax.append(item['Ax'])
                ay.append(item['Ay'])
                az.append(item['Az'])
                Ts.append(str(item['ts']))

            data_freq, ts, t_s = conv_time_secs(Ts)
            # print(data_freq, time_step, time_secs)

            plt.rcParams["figure.figsize"] = [12.50, 7.50]
            plt.rcParams["figure.autolayout"] = True
            plt.close('all')

            scaled_x, dom_x, pos_freq_x, freq_vals_x = preform_fft(ts, ax)
            scaled_y, dom_y, pos_freq_y, freq_vals_y = preform_fft(ts, ay)
            scaled_z, dom_z, pos_freq_z, freq_vals_z = preform_fft(ts, az)
            # print('scaled_x len:', len(scaled_x), 'len t_s:', len(t_s))

            plt.title('Raw Data Plot')
            # X-Axis Acceleration vs Time #
            plt.subplot(3, 2, 1)
            plt.plot(t_s, scaled_x)
            plt.xlabel('Time (Secs)')
            plt.ylabel('A-X (m/s^2)')

            # Y-Axis Acceleration vs Time #
            plt.subplot(3, 2, 3)
            plt.plot(t_s, scaled_y)
            plt.xlabel('Time (Secs)')
            plt.ylabel('A-Y (m/s^2)')

            # Z-Axis Acceleration vs Time #
            plt.subplot(3, 2, 5)
            plt.plot(t_s, scaled_z)
            plt.xlabel('Time (Secs)')
            plt.ylabel('A-Z (m/s^2)')

            # X-Axis FFT Plot #
            plt.subplot(3, 2, 2)
            plt.plot(pos_freq_x, freq_vals_x)
            plt.xlabel('Frequency (Hz)')
            plt.ylabel('Amplitude')

            # Y-Axis FFT Plot #
            plt.subplot(3, 2, 4)
            plt.plot(pos_freq_y, freq_vals_y)
            plt.xlabel('Frequency (Hz)')
            plt.ylabel('Amplitude')

            # Z-Axis FFT Plot #
            plt.subplot(3, 2, 6)
            plt.plot(pos_freq_z, freq_vals_z)
            plt.xlabel('Frequency (Hz)')
            plt.ylabel('Amplitude')

            output = io.BytesIO()
            FigureCanvas(plt.gcf()).print_png(output)

            return Response(output.getvalue(), mimetype='image/png')

    except Exception as e:
        print("Error get_matplotlib_graph:", e)


@app.route('/graph_values')
def get_graph_values():
    limit = 6000
    values_db = list(db.sensors.find().sort("ts"))  # get values from mongodb
    ffts_db = list(db.ffts.find())

    print(ffts_db)

    if len(values_db) > limit:
        values_chunk = values_db[limit:]
    else:
        values_chunk = values_db.copy()

    ax = []
    ay = []
    az = []
    Ts = []

    Axc = []
    Ayc = []
    Azc = []
    Tsc = []

    dominant_x = []
    dominant_y = []
    dominant_z = []
    Ts_freq = []

    for item in values_db:
        ax.append(item['Ax'])
        ay.append(item['Ay'])
        az.append(item['Az'])
        Ts.append(str(item['ts']))

    for item in values_chunk:
        Axc.append(item['Ax'])
        Ayc.append(item['Ay'])
        Azc.append(item['Az'])
        Tsc.append(str(item['ts']))

    for item in ffts_db:
        dominant_x.append(item['dom_freq_X'])
        dominant_y.append(item['dom_freq_Y'])
        dominant_z.append(item['dom_freq_Z'])
        Ts_freq.append(item['ts_fft'])

    data_freq, ts, t_s = conv_time_secs(Ts)
    data_freqc, tsc, t_sc = conv_time_secs(Tsc)

    # print(data_freq, time_step, time_secs)

    scaled_x, dom_x, pos_freq_x, freq_vals_x = preform_fft(ts, ax)
    scaled_y, dom_y, pos_freq_y, freq_vals_y = preform_fft(ts, ay)
    scaled_z, dom_z, pos_freq_z, freq_vals_z = preform_fft(ts, az)

    scaled_xc, dom_xc, pos_freq_xc, freq_vals_xc = preform_fft(tsc, Axc)  # chunks
    scaled_yc, dom_yc, pos_freq_yc, freq_vals_yc = preform_fft(tsc, Ayc)
    scaled_zc, dom_zc, pos_freq_zc, freq_vals_zc = preform_fft(tsc, Azc)

    # print({'dom_x': dominant_x, 'dom_y': dominant_y, 'dom_z': dominant_z})

    return jsonify({'fft_x': scaled_x.tolist(), 'fft_y': scaled_y.tolist(),
                    'fft_z': scaled_z.tolist(), 't_s': t_s,

                    # 'fft_xc': scaled_xc.tolist(), 'fft_yc': scaled_yc.tolist(),
                    # 'fft_zc': scaled_zc.tolist(), 't_sc': t_sc, # no

                    # 'pos_freq_x': pos_freq_x.tolist(), 'freq_vals_x': freq_vals_x.tolist(),
                    # 'pos_freq_y': pos_freq_y.tolist(), 'freq_vals_y': freq_vals_y.tolist(),
                    # 'pos_freq_z': pos_freq_z.tolist(), 'freq_vals_z': freq_vals_z.tolist(),

                    'pos_freq_xc': pos_freq_xc.tolist(), 'freq_vals_xc': freq_vals_xc.tolist(),
                    'pos_freq_yc': pos_freq_yc.tolist(), 'freq_vals_yc': freq_vals_yc.tolist(),
                    'pos_freq_zc': pos_freq_zc.tolist(), 'freq_vals_zc': freq_vals_zc.tolist(),

                    'dom_x': dominant_x, 'dom_y': dominant_y, 'dom_z': dominant_z, 'Ts_freq': Ts_freq
                   }), 200


@sock.route('/ws_push_data')
def ws_push_data(ws):
    try:
        while True:
            ws_data = ws.receive()
            data = json.loads(ws_data)
            if "name" in data and "values" in data:
                name = str(data['name'])
                values = data['values']

                dom_freq_X = data["dom_freq"]["dom_freq_X"]
                dom_freq_Y = data["dom_freq"]["dom_freq_Y"]
                dom_freq_Z = data["dom_freq"]["dom_freq_Z"]
                ts_fft = data["dom_freq"]["ts_fft"]

                # insert each item into mongodb
                db.sensors.insert_many([
                    {'name': name, 'Ax': item['Ax'], 'Ay': item['Ay'],
                     'Az': item['Az'], 'ts': datetime.fromisoformat(item['ts']), 'ts_fft': ts_fft
                     }
                    for item in values
                ])

                db.ffts.insert_one({
                    'dom_freq_X': dom_freq_X, 'dom_freq_Y': dom_freq_Y, 'dom_freq_Z': dom_freq_Z, 'ts_fft': ts_fft
                })

    except Exception as e:
        ws.send(f"Error! {e} ")
        print("Error push_data_ws", e)
        return jsonify({'error': 'somthing went wrong'}), 500


@app.route('/')
@app.route('/index.html')
def index_page():
    return render_template('index.html')


@app.route('/<path:path>')
def static_route(path):
    if os.path.isdir(os.path.join(static_path, path)):
        path = os.path.join(path, 'index.html')
    return send_from_directory(static_path, path)


app.run(host="0.0.0.0", port=5000, debug=True)
