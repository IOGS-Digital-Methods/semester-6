/*  
 *  Structure of a main file for embedded project @ LEnsE
 *
 *  This code shows an example of use of PWM output.
 *****************************************************************
 *  Pinout :
 *      PB_6 - Output - LED on D10 output on Nucleo L476RG board
 *****************************************************************
 *  Tested with Nucleo L476RG board / MBED + STM32
 *****************************************************************
 *  Author : J. VILLEMEJANE / LEnsE - Creation 2024/12/15
 *  LEnsE / https://lense.institutoptique.fr/
 */
 
 #include "mbed.h"

#define WAIT_TIME_MS 200
DigitalOut led1(PB_6);

float val_rc = 0;

int main()
{
    led1.period_ms(10);
    led1.write(0);

    while (true)
    {
        for(int i = 0; i <= 20; i++){
            val_rc = i/20.0;
            led1.write(val_rc);
            thread_sleep_for(WAIT_TIME_MS);
        }
        for(int i = 20; i > 0; i--){
            val_rc = i/20.0;
            led1.write(val_rc);
            thread_sleep_for(WAIT_TIME_MS);
        }
    }
}
