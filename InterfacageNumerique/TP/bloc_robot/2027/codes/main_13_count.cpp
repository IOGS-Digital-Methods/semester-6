/*  
 *  Structure of a main file for embedded project @ LEnsE
 *****************************************************************
 *  Tested with Nucleo L476RG board / Mbed OS 6
 *****************************************************************
 *  ProTIS / https://lense.institutoptique.fr/
 *      Based on Mbed OS 6 example : mbed-os-example-blinky-baremetal
 */

#include "mbed.h"

// Inputs/Outputs
DigitalOut led1(PC_7);
DigitalOut led2(PB_13);

InterruptIn speed_l(PC_9);
InterruptIn speed_r(PC_8);
InterruptIn stop(PC_13);

DigitalOut mot_en(PA_9);
PwmOut mot_L_1(PB_4);
PwmOut mot_L_2(PA_8);
PwmOut mot_R_1(PA_0);
PwmOut mot_R_2(PA_1);

// Global Variables
int cpt_l = 0;
int cpt_r = 0;

// Prototypes
void init();
void stop_robot();
void handle_inc_cpt_l();
void handle_inc_cpt_r();
void move_R(float speed);
void move_L(float speed);

// Main function
int main()
{
	init();
	move_R(0.7);
	move_L(0.7);
	thread_sleep_for(1000);
	stop_robot();
	while (true)
	{
		printf("L=%d / R=%d \n", cpt_l, cpt_r);
	}
}


// Other functions
void init(){
	mot_en = 0;
	stop.fall(&stop_robot);
	cpt_l = 0;
	cpt_r = 0;
	// Pwm Period for motors
	mot_L_1.period_ms(1);
	mot_L_2.period_ms(1);
	mot_R_1.period_ms(1);
	mot_R_2.period_ms(1);
	// Interrupt on Speed sensors
	speed_l.rise(&handle_inc_cpt_l);
	speed_r.rise(&handle_inc_cpt_r);
	// Motors enabled
	mot_en = 1;
}

void handle_inc_cpt_l(){
	cpt_l++;
}
void handle_inc_cpt_r(){
	cpt_r++;
}

void move_R(float speed){
	mot_en = 1;
	if(speed > 0){
		mot_R_1.write(speed);
		mot_R_2.write(0);
	}
	else{
		mot_R_1.write(0);
		mot_R_2.write(speed);
	}
}

void move_L(float speed){
	mot_en = 1;
	if(speed > 0){
		mot_L_1.write(0);
		mot_L_2.write(speed);
	}
	else{
		mot_L_1.write(speed);
		mot_L_2.write(0);
	}
}

void stop_robot(){
	mot_en = 0;
	mot_R_1.write(0);
	mot_R_2.write(0);
	mot_L_1.write(0);
	mot_L_2.write(0);
}	