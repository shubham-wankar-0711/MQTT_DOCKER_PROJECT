from src.servers.database import *
import json
from fastapi import APIRouter
# from publisher import temperature_sensor_id, humidity_sensor_id

# CREATING APIRouter OBJECT
MQTT_Router = APIRouter()


# FASTAPI ENDPOINT THAT ALLOWS USERS TO FETCH SENSOR READINGS BY SPECIFYING A START AND END RANGE.

@MQTT_Router.get("/readings")
def read_root(Sensor_Name: str, Start_Range: int, End_Range: int):

    # CHECKING DATA EXISTS IN REDIS CACHE
    if redis_client.exists('Sensor/Temperature'):
        print('Fetching Data From Redis Server')
        print()

        # FETCHING REDIS DATA FROM REDIS CACHE
        redis_data = json.loads(redis_client.get(
            'Sensor/'+Sensor_Name.title()))

        # CREATING LIST OF DICTIONARY TO STORE SENSOR READINGS
        data = [{"Sensor/"+Sensor_Name.title(): []}]

        r_data = []
        r_data.append(redis_data)

        for records in r_data[0]['Sensor/'+Sensor_Name.title()]:
            for k, v in records.items():
                if k.lower().find(Sensor_Name.lower()) != -1:
                    if int(records['value'].split()[0]) >= Start_Range and int(records['value'].split()[0]) <= End_Range:
                        data[0]["Sensor/"+Sensor_Name.title()].append(records)
        return data

    else:
        print('Fetching Data From Mongo Database')

        # CREATING LIST OF DICTIONARY TO STORE SENSOR READINGS
        data = [{"Sensor/"+Sensor_Name.title(): []}]

        # FETCHING SENSOR DATA FROM MONGO_DB DATABASE
        result = mongodb_client.mqtt_mongo_db.MQTT_Readings.find(
            {}, {'_id': False})

        for record in result:
            for k, v in record.items():
                if k.lower().find(Sensor_Name.lower()) != -1:
                    if int(record['value'].split()[0]) >= Start_Range and int(record['value'].split()[0]) <= End_Range:
                        data[0]["Sensor/"+Sensor_Name.title()].append(record)

        # STORING DATA TO REDIS CACHE
        redis_client.set("Sensor/"+Sensor_Name.title(), json.dumps(data[0]))
        print("Data Inserted Into Redis Server Database")

        return data


# FASTAPI ENDPOINT TO RETRIEVE THE LAST TEN SENSOR READINGS FOR A SPECIFIC SENSOR.

@MQTT_Router.get("/Last_10_readings")
def read_root(Sensor_Name: str):

    # redis_client.flushdb()

    # CHECKING DATA EXISTS IN REDIS CACHE
    if redis_client.exists('Sensor/Temperature'):
        print('Fetching Data From Redis Server')
        print()

        # FETCHING REDIS DATA FROM REDIS CACHE
        redis_data = json.loads(redis_client.get(
            'Sensor/'+Sensor_Name.title()))

        data = []
        data.append(redis_data)

        return data

    else:
        print("Fetching Data From Mongo Database")
        print()

        # CREATING LIST OF DICTIONARY TO STORE SENSOR READINGS
        data = [{"Sensor/"+Sensor_Name.title(): []}]

        # FETCHING TEMPERATURE SENSOR DATA FROM MONGO_DB DATABASE
        if Sensor_Name.lower() == "temperature":
            result = mongodb_client.mqtt_mongo_db.MQTT_Readings.find(
                {Sensor_Name.lower()+'_sensor_id': 'temperature_sensor_id-1'}, {'_id': False}).sort("timestamp", -1).limit(10)
        else:
            # FETCHING HUMIDITY SENSOR DATA FROM MONGO_DB DATABASE
            result = mongodb_client.mqtt_mongo_db.MQTT_Readings.find(
                {Sensor_Name.lower()+'_sensor_id': 'humidity_sensor_id-2'}, {'_id': False}).sort("timestamp", -1).limit(10)

        for record in result:
            for k, v in record.items():
                if k.lower().find(Sensor_Name.lower()) != -1:
                    data[0]["Sensor/"+Sensor_Name.title()].append(record)

        return data
