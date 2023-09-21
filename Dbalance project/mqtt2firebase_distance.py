import json
import paho.mqtt.client as mqtt
from datetime import datetime
import pytz
import pyrebase
# import mqtt2firebase_2
import os
# Firebase Configuration
config = {
    "apiKey": "AIzaSyAIrm8-A_1NNAf0hcxK4vgjf8XjV76SSw8",
    "authDomain": "iotxdb.firebaseapp.com",
    "databaseURL": "https://iotxdb-default-rtdb.firebaseio.com",
    "projectId": "iotxdb",
    "storageBucket": "iotxdb.appspot.com",
    "messagingSenderId": "306265675994",
    "appId": "1:306265675994:web:172e5a6289158d9a93ede3",
    "measurementId": "G-SHPJVJWV93"}

data_key = ""
file_path = 'C:/Users/alex5/Desktop/STUDY/IOT/dbalance/DbalanceV5.2/current_user_run.txt'
card_status_path = 'C:/Users/alex5/Desktop/STUDY/IOT/dbalance/DbalanceV5.2/card_status.txt'


firebase = pyrebase.initialize_app(config)
database = firebase.database()
count_data_global = ""
# MQTT Configuration
MQTT_BROKER = 'hairdresser.cloudmqtt.com'
MQTT_PORT = 18126
MQTT_USERNAME = 'team6_4'
MQTT_PASSWORD = 'braude1234'
MQTT_TOPIC = 'braude/teams/team6/distance'
wait = ""
global_distance = "0"
print("after the mqtt..")

while os.path.getsize(file_path) > 0:
    with open(file_path, 'r') as file:
        data_key = file.read()
        break




# When connected to MQTT
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(MQTT_TOPIC)

# When message is received from MQTT
def on_message(client, userdata, msg):
    print(f"Received message from topic {msg.topic}: {msg.payload.decode()}")
    global global_distance

    with open(card_status_path, 'r') as file:
        card_status = file.read()
    print("data key entered: " + data_key)
    print("card_status: " + card_status)

    if(card_status == "True"):
        print("inside the if..")
        # Get current time once and use it throughout the function
        tz = pytz.timezone('Etc/GMT-3')
        current_time = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')
        print(current_time)


        # Get all the values
        message_data = json.loads(msg.payload.decode())

        distance_val = msg.payload.decode()
        if(int(distance_val) == 1):
            global_distance = 0
        if (int(distance_val)-int(global_distance) >= 1):
            global_distance = distance_val
            # count_data_global = database.child("patients").child(data_key).child("sensors_data").child("distance").child("0").get().val()

            # Prepare data for all sensors
            sensor_values = {
                "distance": ("dis_val", distance_val),
            }


            # Batch the updates for Firebase
            for sensor_name, (value_key, value) in sensor_values.items():
                insert_sensor_data(sensor_name, value_key, value, current_time, data_key)


            print("Data inserted successfully!")
            timeend_check = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')
            print(timeend_check)

    else:
        print("card is not inside")



def on_disconnect(client, userdata, rc):
    # Nothing special to do for Firebase on disconnect
    pass



def insert_sensor_data(sensor_name, value_key, value, time, patient_key):
    # Fetch the current count
    count_data = database.child("patients").child(patient_key).child("sensors_data").child(sensor_name).child("0").get().val()
    print(count_data)
    count_data_int=int(count_data)+1
    count_data = str(count_data_int)
    # Increment the count for the next child's key name
    next_child_key = str(count_data )

    # Construct data
    data = {
        "Time": time,
        value_key: value
    }

    # Insert the data
    database.child("patients").child(patient_key).child("sensors_data").child(sensor_name).child(next_child_key).set(data)

    # Update the 0 key with the new count
    database.child("patients").child(patient_key).child("sensors_data").child(sensor_name).child("0").set(next_child_key)



client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect
client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_forever()
