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

#define	  MOT_EN	  PA9
#define   MOT_R_F   PA0
#define   MOT_R_R   PA1
#define   MOT_L_F   PA8
#define   MOT_L_R   PB4

void stop_motors(){
  digitalWrite(MOT_EN, LOW);
  digitalWrite(MOT_R_F, LOW);
  digitalWrite(MOT_R_R, LOW);
  digitalWrite(MOT_L_F, LOW);
  digitalWrite(MOT_L_R, LOW);
}

void go_forward(int speed){
  // speed between 0 and 255
  analogWrite(MOT_R_F, speed);
  analogWrite(MOT_L_F, speed);
  analogWrite(MOT_R_R, 0);
  analogWrite(MOT_L_R, 0);
  digitalWrite(MOT_EN, HIGH);
}

void go_reverse(int speed){
  // speed between 0 and 255
  analogWrite(MOT_R_R, speed);
  analogWrite(MOT_L_R, speed);
  analogWrite(MOT_R_F, 0);
  analogWrite(MOT_L_F, 0);
  digitalWrite(MOT_EN, HIGH);
}

void setup() {
  pinMode(MOT_EN, OUTPUT);
  pinMode(MOT_R_F, OUTPUT);
  pinMode(MOT_R_R, OUTPUT);
  pinMode(MOT_L_F, OUTPUT);
  pinMode(MOT_L_R, OUTPUT);
}

void loop() {
  go_forward(100);
  delay(1000);
  stop_motors();
  delay(1000);
  go_reverse(100);
  delay(1000);
  stop_motors();
  delay(1000);

  delay(100);
}
