#include <ServoShield.h>

#define SERVO_MAX_ANGLE 2400
#define SERVO_MIN_ANGLE 600
#define TORSO 1
#define HEAD 2
#define LEFT_SHOULDER 3
#define RIGHT_SHOULDER 4
#define LEFT_ARM 5
#define RIGHT_ARM 6
#define LEFT_TREAD 7
#define RIGHT_TREAD 8

#include "WProgram.h"
void setup();
void loop();
void move (int servo, int position);
int smooth(int data, float smoothedVal);
ServoShield servos;
int startbyte;
int val;
int targetValues[16];
int currentValues[16];

void setup() {
  
  Serial.begin(115200);
  
  for (int servo = 0; servo < 16; servo++) {
    // Set the minimum and maximum pulse duration of the servo
    servos.setbounds(servo, SERVO_MIN_ANGLE, SERVO_MAX_ANGLE);
    // Set the initial position of the servo
    servos.setposition(servo, 1500);
    
    targetValues[servo] = 90;
    currentValues[servo] = 90;
  }

  servos.start();
  
  // Initial positions
  servos.setposition(TORSO, 1500);
  delay(500);
  servos.setposition(HEAD, 1500);
  delay(500);
  servos.setposition(LEFT_SHOULDER, 1500); 
  delay(500);
  servos.setposition(RIGHT_SHOULDER, 1500); 
  delay(500);
  servos.setposition(LEFT_ARM, 2000);
  delay(500);
  servos.setposition(RIGHT_ARM, 1200);
}

void loop() {
  if (Serial.available() > 2) {
    startbyte = Serial.read();
    // Move servo
    if (startbyte == 255) {
      move(Serial.read(), Serial.read());
    }
  }
}

void move (int servo, int position) {
  val = map(position, 0, 180, SERVO_MIN_ANGLE, SERVO_MAX_ANGLE);
  servos.setposition(servo, val);
}

int smooth(int data, float smoothedVal){
  float filterVal = .9;
  smoothedVal = (data * (1 - filterVal)) + (smoothedVal  *  filterVal);
  Serial.print(data);
  Serial.print(" = ");
  Serial.println(smoothedVal);
  return (int)smoothedVal;
}



int main(void)
{
	init();

	setup();
    
	for (;;)
		loop();
        
	return 0;
}

