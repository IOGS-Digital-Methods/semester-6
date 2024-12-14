
/*
 *  Robotics / Arduino & Nucleo Board
 **********************************************************************
 *  Engineer training / Digital Interfaces
 **********************************************************************
 *    LEnsE / Institut d'Optique / https://lense.institutoptique.fr/ 
 *    Author : Julien VILLEMEJANE / 18/oct/2024
 */

#define   LED1      PC7
#define   SW1       PC6

int val_sw1, val_sw2, val_ub;

void setup() {
  // put your setup code here, to run once:
  pinMode(LED1, OUTPUT);

  pinMode(SW1, INPUT_PULLUP);

  attachInterrupt(digitalPinToInterrupt(SW1), swInt, RISING);

  digitalWrite(LED1, LOW);
}

void loop() {
  // put your main code here, to run repeatedly:
  delay(100);
}

void swInt(void){
  bool ledState = digitalRead(LED1);
  digitalWrite(LED1, !ledState);
} 
