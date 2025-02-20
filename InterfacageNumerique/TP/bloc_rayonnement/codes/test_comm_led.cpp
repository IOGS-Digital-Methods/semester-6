/*  
 *  Structure of a main file for embedded project @ LEnsE
 *      Light Radiation Project / Communication
 *
 *  This code allows communication between a computer application
 * and a Nucleo board. 
 *  Sending an 'a' on the serial port @115200 bauds ... the LED2.
 *  Sending an 'e' on the serial port @115200 bauds ... the LED2.
 *****************************************************************
 *  Pinout :
 *      PC_7 - Output LED (D1 on the light radiation board)
 *      PB_13 - Output LED (D2 on the light radiation board)
 *****************************************************************
 *  Tested with Nucleo XnnnMM board / Mbed OS 6
 *****************************************************************
 *  Author : J. VILLEMEJANE / LEnsE - Creation 2025/01/18
 *****************************************************************
 *  LEnsE / https://lense.institutoptique.fr/
 *      Based on Mbed OS 6 example : mbed-os-example-blinky-baremetal
 */

#include "mbed.h"

DigitalOut led1(PC_7);
DigitalOut led2(PB_13);

UnbufferedSerial      my_pc(USBTX, USBRX);

void ISR_my_pc_reception(void);

char data;

int main()
{    
    my_pc.baud(115200);
    my_pc.attach(&ISR_my_pc_reception, UnbufferedSerial::RxIrq);
    while (true){}
}
void ISR_my_pc_reception(void){
    led1 = !led1;
    my_pc.read(&data, 1);     // get the received byte
    if(data == 'a'){    led2 = 1;   } 
    if(data == 'e'){    led2 = 0;   }    
    my_pc.write(&data, 1);    // echo of the byte received
}