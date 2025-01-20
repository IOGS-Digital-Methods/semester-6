/*  
 *  Structure of a main file for embedded project @ LEnsE
 *      Light Radiation Project / Power LED control
 *
 *  This code allows to control power LED intensity via a BCR430-UW6
 * driver associated with a digital potentiometer MCP4132 in SPI
 *****************************************************************
 *  Pinout :
 *      PA5, PA6, PA7 - SPI (SCK, MISO, MOSI)
 *      PB5 - CS 
 *****************************************************************
 *  Tested with Nucleo XnnnMM board / Mbed OS 6
 *****************************************************************
 *  Author : J. VILLEMEJANE / LEnsE - Creation 2025/01/18
 *****************************************************************
 *  LEnsE / https://lense.institutoptique.fr/
 *      Based on Mbed OS 6 example : mbed-os-example-blinky-baremetal
 */

////////  ATTENTION !!!!   A TESTER AVEC LED FONCTIONNELLE !!

#include "mbed.h"

SPI my_spi(PA_7, PA_6, PA_5);  // mosi, miso, sck
DigitalOut cs_led(PB_5);

void init_LED(int val){
    cs_led = 1;
    my_spi.format(8,3);          
    my_spi.frequency(100000);
    thread_sleep_for(100);

    // Send value of the potentiometer wiper.
    cs_led = 0;
    uint8_t address = 0;    // Wiper control register 
    uint8_t command = 0;    // Write command   
    uint8_t transferByte = (0 << 4) | ((0 << 2) | 0);
    my_spi.write(transferByte);
    my_spi.write(val);
    cs_led = 1;
}


int main()
{    
    init_LED(100);
    
    while (true){}
}