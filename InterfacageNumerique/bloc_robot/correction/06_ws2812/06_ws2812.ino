/*
 *  Robotics / Arduino & Nucleo Board
 **********************************************************************
 *  Engineer training / Digital Interfaces
 **********************************************************************
 *    LEnsE / Institut d'Optique / https://lense.institutoptique.fr/ 
 *    Author : Julien VILLEMEJANE / 18/oct/2024
 */

#include <Adafruit_NeoPixel.h>
#define   NUMPIXELS 2 

#define   LED1      PC7
#define   LED2      PB13
#define   USER_B    PC13
#define   SW1       PA11
#define   SW2       PA12

#define   HE_LI_1	PC0
#define   HE_LI_2	PA10
#define   HE_LI_3	PC5
#define   HE_LI_4	PA13

int val_sw1, val_sw2, val_ub;
Adafruit_NeoPixel headlight_1(NUMPIXELS, HE_LI_1, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel headlight_2(NUMPIXELS, HE_LI_2, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel headlight_3(NUMPIXELS, HE_LI_3, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel headlight_4(NUMPIXELS, HE_LI_4, NEO_GRB + NEO_KHZ800);

void setup() {
  headlight_1.begin();
  headlight_2.begin();
  headlight_3.begin();
  headlight_4.begin();

  headlight_1.setPixelColor(1, headlight_1.Color(150, 0, 0));
  headlight_1.setPixelColor(0, headlight_1.Color(0, 150, 0));
  headlight_1.show();   

  headlight_2.setPixelColor(1, headlight_2.Color(150, 0, 0));
  headlight_2.setPixelColor(0, headlight_2.Color(0, 150, 0));
  headlight_2.show();   

  headlight_3.setPixelColor(1, headlight_3.Color(150, 0, 0));
  headlight_3.setPixelColor(0, headlight_3.Color(0, 150, 0));
  headlight_3.show();   

  headlight_4.setPixelColor(1, headlight_4.Color(150, 0, 0));
  headlight_4.setPixelColor(0, headlight_4.Color(0, 150, 0));
  headlight_4.show();   
}

void loop() {
  // put your main code here, to run repeatedly:
  delay(100);
}

