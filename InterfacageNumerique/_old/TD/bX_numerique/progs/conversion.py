#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module Digital Tools / Semester 5 / Institut d'Optique

TD Digital process / conversion

Created on 25/May/2024

@author: LEnsE / IOGS / Palaiseau
@author: Julien VILLEMEJANE
"""

import struct

## Definition of a float number
f_nb = 3.14
print(type(f_nb))

# Display the stored value as byte
byte_data = struct.pack('f', f_nb)
print(byte_data)



## From byte to float
byte_data = b'\x00\x00\x00\x10'

new_f_nb = struct.unpack('f', byte_data)[0]
new_i_nb = int.from_bytes(byte_data, byteorder='big')

print(new_f_nb)
print(new_i_nb)