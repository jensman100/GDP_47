#include "CytronMotorDriver.h"
#include "HX711.h"
#include <PID_v1.h>

// Motor Driver Configuration
CytronMD motor(PWM_DIR, 5, 4);  // PWM = Pin 5, DIR = Pin 4.

// Load Cell Configuration
#define DOUT  3
#define CLK   2
HX711 scale;

//desired force
float f = 20;
double error;
double gap;


float max_speed = 50;
// when conservative PID kicks in
float deadband = 5;


//Define Variables we'll be connecting to
double Setpoint, Input, Output;
float forward, backward;
//Define the aggressive and conservative Tuning Parameters
double aggKp=4, aggKi=0.2, aggKd=1;
double consKp=1, consKi=0.05, consKd=0.25;
//Specify the links and initial tuning parameters
PID myPID(&Input, &Output, &Setpoint, consKp, consKi, consKd, DIRECT);


// Calibration Factor
float calibration_factor = -9000; // as determined by Joe - i think this provides Kgs 

void setup() {
  Serial.begin(9600);
  Serial.println("HX711 calibration sketch");
  Serial.println("Remove all weight from scale");
  Serial.println("After readings begin, place known weight on scale");

  // Linear Actuator Setup

  //turn the PID on
  myPID.SetMode(AUTOMATIC);

  // Load Cell Setup
  scale.begin(DOUT, CLK);
  scale.set_scale(calibration_factor);
  scale.tare(); // Reset the scale to 0
}


void loop() {
  Input = load_cell_value();
  match_force(f, max_speed, deadband, Input);
  Serial.print(f);
  Serial.print("   ");
  Serial.print(Input);
  Serial.print("    ");
  Serial.print(Output);
  Serial.print("    ");  
  Serial.println(error);

  delay(10); // Add a small delay to avoid reading the load cell too frequently
}

int load_cell_value() {
  return scale.get_units();
}



void match_force(float f, double max_speed, double deadband, float l) {
  // Calculate error from the input l
  error = f - l;

  // Set Setpoint and Input for the PID controller
  Setpoint = f;
  Input = l;

  
  // Update tuning parameters based on distance from setpoint
//  gap = abs(f - l); // distance away from setpoint
//  if (gap < deadband) {
//    // Use conservative tuning parameters when close to setpoint
//    myPID.SetTunings(consKp, consKi, consKd);
//  } else {
//    // Use aggressive tuning parameters when far from setpoint
//    myPID.SetTunings(aggKp, aggKi, aggKd);
//  }

  if (error < deadband) {
    // Use conservative tuning parameters when close to setpoint
    myPID.SetTunings(consKp, consKi, consKd);
  } else if (error < -deadband) {
    // Use conservative tuning parameters when close to setpoint
    myPID.SetTunings(consKp, consKi, consKd);
  }else {
    // Use aggressive tuning parameters when far from setpoint
    myPID.SetTunings(aggKp, aggKi, aggKd);
  } 

  // Compute PID output
  myPID.Compute();

  // Constrain Output within the range of -max_speed to max_speed
  Output = constrain(Output, 0, max_speed);
  forward = Output;
  backward = -Output;
  
  // Determine motor direction based on the sign of the error
  if (error > 0) {
    // Error is positive, drive motor forward
    motor.setSpeed(forward);
  } else if (error < 0) {
    // Error is negative, drive motor backward
    motor.setSpeed(backward);
  } else {
    // Error is within deadband, stop motor
    motor.setSpeed(0);
  }
}
