/*  
 *  Structure of a main file for embedded project @ LEnsE
 *      Light Radiation Project / Communication
 *
 *  This code allows communication between a computer application
 * and a Nucleo board. The communication is based on the protocol
 * mentionned in :
 *   https://lense.institutoptique.fr/ressources/Annee1/InterfacageNumerique/bloc_rayonnement/S6_IntNum_TP_Bloc_rayonnement.pdf
 *****************************************************************
 *  Pinout :
 *      
 *****************************************************************
 *  Tested with Nucleo L476RG board / Mbed OS 6
 *****************************************************************
 *  Author : J. VILLEMEJANE / LEnsE - Creation 2026/11/02
 *****************************************************************
 *  LEnsE / https://lense.institutoptique.fr/
 *      Based on Mbed OS 6 example : mbed-os-example-blinky-baremetal
 */


#include "mbed.h"

#define		US_START_VALUE	1000
#define		US_END_VALUE	2000
#define		TIMER_MOVE		700		// ms

//// Input and outputs
DigitalOut led1(PC_7);
DigitalOut led2(PB_13);
UnbufferedSerial      my_pc(USBTX, USBRX);

InterruptIn sw1(PC_6);
InterruptIn sw2(PC_8);
InterruptIn sw_user(PC_13);

PwmOut servo(PB_7);

AnalogIn potent(PC_4);
AnalogIn photodiode(PC_3);
AnalogIn r_therm(PC_1);

Ticker tik;


//// Functions prototypes
void ISR_my_pc_reception(void);
bool is_angle_ok(int, int, int);
int deg_to_us(int);
void move_to_position(int);
void acquire_data(int, int*);
void handle_ticker();
void start_timer_move(int);
void handle_acquisition();
void start_acquisition();

//// Global variables
// Serial communication
char input_string[20] = "";      // a String to hold incoming data
char output_string[20] = "";     // a String to hold outcoming data
bool string_complete = false;  // whether the string is complete
int input_cnt = 0;
bool is_ok = false;

// Adaptation parameters
int us_incr = 0;

// Data acquisition
bool acquiring = false;
bool acquiring_once = false;
int data_cpt = 0;
int data_light[180];
int data_light_one;

// Parameters
int angle_start_deg = -100, angle_end_deg = 100;
int angle_step_deg = -1;
int angle_value = 0;
int old_angle = -1;
bool continous_servo = false;
bool data_required = false;

// Ticker
int timer_move = 0;


//// Main function
int main()
{ 
	led1 = 0;
	led2 = 1;
	servo.period_ms(20);
	int val_us = deg_to_us(0);
  servo.pulsewidth_us(val_us);
	
	my_pc.baud(9600);
	my_pc.attach(&ISR_my_pc_reception, UnbufferedSerial::RxIrq);
	
	tik.attach(&handle_ticker, 1ms); 
	
	while (true){
			char acq = 'N';
			// print the string when a newline arrives:
			if (string_complete) {
					// Action to do
					switch(input_string[1]){
						case 'A' :    // start angle in degrees
							old_angle = angle_start_deg;
							sscanf(input_string, "!A:%d?", &angle_start_deg);
		
							is_ok = is_angle_ok(angle_start_deg, angle_start_deg + 1, 1);
							if(is_ok == true){ 
									sprintf(output_string, "!A:%d;", angle_start_deg);
									my_pc.write(output_string, strlen(output_string));
							}
							else{
									sprintf(output_string, "!A:-100;");
									my_pc.write(output_string, strlen(output_string));
									angle_start_deg = old_angle;
							}
							break;

						case 'B' :    // stop angle in degrees
							old_angle = angle_end_deg;
							sscanf(input_string, "!B:%d?", &angle_end_deg);
		
							is_ok = is_angle_ok(angle_end_deg-1, angle_end_deg, 1);
							if(is_ok == true){ 
									sprintf(output_string, "!B:%d;", angle_end_deg);
									my_pc.write(output_string, strlen(output_string));
							}
							else{
									sprintf(output_string, "!B:-100;");
									my_pc.write(output_string, strlen(output_string));
									angle_end_deg = old_angle;
							}
							break;
				
						case 'C' :    // step angle in degrees
							old_angle = angle_step_deg;
							sscanf(input_string, "!C:%d?", &angle_step_deg);
		
							is_ok = is_angle_ok(angle_step_deg, angle_step_deg+1, 1);
							if(is_ok == true){ 
									sprintf(output_string, "!C:%d;", angle_step_deg);
									my_pc.write(output_string, strlen(output_string));
							}
							else{
									sprintf(output_string, "!C:-100;");
									my_pc.write(output_string, strlen(output_string));
									angle_step_deg = old_angle;
							}
							break;

						case 'S' :    // Start acquisition
							// Test if angles ok
							is_ok = is_angle_ok(angle_start_deg, angle_end_deg, angle_step_deg);
						  if(is_ok == true){
								int nb_data = (angle_end_deg - angle_start_deg) / angle_step_deg;
								int r_data = (angle_end_deg - angle_start_deg) % angle_step_deg;
								if(r_data != 0){
									nb_data += 1;
								}
								sprintf(output_string, "!S:%d;", nb_data);
								my_pc.write(output_string, strlen(output_string));
								start_acquisition();
							}
							else{								
								sprintf(output_string, "!S:0;");
								my_pc.write(output_string, strlen(output_string));
							}
							// 
							break;
						
						case 'T' :    // Communication test and initial angle mode
							continous_servo = true;
							sprintf(output_string, "!T;");
							my_pc.write(output_string, strlen(output_string));
							break;
					
						case 'P' :    // Stop initial angle mode
							continous_servo = false;
							sprintf(output_string, "!P;");
							my_pc.write(output_string, strlen(output_string));
							break;						
						
						case 'D' :    // Data transmission
							sscanf(input_string,"!D:%d?",&data_cpt);
							sprintf(output_string, "!D:%d:%d;", data_cpt, data_light[data_cpt]);
							my_pc.write(output_string, strlen(output_string));
							break;

						case 'E' :    // Data transmission
							sscanf(input_string,"!E?");
						  if(acquiring){
								acq = 'Y';
							}
							sprintf(output_string, "!E:%c;", acq);
							my_pc.write(output_string, strlen(output_string));
							break;
						
						case 'Z' : 		// Collect data to specific angle
							sscanf(input_string, "!Z:%d?", &angle_value);
		
							is_ok = is_angle_ok(angle_value, angle_value+1, 1);						
							if(is_ok == true){ 
								val_us = deg_to_us(angle_value);
								servo.pulsewidth_us(val_us);
								thread_sleep_for(500);
								
								acquire_data(-1, &data_light_one);
								
								sprintf(output_string, "!Z:%d:%d;", angle_value, data_light_one);
								my_pc.write(output_string, strlen(output_string));
							}
							else{
									sprintf(output_string, "!C:-100;");
									my_pc.write(output_string, strlen(output_string));
									angle_step_deg = old_angle;
							}
							break;	
						
						default :
							sprintf(output_string, "!ERROR;");
							my_pc.write(output_string, strlen(output_string));
							
					}
					
					input_cnt = 0;
					sprintf(output_string, "");
					string_complete = false;
			}
			// Setup the 0 angle in T mode (stop with P mode)
			if(continous_servo){
				us_incr = (potent.read()-0.5)*100;
				move_to_position(0);
			}
			
			thread_sleep_for(10);
	}
}

