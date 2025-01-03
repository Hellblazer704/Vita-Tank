import random
import time
import json
import sqlite3
from flask import Flask, jsonify, render_template
from sklearn.ensemble import RandomForestRegressor
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import logging

# Constants
PH_THRESHOLD = 7.0
VISCOSITY_THRESHOLD = 10.0
IMPURITY_THRESHOLD = 0.05
TEMP_THRESHOLD = 25.0  # Example temperature threshold

# Setup logging
logging.basicConfig(level=logging.INFO)

# Database setup
def setup_database():
    conn = sqlite3.connect('tank_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS sensor_data
                 (timestamp TEXT, ph REAL, viscosity REAL, impurity REAL, temperature REAL)''')
    conn.commit()
    conn.close()

def log_data(ph, viscosity, impurity, temperature):
    conn = sqlite3.connect('tank_data.db')
    c = conn.cursor()
    c.execute("INSERT INTO sensor_data (timestamp, ph, viscosity, impurity, temperature) VALUES (?, ?, ?, ?, ?)",
              (time.strftime("%Y-%m-%d %H:%M:%S"), ph, viscosity, impurity, temperature))
    conn.commit()
    conn.close()

# Digital Twin Class
class DigitalTwin:
    def __init__(self):
        self.ph = 7.0
        self.viscosity = 10.0
        self.impurity = 0.0
        self.temperature = 25.0
        self.model = self.train_model()

    def update_state(self):
        # Simulate sensor data
        self.ph = round(random.uniform(6.0, 8.5), 2)
        self.viscosity = round(random.uniform(5.0, 15.0), 2)
        self.impurity = round(random.uniform(0.0, 0.1), 2)
        self.temperature = round(random.uniform(20.0, 30.0), 2)  # Simulated temperature
        log_data(self.ph, self.viscosity, self.impurity, self.temperature)
        self.adjust_conditions()

    def adjust_conditions(self):
        # Use the AI model to predict adjustments needed
        adjustments = self.model.predict([[self.ph, self.viscosity, self.impurity, self.temperature]])[0]
        
        # Apply adjustments with limits
        self.ph = max(6.0, min(8.5, self.ph + adjustments[0]))
        self.temperature = max(20.0, min(30.0, self.temperature + adjustments[1]))
        self.viscosity = max(5.0, min(15.0, self.viscosity + adjustments[2]))
        self.impurity = max(0.0, min(0.1, self.impurity + adjustments[3]))

        logging.info(f"Adjusted conditions: pH={self.ph}, Temperature={self.temperature}, "
                     f"Viscosity={self.viscosity}, Impurity={self.impurity}")

    def train_model(self):
        # Example data for training
        data ```python
        data = pd.DataFrame({
            'ph': [6.5, 7.0, 7.5, 8.0, 6.0, 7.2, 7.8, 6.8, 7.1, 7.3],
            'viscosity': [5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
            'impurity': [0.01, 0.02, 0.03, 0.04, 0.05, 0.01, 0.02, 0.03, 0.04, 0.05],
            'temperature': [20, 21, 22, 23, 24, 25, 26, 27, 28, 29],
            'adjustment_ph': [0.1, 0.0, -0.1, 0.2, -0.2, 0.1, 0.0, -0.1, 0.1, 0.0],
            'adjustment_temp': [0.5, 0.0, -0.5, 0.5, -0.5, 0.5, 0.0, -0.5, 0.5, 0.0],
            'adjustment_viscosity': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            'adjustment_impurity': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        })
        X = data[['ph', 'viscosity', 'impurity', 'temperature']]
        y = data[['adjustment_ph', 'adjustment_temp', 'adjustment_viscosity', 'adjustment_impurity']]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = RandomForestRegressor()
        model.fit(X_train, y_train)
        return model

# Flask Web Server
app = Flask(__name__)
digital_twin = DigitalTwin()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/tank_status')
def tank_status():
    digital_twin.update_state()
    return jsonify({
        'ph': digital_twin.ph,
        'viscosity': digital_twin.viscosity,
        'impurity': digital_twin.impurity,
        'temperature': digital_twin.temperature
    })

if __name__ == '__main__':
    setup_database()
    app.run(debug=True, host='0.0.0.0', port=5000)
