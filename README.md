
# Smart Home Automation

A WiFi-enabled home automation system to control home devices using the ESP32 DevKit board. This project was developed as a physics mini-project and demonstrates practical applications of WiFi technology and electromagnetic wave communication, alongside gesture tracking using computer vision.

## Table of Contents

- [About](#about)
    
- [Project Components](#project-components)
    
- [How It Works](#how-it-works)
    
- [Software and Libraries](#software-and-libraries)
    
- [Arduino Code: WiFi LED Control](#arduino-code-wifi-led-control)
    
- [Future Enhancements](#future-enhancements)
    
- [Setup and Usage](#setup-and-usage)
    
- [License](#license)
    
- [Contact](#contact)
    

## About

This project showcases a home automation system where an ESP32 board is used to control a 9W bulb through a relay module over WiFi. In addition, the project integrates gesture tracking using the MediaPipe library and OpenCV to capture camera input and translate specific gestures into control commands. Designed for a physics course mini-project, it emphasizes the electromagnetic nature of WiFi technology, exploring how wireless signals are harnessed to transmit control data.

## Project Components

The hardware used for this project includes:

- **Espressif ESP32-WROOM-32**: The main microcontroller responsible for WiFi connectivity and control logic.
    
- **Relay Module**: (For example, the SRD-05VDC-SL-C relay module) used to switch the 9W bulb on and off.
    
- **Jumper Wires**: For making the necessary electrical connections.
    
- **Micro USB Cable**: (Typically a USB 2.0 Micro-B cable) used to power and program the ESP32.
    
- **9W Bulb and Connecting Wires**: The load controlled by the system.
    

## How It Works

- **WiFi Connectivity:**  
    The ESP32 board connects to a WiFi network, harnessing electromagnetic waves for wireless communication. This aspect of the project highlights the physical principles behind WiFi technology, such as radio wave propagation and modulation.
    
- **Device Control:**  
    Commands are sent over the network to control the relay, which in turn switches the bulb on or off. The system can be further enhanced to support more devices.
    
- **Gesture Tracking:**  
    Using the MediaPipe library for hand or gesture tracking and OpenCV for real-time camera feed processing, the project can detect specific gestures. These gestures are interpreted by the Python script (`gesture_tracker.py`) to trigger device control commands over WiFi.
    

## Software and Libraries

- **Python Scripts:**
    
    - `gesture_tracker.py`: Captures and processes camera feed, utilizing MediaPipe for gesture recognition.
        
    - `wifi_talker.py`: Manages WiFi communication between the ESP32 and the control interface.
        
- **Required Libraries:**  
    Check the `requirements.txt` file for a complete list of Python dependencies. Essential libraries include:
    
    - **MediaPipe:** For robust gesture recognition.
        
    - **OpenCV:** For accessing and processing the camera feed.
        

## Arduino Code: WiFi LED Control

Inside the `wifi_led_control` folder, you will find Arduino sketches that serve as the firmware for the ESP32 board. These sketches include:

- **WiFi Server Setup:**  
    The Arduino code sets up a WiFi server on the ESP32, allowing it to listen for incoming control commands.
    
- **LED/Relay Control:**  
    The code includes routines to switch the relay (and hence the connected bulb) on or off based on the commands received over WiFi.
    
- **Ease of Integration:**  
    These sketches provide a template for further expansion, making it easy to integrate additional features like custom SSID/password control or interfacing with other sensors/devices.
    

## Future Enhancements

Plans for future development include:

- **Custom SSID and Password Control:**  
    Allowing users to define custom network credentials for enhanced security and ease of setup.
    
- **Hosting a Webpage on the LAN:**  
    Creating a local web interface to simplify device control and configuration without needing additional software.
    
- **Android Integration:**  
    Extending control features to Android devices, enabling a more accessible and user-friendly mobile interface.
    

## Setup and Usage

### Hardware Connections

Make the connections as follows:

- **ESP32 to Relay:**
    
    - **D4 (ESP32)** → Signal pin of relay
        
    - **3V3 (ESP32)** → '+' pin of relay
        
    - **GND (ESP32)** → '-' pin of relay
        
- **Relay to Appliance Power:**
    
    - **COMMON (relay)** → Live wire from the power source
        
    - **NO (Normally Open) (relay)** → Appliance power input
        
    - **Neutral (Power Source)** → Neutral terminal of the appliance
        

### Steps

1. **Hardware Setup:**
    
    - Connect the ESP32 to the relay module following the connections above.
        
    - Wire the relay to control the 9W bulb.
        
    - Power the ESP32 using the micro USB cable.
        
2. **Programming the ESP32:**
    
    - Open the Arduino IDE and load the sketches from the `wifi_led_control` folder.
        
    - Compile and upload the code to your ESP32 board.
        
3. **Running the Python Scripts:**
    
    - Ensure all dependencies from `requirements.txt` are installed.
        
    - Run `gesture_tracker.py` to start the camera feed and gesture recognition.
        
    - Use `wifi_talker.py` to send control commands over WiFi as detected by gestures.