// Interrupt Sub Routine for Serial incoming data
void ISR_my_pc_reception(void){
    char in_char;
    my_pc.read(&in_char, 1);     // get the received byte   
    if(in_char == '!'){
        led2 = !led2;
        input_cnt = 0;
    }
    else{
        input_cnt += 1;
    }
    // add it to the inputString:
    input_string[input_cnt] = in_char;
    // end of command !
    if (in_char == '?') {
      string_complete = true;
    }
}

// Angle test
bool is_angle_ok(int angle_start, int angle_end, int angle_step){
  if((angle_start >= 90) | (angle_start < -90))  return false;
  if((angle_end > 90) | (angle_end <= -90))  return false;
  if((angle_step > 90) | (angle_step < 0))  return false;
  if(angle_start > angle_end)  return false;
  return true;
}



// Degree to us for servo (-90 to 90 degrees)
int deg_to_us(int deg){
	int us_value = (US_END_VALUE - US_START_VALUE) * deg / 180 + (US_END_VALUE + US_START_VALUE) / 2 + us_incr;
	return us_value;
}

// Move servo to specific position (-90 to 90 degrees)
void move_to_position(int deg){
	int val_us = deg_to_us(deg);
	servo.pulsewidth_us(val_us);
}
// Acquisition of a data from the photodiode
void acquire_data(int index, int *value){
	int data = photodiode.read_u16();
	if(index == -1){ // Simple acquisition
		*value = data;
	}
	else{ // Multi acquisition
		value[index] = data;
	}
}
// Action performed at the end of the ticker
void handle_ticker(){
	if(timer_move == 0){
		if(acquiring){
			handle_acquisition();
		}
	}
	else{
		timer_move--;
	}
}
// Start acquisition
void start_acquisition(){
	acquiring = true;	
	acquire_data(0, data_light);	// Bug on first acquisition
	led1 = 1;
	data_cpt = 0;
	move_to_position(angle_start_deg);
	start_timer_move(3*TIMER_MOVE);
}
// Start acquisition
void handle_acquisition(){
	// Collect data
	acquire_data(data_cpt, data_light);
	data_cpt++;
	// Move to next
	int deg = angle_start_deg + data_cpt * angle_step_deg;
	if(deg > angle_end_deg){
		acquiring = false;
		led1 = 0;
	}
	else{
		move_to_position(deg);
		// Start timer move
		start_timer_move(TIMER_MOVE);
	}
}
// Start timeout timer for movement
void start_timer_move(int value){
	timer_move = value;
}
	