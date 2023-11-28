#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IeTI / Semestre 6 / Institut d'Optique

Control library

Created on 28/nov/2023

@author: LEnsE / IOGS / Palaiseau
@author: Julien Villemejane
"""

import control
import numpy as np
import matplotlib.pyplot as plt

omega = np.logspace(-2, 6, 101)

#%% System A
H0 = 10
w0 = 1000
numA = np.array([H0])
denA = np.array([1/w0, 1])
sys_A = control.tf(numA, denA)

Gmag_A, Gphase_A, Gomega = control.bode_plot(sys_A, omega=omega, plot=False)

#%% System B
H1 = 1
numB = np.array([H1])
denB = np.array([1])
sys_B = control.tf(numB, denB)

Gmag_B, Gphase_B, Gomega = control.bode_plot(sys_B, omega=omega, plot=False)

#%% Correction
K = 10
num_corr = [K]
den_corr = [1]
sys_corr = control.tf(num_corr, den_corr)
sys_A = control.series(sys_A, sys_corr)

#%% System AB
sys_C = control.feedback(sys_A, sys_B)
Gmag_C, Gphase_C, Gomega = control.bode_plot(sys_C, omega=omega, plot=False)

#%% Display 
fig, axs = plt.subplots(2, 1)
fig.suptitle('Frequency Response')
axs[0].set_ylabel('Magnitude (dB)')
axs[0].set_xscale('log')
axs[0].grid(which="major", linewidth=1.0)
axs[0].grid(which="minor", linewidth=0.2)
axs[0].minorticks_on()

axs[0].plot(Gomega, 20 * np.log10(Gmag_A), label="System A")
axs[0].plot(Gomega, 20 * np.log10(Gmag_B), label="System B")
axs[0].plot(Gomega, 20 * np.log10(Gmag_C), label="System C")

axs[0].legend()


axs[1].set_ylabel('Phase (rd)')
axs[1].set_xlabel('Pulsation (rd/s)')
axs[1].set_xscale('log')
axs[1].grid(which="major", linewidth=1.0)
axs[1].grid(which="minor", linewidth=0.2)
axs[1].minorticks_on()

axs[1].plot(Gomega, Gphase_A)
axs[1].plot(Gomega, Gphase_B)
axs[1].plot(Gomega, Gphase_C)
plt.show()