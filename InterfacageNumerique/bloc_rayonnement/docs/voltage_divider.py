# -*- coding: utf-8 -*-
"""*voltage_divider.py* file.

Voltage Divider calculation / MCP4xxx
----
Engineer training / Digital Interfaces


.. moduleauthor:: Julien VILLEMEJANE <julien.villemejane@institutoptique.fr>
"""
import numpy as np
from matplotlib import pyplot as plt

# MCP4132 - 503
Rw = 75     # Ohms - Wiper resistor
Rab = 50e3  # Ohms - 503 version 
Nmax = 128  # 7 bits version

Rwb = np.arange(0, Rab+Rab/Nmax, Rab/Nmax) + Rw

# Display Rwb evolution
plt.figure()
plt.plot(Rwb, '.')
plt.ylabel('Resistor (Ohms)')
plt.xlabel('N (from 0 to 128)')
plt.grid()

## Voltage divider - Radiation board
# 3.3V --[Rwb]-OUT-[R1]-GND
R1 = 10e3
Vout = R1 / (R1 + Rwb) * 3.3
# Display Rwb evolution
plt.figure()
plt.plot(Vout, '.')
plt.ylabel('Vout (V)')
plt.xlabel('N (from 0 to 128)')
plt.grid()
plt.show()