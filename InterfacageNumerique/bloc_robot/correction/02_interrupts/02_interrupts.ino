/*
 *  Robotics / Arduino & Nucleo Board
 **********************************************************************
 *  Engineer training / Digital Interfaces
 **********************************************************************
 *    LEnsE / Institut d'Optique / https://lense.institutoptique.fr/ 
 *    Author : Julien VILLEMEJANE / 18/oct/2024
 */

#include <Servo.h>

#define   LED1      PC7
#define   LED2      PB13
#define   USER_B    PC13
#define   SW1       PA11
#define   SW2       PA12
#define   SERVO     PB7

int val_sw1, val_sw2, val_ub;

void setup() {
  // put your setup code here, to run once:
  pinMode(LED1, OUTPUT);
  pinMode(LED2, OUTPUT);

  pinMode(SW1, INPUT_PULLUP);
  pinMode(SW2, INPUT_PULLUP);
  pinMode(USER_B, INPUT_PULLUP);

  attachInterrupt(digitalPinToInterrupt(SW2), swInt, CHANGE);
  attachInterrupt(digitalPinToInterrupt(SW1), swInt, CHANGE);
  attachInterrupt(digitalPinToInterrupt(USER_B), swInt, CHANGE);

  digitalWrite(LED1, LOW);
  digitalWrite(LED2, HIGH);
}

void loop() {
  // put your main code here, to run repeatedly:
  delay(100);
}

void swInt(void){
  val_sw1 = digitalRead(SW1);
  val_sw2 = digitalRead(SW2);
  val_ub = digitalRead(USER_B);
  digitalWrite(LED1, val_sw1);
  digitalWrite(LED2, val_sw2 | !val_ub);
}
