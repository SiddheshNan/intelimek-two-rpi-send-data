import json
import time
from datetime import datetime
from threading import Thread

from smbus2 import SMBus
from websocket import create_connection

ws_url = "ws://192.168.42.10:8888/api/sensor/MPU6050/ws_push_data"

# some MPU6050 Registers and their Address
PWR_MGMT_1 = 0x6B
SMPLRT_DIV = 0x19
CONFIG = 0x1A
GYRO_CONFIG = 0x1B
INT_ENABLE = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F


# GYRO_XOUT_H = 0x43
# GYRO_YOUT_H = 0x45
# GYRO_ZOUT_H = 0x47


def MPU_Init():
    # write to sample rate register
    bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)

    # Write to power management register
    bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)

    # Write to Configuration register
    bus.write_byte_data(Device_Address, CONFIG, 0)

    # Write to Gyro configuration register
    bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)

    # Write to interrupt enable register
    bus.write_byte_data(Device_Address, INT_ENABLE, 1)


def read_raw_data(addr):
    # Accelero and Gyro value are 16-bit
    high = bus.read_byte_data(Device_Address, addr)
    low = bus.read_byte_data(Device_Address, addr + 1)

    # concatenate higher and lower value
    value = ((high << 8) | low)

    # to get signed value from mpu6050
    if value > 32768:
        value = value - 65536

    return value


ws = create_connection(ws_url)

# def send_data(value): ## REST API Call
#     BASE_URL = "http://192.168.42.10:8888/api/sensor"
#     SENSOR_NAME = "MPU6050"
#     response = requests.post(f"{BASE_URL}/{SENSOR_NAME}", json={"value": value})
#
#     if response.status_code == 200:
#         print(time.time(), f"Data Sent!")
#     else:
#         print(f"Data Sent Failed!")
#         print('Response:', response.status_code, response.text)


bus = SMBus(1)  # or bus = smbus.SMBus(0) for older version boards
Device_Address = 0x68  # MPU6050 device address

MPU_Init()

print("Reading Data of Gyroscope and Accelerometer")

delay = 0.02

duration_between_send = 5

values = []

start_time = time.time()


def send_data_thread():
    while True:
        if len(values):
            data_to_send = values.copy()  # Copy the sensor data to send
            values.clear()  # Clear the data list
            # Thread(target=send_data, args=(data_to_send,), daemon=True).start() ## for REST API call
            json_data = json.dumps(data_to_send)
            ws.send(json_data)

        time.sleep(duration_between_send)


Thread(target=send_data_thread, daemon=True,).start()

while True:
    # Read Accelerometer raw value
    acc_x = read_raw_data(ACCEL_XOUT_H)
    acc_y = read_raw_data(ACCEL_YOUT_H)
    acc_z = read_raw_data(ACCEL_ZOUT_H)

    # Read Gyroscope raw value
    # gyro_x = read_raw_data(GYRO_XOUT_H)
    # gyro_y = read_raw_data(GYRO_YOUT_H)
    # gyro_z = read_raw_data(GYRO_ZOUT_H)

    # Full scale range +/- 250 degree/C as per sensitivity scale factor
    Ax = acc_x / 16384.0
    Ay = acc_y / 16384.0
    Az = acc_z / 16384.0

    # Gx = gyro_x / 131.0
    # Gy = gyro_y / 131.0
    # Gz = gyro_z / 131.0

    current_timestamp = int(datetime.utcnow().timestamp() * 1e3)

    print(current_timestamp,
          # "Gx=%.2f" % Gx, u'\u00b0' + "/s", "\tGy=%.2f" % Gy, u'\u00b0' + "/s", "\tGz=%.2f" % Gz,
          # u'\u00b0' + "/s",
          "\tAx=%.2f g" % Ax, "\tAy=%.2f g" % Ay, "\tAz=%.2f g" % Az)

    values.append({
        # 'Gx': Gx,
        # 'Gy': Gy,
        # 'Gz': Gz,
        'Ax': Ax,
        'Ay': Ay,
        'Az': Az,
        'ts': current_timestamp
    })

    time.sleep(delay)
