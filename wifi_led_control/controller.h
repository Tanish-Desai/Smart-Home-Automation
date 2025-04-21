#ifndef controller
#define controller

#include <Arduino.h>

// function prototype created here. Defined in wifi_server.cpp
void update_led(String command, int led);
void update_motor(String command, int motor);

#endif