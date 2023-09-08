import os
import sys
import time
import Adafruit_DHT as dht

try:
    while True:
        humidity, temperature = dht.read_retry(dht.DHT22, 4)
        humidity = round(humidity, 2)
        temperature = round(temperature, 2)
        print("Temperature : {0}*C , Humidity: {1}%".format(temperature, humidity))
        # print("Temperature : {0}{1} Humidity: {2}".format(temperature, chr(176), humidity))
        # print ("Temperature: "+temperature+chr(176)+" Humidity: "+humidity+"%")
        time.sleep(10)
except:
    print(str(sys.exc_info()))
