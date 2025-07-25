import serial
import time

def send_sms(phone_number, message, smsc_number):
    try:
        # Initialize serial connection
        ser = serial.Serial(
            port='/dev/serial0',
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )

        # Check module responsiveness
        ser.write(b'AT\r\n')
        time.sleep(1)
        response = ser.read(100).decode()
        print(f"AT response: {response}")
        if "OK" not in response:
            raise Exception("Module not responding")

        # Check SIM status
        ser.write(b'AT+CPIN?\r\n')
        time.sleep(1)
        response = ser.read(100).decode()
        print(f"SIM status: {response}")
        if "READY" not in response:
            raise Exception("SIM not ready")

        # Check network registration
        ser.write(b'AT+CREG?\r\n')
        time.sleep(1)
        response = ser.read(100).decode()
        print(f"Network registration: {response}")
        if "0,1" not in response and "0,5" not in response:
            # Attempt manual registration to BSNL
            ser.write(b'AT+COPS=1,2,"40471"\r\n')
            time.sleep(10)
            ser.write(b'AT+CREG?\r\n')
            time.sleep(1)
            response = ser.read(100).decode()
            print(f"Network registration after COPS: {response}")
            if "0,1" not in response and "0,5" not in response:
                raise Exception("Failed to register to network")

        # Set SMSC number
        ser.write(f'AT+CSCA="{smsc_number}"\r\n'.encode())
        time.sleep(1)
        response = ser.read(100).decode()
        print(f"SMSC response: {response}")
        if "OK" not in response:
            raise Exception("Failed to set SMSC")

        # Set SMS text mode
        ser.write(b'AT+CMGF=1\r\n')
        time.sleep(1)
        response = ser.read(100).decode()
        print(f"Text mode response: {response}")
        if "OK" not in response:
            raise Exception("Failed to set text mode")

        # Send SMS
        ser.write(f'AT+CMGS="{phone_number}"\r\n'.encode())
        time.sleep(1)
        response = ser.read(100).decode()
        print(f"Send command response: {response}")
        if ">" not in response:
            raise Exception("Failed to initiate SMS")

        # Send message content
        ser.write(f"{message}\r\n".encode())
        time.sleep(1)

        # Send Ctrl+Z
        ser.write(chr(26).encode())
        time.sleep(2)
        response = ser.read(100).decode()
        print(f"Message sent response: {response}")
        if "OK" not in response:
            raise Exception("Failed to send SMS")

        ser.close()
        print(f"SMS sent successfully to {phone_number}: {message}")
        return True

    except Exception as e:
        print(f"Error: {e}")
        if ser.is_open:
            ser.close()
        return False

if __name__ == "__main__":
    recipient = "+919164047824"  # Your recipient number
    message = "Test SMS from Raspberry Pi!"
    smsc_number = "+919434022121"  # BSNL SMSC number
    send_sms(recipient, message, smsc_number)

