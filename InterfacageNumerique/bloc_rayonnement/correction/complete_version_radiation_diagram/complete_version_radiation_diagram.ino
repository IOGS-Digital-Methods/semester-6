/*
 *  Serial Communication / Radiation Diagram Acquiring
 **********************************************************************
 *  Engineer training / Digital Interfaces
 **********************************************************************
 *    LEnsE / Institut d'Optique / https://lense.institutoptique.fr/ 
 *    Author : Julien VILLEMEJANE / 06/oct/2024
 */
#include <SPI.h>
#include <Servo.h>

// LED control - MCP4102
#define   MCP_WIPER     0x00
#define   MCP_CONFIG    0x04
#define   MCP_STATUS    0x05
#define   MCP_WRITE_WR  0b00
#define   MCP_WRITE_RD  0b11
const int spi_sck_ = PA5;
const int spi_miso_ = PA6;
const int spi_mosi_ = PA7;
//SPIClass  power_led_spi(spi_mosi_, spi_miso_, spi_sck_);
const int cs_led_ = PB5;

// Inputs and outputs
const int   led1 = PC7;
const int   led2 = PB13;
const int   servo_mot = PB7;
const int   therm_res_in = PC1;
const int   photo_det_in = PC3;
const int   dig_pot_in = PB0;

// Servo motor
Servo my_servo;

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
int temperature;

// Parameters
int angle_start_deg = -100, angle_end_deg = 100;
int angle_step_deg = -1;
int old_angle = 0;
int nb_of_steps = 0;

byte tick = 0;


// Angle to servocommand
void set_angle_servo(int angle){
  int val = map(angle, -90, 90, 0, 180);     // scale it to use it with the servo (value between 0 and 180)
  delay(1);
  my_servo.write(val);
  delay(1);
}

// Angle test
bool is_angle_ok(int angle_start, int angle_end, int angle_step){
  delay(1);
  if((angle_start >= 90) | (angle_start < -90))  return false;
  if((angle_end > 90) | (angle_end <= -90))  return false;
  if((angle_step > 90) | (angle_step < 0))  return false;
  if(angle_start > angle_end)  return false;
  return true;
}

// Send command to MCP4201
byte mcp_send_command_led(byte address, char command, int data){
  //Serial.print("Test SEND");
  delay(10);
  // Adjust SPI settings to fit MCP4131
  //power_led_spi.beginTransaction(SPISettings(250000, MSBFIRST, SPI_MODE0));
  // take the SS pin low to select the chip:
  digitalWrite(cs_led_, LOW);
  byte transferByte = (address << 4) | ((command << 2) | 0);
  SPI.transfer(transferByte);
  byte result = SPI.transfer(data);
  // take the SS pin high to de-select the chip:
  digitalWrite(cs_led_, HIGH);
  // Stop using the SPI bus to allow other chips to use SPI
  //power_led_spi.endTransaction();
  return result;
}

// Set a value to the power LED (via MCP4201)
void set_led(int value){
  mcp_send_command_led(MCP_WIPER, MCP_WRITE_WR, value);
}

// Setup function
void setup() {
  pinMode(led1, OUTPUT);
  pinMode(led2, OUTPUT);
  digitalWrite(led1, LOW);
  digitalWrite(led2, HIGH);
  pinMode(cs_led_, OUTPUT);
  digitalWrite(cs_led_, HIGH);
  SPI.setMISO(spi_miso_);
  SPI.setMOSI(spi_mosi_);
  SPI.setSCLK(spi_sck_);
  SPI.begin();
  delay(10);
  pinMode(photo_det_in, INPUT_PULLUP);
  pinMode(therm_res_in, INPUT_PULLUP);
  pinMode(dig_pot_in, INPUT_PULLUP);
  //analogReadResolution(12);
  // initialize serial:
  Serial.begin(9600);
  delay(1);
  my_servo.attach(servo_mot);
  delay(10);
  my_servo.write(90);
  delay(10);
  set_led(0);
  delay(10);
}

// Main LOOP
void loop() {
  
  // print the string when a newline arrives:
  if ((string_complete) & (!acquiring)) {
    // Action to do
    if(input_string[1] == 'T'){   // transmission test
        sscanf(input_string,"!T?");
        Serial.print("!T;");
    }
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
    
    if(input_string[1] == 'B'){   // end angle in degrees
      old_angle = angle_end_deg;
      sscanf(input_string, "!B:%d?", &angle_end_deg);
      delay(1); // VERY IMPORTANT AFTER sscanf (don't know why...)
      is_ok = is_angle_ok(angle_end_deg - 1, angle_end_deg, 1);
      if(is_ok == true){ 
        Serial.print("!B:");
        Serial.print(String(angle_end_deg));
        Serial.print(";");
      }
      else{
        Serial.print("!B:-100;");
        angle_end_deg = old_angle;
      }
    }
    if(input_string[1] == 'P'){   // step angle in degrees
      old_angle = angle_step_deg;
      sscanf(input_string, "!P:%d?", &angle_step_deg);
      delay(1); // VERY IMPORTANT AFTER sscanf (don't know why...)
      is_ok = is_angle_ok(-10, 10, angle_step_deg);
      if(is_ok == true){ 
        Serial.print("!P:");
        Serial.print(String(angle_step_deg));
        Serial.print(";");
      }
      else{
        Serial.print("!P:-100;");
        angle_step_deg = old_angle;
      }
    }
    if(input_string[1] == 'S'){   // Start acquisition
      is_ok = is_angle_ok(angle_start_deg, angle_end_deg, angle_step_deg);
      delay(1);
      if(is_ok == true){ 
        nb_of_steps = (angle_end_deg - angle_start_deg) / angle_step_deg;
        Serial.print("!S:");
        Serial.print(String(nb_of_steps));
        Serial.print(";");
        acquiring = true;
        delay(1);
      }
      else{
        Serial.print("!S:0;");
        delay(1);
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

    if(input_string[1] == 'E'){   // test if acquiring
      if(acquiring == true){
        Serial.print("!E:N;");
        delay(10);
      }
      else{
        Serial.print("!E:Y;");
        delay(10);
      }
    }
      /*
      case 'K':   // Get temperature
        temperature = analogRead(therm_res_in);
        sprintf(output_string, "K_%d!",temperature);
        Serial.print(output_string);
        break;
      */
    // clear the string:
    input_cnt = 0;
    sprintf(output_string, "");
    string_complete = false;
  }

  if(acquiring){
    int k_cpt = 0;
    set_angle_servo(angle_start_deg);
    delay(1000);
    digitalWrite(led1, LOW);
    for(int angle = angle_start_deg; angle <= angle_end_deg; angle+=angle_step_deg){
      set_angle_servo(angle);
      delay(200);
      data_light[k_cpt] = analogRead(photo_det_in);
      delay(100);
      k_cpt++;
    }
    digitalWrite(led1, HIGH);
    acquiring = false;
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
    // add it to the inputString:
    input_string[input_cnt] = in_char;
    input_cnt += 1;
    // end of command !
    if (in_char == '?') {
      string_complete = true;
    }
    digitalWrite(led2, !digitalRead(led2));
  }
}
