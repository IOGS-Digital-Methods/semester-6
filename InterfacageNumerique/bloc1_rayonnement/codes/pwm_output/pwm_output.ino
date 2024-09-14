/*
 *  PWM Outputs / Example of light control with PWM
 **********************************************************************
 *  Engineer training / Digital Interfaces
 **********************************************************************
 *    LEnsE / Institut d'Optique / https://lense.institutoptique.fr/ 
 *    Author : Julien VILLEMEJANE / 14/sep/2024
 */

#define   ANALOG3   PB0
#define   LED2      PB4

int val = 0;

/* SETUP FUNCTION */
void setup() {
  pinMode(LED2, OUTPUT);
  Serial.begin(9600);    
}

/* MAIN LOOP */
void loop() {
  val = analogRead(ANALOG3);  
  Serial.println("ADC value = " + String(val));
  val = val / 4;
  analogWrite(LED2, val);
  Serial.println("Calculated value = " + String(val));
}