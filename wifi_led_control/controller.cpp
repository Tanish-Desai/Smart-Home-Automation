#include<controller.h>

void update_led(String command, int led){
    if(command == "on"){ 
        Serial.println("Switched ON");
		digitalWrite(led, HIGH);
	}
    else if(command=="off"){
        Serial.println("Switched OFF");
        digitalWrite(led, LOW);
    }
}