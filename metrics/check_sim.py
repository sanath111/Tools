import serial
import time

ser = serial.Serial(
    port='/dev/serial0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

ser.write(b'AT+CPIN?\r\n')
time.sleep(1)
response = ser.read(100).decode()
print(f"SIM status: {response}")
ser.close()

