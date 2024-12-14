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

#define   SPEED_R   PC8
#define   SPEED_L   PC9

int val_speed_r, val_speed_l;

void setup() {
  // put your setup code here, to run once:
  pinMode(LED1, OUTPUT);
  pinMode(LED2, OUTPUT);

  pinMode(SPEED_R, INPUT_PULLUP);
  pinMode(SPEED_L, INPUT_PULLUP);

  attachInterrupt(digitalPinToInterrupt(SPEED_R), swInt, CHANGE);
  attachInterrupt(digitalPinToInterrupt(SPEED_L), swInt, CHANGE);

  digitalWrite(LED1, LOW);
  digitalWrite(LED2, HIGH);
}

void loop() {
  // put your main code here, to run repeatedly:
  delay(100);
}

void swInt(void){
  val_speed_r = digitalRead(SPEED_R);
  val_speed_l = digitalRead(SPEED_L);
  digitalWrite(LED1, val_speed_r);
  digitalWrite(LED2, val_speed_l);
}
