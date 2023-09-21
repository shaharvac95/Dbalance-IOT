import json
import paho.mqtt.client as mqtt
from datetime import datetime
import pytz
import pyrebase

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

firebase = pyrebase.initialize_app(config)
database = firebase.database()
count_data_global = ""
# MQTT Configuration
MQTT_BROKER = 'hairdresser.cloudmqtt.com'
MQTT_PORT = 15697
MQTT_USERNAME = 'team6_2'
MQTT_PASSWORD = 'braude1234'
MQTT_TOPIC = 'braude/teams/team6'
patient_data_key = ""
message_data = ""
patients_data = ""
patient_data = ""
sensors_data = ""
distance_val = ""
# When connected to MQTT
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(MQTT_TOPIC)

# When message is received from MQTT
def on_message(client, userdata, msg):
    global patient_data_key,sensors_data
    print(f"Received message from topic {msg.topic}: {msg.payload.decode()}")



    message_data = json.loads(msg.payload.decode())

    patients_data = json.loads(message_data['patients'])
    patient_data_key = next(iter(patients_data))
    patient_data = json.loads(patients_data[patient_data_key])
    sensors_data = json.loads(patient_data['sensors_data'])
    card_in_value = sensors_data.get('card_in', None)

    print("card_in_value" + str(card_in_value))


    if (card_in_value):

        with open('C:/Users/alex5/Desktop/STUDY/IOT/dbalance/DbalanceV5.2/current_user_run.txt', 'w') as file1:
            file1.write(patient_data_key)
        with open('C:/Users/alex5/Desktop/STUDY/IOT/dbalance/DbalanceV5.2/card_status.txt', 'w') as file2:
            file2.write(str(card_in_value))


        # Get all the values
        deflection_val = float(sensors_data['deflection'])
        weight_left = float(sensors_data['weight_left'])
        weight_right = float(sensors_data['weight_right'])
        count_data_global = database.child("patients").child(patient_data_key).child("sensors_data").child("deflection").child("0").get().val()

        # Prepare data for all sensors
        sensor_values = {
            "deflection": ("def_val", deflection_val),
            "weight_right": ("wg_val", weight_right),
            "weight_left": ("wg_val", weight_left),
        }
        # Get current time once and use it throughout the function


        tz = pytz.timezone('Etc/GMT-3')
        current_time = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')
        print(current_time)

        # Batch the updates for Firebase
        for sensor_name, (value_key, value) in sensor_values.items():
            insert_sensor_data(sensor_name, value_key, value, current_time, patient_data_key)

        print("Data inserted successfully!")
        timeend_check = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')
        print(timeend_check)

    else:
        with open('C:/Users/alex5/Desktop/STUDY/IOT/dbalance/DbalanceV5.2/card_status.txt', 'w') as file:
            file.write(str(card_in_value))



    # Construct the data for Firebase
    # data = {
    #     "Time": current_time,
    #     "def_val": deflection_val,
    #     "wg_val": weight_val,
    #     "dis_val":distance_val
    # }

    # # Now insert data to Firebase using the helper function
    # insert_sensor_data("deflection", "def_val", deflection_val, current_time, patient_data_key)
    # insert_sensor_data("weight_right", "wg_val", weight_right, current_time, patient_data_key)
    # insert_sensor_data("weight_left", "wg_val", weight_left, current_time, patient_data_key)
    # insert_sensor_data("distance", "dis_val", distance_val, current_time, patient_data_key)


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
    next_child_key = str(count_data)

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
