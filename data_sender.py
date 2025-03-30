import serial
import time

unoPort = "COM11"

arduino = serial.Serial(port=unoPort, baudrate=9600, timeout=1)
time.sleep(1)

def send_data(data):
    arduino.write(data.encode())
    print(f"Sent: {data}\n")
    
def read_data():
    if arduino.in_waiting > 0:
        response = arduino.readLine().decode().strip()
        print(f"Received: \n{response}\n")
        return response
    return None

def close_serial():
    arduino.close()
    print("Serial communication closed.\n")
        