// Setting up the linear actuator and load cell
#include <CytronMotorDriver.h>
#include <HX711.h>

// Define pins for load cell and linear actuator
const int LOAD_CELL_DOUT_PIN = 3;
const int LOAD_CELL_SCK_PIN = 2;
const int MOTOR_PWM_PIN = 5;
const int MOTOR_DIR_PIN = 4;

// Define PID constants
const float Kp = 0.5;
const float Ki = 0;
const float Kd = 0;

// Define setpoint and initial variables
float input, output, error, lastError, integral;
HX711 loadCell;
CytronMD motor(PWM_DIR, MOTOR_PWM_PIN, MOTOR_DIR_PIN);

// Setting up stepper motor
#include <Stepper.h>

// change this to the number of steps on your motor
#define STEPS 200

// create an instance of the stepper class, specifying
// the number of steps of the motor and the pins it's
// attached to
Stepper stepper(STEPS, 7, 8, 9, 10);

// Sleep pin
const int sleep_pin = 11;

// INTERNAL VARIABLES
bool initial_success = false;
String recieved = "";
String instruction = "";
int activity = 0;

// ADD LIST OF ACTIVITIES

// SETUP
void setup() {
// Initialize serial communication
  Serial.begin(9600);

  // Initialize load cell
  loadCell.begin(LOAD_CELL_DOUT_PIN, LOAD_CELL_SCK_PIN);
  loadCell.set_scale(-9000);  // This calibration factor is obtained by using the SparkFun_HX711_Calibration sketch
  loadCell.tare();       // Reset the scale to 0

  // Set speed of ROM motor
  stepper.setSpeed(100);

  // Define sleep pin
  pinMode(sleep_pin, OUTPUT);

  // Send message to computer, wait for a response
  while (not initial_success) {
    Serial.println("Arduino running, computer respond?");
    delay(1000);

    recieved = read_serial();
    if (recieved.equals("Computer respond")) {
      initial_success = true;
    }
    else {
      delay(5000);
    }
  }
  Serial.println(activities);
  delay(1000);
}

// ***START VOID LOOP***
void loop() {
// INSTRUCTIONS FROM COMPUTER
Serial.println("Getting instructions");
instruction = read_serial();


if (instruction.equals("PAUSE")){
  activity = 0;
}
  else if (instruction.equals("Test Finish")){
  activity = 1;
}
  else if (instruction.equals("No response received")){
  Serial.println("No response recieved");
  delay(1000);
}
// ADD SWITCH VALUES HERE
 
switch (activity) {
case 0: // If paused
  break;
case 1: // If finished
  while (true){
    delay(1000);
}
// ADD SWITCH CASES HERE

}
}
// ***END VOID LOOP***

// FUNCTIONS
// GET MESSAGE FROM COMPUTER
String read_serial() {
  String incoming = "";
  while (Serial.available() > 0) {
    char c = Serial.read();
    if (c == '\n') { // Check for newline character
      break; // Exit the loop when newline character is found
    }
    incoming += c; // Append character to the incoming string
  }

  // Trim any whitespace characters at the beginning and end of the string
  incoming.trim();

  if (incoming.length() == 0) {
    incoming = "No response received"; // Provide a default message if no response is received
  }
  return incoming;
}

/// TESTING FOR PAUSE
void test_pause() {
  String instruction = read_serial();
  if (instruction.equals("PAUSE")){
    bool wait_til_play = true;
    while (wait_til_play){
      String play_command = read_serial();
      if (play_command.equals("PLAY")){
        wait_til_play = false;
      }
      else{
        delay(500);
      }
      }
      }
  }
/// FOR SETTING LOAD ///
void set_load (float force_setpoint, float total_duration){
  // Read load cell value

  // Initialize PID variables
  float output = 0;
  float error = 0;
  float lastError = 0;
  float integral = 0;

  float start_time = millis();
  float time_left = total_duration;
  
  while(time_left > 0){
    input = loadCell.get_units();
  
    // Calculate error
    error = force_setpoint - input;
  
    // Calculate PID terms
    float proportional = Kp * error;
    integral += Ki * error;
    float derivative = Kd * (error - lastError);
  
    // Calculate PID output
    output = proportional + integral + derivative;
  
  //  // Limit output to prevent motor overshoot
  //    output = constrain(output, -100, 100);
  
      if (output > 3){
        output = constrain(output, 30, 100);
      }
      else if (output < -3){
        output = constrain(output, -100, -30);
      }
      else{
        output = 0;
      }
  
      // Drive motor based on PID output
      motor.setSpeed(output);
  
      // Update last error
      lastError = error;
      Serial.print("PID:");
      Serial.print(input);
      Serial.print(",");
      Serial.println(force_setpoint);

    float time_elapsed = millis() - start_time;
    time_left = total_duration - time_elapsed;

    // Add a small delay to prevent excessive PID loop execution
    delay(10);
  }
}

/// FOR VARYING MOTION
void turn_steps(int pos){
  digitalWrite(sleep_pin, HIGH);
  stepper.step(pos);
  test_pause();
  Serial.print("Stepper:");
  Serial.println(pos);
  delay(10);
  digitalWrite(sleep_pin, LOW);
}
  

// ADD ACTIVITY FUNCTIONS HERE
