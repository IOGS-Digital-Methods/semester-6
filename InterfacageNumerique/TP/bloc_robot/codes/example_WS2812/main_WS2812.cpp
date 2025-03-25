/**
 * FILENAME :        main_WS2812.cpp          
 *
 * DESCRIPTION :
 *       WS2812 / Intelligent control LED integrated light source Library Testing.
 *		 required : WS2812 library for MBED OS 6
 *		 required : PixelArray library for MBED OS 6
 *
 * NOTES :
 *       Developped by Villou / LEnsE
 **
 * AUTHOR :    Julien VILLEMEJANE        START DATE :    25/oct/2023
 *
 *       LEnsE / Institut d'Optique Graduate School
 */
#include "mbed.h"
#include "WS2812.h"
#include "PixelArray.h"

#define     STRIP_SIZE      10

WS2812  my_strip(D8, STRIP_SIZE, WS2812_STD);
PixelArray my_leds(STRIP_SIZE, WS2812_STD);
int colors[STRIP_SIZE];

// Main function
int main() {
    my_strip.set_timings(6, 13, 14, 5);

    my_strip.break_trame();
    my_strip.send_leds(my_leds.get_array()); 

    int cpt = 0;

    while(1){
        my_strip.break_trame();
        wait_us(200000);
        my_leds.set_all_RGB(255, 0, 128);
        my_strip.send_leds(my_leds.get_array());

        my_strip.break_trame();
        wait_us(200000);  
        my_leds.set_black_all();
        my_strip.send_leds(my_leds.get_array());

        my_strip.break_trame();
        wait_us(200000);  
        my_leds.set_pix_RGB(cpt%STRIP_SIZE, 0, 255, 0);
        my_strip.send_leds(my_leds.get_array());

        my_strip.break_trame();
        wait_us(200000);  
        my_leds.set_black_all();
        my_strip.send_leds(my_leds.get_array());
        
        cpt+=1;
    }
}