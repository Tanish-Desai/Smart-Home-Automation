import socket

ESP32_IP = '192.168.137.21'
PORT = 80  # You can change the port if needed

# Create the TCP/IP socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(5) # Set a 500ms timeout


def connect_socket():
    try:
        print("Connecting...\n")
        s.connect((ESP32_IP, PORT))
        print("Connected!")
    except socket.timeout as e:
        print("Socket timeout error:", e)
    except Exception as e:
        print("Socket error:", e)

# connect_socket()

def send_data(data):
    data += "\n"
    s.sendall(data.encode())
    # print(f"Sent: {data}")

def close_socket():
    print("WiFi Socket closed.\n")
    s.close()
    
def read_data():
    chunks = []
    try:
        while True:
            chunk = s.recv(4096)  # read 4096 bytes at a time
            if not chunk:
                break
            chunks.append(chunk)
            if b'\n' in chunk:  # stop reading when newline is found
                break
    except socket.timeout:
        # If no data received yet, exit from loop
        # NOTE: socket.timeout is the exception object returned by python. Whereas s.timeout only holds the timeout value 
        pass
    data = b''.join(chunks).decode()
    return None if data == "" else data

if __name__ == "__main__":
    connect_socket()
    while True:
        user_input = input("->")
        if user_input.lower() == "exit":
            break
        send_data(user_input)
        print(f"Sent: {user_input}\n")
        # time.sleep(0.01)
        print("Client (ME) Received...\n"+(30*'-'))
        print(f"{read_data()}"+(30*'-'))

    close_socket()
# else:
#     while(True):
#         chunks = []
#         try:
#             while True:
#                 chunk = s.recv(4096)  # read 4096 bytes at a time
#                 if not chunk:
#                     break
#                 chunks.append(chunk)
#                 if b'\n' in chunk:  # stop reading when newline is found
#                     break
#         except socket.timeout:
#             # If no data received yet, exit from loop
#             # NOTE: socket.timeout is the exception object returned by python. Whereas s.timeout only holds the timeout value 
#             pass
#         data = b''.join(chunks).decode()
    
# Usage:
# ... use send_data() and read_data() as needed ...
# When finished, close the socket:
# close_socket()