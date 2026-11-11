/*  
 *  Structure of a main file for embedded project @ LEnsE
 *      Robotics Project / Smart NeoPixel LEDs
 *
 *  This code allows to control NeoPixel LEDs from a Nucleo board. 
 *****************************************************************
 *  Pinout :
 *      PC_0 - Front Right headlight 
 *****************************************************************
 *  Tested with Nucleo XnnnMM board / Mbed OS 6
 *****************************************************************
 *  Author : J. VILLEMEJANE / LEnsE - Creation 2025/01/18
 *****************************************************************
 *  LEnsE / https://lense.institutoptique.fr/
 *      Based on Mbed OS 6 example : mbed-os-example-blinky-baremetal
 */


#include "mbed.h"
#include "PixelArray.h"
#include "WS2812.h"

#define     STRIP_SIZE      2

WS2812  my_hl1(PC_0, STRIP_SIZE, WS2812_STD);
PixelArray my_px1(STRIP_SIZE, WS2812_STD);

// Main function
int main() {
    my_hl1.set_timings(6, 13, 14, 5);

    my_hl1.break_trame();
    my_hl1.send_leds(my_px1.get_array()); 

    int cpt = 0;

    while(1){
        my_hl1.break_trame();
        thread_sleep_for(1000);
        my_px1.set_all_RGB(255, 0, 128);
        my_hl1.send_leds(my_px1.get_array());

        my_hl1.break_trame();
        thread_sleep_for(1000);  
        my_px1.set_black_all();
        my_hl1.send_leds(my_px1.get_array());

        my_hl1.break_trame();
        thread_sleep_for(1000);
        my_px1.set_pix_RGB(0, 0, 255, 128);
        my_px1.set_pix_RGB(1, 0, 0, 255);
        my_hl1.send_leds(my_px1.get_array());

        my_hl1.break_trame();
        thread_sleep_for(1000);
        my_px1.set_black_all();
        my_hl1.send_leds(my_px1.get_array());
        
        cpt+=1;
    }
}