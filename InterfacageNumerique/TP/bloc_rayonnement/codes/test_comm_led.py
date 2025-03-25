# -*- coding: utf-8 -*-
"""
First code to transmit and receive data between a computer and
a Nucleo Board.

***************************************************************
  Tested with Nucleo L476RG board / Arduino + STM32
***************************************************************

Creation 2024/12/16
@author: julien.villemejane <julien.villemejane@institutoptique.fr>
LEnsE / https://lense.institutoptique.fr/
"""

from serial import Serial
import serial.tools.list_ports


def receiving_data(ser):
    received_data = ""
    while True:
        byte = ser.read(1).decode('ascii')
        if byte == ';':  # Check if byte is ending character
            break
        received_data += byte
    return received_data


if __name__ == "__main__":
    ports = serial.tools.list_ports.comports()
    # To obtain the list of the communication ports
    for port, desc, hwid in sorted(ports):
        print("{}: {}".format(port, desc))
    # To select the port to use
    selectPort = input("Select a COM port : ")    
    print(f"Port Selected : COM{selectPort}")
    # To open the serial communication at a specific baudrate
    serNuc = Serial('COM'+str(selectPort), 9600)

    appOk = 1

    while appOk:
        choice = input("Char to send : ") 
        if choice == 'q' or choice == 'Q':
            appOk = 0
        else:
            if choice == 'a': # Send 'a'
                data_to_send = 'a'
                serNuc.write(bytes(data_to_send, 'ascii'))
                data_rec = receiving_data(serNuc)
                print(str(data_rec))
            elif choice == 'e': # Send 'e'
                data_to_send = 'e'
                serNuc.write(bytes(data_to_send, 'ascii'))
                data_rec = receiving_data(serNuc)
                print(str(data_rec))            
       
    
    
    serNuc.close()
    