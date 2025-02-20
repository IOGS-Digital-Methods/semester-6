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


#include "mbed.h"

SPI my_spi(PA_7, PA_6, PA_5);  // mosi, miso, sck
DigitalOut cs_led(PB_5);

void init_LED(int val){
    cs_led = 1;
    my_spi.format(8,0);          
    my_spi.frequency(250000);
    thread_sleep_for(100);
    // Send value of the potentiometer wiper.
    cs_led = 0; 
    int cfg_value = 0b0100001111;
    uint8_t address = 0x04; // Config control register 
    uint8_t command = 0;    // Write command   
    uint8_t transferByte = (address << 4) | (command << 2) | 0b01;
    my_spi.write(transferByte);
    my_spi.write(cfg_value);
    cs_led = 1;
    thread_sleep_for(10);
    cs_led = 0;
    transferByte = (0 << 4) | (0 << 2) | 0;
    my_spi.write(transferByte);
    my_spi.write(255-val);
    cs_led = 1;
    thread_sleep_for(10);
}


int main()
{    
    init_LED(10);
    
    while (true){
        thread_sleep_for(100);
    }
}