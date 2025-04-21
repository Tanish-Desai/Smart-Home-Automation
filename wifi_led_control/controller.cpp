#include<controller.h>

void update_led(String command, int led){
    if(command == "on"){ 
        Serial.println("Switched ON");
		digitalWrite(led, HIGH);
	}#include<controller.h>

    void update_led(String command, int led){
        if(command == "led_on"){ 
            Serial.println("LED Switched ON");
            digitalWrite(led, HIGH);
        }
        else if(command=="led_off"){
            Serial.println("LED Switched OFF");
            digitalWrite(led, LOW);
        }
    }
    
    void update_motor(String command, int motor){
        if(command == "motor_on"){ 
            Serial.println("Motor Switched ON");
            digitalWrite(motor, HIGH);
        }
        else if(command=="motor_off"){
            Serial.println("Motor Switched OFF");
            digitalWrite(motor, LOW);
        }
    }
    else if(command=="off"){
        Serial.println("Switched OFF");
        digitalWrite(led, LOW);
    }
}