import random
import time
import json
import sqlite3
from flask import Flask, jsonify, render_template
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
from sklearn.model_selection import train_test_split

# Constants
PH_THRESHOLD = 7.0
VISCOSITY_THRESHOLD = 10.0
IMPURITY_THRESHOLD = 0.05

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

# Digital Twin Class
class DigitalTwin:
    def __init__(self):
        self.ph = 7.0
        self.viscosity = 10.0
        self.impurity = 0.0
        self.maintenance_needed = False
        self.model = self.train_model()

    def update_state(self):
        # Simulate sensor data
        self.ph = round(random.uniform(6.0, 8.5), 2)
        self.viscosity = round(random.uniform(5.0, 15.0), 2)
        self.impurity = round(random.uniform(0.0, 0.1), 2)
        log_data(self.ph, self.viscosity, self.impurity)
        self.check_conditions()

    def check_conditions(self):
        if self.ph < PH_THRESHOLD or self.viscosity > VISCOSITY_THRESHOLD or self.impurity > IMPURITY_THRESHOLD:
            self.maintenance_needed = True
        else:
            self.maintenance_needed = False

    def train_model(self):
        # Example data for training
        data = pd.DataFrame({
            'viscosity': [5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
            'maintenance_needed': [0, 0, 0, 1, 1, 1, 1, 1, 1, 1]
        })
        X = data[['viscosity']]
        y = data['maintenance_needed']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = RandomForestClassifier()
        model.fit(X_train, y_train)
        return model

    def predict_maintenance(self):
        return self.model.predict([[self.viscosity]])[0]

# Flask Web Server
app = Flask(__name__)
digital_twin = DigitalTwin()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/tank_status')
def tank_status():
    digital_twin.update_state()
    maintenance_prediction = digital_twin.predict_maintenance()
    return jsonify({
        'ph': digital_twin.ph,
        'viscosity': digital_twin.viscosity,
        'impurity': digital_twin.impurity,
        'maintenance_needed': digital_twin.maintenance_needed,
        'predicted_maintenance': bool(maintenance_prediction)
    })

if __name__ == '__main__':
    setup_database()
    app.run(debug=True, host='0.0.0.0', port=5000)
