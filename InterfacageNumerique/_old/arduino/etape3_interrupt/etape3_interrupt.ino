/*  
 *  Structure of a main file for embedded project @ LEnsE
 *
 *  This code shows an example of use of interruption on inputs.
 *  Tested on robot platform of LEnsE.
 *****************************************************************
 *  Pinout :
 *      PC7 - Output - LED1 of the robot platform
 *      PA11 - Input - SW1 - active high input
 *      PA12 - Input - SW2 - active high input
 *****************************************************************
 *  Tested with Nucleo L476RG board / Arduino + STM32
 *****************************************************************
 *  Author : J. VILLEMEJANE / LEnsE - Creation 2024/12/15
 *  LEnsE / https://lense.institutoptique.fr/
 */

const int led1 = PC7;
const int bp1 = PA11;
const int bp2 = PA12;

void sw1Int(){
  digitalWrite(led1, HIGH);      // New state of the LED
}

void sw2Int(){
  digitalWrite(led1, LOW);      // New state of the LED
}

void setup() {
  pinMode(led1, OUTPUT);
  digitalWrite(led1, LOW);
  pinMode(bp1, INPUT_PULLUP);
  pinMode(bp2, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(bp1), sw1Int, RISING);
  attachInterrupt(digitalPinToInterrupt(bp2), sw2Int, RISING);
}

void loop() {
  delay(10);
}
