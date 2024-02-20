/*******************************************************************************
 * DESCRIPTION:
 *
 * This example shows how to drive a motor using the PWM and DIR pins.
 * This example only shows how to drive a single motor for simplicity.
 * For dual channel motor driver, both channel work the same way.
 * 
 * 
 * CONNECTIONS:
 * 
 * Arduino D5  - Motor Driver PWM Input
 * Arduino D4  - Motor Driver DIR Input
 * Arduino GND - Motor Driver GND
 *
 *******************************************************************************/

 #include "CytronMotorDriver.h"


// Configure the motor driver.
CytronMD motor(PWM_DIR, 5, 4);  // PWM = Pin 5, DIR = Pin 4.


// The setup routine runs once when you press reset.
void setup() {
}

// The loop routine runs over and over again forever.
void loop() {
  motor.setSpeed(125);  // Run forward at 25% speed.
  delay(1000);
  
  motor.setSpeed(0);    // Stop.
  delay(1000);

  motor.setSpeed(-125);  // Run backward at 25% speed.
  delay(1000);

  motor.setSpeed(0);    // Stop.
  delay(1000);
}
