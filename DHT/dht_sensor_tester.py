#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import time
import board
import adafruit_dht

# Sensor setup
DHT_SENSOR = adafruit_dht.DHT22
# The pin connected to the DHT22 data line.
# Use the Board pin numbering scheme. For example, D4 refers to GPIO 4.
DHT_PIN = board.D4

def test_dht22_sensor():
    """
    Tests the DHT22 sensor by continuously reading temperature and humidity.
    Prints the readings or an error message if the sensor fails.
    """
    print("--- DHT22 Sensor Tester (using Adafruit CircuitPython DHT) ---")
    print(f"Attempting to read from DHT22 sensor on pin {DHT_PIN}.")
    print("Press Ctrl+C to stop.")

    # Initial the dht device, with data pin connected to:
    dht_device = DHT_SENSOR(DHT_PIN)

    try:
        while True:
            try:
                temperature_c = dht_device.temperature
                humidity = dht_device.humidity

                if temperature_c is not None and humidity is not None:
                    # Round values for cleaner output
                    temperature_c = round(temperature_c, 2)
                    humidity = round(humidity, 2)
                    print(f"{time.ctime()} - Temperature: {temperature_c}°C, Humidity: {humidity}%")
                else:
                    print(f"{time.ctime()} - Failed to retrieve data from sensor. Retrying...")

            except RuntimeError as error:
                # Errors happen fairly often, DHT readings are touchy!
                print(f"{time.ctime()} - DHT sensor error: {error.args[0]}. Retrying...")
                time.sleep(2.0)  # Wait a bit before retrying to avoid spamming
                continue
            except Exception as error:
                dht_device.exit()
                raise error

            time.sleep(2.0)  # DHT22 can only be read every 2 seconds (minimum)
    except KeyboardInterrupt:
        print("\n--- DHT22 Sensor Test Stopped ---")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
    finally:
        # Clean up the DHT device when done
        dht_device.exit()

if __name__ == "__main__":
    test_dht22_sensor()
