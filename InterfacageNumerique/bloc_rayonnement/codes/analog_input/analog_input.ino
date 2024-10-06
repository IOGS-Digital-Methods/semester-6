/*
 *  Analog inputs / Example of analog signal sampling  
 **********************************************************************
 *  Engineer training / Digital Interfaces
 **********************************************************************
 *    LEnsE / Institut d'Optique / https://lense.institutoptique.fr/ 
 *    Author : Julien VILLEMEJANE / 14/sep/2024
 */

#define   ANALOG3   PB0
#define   SWITCH1   PC13

int val = 0;

/* SETUP FUNCTION */
void setup() {
  pinMode(SWITCH1, INPUT_PULLUP);
  Serial.begin(9600);           //  setup serial
  attachInterrupt(digitalPinToInterrupt(SWITCH1), sample, RISING);
}

/* MAIN LOOP */
void loop() {

}

/* ISR Blink */
void sample() {
  val = analogRead(ANALOG3);  // read the input pin
  Serial.println("ADC value = " + String(val));
}