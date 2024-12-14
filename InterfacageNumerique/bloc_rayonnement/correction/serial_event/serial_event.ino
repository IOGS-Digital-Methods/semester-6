/*
 *  Serial Communication / Example of PWM LED control
 **********************************************************************
 *  Engineer training / Digital Interfaces
 **********************************************************************
 *    LEnsE / Institut d'Optique / https://lense.institutoptique.fr/ 
 *    Author : Julien VILLEMEJANE / 14/sep/2024
 */

#define   LED2      PA5   //PB4

String inputString = "";      // a String to hold incoming data
bool stringComplete = false;  // whether the string is complete

int dutycycle = 0;

void setup() {
  pinMode(LED2, OUTPUT);
  // initialize serial:
  Serial.begin(9600);
  // reserve 200 bytes for the inputString:
  inputString.reserve(200);
}

void loop() {
  // print the string when a newline arrives:
  if (stringComplete) {
    Serial.print(inputString[0]);
    // Action to do
    switch(inputString[0]){
      case 'A':
        digitalWrite(LED2, HIGH);
        break;
      case 'E':
        digitalWrite(LED2, LOW);
        break;
      case 'M':
        sscanf(inputString.c_str(),"M_%d!",&dutycycle);
        analogWrite(LED2, dutycycle);
        break;
      default:
        break;
    }


    // clear the string:
    inputString = "";
    stringComplete = false;
  }
}

/*
  SerialEvent occurs whenever a new data comes in the hardware serial RX. This
  routine is run between each time loop() runs, so using delay inside loop can
  delay response. Multiple bytes of data may be available.
*/
void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read();
    // add it to the inputString:
    inputString += inChar;
    // end of command !
    if (inChar == '!') {
      stringComplete = true;
    }
  }
}
