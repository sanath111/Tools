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

ser.write(b'AT\r\n')
time.sleep(1)
print(ser.read(100).decode())
ser.close()

