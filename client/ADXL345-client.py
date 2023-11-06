import json
import time
import board
import busio
import adafruit_adxl34x
from datetime import datetime
from websocket import create_connection
from threading import Thread

ws_url = "ws://192.168.208.3:8888/api/sensor/ws_push_data"

# Initialize Accelerometer #
i2c = busio.I2C(board.SCL, board.SDA)
accelerometer = adafruit_adxl34x.ADXL345(i2c)
accelerometer.data_rate = adafruit_adxl34x.DataRate.RATE_3200_HZ
accelerometer.range = adafruit_adxl34x.Range.RANGE_16_G
acr = accelerometer.data_rate

print(acr)
print("Reading Data of Accelerometer")

ws = create_connection(ws_url)

delay = 0.02
duration_between_send = 5
values = []

# start_time = time.time()
# cycle_values = 100


def send_data_thread():
    while True:
        if len(values):  # > cycle_values
            data_to_send = values.copy()  # Copy the sensor data to send
            values.clear()  # Clear the data list
            ws.send(json.dumps({"name": "ADXL345", "values": data_to_send}))

        time.sleep(duration_between_send)


Thread(target=send_data_thread, daemon=True, ).start()

while True:
    a_x, a_y, a_z = accelerometer.acceleration
    current_timestamp = str(datetime.now())
    print(f'Timestamp: {current_timestamp}, A-X: {a_x}, A-Y: {a_y}, A-Z: {a_z}')
    values.append({'Ax': a_x, 'Ay': a_y, 'Az': a_z, 'ts': current_timestamp})
    time.sleep(delay)
