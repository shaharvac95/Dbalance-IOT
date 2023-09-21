# Dbalance-IOT
This is a project i made in course called: Requierments engineering IOT (internet of things).
I am excited to share with you the project I did together with my amazing team as part of the IOT(Internet Of Things) requirements engineering course:
Our project is designed to respond to people who have had a stroke, or a heart attack and their arms or legs are not fully functioning.

Our project is called Dbalance, it is a rehabilitation treadmill that contains controllers and sensors, each of which has a role to improve the patients' rehabilitation:

There are 3 controllers on the system: 2 M5STACK core2 controllers and one M5STICK C PLUS controller.
The role of the controllers is to collect, display, and analyze the information coming from the sensors.
Our system includes the following sensors:
1) NFC reader - each patient will have a unique card that will be inserted into the walker and will serve as their ID card.

2) Weight sensors - were installed on both sides of the treadmill, their function is to analyze in real time weight deviation that the patient exerts on one of the sides.

3) Distance sensor - it measures the distance the patient travels in each treatment session, which will indicate the extent of his progress in the rehabilitation process.

4) Voice and LED sensors - their purpose is to give feedback to the patient and let him know if he needs to correct/not correct his position on the treadmill.

5) Camera - designed to record the patient's legs and analyze whether his legs were dragged during the deviation, which would indicate a situation in which the patient's rehabilitation process should be treated differently.

The UI controller displays will show the weights that the patient uses on each side of the treadmill and the distance that he has traveled in the current session.

All the information collected from the controllers and sensors is transferred directly by the MQTT protocol which is better than HTTP when working with IOT, to MQTTCLOUD in a JSON data structure and with the help of Python code the data is pulled in real time from the MQTTCLOUD to the tables in FIRE-BASE data base.
Then an application web page that we created in order to allow the members of the medical staff to enter the patient's profile and view in real time the data , pulls the data from the FIRE-BASE data base and performs several filters on it to filter out unwanted data.
Then the website will present all the relevent statistics on intercative graphs.

Doing the project was a fun and challenging experience and we intend to continue developing it in order to improve its performance and help the patients who need it so much.
