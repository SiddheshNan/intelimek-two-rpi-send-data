import requests
import random
import time

BASE_URL = "http://localhost:8888/api/sensor"  # replace with your API endpoint


SENSORS =  ["hall_effect", "temprature", "humidity", "light"]

while True:
    
    for sensor_name in SENSORS:

        value = random.randint(0, 100)

        response = requests.post(f"{BASE_URL}/{sensor_name}", json={"value": value})

        if response.status_code == 200:
            print(f"Data Sent! {sensor_name} = {value}")
        else:
            print(f"Data Sent Failed! {sensor_name} = {value}")
            print('Response:', response.status_code, response.text)  

    time.sleep(2) 
