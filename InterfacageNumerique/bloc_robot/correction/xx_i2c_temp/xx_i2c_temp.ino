/*
 *  Robotics / Arduino & Nucleo Board
 **********************************************************************
 *  Engineer training / Digital Interfaces
 **********************************************************************
 *        Accelerometer DOF6 - IMU Click from MikroE
 *          chip : FXOS 8700 CQ
 *    LEnsE / Institut d'Optique / https://lense.institutoptique.fr/ 
 *    Author : Julien VILLEMEJANE / 18/oct/2024
 */

#include <Wire.h>

#define   LED1      PC7
#define   LED2      PB13

#define   TC74A2_ADD    0x4A
#define   TC74A2_TEMP   0x00
#define   TC74A2_CFG    0x01

byte    i2c_buff[16];

void read_i2c_buffer(byte *buff, int nb_bytes){
  for(int k = 0; k < nb_bytes; k++){
    buff[k] = (byte) Wire.read();
  }  
}

void config_TC74A2(){
  Wire.beginTransmission(TC74A2_ADD); 
  byte error = Wire.endTransmission();
  if (error != 0){
    Serial.println("No I2C Device Detected !");
  }
  delay(20);
  // write 0000 0000 = 0x00 to configuration register
  // [7]: STANDBY_Switch=0 to set the normal mode
  Wire.beginTransmission(TC74A2_ADD); 
  Wire.write(TC74A2_CFG);
  Wire.write(0x00);
  error = Wire.endTransmission();
  delay(20);
}

int get_temp_TC74A2(){
  int error = 0;
  // get configuration register to check if a data is ready
  // [6]: Data Ready : 1 data is ready
  Wire.beginTransmission(TC74A2_ADD); 
  Wire.write(TC74A2_CFG);
  error += Wire.endTransmission(false);
  delay(20);
  
  int n = Wire.requestFrom(TC74A2_ADD, byte(1));
  if( n == 1){
    read_i2c_buffer(i2c_buff, 1);
  }
  if(i2c_buff[0] & 0b01000000 == 0){
    return -1;
  }
  delay(20);
  // get temp register
  Wire.beginTransmission(TC74A2_ADD); 
  Wire.write(TC74A2_TEMP);
  error += Wire.endTransmission(false);
  delay(20);
  n = Wire.requestFrom(TC74A2_ADD, byte(1));
  if( n == 1){
    read_i2c_buffer(i2c_buff, 1);
  }
  return i2c_buff[0];
}

void setup() {
  Wire.setSDA( PB9 );    
  Wire.setSCL( PB8 );  
  Wire.begin();
  Serial.begin(9600);
  while (!Serial)
     delay(10);

  Serial.println("Digital Temperature Sensor Test");
  config_TC74A2();
  delay(100);
}

void loop() {
  int val_temp = get_temp_TC74A2();
  Serial.println(val_temp);
  delay(500);
}

