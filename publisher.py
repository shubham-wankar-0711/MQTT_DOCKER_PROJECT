''''
In this implementation, the `Publisher` class is responsible for establishing a connection to the MQTT broker and publishing messages to a specified topic using the `publish()` method.

You can create instances of the `Publisher` class to publish to different topics as needed.

Remember to provide the MQTT broker address when creating instances of the `Publisher` class.
'''


import paho.mqtt.client as mqtt
import socket
from datetime import datetime
import random
import time
import os


# ECLIPSE_MOSQUITTO BROKER CONFIGURATION DETAILS

HOSTNAME = socket.gethostname()
IPADDRESS = socket.gethostbyname('eclipse_mosquitto')
MQTT_HOST = IPADDRESS
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 60

# CONNECTING TO ECLIPSE_MOSQUITTO BROKER


def connect_mqtt():

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
            print()
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt.Client()
    client.on_connect = on_connect
    client.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)
    return client


class Publisher:
    def __init__(self, broker_client):
        self.broker_client = broker_client

    def publish(self, message, topic):
        time.sleep(1)
        result = self.broker_client.publish(topic, str(message))
        status = result[0]
        if status == 0:

            print(f"Send `{message}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {self.topic}")


broker_client = connect_mqtt()
broker_client.loop_start()

temperature_sensor_id = 'temperature_sensor_id-1'
humidity_sensor_id = 'humidity_sensor_id-2'

Publishers = Publisher(broker_client)

readings = 0

# WHILE LOOP TO GENERATE RANDOM DATA WITH SENSOR READINGS, VALUES AND ISO8601_FORMATTED_DATE_TIME
while readings < 20:

    topic_1 = "Sensor/Temperature"
    topic_1_message = {'temperature_sensor_id': temperature_sensor_id,
                       'value': f"{random.randint(10, 50)}" + " \N{DEGREE SIGN}" + "C", 'timestamp': datetime.now().isoformat()}
    Publishers.publish(topic_1_message, topic_1)

    topic_2 = "Sensor/Humidity"
    topic_2_message = {'humidity_sensor_id': humidity_sensor_id,
                       'value': f"{random.randint(10, 50)}" + " \N{DEGREE SIGN}" + "C", 'timestamp': datetime.now().isoformat()}
    Publishers.publish(topic_2_message, topic_2)

    readings = readings+1
