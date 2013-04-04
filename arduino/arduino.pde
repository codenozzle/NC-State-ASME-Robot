#include <Servo.h>

// Servo variables
int val;
int diff;
int startbyte;
int serialServoId;
int serialServoValue;
int servoStartPin = 2;
Servo servos[8];

// Flags
int serialServoFlag = 255;

// Initial setup
void setup() {
  Serial.begin(9600);
  int servoPin = servoStartPin;
  for (int servoId = 0; servoId < 8; servoId++) {
    servos[servoId].attach(servoPin);
    move(servoId, 90);
    servoPin++;
  }
}

// Main loop
void loop() {
  if (Serial.available() > 2) {
    startbyte = Serial.read();
    
    // Move servo
    if (startbyte == serialServoFlag) {
      move(Serial.read()-1, Serial.read());
    }
    
    // Toggle laser
    if (startbyte == 254) {
      laser(Serial.read(), Serial.read());
    }
  }
}

// Writes a PWM signal to a servo
void move(int servoId, int position) {
  servos[servoId].write(position);
}

// Writes a high/low signal to a pin that has a laser
void laser(int laser, int position) {
  
  if (position == 1) {
    digitalWrite(laser, HIGH);
  } 
  
  if (position == 0) {
    digitalWrite(laser, LOW); 
  }
  
}


