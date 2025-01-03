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
import sqlite3  # For local data storage
import smtplib  # For sending alerts via email

# Constants
PH_THRESHOLD = 7.0  # Neutral pH
VISCOSITY_THRESHOLD = 10.0  # Example viscosity threshold
IMPURITY_THRESHOLD = 0.05  # Example impurity threshold
ENCRYPTION_KEY = b'Sixteen byte key'  # Must be 16, 24, or 32 bytes long for AES
ALERT_EMAIL = "your_email@example.com"  # Replace with your email

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

# Database setup
def setup_database():
    conn = sqlite3.connect('tank_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS sensor_data
                 (timestamp TEXT, ph REAL, viscosity REAL, impurity REAL)''')
    conn.commit()
    conn.close()

def log_data(ph, viscosity, impurity):
    conn = sqlite3.connect('tank_data.db')
    c = conn.cursor()
    c.execute("INSERT INTO sensor_data (timestamp, ph, viscosity, impurity) VALUES (?, ?, ?, ?)",
              (time.strftime("%Y-%m-%d %H:%M:%S"), ph, viscosity, impurity))
    conn.commit()
    conn.close()

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
            'viscosity': [5 , 6, 7, 8, 9, 10, 11, 12, 13, 14],
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

# Alert System
def send_alert(message):
    try:
        with smtplib.SMTP('smtp.example.com', 587) as server:  # Replace with your SMTP server
            server.starttls()
            server.login("your_email@example.com", "your_password")  # Replace with your email and password
            server.sendmail(ALERT_EMAIL, ALERT_EMAIL, message)
            logging.info("Alert sent successfully.")
    except Exception as e:
        logging.error(f"Failed to send alert: {e}")

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
        logging.info("Connected to MQTT Broker")
        self.client.subscribe("tank/sensor_data")

    def on_message(self, client, userdata, msg):
        data = json.loads(msg.payload)
        ph = data['ph']
        viscosity = data['viscosity']
        impurity = data['impurity']
        log_data(ph, viscosity, impurity)

        # Check conditions and send alerts if necessary
        if ph < PH_THRESHOLD or viscosity > VISCOSITY_THRESHOLD or impurity > IMPURITY_THRESHOLD:
            send_alert(f"Alert! Conditions exceeded: pH={ph}, Viscosity={viscosity}, Impurity={impurity}")

# Main function to run the system
def main():
    setup_database()
    sensor = IoTSensor()
    rfid = RFIDSystem()
    maintenance_model = PredictiveMaintenanceModel()
    mqtt_client = MQTTClient("mqtt_broker_address", 8883, "username", "password")  # Replace with actual values

    while True:
        ph, viscosity, impurity = sensor.read_data()
        mqtt_client.client.publish("tank/sensor_data", json.dumps({
            'ph': ph,
            'viscosity': viscosity,
            'impurity': impurity
        }))
        maintenance_needed = maintenance_model.predict_maintenance(viscosity)
        if maintenance_needed:
            send_alert("Maintenance required for the tank.")
        time.sleep(10)  # Adjust the sleep time as needed

if __name__ == "__main__":
    main()
