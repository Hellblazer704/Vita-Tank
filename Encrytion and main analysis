import random
import time
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import paho.mqtt.client as mqtt
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import logging

# Constants
PH_THRESHOLD = 7.0  # Neutral pH
VISCOSITY_THRESHOLD = 10.0  # Example viscosity threshold
IMPURITY_THRESHOLD = 0.05  # Example impurity threshold
ENCRYPTION_KEY = b'Sixteen byte key'  # Must be 16, 24, or 32 bytes long for AES

# Setup logging
logging.basicConfig(level=logging.INFO)

# AES Encryption/Decryption
def encrypt(data):
    cipher = AES.new(ENCRYPTION_KEY, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(data.encode(), AES.block_size))
    iv = base64.b64encode(cipher.iv).decode('utf-8')
    ct = base64.b64encode(ct_bytes).decode('utf-8')
    return iv, ct

def decrypt(iv, ct):
    iv = base64.b64decode(iv)
    ct = base64.b64decode(ct)
    cipher = AES.new(ENCRYPTION_KEY, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    return pt.decode('utf-8')

# Simulated IoT Sensor Data Collection
class IoTSensor:
    def __init__(self):
        self.ph = 0.0
        self.viscosity = 0.0
        self.impurity = 0.0

    def read_data(self):
        # Simulate reading data from sensors
        self.ph = round(random.uniform(6.0, 8.5), 2)  # Simulated pH value
        self.viscosity = round(random.uniform(5.0, 15.0), 2)  # Simulated viscosity
        self.impurity = round(random.uniform(0.0, 0.1), 2)  # Simulated impurity level
        return self.ph, self.viscosity, self.impurity

# RFID Tracking System
class RFIDSystem:
    def __init__(self):
        self.tank_id = "VitaTank001"

    def track_tank(self):
        # Simulate RFID tracking
        return f"Tracking Tank ID: {self.tank_id}"

# Enhanced Predictive Maintenance Model
class PredictiveMaintenanceModel:
    def __init__(self):
        # Example data for training
        self.data = pd.DataFrame({
            'viscosity': [5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
            'maintenance_needed': [0, 0, 0, 1, 1, 1, 1, 1, 1, 1]
        })
        self.model = RandomForestClassifier()
        self.train_model()

    def train_model(self):
        X = self.data[['viscosity']]
        y = self.data['maintenance_needed']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)

    def predict_maintenance(self, viscosity):
        return self.model.predict([[viscosity]])[0]

# MQTT Client for IoT Sensor Data
class MQTTClient:
    def __init__(self, broker, port, username, password):
        self.client = mqtt.Client()
        self.broker = broker
        self.port = port
        self.client.username_pw_set(username, password)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.connect()

    def connect(self):
        try:
            self.client.tls_set()  # Enable TLS
            self.client.connect(self.broker, self.port, 60)
            self.client.loop_start()
        except Exception as e:
            logging.error(f"Failed to connect to MQTT Broker: {e}")

    def on_connect(self, client, userdata, flags, rc):
        logging.info("Connected")
