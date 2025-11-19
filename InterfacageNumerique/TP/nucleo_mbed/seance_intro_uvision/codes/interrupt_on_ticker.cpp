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

/* Interrupt subroutine */
void tik_ISR(){
	led1 = !led1;
}

/* Main function */
int main()
{	
	tik.attach(&tik_ISR, 0.7);

	while (true)
	{
		led2 = !led2;
		thread_sleep_for(200);
	}
}