import sqlite3
import time
import threading
import Adafruit_DHT
from flask import Flask, jsonify, render_template, request
from datetime import datetime, timedelta
import pytz

app = Flask(__name__)

# Sensor and database setup
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4
DB_FILE = "sensor_data.db"
IST = pytz.timezone('Asia/Kolkata')


# Create table if it doesn't exist
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            temperature REAL,
            humidity REAL
        )
    ''')
    conn.commit()
    conn.close()


# Function to log sensor data in the database
def log_data():
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
        if humidity is not None and temperature is not None:
            humidity = round(humidity, 2)
            temperature = round(temperature, 2)
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO readings (temperature, humidity) VALUES (?, ?)", (temperature, humidity))
            conn.commit()
            conn.close()
        time.sleep(10)  # Read every 10 seconds


# API to get the latest sensor data
@app.route('/current', methods=['GET'])
def get_current_data():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT temperature, humidity, timestamp FROM readings ORDER BY timestamp DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()

    if row:
        timestamp_utc = datetime.strptime(row[2], "%Y-%m-%d %H:%M:%S")
        timestamp_ist = timestamp_utc.replace(tzinfo=pytz.utc).astimezone(IST).strftime("%Y-%m-%d %H:%M:%S")

        return jsonify({"temperature": row[0], "humidity": row[1], "timestamp": timestamp_ist})
    return jsonify({"error": "No data available"}), 500


# API to get historical data for chart with time range filtering
@app.route('/history', methods=['GET'])
def get_history():
    time_range = request.args.get('range', 'live')  # Default to 'live'
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    if time_range == 'live':
        cursor.execute("SELECT timestamp, temperature, humidity FROM readings ORDER BY timestamp DESC LIMIT 10")  # Last 100 readings
    elif time_range == 'daily':
        now = datetime.now(IST)
        start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
        cursor.execute("SELECT timestamp, temperature, humidity FROM readings WHERE timestamp BETWEEN ? AND ? ORDER BY timestamp DESC", (start_of_day.strftime("%Y-%m-%d %H:%M:%S"), now.strftime("%Y-%m-%d %H:%M:%S")))
    elif time_range == 'weekly':
        now = datetime.now(IST)
        start_of_week = now - timedelta(days=now.weekday())  # Start of this week
        start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
        cursor.execute("SELECT timestamp, temperature, humidity FROM readings WHERE timestamp BETWEEN ? AND ? ORDER BY timestamp DESC", (start_of_week.strftime("%Y-%m-%d %H:%M:%S"), now.strftime("%Y-%m-%d %H:%M:%S")))
    elif time_range == 'monthly':
        now = datetime.now(IST)
        start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        cursor.execute("SELECT timestamp, temperature, humidity FROM readings WHERE timestamp BETWEEN ? AND ? ORDER BY timestamp DESC", (start_of_month.strftime("%Y-%m-%d %H:%M:%S"), now.strftime("%Y-%m-%d %H:%M:%S")))
    elif time_range == 'yearly':
        now = datetime.now(IST)
        start_of_year = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        cursor.execute("SELECT timestamp, temperature, humidity FROM readings WHERE timestamp BETWEEN ? AND ? ORDER BY timestamp DESC", (start_of_year.strftime("%Y-%m-%d %H:%M:%S"), now.strftime("%Y-%m-%d %H:%M:%S")))
    else:
        return jsonify({"error": "Invalid time range"}), 400


    rows = cursor.fetchall()
    conn.close()

    data = []
    for row in rows:
        timestamp_utc = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
        timestamp_ist = timestamp_utc.replace(tzinfo=pytz.utc).astimezone(IST).strftime("%Y-%m-%d %H:%M:%S")
        data.append({"timestamp": timestamp_ist, "temperature": row[1], "humidity": row[2]})

    return jsonify(data)


@app.route('/')
def index():
    return render_template('index.html')


# Start data logging in a background thread
init_db()
threading.Thread(target=log_data, daemon=True).start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
