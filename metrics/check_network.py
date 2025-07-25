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

# Check network registration
ser.write(b'AT+CREG?\r\n')
time.sleep(1)
response = ser.read(100).decode()
print(f"Network registration: {response}")
ser.close()
