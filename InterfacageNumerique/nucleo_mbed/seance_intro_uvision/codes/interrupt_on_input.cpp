/*  
 *  Structure of a main file for embedded project @ LEnsE
 *
 *  This code shows an example of use of interruption on input.
 *****************************************************************
 *  Pinout :
 *      PB_6 - Output - LED on D10 output on Nucleo L476RG board
 *      PA_8 - Input - D7 input on Nucleo L476RG board 
 *****************************************************************
 *  Tested with Nucleo L476RG board / MBED + STM32
 *****************************************************************
 *  Author : J. VILLEMEJANE / LEnsE - Creation 2024/12/15
 *  LEnsE / https://lense.institutoptique.fr/
 */
 
 #include "mbed.h"

#define WAIT_TIME_MS 50
DigitalOut led1(PB_6);

InterruptIn   sw1(PA_8);

void sw_ISR(){
    bool led_state = led1;
    led1 = !led_state;
}


int main()
{
    sw1.rise(&sw_ISR);

    while (true)
    {
        thread_sleep_for(WAIT_TIME_MS);
    }
}