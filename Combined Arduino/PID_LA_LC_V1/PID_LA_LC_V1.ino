/****
 * COMBINED WHICH DOES LA AND LOAD CELL TOGETHER
 */

// Configuring Linear Actuator
 #include "CytronMotorDriver.h"
 
CytronMD motor(PWM_DIR, 5, 4);  // PWM = Pin 5, DIR = Pin 4.

// Configuring Load Cell
#include "HX711.h"

#define DOUT  3
#define CLK  2

HX711 scale;

float calibration_factor = -7050; //-7050 worked for my 440lb max scale setup *** NEED TO FIND CALIBRATION FACTOR IN TSRL. CAN CHANGE TO FIXED VAIRABLE WHEN CONFIRMED *** 
float f = 20; //intended force
float l; //load cell value



//////////////////////////  PID CONTROL VALUE //////////////////////////

#include <PID_v1.h>

// Define Variables
double Setpoint, Input, Output;
double aggKp = 4, aggKi = 0.2, aggKd = 1;
double consKp = 1, consKi = 0.05, consKd = 0.25;
double max_speed = 150; // Maximum speed the motor can be set to
double deadband = 5; // Size of the deadband around the setpoint

// Specify the links and initial tuning parameters
PID myPID(&Input, &Output, &Setpoint, consKp, consKi, consKd, DIRECT);




void setup() {
// Linear Actuator Set Up


 // Load Cell Setup
  Serial.begin(9600);
  Serial.println("HX711 calibration sketch");
  Serial.println("Remove all weight from scale");
  Serial.println("After readings begin, place known weight on scale");
  Serial.println("Press + or a to increase calibration factor");
  Serial.println("Press - or z to decrease calibration factor");

  scale.begin(DOUT, CLK);
  scale.set_scale();
  scale.tare(); //Reset the scale to 0

  long zero_factor = scale.read_average(); //Get a baseline reading
  Serial.print("Zero factor: "); //This can be used to remove the need to tare the scale. Useful in permanent scale projects.
  Serial.println(zero_factor);
}

// The loop routine runs over and over again forever.
void loop() {
  //read_load_cell();
  l = load_cell_value();
  match_force(f, max_speed, deadband, l);
  Serial.print(f);
  Serial.print("   ");
  Serial.print(l);
  Serial.print("    ");
  Serial.println(Output); //dont know if this works
}


void read_load_cell(){
    scale.set_scale(calibration_factor); //Adjust to this calibration factor

  Serial.print("Reading: ");
  Serial.print(scale.get_units(), 1);
  Serial.print(" lbs"); //Change this to kg and re-adjust the calibration factor if you follow SI units like a sane person
  Serial.print(" calibration_factor: ");
  Serial.print(calibration_factor);
  Serial.println();

  if(Serial.available())
  {
    char temp = Serial.read();
    if(temp == '+' || temp == 'a')
      calibration_factor += 10;
    else if(temp == '-' || temp == 'z')
      calibration_factor -= 10;
  }
}

int load_cell_value(){
    scale.set_scale(calibration_factor); //Adjust to this calibration factor
  return scale.get_units();
}




void match_force(float f, double max_speed, double deadband, float l) {
  double error = f - l;

  Setpoint = f;
  Input = l;

  double gap = abs(f - l);
  if (gap < deadband) {
    myPID.SetTunings(consKp, consKi, consKd);
  } else {
    myPID.SetTunings(aggKp, aggKi, aggKd);
    // Change sign of the output when outside the deadband
    Output = -Output;  
  }

  myPID.Compute();
  Output = max(-max_speed, min(max_speed, Output));
  motor.setSpeed(Output);
}
