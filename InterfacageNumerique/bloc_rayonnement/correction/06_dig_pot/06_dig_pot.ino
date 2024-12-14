/*
 *  Robotics / Arduino & Nucleo Board
 **********************************************************************
 *  Engineer training / Digital Interfaces
 **********************************************************************
 *    LEnsE / Institut d'Optique / https://lense.institutoptique.fr/ 
 *    Author : Julien VILLEMEJANE / 18/oct/2024
 */
#include <SPI.h>

#define   LED1      PC7
#define   LED2      PB13
#define   USER_B    PC13
#define   SW1       PC6
#define   SW2       PC8

#define   SPI_SCK   PA5
#define   SPI_MISO  PA6
#define   SPI_MOSI  PA7
SPIClass  my_spi( SPI_MOSI, SPI_MISO, SPI_SCK );

#define   MCP_CS2   PB9
#define   MCP_WIPER     0x00
#define   MCP_CONFIG    0x04
#define   MCP_STATUS    0x05
#define   MCP_WRITE_WR  0b00
#define   MCP_WRITE_RD  0b11

#define   POT_IN	  PC4
#define   POT_DIG   PB0

int val_pot;

byte mcp_send_command(byte address, char command, unsigned int data){
      // Adjust SPI settings to fit MCP4131
    my_spi.beginTransaction(SPISettings(250000, MSBFIRST, SPI_MODE0));

    // take the SS pin low to select the chip:
    digitalWrite(MCP_CS2, LOW);

    byte transferByte = (address << 4) | ((command << 2) | 0);

    my_spi.transfer(transferByte);
    byte result = my_spi.transfer(data);

    // take the SS pin high to de-select the chip:
    digitalWrite(MCP_CS2, HIGH);

    // Stop using the SPI bus to allow other chips to use SPI
    my_spi.endTransaction();

    return result;
}

void init_pot(){
  // 0100 00nn nnnn nnnn
  // [0] R0B = 1
  // [1] R0W = 1
  // [2] R0A = 1
  // [3] R0HW = 1
  int cfg_value = 0b0100001111;
  mcp_send_command(MCP_CONFIG, MCP_WRITE_WR, cfg_value);
}

int read_status(){
  int status_value = mcp_send_command(MCP_STATUS, MCP_WRITE_RD, 255);
  return status_value;
}

void set_pot(int value){
  mcp_send_command(MCP_WIPER, MCP_WRITE_WR, value);
}

void setup() {
  Serial.begin(9600);
  while(!Serial);
  pinMode(LED1, OUTPUT);
  pinMode(LED2, OUTPUT);
  pinMode(MCP_CS2, OUTPUT);
  digitalWrite(MCP_CS2, HIGH);

  my_spi.begin();
  delay(100);

  //init_pot();
}

void loop() {
  for(int k = 0; k < 128; k++){
    set_pot(k);
    val_pot = analogRead(POT_DIG);
    delay(1);
    //Serial.println(val_pot);
  }
  delay(10);
}
