/*  
 *  Structure of a main file for embedded project @ LEnsE
 *****************************************************************
 *  Tested with Nucleo L476RG board / Mbed OS 6
 *****************************************************************
 *  ProTIS / https://lense.institutoptique.fr/
 *      Based on Mbed OS 6 example : mbed-os-example-blinky-baremetal
 */

#include "mbed.h"
#include "main_robot.h"
 
DigitalOut led_ld2(LED1);



int main()
{
    printf("\tLEnsE - L476RG  v%lf\n", 1.0);

    while (true)
    {
        led_ld2 = !led_ld2;
				led1 = !led1;
				thread_sleep_for(300);	// 300 ms
    }
}
