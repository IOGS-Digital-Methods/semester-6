/*  
 *  Structure of a main file for embedded project @ LEnsE
 *
 *  This code shows an example of use of ADC.
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

const int analog_in = PC3;

// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
}

// the loop routine runs over and over again forever:
void loop() {
  // read the input on analog pin 0:
  int sensorValue = analogRead(analog_in);
  // print out the value you read:
  Serial.println(sensorValue);
  delay(100);  
}
