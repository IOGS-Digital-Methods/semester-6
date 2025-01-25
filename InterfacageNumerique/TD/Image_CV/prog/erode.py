# -*- coding: utf-8 -*-
"""*erode.py* file.

This file contains a script to open images in Grayscale and 
to process erosion effects.

This file is attached to a 1st year of engineer training labwork 
in digital interface development.

.. note:: LEnsE - Institut d'Optique - version 0.1

.. moduleauthor:: Julien VILLEMEJANE <julien.villemejane@institutoptique.fr>
.. creation:: 25/jan/2025
"""

import cv2
import numpy as np
from matplotlib import pyplot as plt

if __name__ == "__main__":
    file_name = input('Name of the file : ')
    # Open an image - GrayScale
    image_gray = cv2.imread('./images/'+file_name+'.png', cv2.IMREAD_GRAYSCALE)

    # Creating kernels
    kernel_cross = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))

    # Erosion (morpho) on an image
    image_eroded_cross = cv2.erode(image_gray, kernel_cross)
    # Dilation (morpho) on an image
    image_dilated_cross = cv2.dilate(image_gray, kernel_cross)
    
    
    # Display all
    fig, ax = plt.subplots(nrows=1, ncols=4)
    # Plot data in each subplot
    ax[0].imshow(kernel_cross, cmap='gray')
    ax[0].set_title('Kernel')
    ax[1].imshow(image_gray, cmap='gray')
    ax[1].set_title('Original Image')
    ax[2].imshow(image_eroded_cross, cmap='gray')
    ax[2].set_title('Eroded Image')
    ax[3].imshow(image_dilated_cross, cmap='gray')
    ax[3].set_title('Dilated Image')


    plt.show()