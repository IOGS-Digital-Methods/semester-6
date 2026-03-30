/*  
 *  Base for light radiation measurement transmission. 
 *****************************************************************
 *  Pinout :
 *      D13 - Output - LED LD2 on Nucleo L476RG board
 *      PC13 - Input - User Button - active high input
 *****************************************************************
 *  Tested with Nucleo L476RG board / Arduino + STM32
 *****************************************************************
 *  Author : J. VILLEMEJANE / LEnsE - Creation 2024/12/15
 *  LEnsE / https://lense.institutoptique.fr/
 */


// Inputs and outputs
const int   led2 = PB13;


// Serial communication
char input_string[20] = "";      // a String to hold incoming data
char output_string[20] = "";     // a String to hold outcoming data
bool string_complete = false;  // whether the string is complete
int input_cnt = 0;
bool is_ok = false;

// Data acquisition
bool acquiring = false;
int data_cpt = 0;
int data_light[180];

// Parameters
int angle_start_deg = -100, angle_end_deg = 100;
int angle_step_deg = -1;
int old_angle = -1;

// Angle test
bool is_angle_ok(int angle_start, int angle_end, int angle_step){
  delay(1);
  if((angle_start >= 90) | (angle_start < -90))  return false;
  if((angle_end > 90) | (angle_end <= -90))  return false;
  if((angle_step > 90) | (angle_step < 0))  return false;
  if(angle_start > angle_end)  return false;
  return true;
}

// Setup function
void setup() {
  for(int i = 0; i < 180; i++){
    data_light[i] = 3*i;
  }
  // Setup output
  pinMode(led2, OUTPUT);
  digitalWrite(led2, HIGH);
  delay(10);
  // initialize serial:
  Serial.begin(9600);
  delay(10);
}

// Main LOOP
void loop() {
  
  // print the string when a newline arrives:
  if (string_complete) {
    // Action to do
    if(input_string[1] == 'A'){   // start angle in degrees
      old_angle = angle_start_deg;
      sscanf(input_string, "!A:%d?", &angle_start_deg);
      delay(1); // VERY IMPORTANT AFTER sscanf (don't know why...)
      is_ok = is_angle_ok(angle_start_deg, angle_start_deg + 1, 1);
      if(is_ok == true){ 
        Serial.print("!A:");
        Serial.print(String(angle_start_deg));
        Serial.print(";");
      }
      else{
        Serial.print("!A:-100;");
        angle_start_deg = old_angle;
      }
    }
    
    if(input_string[1] == 'D'){   // Data transmission
      sscanf(input_string,"!D:%d?",&data_cpt);
      delay(1);
      Serial.print("!D:");
      Serial.print(data_cpt);
      Serial.print(":");
      Serial.print(data_light[data_cpt]);
      Serial.print(";");
      //delay(10);
    }

    input_cnt = 0;
    sprintf(output_string, "");
    string_complete = false;
  }

  delay(10);
}

/*
  SerialEvent occurs whenever a new data comes in the hardware serial RX. This
  routine is run between each time loop() runs, so using delay inside loop can
  delay response. Multiple bytes of data may be available.
*/
void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    char in_char = (char)Serial.read();
    if (in_char == '!') {
      input_cnt = 0;
    }
    else{
      input_cnt += 1;
    }
    // add it to the inputString:
    input_string[input_cnt] = in_char;
    // end of command !
    if (in_char == '?') {
      string_complete = true;
    }
    digitalWrite(led2, !digitalRead(led2));
  }
}
