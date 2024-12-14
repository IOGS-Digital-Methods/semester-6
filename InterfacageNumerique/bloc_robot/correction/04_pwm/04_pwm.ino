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

#define   POT_IN	PC3
#define   TEMP_IN	PC2

#define	  MOT_EN	PA9

int val_pot, val_pot_m;

void setup() {
  Serial.begin(9600);
  pinMode(LED1, OUTPUT);
  pinMode(LED2, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  val_pot = analogRead(POT_IN);
  val_pot_m = map(val_pot, 0, 1023, 0, 255);
  Serial.println(val_pot_m);
  analogWrite(LED2, val_pot_m);

  delay(100);
}
