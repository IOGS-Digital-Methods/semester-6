# -*- coding: utf-8 -*-
"""*serial_mini_gui.py* file.

Serial Communication / Example of a script to control LED toggle
----
Engineer training / Digital Interfaces


.. moduleauthor:: Julien VILLEMEJANE <julien.villemejane@institutoptique.fr>
"""

from serial import Serial
import serial.tools.list_ports                          
                             
# -------------------------------
# Launching as main for tests
if __name__ == "__main__":
    ports = serial.tools.list_ports.comports()
    # To obtain the list of the communication ports
    for port, desc, hwid in sorted(ports):
        print("{}: {}".format(port, desc))
    # To select the port to use
    select_port = input("Select a COM port : ")    
    print(f"Port Selected : COM{select_port}")
    # To open the serial communication at a specific baudrate
    ser_nuc = Serial('COM'+str(select_port), 9600)  
    
    appOk = 1

    while(appOk == 1):
        choice = input('Enter a command (q for quit):')
        
        if(choice == 'q'):
            appOk = 0
            break
        else:
            if choice == 'A' or choice == 'E':
                choice += '!'
                print(choice)
                ser_nuc.write(bytes(choice, 'utf-8'))
                while ser_nuc.inWaiting() == 0:
                    pass
                data_rec = ser_nuc.read(1)  # bytes
                print(f'D = {data_rec}')
       
    # Close the serial port
    ser_nuc.close()