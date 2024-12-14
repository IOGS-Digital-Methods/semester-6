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

#define   FXOS_ADD      0x1E
#define   FXOS_WHOAMI   0x0D
#define   FXOS_WHOAMI_VAL     0xC7
#define   FXOS_STATUS   0x00
#define   FXOS_XYZ_DATA_CFG   0x0E
#define   FXOS_CTRL_REG1      0x2A
#define   FXOS_M_CTRL_REG1    0x5B
#define   FXOS_M_CTRL_REG2    0x5C

byte    i2c_buff[16];

void read_i2c_buffer(byte *buff, int nb_bytes){
  for(int k = 0; k < nb_bytes; k++){
    buff[k] = (byte) Wire.read();
  }  
}

void test_FXOS(){
  Wire.beginTransmission(FXOS_ADD); 
  byte error = Wire.endTransmission();
  if (error != 0){
    Serial.println("No I2C Device Detected !");
  }
  delay(20);
  /* WHO AM I Register */
  Wire.beginTransmission(FXOS_ADD); 
  Wire.write(FXOS_WHOAMI);
  error = Wire.endTransmission(false);
  delay(20);
  int n = Wire.requestFrom(FXOS_ADD, byte(1));
  if( n == 1){
    read_i2c_buffer(i2c_buff, 1);
  }
  if(i2c_buff[0] == FXOS_WHOAMI_VAL){
    Serial.println("FXOS 8700 Detected !");
  }
}

int config_FXOS(){
  int error = 0;
  // write 0000 0000 = 0x00 to accelerometer control register 1 to place FXOS8700CQ into standby
  // [7-1] = 0000 000
  // [0]: active=0
  Wire.beginTransmission(FXOS_ADD); 
  Wire.write(FXOS_CTRL_REG1);
  Wire.write(0x00);
  error += Wire.endTransmission();
  delay(10);

  // write 0001 1111 = 0x1F to magnetometer control register 1
  // [7]: m_acal=0: auto calibration disabled
  // [6]: m_rst=0: no one-shot magnetic reset
  // [5]: m_ost=0: no one-shot magnetic measurement
  // [4-2]: m_os=111=7: 8x oversampling (for 200Hz) to reduce magnetometer noise
  // [1-0]: m_hms=11=3: select hybrid mode with accel and magnetometer active
  Wire.beginTransmission(FXOS_ADD); 
  Wire.write(FXOS_M_CTRL_REG1);
  Wire.write(0x1F);
  error += Wire.endTransmission();
  delay(10);

  // write 0010 0000 = 0x20 to magnetometer control register 2
  // [5]: hyb_autoinc_mode=1 to map the magnetometer registers to follow the
  // accelerometer registers
  // [4]: m_maxmin_dis=0 to retain default min/max latching even though not used
  // [3]: m_maxmin_dis_ths=0
  // [2]: m_maxmin_rst=0
  // [1-0]: m_rst_cnt=00 to enable magnetic reset each cycle
  Wire.beginTransmission(FXOS_ADD); 
  Wire.write(FXOS_M_CTRL_REG2);
  Wire.write(0x20);
  error += Wire.endTransmission();

  // write 0000 0001= 0x01 to XYZ_DATA_CFG register
  // [4]: hpf_out=0
  // [1-0]: fs=01 for accelerometer range of +/-4g range with 0.488mg/LSB
  Wire.beginTransmission(FXOS_ADD); 
  Wire.write(FXOS_XYZ_DATA_CFG);
  Wire.write(0x01);
  error += Wire.endTransmission();

  // write 0000 1101 = 0x0D to accelerometer control register 1
  // [7-6]: aslp_rate=00
  // [5-3]: dr=001 for 200Hz data rate (when in hybrid mode)
  // [2]: lnoise=1 for low noise mode
  // [1]: f_read=0 for normal 16 bit reads
  // [0]: active=1 to take the part out of standby and enable sampling
  Wire.beginTransmission(FXOS_ADD); 
  Wire.write(FXOS_CTRL_REG1);
  Wire.write(0x0D);
  error += Wire.endTransmission();
  delay(10);

  return error;
}

int read_data_FXOS(){
  int error = 0;
  Wire.beginTransmission(FXOS_ADD); 
  Wire.write(FXOS_STATUS);
  error += Wire.endTransmission(false);
  delay(20);
  int n = Wire.requestFrom(FXOS_ADD, byte(13));
  if( n == 13){
    read_i2c_buffer(i2c_buff, 13);
  }
  
  /*
  Serial.print("Status = ");
  Serial.println(i2c_buff[0]);
  */
  /*
  int16_t accel_x = (i2c_buff[1] << 8) + i2c_buff[2];
  Serial.print(accel_x); 
  Serial.print(",");
  int16_t accel_y = (i2c_buff[3] << 8) + i2c_buff[4];
  Serial.print(accel_y); 
  Serial.print(",");
  int16_t accel_z = (i2c_buff[5] << 8) + i2c_buff[6];
  Serial.print(accel_z); 
  Serial.println();
  */
  int16_t mag_x = (i2c_buff[7] << 8) + i2c_buff[8];
  Serial.print(mag_x); 
  Serial.print(",");
  int16_t mag_y = (i2c_buff[9] << 8) + i2c_buff[10];
  Serial.print(mag_y); 
  Serial.print(",");
  int16_t mag_z = (i2c_buff[11] << 8) + i2c_buff[12];
  Serial.print(mag_z); 
  Serial.println();

  return error;
}


void setup() {
  Wire.setSDA( PB9 );    
  Wire.setSCL( PB8 );  
  Wire.begin();
  Serial.begin(9600);
  while (!Serial)
     delay(10);

  Serial.println("Accelerometer Test");
  delay(100);
  test_FXOS();
  delay(100);
  int config_ok = config_FXOS();
  Serial.println(config_ok);
}

void loop() {
  int error_data = read_data_FXOS();
  delay(50);
}

