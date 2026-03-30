/*  
 *  Structure of a main file for embedded project @ LEnsE
 *
 *  This code shows an example of use of interruption on input.
 *****************************************************************
 *  Pinout :
 *      D13 - Output - LED LD2 on Nucleo L476RG board
 *      PC13 - Input - User Button - active high input
 *****************************************************************
 *  Tested with Nucleo L476RG board / Arduino + STM32
 *****************************************************************
 *  Author : J. VILLEMEJANE / LEnsE - Creation 2024/12/15
 *  LEnsE / https://lense.institutoptique.fr/
 */

const int led1 = PA5;       // D13 - LD2 on Nucleo board
const int userBut = PC13;   // PC13 - User Button (blue) on Nucleo board

void swInt(){
  bool ledState = digitalRead(led1);  // Actual state of the LED
  digitalWrite(led1, !ledState);      // New state of the LED
}


void setup() {
  pinMode(led1, OUTPUT);
  digitalWrite(led1, LOW);
  pinMode(userBut, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(userBut), swInt, FALLING);
}

void loop() {
  delay(10);
}
