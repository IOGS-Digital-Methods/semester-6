/*
 * See documentation at https://nRF24.github.io/RF24
 * See License information at root directory of this library
 * Author: Brendan Doherty (2bndy5)
 */

#include <SPI.h>
#include "RF24.h"
#include "printf.h"

#define   NRF_CE    PA15
#define   NRF_CSN   PB7
#define   NRF_INT   PA14
#define   SPI_SCK   PA5
#define   SPI_MISO  PA6
#define   SPI_MOSI  PA7
// instantiate an object for the nRF24L01 transceiver
RF24 radio(NRF_CE, NRF_CSN);

const byte address_tx[6] = "00001";
const byte address_rx[6] = "00010";


char data_tx[4] = {0x00, 0xAA, 0x55, 0x87};

void setup() {
  Serial.begin(115200);
  while (!Serial);
  delay(1000);
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
  // set the TX address of the RX node into the TX pipe
  radio.openWritingPipe(address_tx);  // always uses pipe 0

  printf_begin();
  radio.printDetails();

  radio.stopListening();  // put radio in TX mode
}  // setup

void loop() {
  data_tx[0]++;
  radio.write(&data_tx, sizeof(data_tx));
  Serial.println(data_tx[0]);
  delay(1000);
}  // loop
