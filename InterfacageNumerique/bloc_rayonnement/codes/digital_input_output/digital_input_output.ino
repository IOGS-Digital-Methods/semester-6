/*
 *  Digital inputs and outputs / Example code using interrupt 
 **********************************************************************
 *  Engineer training / Digital Interfaces
 **********************************************************************
 *    LEnsE / Institut d'Optique / https://lense.institutoptique.fr/ 
 *    Author : Julien VILLEMEJANE / 14/sep/2024
 */

#define   LED2      PA5
#define   SWITCH1   PC13

byte state = LOW;

/* SETUP FUNCTION */
void setup() {
  pinMode(LED2, OUTPUT);
  pinMode(SWITCH1, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(SWITCH1), blink, RISING);
}

/* MAIN LOOP */
void loop() {

}

/* ISR Blink */
void blink() {
  state = !state;
  digitalWrite(LED2, state);
}