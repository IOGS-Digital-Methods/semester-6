/*  
 *  Structure of a main file for embedded project @ LEnsE
 *
 *  This code shows an example of use of PWM output.
 *****************************************************************
 *  Pinout :
 *      PA_0 - Analog Input - A0 on Nucleo L476RG board
 *****************************************************************
 *  Tested with Nucleo L476RG board / MBED + STM32
 *****************************************************************
 *  Author : J. VILLEMEJANE / LEnsE - Creation 2024/12/15
 *  LEnsE / https://lense.institutoptique.fr/
 */
 
#include "mbed.h"

#define WAIT_TIME_MS 200 
AnalogIn adc_in(PA_0);

int val_adc = 0;

int main()
{

    while (true)
    {
        val_adc = adc_in.read_u16();
        printf("Val = %d \r\n", val_adc);
        thread_sleep_for(WAIT_TIME_MS);
    }
}