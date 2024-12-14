#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SupOpNumTools / Institut d'Optique

2D numerical functions

Created on 24/Apr/2023

@author: LEnsE / IOGS / Palaiseau
@author: Julien Villemejane
"""



def generate_sine(xx, yy, freq=1, alpha=0):
    """
    Generates a 2D sine waveform for meshgrid

    Parameters
    ----------
    xx : int
        x values of the 2D meshgrid.
    yy : int
        y values of the 2D meshgrid.
    freq : real
        frequency of the sine waveform
    alpha : real
        angle of the sine waveform

    Returns
    -------
    2-dimension vector - double
        Array of values of the sine waveform 
        taken for xx,yy point of the meshgrid.

    """
    return (1+np.sin(freq*(xx*np.sin(alpha)+yy*np.cos(alpha))))/2

def generate_square(xx, yy, freq=1, alpha=0):
    """
    Generates a 2D square waveform for meshgrid

    Parameters
    ----------
    xx : int
        x values of the 2D meshgrid.
    yy : int
        y values of the 2D meshgrid.
    freq : real
        frequency of the square waveform
    alpha : real
        angle of the square waveform

    Returns
    -------
    2-dimension vector - double
        Array of values of the square waveform 
        taken for xx,yy point of the meshgrid.

    """
    image = 255*(1+np.sin(freq*(xx*np.sin(alpha)+yy*np.cos(alpha))))/2
    th, im_th = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY)
    print(th)
    return im_th
    

if __name__ == "__main__":
    import numpy as np
    from matplotlib import pyplot as plt
    # meshgrid
    x = np.linspace(0,499,500)
    y = np.linspace(0,349,350)
    xv, yv = np.meshgrid(x, y)
    # generate trame
    image_sin = generate_sine(xv, yv, freq=1/5, alpha = 71/180.0)
    plt.figure()
    plt.imshow(image_sin)   
    
    # FFT 2D
    image_sin_tf = np.fft.fft(image_sin)
    plt.figure()
    plt.imshow(np.fft.fftshift(np.log(np.abs(image_sin_tf))))
    plt.show()
    
    