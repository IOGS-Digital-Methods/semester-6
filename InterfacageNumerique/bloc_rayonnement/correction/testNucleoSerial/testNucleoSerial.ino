/*
  DigitalReadSerial

  Reads a digital input on pin 2, prints the result to the Serial Monitor

  This example code is in the public domain.

  https://www.arduino.cc/en/Tutorial/BuiltInExamples/DigitalReadSerial
*/

#include <Servo.h>

int cnt = 0;

// inputs definition
int sw1 = PC6;
int sw2 = PC8;
int potIn = PC4;
// outputs definition
int led1 = PC7;
int led2 = PB13;
int servoOut = PB7;
// Peripherals
Servo   myServo;

// Global Variables
int valPotIn = 0, valPotInM = 0;

// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
  // inputs
  pinMode(sw1, INPUT);
  pinMode(sw2, INPUT);
  // outputs
  pinMode(led1, OUTPUT);
  pinMode(led2, OUTPUT);

  //pinMode(servoOut, INPUT_PULLUP);
  //LL_GPIO_SetAFPin_0_7(GPIOB,  GPIO_PIN_7,  GPIO_AF1_TIM2);
  pinMode(servoOut, OUTPUT);
  myServo.attach(servoOut);

  cnt = 0;
  
  Serial.println("End of SETUP");
}

// the loop routine runs over and over again forever:
void loop() {
  cnt += 1;
  // read the input pin:
  int buttonState = digitalRead(sw1);
  valPotIn = analogRead(potIn);
  digitalWrite(led1, HIGH);
  // print out the state of the button:
  Serial.print("LOOP ");
  Serial.print(cnt);
  Serial.print(" = ");
  Serial.println(valPotIn);
  valPotInM = map(valPotIn, 0, 1013, 0, 180);
  int kk = cnt % 180;
  myServo.write(kk);
  delay(200);  // delay in between reads for stability
}
