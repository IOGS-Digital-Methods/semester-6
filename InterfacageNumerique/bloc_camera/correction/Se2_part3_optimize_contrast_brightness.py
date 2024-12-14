# -*- coding: utf-8 -*-
"""*Se2_part3_optimize_contrast_brightness.py* file.

This file contains a script to modify the contrast and the brightness of an image.

This file is attached to a 1st year of engineer training labwork in digital interface development.

For tutorials on image processing, see : https://iogs-lense-training.github.io/image-processing/

.. note:: LEnsE - Institut d'Optique - version 0.1

.. moduleauthor:: Julien VILLEMEJANE <julien.villemejane@institutoptique.fr>
.. creation:: 20/oct/2024
"""

import cv2
import numpy as np
from matplotlib import pyplot as plt
from images_manipulation import *


if __name__ == "__main__":
    
    # Open an image - Grayscale
    image_gray = cv2.imread('../../_images/robot.jpg', cv2.IMREAD_GRAYSCALE)
    
    alpha = 1.5
    beta = -50
    image_adjusted = cv2.convertScaleAbs(image_gray, alpha=alpha, beta=beta)

    # Display two images
    fig, ax = plt.subplots(nrows=2, ncols=1)
    # Plot data in each subplot
    ax[0].imshow(image_gray, cmap='gray')
    ax[0].set_title('Original Image')
    ax[1].imshow(image_adjusted, cmap='gray')
    ax[1].set_title('Adjusted Image')

    # Process and display histogram
    image_bits_depth = 8
    bins = np.linspace(0, 2 ** image_bits_depth, 2 ** image_bits_depth+1)
    bins_ori, data_ori = process_hist_from_array(image_gray, bins)
    bins_adj, data_adj = process_hist_from_array(image_adjusted, bins)

    # Display two histogram
    fig, ax = plt.subplots(nrows=2, ncols=1)
    # Plot data in each subplot
    ax[0].bar(bins_ori[:-1], data_ori, width=np.diff(bins),
            edgecolor='black', alpha=0.75, color='blue')
    ax[0].set_title('Original Image Histogram')
    ax[1].bar(bins_adj[:-1], data_adj, width=np.diff(bins),
            edgecolor='black', alpha=0.75, color='blue')
    ax[1].set_title('Adjusted Image Histogram')
    plt.show()