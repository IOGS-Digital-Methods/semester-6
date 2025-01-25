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
    # Open an image - GrayScale
    image_gray = cv2.imread('./images/image2.png', cv2.IMREAD_GRAYSCALE)

    # Creating kernels
    kernel_cross = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    kernel_2 = np.array([[0, 0, 0],[0, 1, 1],[0, 1, 0]], dtype=np.uint8)
    kernel_3 = np.array([[0, 0, 0],[1, 1, 1],[0, 0, 0]], dtype=np.uint8)

    # Erosion (morpho) on an image
    image_eroded_cross = cv2.erode(image_gray, kernel_cross)
    image_eroded_2 = cv2.erode(image_gray, kernel_2)
    image_eroded_3 = cv2.erode(image_gray, kernel_3)

    # Display all
    fig, ax = plt.subplots(nrows=1, ncols=3)
    # Plot data in each subplot
    ax[0].imshow(kernel_cross, cmap='gray')
    ax[0].set_title('Kernel')
    ax[1].imshow(image_gray, cmap='gray')
    ax[1].set_title('Original Image')
    ax[2].imshow(image_eroded_cross, cmap='gray')
    ax[2].set_title('Erosion Image')

    fig, ax = plt.subplots(nrows=1, ncols=3)
    # Plot data in each subplot
    ax[0].imshow(kernel_2, cmap='gray')
    ax[0].set_title('Kernel')
    ax[1].imshow(image_gray, cmap='gray')
    ax[1].set_title('Original Image')
    ax[2].imshow(image_eroded_2, cmap='gray')
    ax[2].set_title('Erosion Image')

    fig, ax = plt.subplots(nrows=1, ncols=3)
    # Plot data in each subplot
    ax[0].imshow(kernel_3, cmap='gray')
    ax[0].set_title('Kernel')
    ax[1].imshow(image_gray, cmap='gray')
    ax[1].set_title('Original Image')
    ax[2].imshow(image_eroded_3, cmap='gray')
    ax[2].set_title('Erosion Image')


    # Dilation (morpho) on an image
    kernel_dil_1 = np.array([[0, 0, 0],[0, 1, 0],[1, 0, 0]], dtype=np.uint8)
    image_dil_1 = cv2.dilate(image_gray, kernel_dil_1)
    kernel_dil_2 = np.array([[0, 1, 0],[0, 1, 1],[0, 1, 0]], dtype=np.uint8)
    image_dil_2 = cv2.dilate(image_gray, kernel_dil_2)

    fig, ax = plt.subplots(nrows=1, ncols=3)
    # Plot data in each subplot
    ax[0].imshow(kernel_dil_1, cmap='gray')
    ax[0].set_title('Kernel')
    ax[1].imshow(image_gray, cmap='gray')
    ax[1].set_title('Original Image')
    ax[2].imshow(image_dil_1, cmap='gray')
    ax[2].set_title('Dilation Image')


    fig, ax = plt.subplots(nrows=1, ncols=3)
    # Plot data in each subplot
    ax[0].imshow(kernel_dil_2, cmap='gray')
    ax[0].set_title('Kernel')
    ax[1].imshow(image_gray, cmap='gray')
    ax[1].set_title('Original Image')
    ax[2].imshow(image_dil_2, cmap='gray')
    ax[2].set_title('Dilation Image')

    plt.show()