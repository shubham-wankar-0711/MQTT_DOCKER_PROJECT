'''
In this implementation, the `Subscriber` class is responsible for establishing a connection to the MQTT broker and subscribing messages to a specified topic using the `subscribe()` method.

You can create instances of the `Subscriber` class to subscribe to different topics as needed.

Remember to provide the MQTT broker address when creating instances of the `Subscriber` class.
'''


import paho.mqtt.client as mqtt
import socket
from Singleton_MongoDB import singleton_mongodb
from Singleton_Redis import redis_client
import json
from abc import ABC, abstractmethod


# ECLIPSE_MOSQUITTO BROKER CONFIGURATION DETAILS

HOSTNAME = socket.gethostname()
IPADDRESS = socket.gethostbyname('eclipse_mosquitto')
MQTT_HOST = IPADDRESS
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 60

# GETTING MONGO_DB CLIENT
myclient = singleton_mongodb.get_mongo_db()

mydb = myclient["mqtt_mongo_db"]
mycollection = mydb["MQTT_Readings"]

# GETTING REDIS CLIENT
myredis = redis_client.get_redis_client()

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


# TOPIC NAMES TO SUBSCRIBE

topic_1 = "Sensor/Temperature"
topic_2 = "Sensor/Humidity"


class Subscriber:

    def subscribe(self, broker_client):
        def on_message(client, userdata, msg):
            print()
            print(
                f'Received "{msg.payload.decode()}" from "{msg.topic}" topic')

            # STORING THE INCOMING MESSAGES FROM PUBLISHER

            test_string = msg.payload.decode().replace("'", '"')

            # DESERIALISE A JSON OBJECT TO A STANDARD PYTHON OBJECT.

            res = json.loads(test_string)

            # INSERTING DATA INTO MONGO_DB

            # mycollection.insert_one(res)
            # print("Data Inserted To MongoDB Successfully : \n {}".format(res))

            DB_Storage.save(res)
            Redis_Storage.save()

            # # IN-MEMORY DATA MANAGEMENT - TO STORE THE LATEST TEN SENSOR READINGS TO REDIS.
            # # TO FETCH AND STORE THE LATEST TEN SENSOR READINGS.

            # # CREATING EMPTY LISTTO STORE THE SENSOR READINGS
            # Sensors_Temperature_Readings = []
            # Sensors_Humidity_Readings = []

            # # FETCHING SENSOR DATA FROM MONGO_DB DATABASE

            # sensor_readings = mycollection.find({}, {'_id': False}).sort(
            #     "timestamp", -1).limit(20)

            # for reading in sensor_readings:
            #     for key, value in reading.items():
            #         if key == "temperature_sensor_id":
            #             Sensors_Temperature_Readings.append(
            #                 reading)

            #         elif key == "humidity_sensor_id":
            #             Sensors_Humidity_Readings.append(
            #                 reading)

            # # CREATING DICTIONARY TO STORE DATA IN REDIS SERVER.

            # temperature_redis_data = {
            #     'Sensor/Temperature': Sensors_Temperature_Readings,
            # }

            # humidity_redis_data = {
            #     'Sensor/Humidity': Sensors_Humidity_Readings,
            # }

            # # TO STORE DICTIONARY DATA TO REDIS SERVER.

            # myredis.set('Sensor/Temperature',
            #             json.dumps(temperature_redis_data))
            # myredis.set('Sensor/Humidity',
            #             json.dumps(humidity_redis_data))

            # print("Data Inserted To RedisDB Successfully : \n {}".format(res))

        broker_client.subscribe(topic_1)
        broker_client.subscribe(topic_2)
        broker_client.on_message = on_message


class DB_Storage:
    def save(message):
        mycollection.insert_one(message)
        print("Data Inserted To MongoDB Successfully : \n {}".format(message))


class Redis_Storage:
    def save():
        # IN-MEMORY DATA MANAGEMENT - TO STORE THE LATEST TEN SENSOR READINGS TO REDIS.
        # TO FETCH AND STORE THE LATEST TEN SENSOR READINGS.

        # CREATING EMPTY LISTTO STORE THE SENSOR READINGS
        Sensors_Temperature_Readings = []
        Sensors_Humidity_Readings = []

        # FETCHING SENSOR DATA FROM MONGO_DB DATABASE

        sensor_readings = mycollection.find({}, {'_id': False}).sort(
            "timestamp", -1).limit(20)

        for reading in sensor_readings:
            for key, value in reading.items():
                if key == "temperature_sensor_id":
                    Sensors_Temperature_Readings.append(
                        reading)

                elif key == "humidity_sensor_id":
                    Sensors_Humidity_Readings.append(
                        reading)

        # CREATING DICTIONARY TO STORE DATA IN REDIS SERVER.

        temperature_redis_data = {
            'Sensor/Temperature': Sensors_Temperature_Readings,
        }

        humidity_redis_data = {
            'Sensor/Humidity': Sensors_Humidity_Readings,
        }

        # TO STORE DICTIONARY DATA TO REDIS SERVER.

        myredis.set('Sensor/Temperature',
                    json.dumps(temperature_redis_data))
        myredis.set('Sensor/Humidity',
                    json.dumps(humidity_redis_data))

        print("Data Inserted To RedisDB Successfully")


broker_client = connect_mqtt()
Subscribers = Subscriber()
Subscribers.subscribe(broker_client)
broker_client.loop_forever()
