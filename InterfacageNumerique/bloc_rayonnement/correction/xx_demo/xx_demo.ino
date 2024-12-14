/*
 *  Robotics / Arduino & Nucleo Board
 **********************************************************************
 *  Engineer training / Digital Interfaces
 **********************************************************************
 *    LEnsE / Institut d'Optique / https://lense.institutoptique.fr/ 
 *    Author : Julien VILLEMEJANE / 18/oct/2024
 */
#include <Servo.h>
#include <SPI.h>

#define   LED1      PC7
#define   LED2      PB13
#define   USER_B    PC13
#define   SW1       PC6
#define   SW2       PC8

#define   SERVO     PB7
Servo   my_servo;

#define   POT_IN	  PC4


#define   SPI_SCK   PA5
#define   SPI_MISO  PA6
#define   SPI_MOSI  PA7
SPIClass  my_spi( SPI_MOSI, SPI_MISO, SPI_SCK );

#define   MCP_CS_LED  PB5
#define   MCP_CS2     PB9
#define   MCP_WIPER     0x00
#define   MCP_CONFIG    0x04
#define   MCP_STATUS    0x05
#define   MCP_WRITE_WR  0b00
#define   MCP_WRITE_RD  0b11

void set_led(int value);

int val_pot, val_pot_m;

void setup() {
  Serial.begin(9600);
  while(!Serial);
  Serial.println("Hello");
  delay(100);
  
  pinMode(SERVO , INPUT_PULLUP);  // TIM2
  LL_GPIO_SetAFPin_0_7(GPIOB, GPIO_PIN_7, GPIO_AF2_TIM4); // TO ADD IN DOC !!!
  pinMode(SERVO, OUTPUT);
  my_servo.attach(SERVO);
  pinMode(LED1, OUTPUT);
  pinMode(LED2, OUTPUT);
  pinMode(MCP_CS_LED, OUTPUT);
  pinMode(MCP_CS2, OUTPUT);
}

void loop() {

  set_led(127);
  for(int k = 0; k < 180; k++){
    my_servo.write(k);
    delay(10);
  }
  set_led(0);
  for(int k = 180; k > 0; k--){
    my_servo.write(k);
    delay(10);
  }

  delay(100);
}


// OTHER FUNCTIONS

byte mcp_send_command_led(byte address, char command, unsigned int data){
      // Adjust SPI settings to fit MCP4131
    my_spi.beginTransaction(SPISettings(250000, MSBFIRST, SPI_MODE0));

    // take the SS pin low to select the chip:
    digitalWrite(MCP_CS_LED, LOW);

    byte transferByte = (address << 4) | ((command << 2) | 0);

    my_spi.transfer(transferByte);
    byte result = my_spi.transfer(data);

    // take the SS pin high to de-select the chip:
    digitalWrite(MCP_CS_LED, HIGH);

    // Stop using the SPI bus to allow other chips to use SPI
    my_spi.endTransaction();

    return result;
}

void set_led(int value){
  mcp_send_command_led(MCP_WIPER, MCP_WRITE_WR, value);
}