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
#define   SW1       PA11
#define   SW2       PA12
#define   SERVO     PB7

#define   POT_IN	PC3
#define   TEMP_IN	PC2

int val_pot;
int val_temp;
bool sampling_ok = false;

void samplingIsr(){
  val_pot = analogRead(POT_IN);
  val_temp = analogRead(TEMP_IN);
  sampling_ok = true;
}

void setup() {
  Serial.begin(9600);

  // // Setup TIMER !
#if defined(TIM1)
  TIM_TypeDef *Instance = TIM1;
#else
  TIM_TypeDef *Instance = TIM2;
#endif
  // Instantiate HardwareTimer object. Thanks to 'new' instanciation, HardwareTimer is not destructed when setup() function is finished.
  HardwareTimer *MyTim = new HardwareTimer(Instance);
  MyTim->setOverflow(10, HERTZ_FORMAT); // 10 Hz
  MyTim->attachInterrupt(samplingIsr);
  MyTim->resume();
  // // Setup TIMER ! // END
}


void loop() {
  if(sampling_ok == true){
    Serial.print("Pot = ");
    Serial.println(val_pot);
    Serial.print("Temp = ");
    Serial.println(val_temp);
    sampling_ok = false;
  }
  delay(10);
}

