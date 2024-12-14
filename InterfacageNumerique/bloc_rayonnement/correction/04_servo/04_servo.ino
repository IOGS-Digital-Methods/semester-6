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
#define   SW1       PC6
#define   SW2       PC8

#define   SERVO     PB7
Servo   my_servo;

#define   POT_IN	  PC4

int val_pot, val_pot_m;

void setup() {
  Serial.begin(9600);
  while(!Serial);
  Serial.println("Hello");
  delay(100);
  LL_GPIO_SetAFPin_0_7(GPIOB,  GPIO_PIN_7,  GPIO_AF1_TIM2); // TO ADD IN DOC !!!
  pinMode(SERVO, OUTPUT);
  my_servo.attach(SERVO);
  pinMode(LED1, OUTPUT);
  pinMode(LED2, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  val_pot = analogRead(POT_IN);
  val_pot_m = map(val_pot, 0, 1013, 0, 180);
  Serial.println(val_pot_m);
  my_servo.write(val_pot_m);
  // monServo.writeMicroseconds(1500);

  delay(100);
}
