"""
This Code is belong to SME Dehraun. for any query write to schematicslab@gmail.com

"""

import BlynkLib
import RPi.GPIO as GPIO
from BlynkTimer import BlynkTimer

import Adafruit_DHT
import time

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4
BLYNK_AUTH_TOKEN = '6_Fh7GGUAo9SXgv_IZDt147E3_6M9-Lu'

# Initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH_TOKEN)

# Create BlynkTimer Instance
timer = BlynkTimer()


# function to sync the data from virtual pins
@blynk.on("connected")
def blynk_connected():
    print("Hi, You have Connected to New Blynk2.0")
    time.sleep(5);

# Functon for collect data from sensor & send it to Server
def myData():
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    if humidity is not None and temperature is not None:
        # print("Temp={0:0.1f}C Humidity={1:0.1f}%".format(temperature, humidity))
        humidity = round(humidity, 2)
        temperature = round(temperature, 2)
        print("Temperature : {0}*C , Humidity: {1}%".format(temperature, humidity))
        time.sleep(5)
        if temperature > 38.0:
            blynk.log_event("temperature_warning")
        blynk.virtual_write(0, humidity,)
        blynk.virtual_write(1, temperature)
        print("Values sent to New Blynk Server!")
    else:
        print("Sensor failure. Check wiring.");


timer.set_interval(5, myData)


while True:
    blynk.run()
    timer.run()
