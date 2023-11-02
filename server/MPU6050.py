import json
import os
from datetime import datetime
import matplotlib.pyplot as plt
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from flask import Flask, current_app, g, jsonify, Response, render_template, send_from_directory
from flask_cors import CORS
from flask_pymongo import PyMongo
from flask_sock import Sock
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
            print('scaled_x len:', len(scaled_x), 'len t_s:', len(t_s))

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

    scaled_x, dom_x, pos_freq_x, freq_vals_x = preform_fft(ts, ax)
    scaled_y, dom_y, pos_freq_y, freq_vals_y = preform_fft(ts, ay)
    scaled_z, dom_z, pos_freq_z, freq_vals_z = preform_fft(ts, az)

    return jsonify({'fft_x': scaled_x.tolist(), 'fft_y': scaled_y.tolist(),
                    'fft_z': scaled_z.tolist(), 'time_secs': t_s,
                    'pos_freq_x': pos_freq_x.tolist(), 'freq_vals_x': freq_vals_x.tolist(),
                    'pos_freq_y': pos_freq_y.tolist(), 'freq_vals_y': freq_vals_y.tolist(),
                    'pos_freq_z': pos_freq_z.tolist(), 'freq_vals_z': freq_vals_z.tolist()
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

                # insert each item into mongodb
                db.sensors.insert_many([
                    {'name': name, 'Ax': item['Ax'], 'Ay': item['Ay'],
                     'Az': item['Az'], 'ts': datetime.fromisoformat(item['ts'])}
                    for item in values
                ])

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
