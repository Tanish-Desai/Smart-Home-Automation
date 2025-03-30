import serial
import time

unoPort = 'COM11'

# Setup Serial connection
arduino = serial.Serial(port=unoPort, baudrate=9600, timeout=1)

time.sleep(1) # Wait for connection to establish

def send_data(data):
    data+='\n'
    arduino.write(data.encode()) # send data in bytes
    print(f"Sent: {data}\n")
    
def read_data():
    if arduino.in_waiting > 0:
        response = arduino.readline().decode().strip()
        print(f"Received: \n{response}\n")
        return response
    return None

print("Type \"exit\" to quit")

while True:
    user_input = input("->")
    if user_input.lower() == exit:
        break
    send_data(user_input)
    # time.sleep(0.01)
    read_data()

arduino.close()
print("Serial connection closed.")
    