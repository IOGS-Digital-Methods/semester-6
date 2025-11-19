/*  
 *  Structure of a main file for embedded project @ LEnsE
 *
 *  This code shows an example of use of interruption on a Ticker.
 *****************************************************************
 *  Pinout :
 *      PB_6 - Output - LED on D10 output on Nucleo L476RG board
 *****************************************************************
 *  Tested with Nucleo L476RG board / MBED + STM32
 *****************************************************************
 *  Author : J. VILLEMEJANE / LEnsE - Creation 2025/11/19
 *  LEnsE / https://lense.institutoptique.fr/
 */
 
#include "mbed.h"

DigitalOut led1(PB_6);	// D10
DigitalOut led2(PA_7);	// D11

Ticker tik;

bool led_on = false;
int timer_1 = 0;


void led_action(){
	if(led_on){
		led1 = !led1;
	}
	else{
		led1 = 0;
	}
}

/* Interrupt subroutine */
void tik_ISR(){
	if(timer_1 != 0){
		timer_1 = timer_1 - 1;
	}
	led_action();
}

/* Main function */
int main()
{	
	tik.attach(&tik_ISR, 0.1);
	
	while (true)
	{
		if(timer_1 == 0){
			led_on = !led_on;
			timer_1 = TIMER_MAX;
		}
		thread_sleep_for(10);
	}
}