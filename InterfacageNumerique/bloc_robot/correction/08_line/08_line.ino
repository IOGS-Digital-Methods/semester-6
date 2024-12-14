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

#define   LINE_R    PA5
#define   LINE_C    PB6
#define   LINE_L    PA7

int val_line_r, val_line_c, val_line_l;

void setup() {
  // put your setup code here, to run once:
  pinMode(LED1, OUTPUT);
  pinMode(LED2, OUTPUT);

  pinMode(LINE_R, INPUT_PULLUP);
  pinMode(LINE_C, INPUT_PULLUP);
  pinMode(LINE_L, INPUT_PULLUP);

  attachInterrupt(digitalPinToInterrupt(LINE_R), swInt, CHANGE);
  attachInterrupt(digitalPinToInterrupt(LINE_C), swInt, CHANGE);
  attachInterrupt(digitalPinToInterrupt(LINE_L), swInt, CHANGE);

  digitalWrite(LED1, LOW);
  digitalWrite(LED2, HIGH);
}

void loop() {
  // put your main code here, to run repeatedly:
  delay(100);
}

void swInt(void){
  val_line_r = digitalRead(LINE_R);
  val_line_c = digitalRead(LINE_C);
  val_line_l = digitalRead(LINE_L);
  digitalWrite(LED1, val_line_c);
  digitalWrite(LED2, val_line_r | val_line_l);
}
