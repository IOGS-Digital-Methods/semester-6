/*  
 *  Structure of a main file for embedded project @ LEnsE
 *****************************************************************
 *  Tested with Nucleo L476RG board / Mbed OS 6
 *****************************************************************
 *  ProTIS / https://lense.institutoptique.fr/
 *      Based on Mbed OS 6 example : mbed-os-example-blinky-baremetal
 */

#include "mbed.h"
#define		MAX_SPEED		0.6
#define		DIFF_SPEED	0.5

// Global Variables
bool capt_L, capt_C, capt_R;

void test_line(bool line_L, bool line_C, bool line_R);

// Main function
int main()
{
	test_line(false, false, false);
	test_line(false, true, false);
	test_line(false, false, true);
	while (true)
	{
		
		thread_sleep_for(10);
	}
}

void test_line(bool line_L, bool line_C, bool line_R){
	capt_L = line_L;
	capt_C = line_C;
	capt_R = line_R;
	int position_line = (capt_L << 2) + (capt_C << 1) + capt_R;
	printf("%d / %d / %d  ==  %d\r\n", capt_L, capt_C, capt_R, position_line);
	
	switch(position_line){
		case 1:		// F F T
			printf("CASE 1\n");
			break;
		case 2:		// F T F
			printf("CASE 2\n");
			break;
		default:	// F F F
			printf("DEFAULT\n");
			break;
	}
}
