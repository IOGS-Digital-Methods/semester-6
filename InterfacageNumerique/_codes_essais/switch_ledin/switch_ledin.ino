#define   SW1   PA11
#define   SW2   PA11
#define   LED_TEST    LED_BUILTIN
volatile byte state = LOW;
int valSw1;

#include <SPI.h>
#include <RF24.h>

#define pinCE   PD2         
#define pinCSN  PA14     
#define tunnel  "PIPE1"  

RF24 radio(pinCE, pinCSN);
const byte adresse[6] = tunnel;

void setup() {
  // put your setup code here, to run once:

  SPI.setMOSI(PC12);
  SPI.setMISO(PC11);
  SPI.setSCLK(PC10);

  pinMode(SW1, INPUT);
  pinMode(LED_TEST, OUTPUT);
  Serial.begin(9600);
  Serial.println("Hello !");
  digitalWrite(LED_TEST, HIGH);

  attachInterrupt(digitalPinToInterrupt(SW2), blink, RISING);

  radio.begin();
  radio.openWritingPipe(adresse);

  radio.setPayloadSize(32); //packet size, in bytes
  radio.setChannel(100); //select a channel (in which there is no noise!) 0 ... 125

  radio.setPALevel (RF24_PA_MIN); //transmitter power level. To choose RF24_PA_MIN, RF24_PA_LOW, RF24_PA_HIGH, RF24_PA_MAX
  radio.setDataRate (RF24_2MBPS); //exchange rate. To choose RF24_2MBPS, RF24_1MBPS, RF24_250KBPS
  radio.powerUp(); //get started
  radio.stopListening(); //do not listen to radio broadcasts, we are a transmitter

  radio.printDetails();
}

void loop() {
  // put your main code here, to run repeatedly:
  //valSw1 = digitalRead(SW1);
  //Serial.println(valSw1);
  digitalWrite(LED_TEST, state);
  //delay(500);
}

void blink(){
  state = !state;
}
