/*  
 *  Structure of a main file for embedded project @ LEnsE
 *      Light Radiation Project / Communication
 *
 *  This code allows to control the servomotor
 *****************************************************************
 *  Pinout :
 *      PC_7 - Output LED (D1 on the light radiation board)
 *      PB_7 - Output PWM (Servomotor on the light radiation board)
 *****************************************************************
 *  Tested with Nucleo XnnnMM board / Mbed OS 6
 *****************************************************************
 *  Author : J. VILLEMEJANE / LEnsE - Creation 2025/01/18
 *****************************************************************
 *  LEnsE / https://lense.institutoptique.fr/
 *      Based on Mbed OS 6 example : mbed-os-example-blinky-baremetal
 */


#include "mbed.h"

PwmOut led1(PC_7);
PwmOut servo(PB_7);

float min_val = 1000;
float max_val = 2000;
float step_val = 50;

int main()
{
    servo.period_ms(20);
    servo.pulsewidth_us(1000);

    while (true)
    {
        for(int i = min_val; i <= max_val; i+=step_val){
            servo.pulsewidth_us(i);
            thread_sleep_for(100);
        }
        for(int i = max_val; i > min_val; i-=step_val){
            servo.pulsewidth_us(i);
            thread_sleep_for(100);
        }
    }
}
