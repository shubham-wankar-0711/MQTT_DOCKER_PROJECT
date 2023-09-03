import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

# TESTING FASTAPI ENDPOINT THAT ALLOWS USERS TO FETCH SENSOR READINGS BY SPECIFYING A START AND END RANGE.


def test_readings_range():
    response = client.get(
        "/readings?Sensor_Name=temperature&Start_Range=10&End_Range=30")
    assert response.status_code == 200
    assert response.json() != ''

# FASTAPI ENDPOINT TO RETRIEVE THE LAST TEN SENSOR READINGS FOR A SPECIFIC SENSOR.


def test_latest_10_readings():
    response = client.get(
        "http://localhost/Last_10_readings?Sensor_Name=humidity")
    assert response.status_code == 200
    assert response.json() != ''
