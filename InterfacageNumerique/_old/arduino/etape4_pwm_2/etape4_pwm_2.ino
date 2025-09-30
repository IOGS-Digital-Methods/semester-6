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

const int led1 = PC7;
const int bp1 = PA11;
const int bp2 = PA12;

int brightness = 0;  // how bright the LED is
int fadeAmount = 5;  // how many points to fade the LED by

void sw1Int(){
  brightness = brightness + fadeAmount;
  if(brightness > 255){ brightness = 255; }
  Serial.println(brightness);
  analogWrite(led1, brightness);
}

void sw2Int(){
  brightness = brightness - fadeAmount;
  if(brightness < 0){ brightness = 0; }
  Serial.println(brightness);
  analogWrite(led1, brightness);
}

void setup() {
  Serial.begin(9600);
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