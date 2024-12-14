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

int valPot, valTemp, valPhd;
bool samplingOk = false;

void samplingIsr(){
  valPot = analogRead(POT_IN);
  valTemp = analogRead(THERM_IN);
  valPhd = analogRead(PHD_IN);
  samplingOk = true;
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
  if(samplingOk == true){
    Serial.print("Pot = ");
    Serial.println(valPot);
    Serial.print("Temp = ");
    Serial.println(valTemp);
    Serial.print("Phd = ");
    Serial.println(valPhd);
    sampling_ok = false;
  }
  delay(10);
}

