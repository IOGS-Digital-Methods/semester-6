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

int val_pot;
int val_temp;

void setup() {
  Serial.begin(9600);
}

void loop() {
  val_pot = analogRead(POT_IN);
  Serial.print("Pot = ");
  Serial.println(val_pot);
  val_temp = analogRead(TEMP_IN);
  Serial.print("Temp = ");
  Serial.println(val_temp);
  delay(500);
}

