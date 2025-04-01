// #include <wifi_server.h>
#include <controller.h>
#include <WiFi.h>

const char *ssid = "Da PC Oh Yeah!";
const char *password = "babubro345";

/*
Da PC Oh Yeah!
-------------------------------
IP Address: 192.168.137.21
Gateway: 192.168.137.1
Subnet Mask: 255.255.255.0
DNS: 192.168.137.1
*/

// Set your Static IP address parameters
IPAddress local_IP(192, 168, 137, 21);      // Choose an IP outside your DHCP pool
IPAddress gateway(192, 168, 137, 1);        // Your router's IP address
IPAddress subnet(255, 255, 255, 0);       // Typically 255.255.255.0
IPAddress primaryDNS(8, 8, 8, 8);         // Google DNS (or your router's IP)
IPAddress secondaryDNS(8, 8, 4, 4);       // Secondary DNS


// WiFi module is listening on port 80, which is the port for listening HTML data
NetworkServer server(80);

#define led 4
#define LED_BUILTIN 2

void setup(){
    // Run this in setup(). Not in loop()
    Serial.begin(115200);
    pinMode(led, OUTPUT);
    pinMode(LED_BUILTIN, OUTPUT);

    WiFi.mode(WIFI_STA);

    // Configure static IP settings
    if (!WiFi.config(local_IP, gateway, subnet, primaryDNS, secondaryDNS)) {
        Serial.println("STA Failed to configure");
    }

    Serial.println();
    Serial.println();
    Serial.print("Connecting to ");
    Serial.println(ssid);

    WiFi.begin(ssid, password);

    while (WiFi.status() != WL_CONNECTED) {
        digitalWrite(LED_BUILTIN, HIGH);
        delay(250);
        digitalWrite(LED_BUILTIN, LOW);
        delay(250);
        Serial.print(".");
    }
    
    Serial.println("");
    Serial.println("WiFi connected.");
    Serial.println("Static IP address: ");
    Serial.println(WiFi.localIP());

    server.begin();
}

bool was_client_connected = false;
bool was_WiFi_disconnected = false;

void loop(){
    // Run this in loop()
    NetworkClient client = server.accept();  // listen for incoming clients

    // Check and fix if WiFi is disconnected.
    if(WiFi.status() != WL_CONNECTED){
        Serial.println("WiFi Disconnected");
        while(WiFi.status() != WL_CONNECTED){
            digitalWrite(LED_BUILTIN, HIGH);
            delay(250);
            digitalWrite(LED_BUILTIN, LOW);
            delay(250);
            Serial.print(".");
        }
        Serial.println("");
        Serial.println("WiFi connected.");
        Serial.println("Static IP address: ");
        Serial.println(WiFi.localIP());
    }

    if (client) {                     // if you get a client,
    digitalWrite(LED_BUILTIN, LOW);
    
    Serial.println("New Client.");  // print a message out the serial port
    client.println("Connected");
    String currentLine = "";        // make a String to hold incoming data from the client
        while (client.connected()) {    // loop while the client's connected
            was_client_connected = true;
            if (client.available()) {     // if there's bytes to read from the client,
                // Do something with the data
                digitalWrite(LED_BUILTIN, HIGH);
                String data = client.readStringUntil('\n');
                data.trim();

                Serial.print("Received: ");
                Serial.println(data);
                Serial.println();

                client.print("Data Received (ESP32): ");
                client.println(data);

                update_led(data, led);
                digitalWrite(LED_BUILTIN, LOW);
            }
        }
    }
    if(was_client_connected){
        // close the connection:
        client.stop();
        Serial.println("Client Disconnected.");
        was_client_connected = false;
    }

    // Blinker to indicate no connected client
    digitalWrite(LED_BUILTIN, HIGH);
    delay(100);
    digitalWrite(LED_BUILTIN, LOW);
    delay(100);
}
