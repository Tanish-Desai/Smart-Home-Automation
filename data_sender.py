import serial
import time

unoPort = "COM11"

arduino = serial.Serial(port=unoPort, baudrate=9600, timeout=1)
time.sleep(1)

def send_data(data):
    data += "\n"  # append newline so Arduino readStringUntil('\n') can detect the end
    arduino.write(data.encode())
    print(f"Sent: {data}\n")
    
def read_data():
    if arduino.in_waiting > 0:
        response = arduino.readline().decode('utf-8', errors='ignore').strip()
        print(f"Received: {response}\n")
        return response
    return None

def close_serial():
    arduino.close()
    print("Serial communication closed.\n")

if __name__ == "__main__":
    while True:
        user_input = input("->")
        if user_input.lower() == exit:
            break
        send_data(user_input)
        # time.sleep(0.01)
        read_data()

    arduino.close()
    print("Serial connection closed.")