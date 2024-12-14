/*
 * See documentation at https://nRF24.github.io/RF24
 * See License information at root directory of this library
 * Author: Brendan Doherty (2bndy5)
 */

#include <SPI.h>
#include "RF24.h"
#include "printf.h"

#define   NRF_CE    PD2
#define   NRF_CSN   PA14
#define   NRF_INT   PA15
#define   SPI_SCK   PC10
#define   SPI_MISO  PC11
#define   SPI_MOSI  PC12
// instantiate an object for the nRF24L01 transceiver
RF24 radio(NRF_CE, NRF_CSN);

const byte address_tx[6] = "00010";
const byte address_rx[6] = "00001";


char data_rx[4] = {0};

void setup() {
  Serial.begin(115200);
  while (!Serial);
  delay(100);
  Serial.println("nRF24 Test !");
  SPI.setMISO(SPI_MISO);
  SPI.setMOSI(SPI_MOSI);
  SPI.setSCLK(SPI_SCK);

  // initialize the transceiver on the SPI bus
  if (!radio.begin()) {
    Serial.println("radio hardware is not responding !!");
  }
  Serial.println("RF24/examples/GettingStarted");
  // data_rate: RF24_250KBPS, RF24_1MBPS ou RF24_2MBPS
  radio.setDataRate(RF24_1MBPS);
  // power: RF24_PA_MIN=-18dBm, RF24_PA_LOW=-12dBm, RF24_PA_MED=-6dBM
  radio.setPALevel(RF24_PA_LOW);  
  // channel : from 0 to 127
  radio.setChannel(0);
  radio.openReadingPipe(1, address_rx);

  printf_begin();
  radio.printDetails();

  radio.startListening();  // put radio in RX mode
}  // setup

void loop() {
  if(radio.available()){
    radio.read(&data_rx, sizeof(data_rx));
    Serial.print("RX : ");
    Serial.println(data_rx[0]);
  }
  delay(10);
}  // loop
