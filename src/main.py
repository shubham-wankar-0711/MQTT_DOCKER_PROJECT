from fastapi import FastAPI
from src.servers.database import *
from src.servers.routes import MQTT_Router

# CREATING FASTAPI OBJECT
app = FastAPI()

# LINK ROUTES TO FAST API APPLICATION
app.include_router(MQTT_Router)
