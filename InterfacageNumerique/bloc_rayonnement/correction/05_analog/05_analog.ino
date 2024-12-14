/*
 *  Robotics / Arduino & Nucleo Board
 **********************************************************************
 *  Engineer training / Digital Interfaces
 **********************************************************************
 *    LEnsE / Institut d'Optique / https://lense.institutoptique.fr/ 
 *    Author : Julien VILLEMEJANE / 18/oct/2024
 */

#define   LED1      PC7
#define   LED2      PB13
#define   USER_B    PC13
#define   SW1       PC6
#define   SW2       PC8

#define   POT_IN	  PC4
#define   PHD_IN	  PC3
#define   THERM_IN  PC1

int val_pot, val_temp, val_phd;

void setup() {
  Serial.begin(9600);
}

void loop() {
  val_pot = analogRead(POT_IN);
  Serial.print("Pot = ");
  Serial.println(val_pot);
  val_temp = analogRead(THERM_IN);
  Serial.print("Temp = ");
  Serial.println(val_temp);
  val_phd = analogRead(PHD_IN);
  Serial.print("Phd = ");
  Serial.println(val_phd);
  delay(500);
}

