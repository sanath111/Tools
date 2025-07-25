#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import board
import adafruit_dht
import mysql.connector
import socket

# Sensor setup
DHT_SENSOR = adafruit_dht.DHT22
DHT_PIN = board.D4

# Database config
DB_HOST = '192.168.1.183'
DB_PORT = 3306
DB_USER = 'sensor_user'
DB_PASSWORD = ''
DB_NAME = 'sensor_db'
DB_TABLE = 'dht_sensor_data'

hostname = str(socket.gethostname().strip())

# Function to insert data into MariaDB
def insert_to_db(temperature, humidity):
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor()
        sql = f"INSERT INTO {DB_TABLE} (timestamp, temperature, humidity, host) VALUES (NOW(), %s, %s, %s)"
        cursor.execute(sql, (temperature, humidity, hostname))
        conn.commit()
        print(f"Data inserted: Temp={temperature:.2f}°C, Humidity={humidity:.2f}%")
    except mysql.connector.Error as err:
        print("MySQL Error:", err)
    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass


# Initialize DHT device
dht_device = DHT_SENSOR(DHT_PIN)

try:
    while True:
        try:
            # Read temperature and humidity
            temperature = dht_device.temperature
            humidity = dht_device.humidity

            if temperature is not None and humidity is not None:
                # Round values for consistency
                temperature = round(temperature, 2)
                humidity = round(humidity, 2)
                # Print readings
                print(time.ctime() + f" Temp={temperature:.2f}°C, Humidity={humidity:.2f}%")
                # Insert into database
                insert_to_db(temperature, humidity)
            else:
                print("Sensor failure. Check wiring.")
        except RuntimeError as error:
            print(f"DHT sensor error: {error.args[0]}. Retrying...")
            time.sleep(2.0)  # Wait before retrying
        time.sleep(10)  # Main loop interval
except KeyboardInterrupt:
    print("\n--- Sensor Logging Stopped ---")
finally:
    dht_device.exit()  # Clean up DHT device

