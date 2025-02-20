/*  
 *  Structure of a main file for embedded project @ LEnsE
 *      Robotics Project / Ultrasound distance sensor
 *
 *  This code allows to get the distance from an ultrasound sensor. 
 *****************************************************************
 *  Pinout :
 *      PB_5 - Output - US trig input 
 *      PB_3 - Input - US echo output 
 *****************************************************************
 *  Tested with Nucleo XnnnMM board / Mbed OS 6
 *****************************************************************
 *  Author : J. VILLEMEJANE / LEnsE - Creation 2025/01/28
 *****************************************************************
 *  LEnsE / https://lense.institutoptique.fr/
 *      Based on Mbed OS 6 example : mbed-os-example-blinky-baremetal
 */

#include "mbed.h"

DigitalOut  led1(PC_7);
DigitalOut  trig_us(PB_5);
InterruptIn  echo_us(PB_3);

Ticker tik;
bool new_dist = false;
int dist_us;
int tik_cnt;

void tik_ISR(){
    tik_cnt += 1;
}

void start_us(){
    trig_us = 1;
    wait_us(10);
    trig_us = 0;
    led1 = 0;
}

void echo_rise_ISR(){
    led1 = 1;
    tik_cnt = 0;
    tik.attach(&tik_ISR, 30us);
}

void echo_fall_ISR(){
    tik.detach();
    dist_us = tik_cnt;
    new_dist = true;
}

int main()
{
    trig_us = 0;
    thread_sleep_for(10);
    echo_us.rise(&echo_rise_ISR);
    echo_us.fall(&echo_fall_ISR);
    printf("Start");
    start_us();

    while(1)
    {
        if(new_dist == true){
            printf("New Distance = %d cm\r\n", dist_us);
            //thread_sleep_for(100);
            start_us();
        }
        thread_sleep_for(10);
    }
}