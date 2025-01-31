/*  
 *  Structure of a main file for embedded project @ LEnsE
 *****************************************************************
 *  Pinout :
 *      - outS1 /   Output of the system
 *      - outS2 /   Output for time measurement
 *      - inBP /    Input for onboard switch (blue button) Active LOW
 *      - inE1 /    Analog input - 0 to 3.3V
 *      
 *****************************************************************
 *  Tested with Nucleo L476RG board / Mbed OS 6
 *****************************************************************
 *  Author : J. VILLEMEJANE / LEnsE - Creation 2025/01/26
 *****************************************************************
 *  ProTIS / https://lense.institutoptique.fr/
 *      Based on Mbed OS 6 example : mbed-os-example-blinky-baremetal
 */

#include "mbed.h"
 
DigitalOut outS1(PA_5);
DigitalOut outS2(PA_4);
InterruptIn inBP(PC_13);    // User button (onboard blue switch)
AnalogIn inE1(PA_0);     

Ticker  tik;   

int     counter = 0;        // User button clicks counter
int   	analog_value = 0;

void sampling() {
    outS1 = !outS1;
    analog_value = inE1.read_u16();
    counter++;  
    outS2 = 1;     
    printf("Measure [%d] = %d \r\n", counter, analog_value);
    outS2 = 0;       
}

int main()
{
    printf("Bare metal example / Mbed OS %d.%d\n", MBED_MAJOR_VERSION, MBED_MINOR_VERSION);
    printf("\tSolec Group / LEnsE \n");

    tik.attach(&sampling, 200ms);

    while (true)
    {
        wait_us(10);
    }
}
