# -*- coding: utf-8 -*-
"""*Se2_part5_high_pass_filter_roberts.py* file.

This file contains a script to apply a high-pass (roberts operator) filter on an image.

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
    image_gray = cv2.imread('../../_images/bricks2.jpg', cv2.IMREAD_GRAYSCALE)

    # Roberts kernels
    kernel_x = np.array([[1, 0], [0, -1]], dtype=np.float32)
    kernel_y = np.array([[0, 1], [-1, 0]], dtype=np.float32)

    # Process image filtering
    gradient_x = cv2.filter2D(image_gray, -1, kernel_x)
    gradient_y = cv2.filter2D(image_gray, -1, kernel_y)
    gradient = gradient_y + gradient_x

    # Process amplitude of the gradient
    gradient_magnitude = np.sqrt(np.square(gradient_x) + np.square(gradient_y))
    gradient_magnitude = np.uint8(gradient_magnitude / gradient_magnitude.max() * 255)  # Normalization

    ### TF
    tf_orig = np.fft.fft2(image_gray)
    tf_blur = np.fft.fft2(gradient)
    tf_diff_log = np.log(0.1+np.abs(np.fft.fftshift(tf_orig)))-np.log(0.1+np.abs(np.fft.fftshift(tf_blur)))

    # Display all
    fig, ax = plt.subplots(nrows=2, ncols=3)
    # Plot data in each subplot
    ax[0,0].imshow(image_gray, cmap='gray')
    ax[0,0].set_title('Original Image')
    ax[0,1].imshow(gradient, cmap='gray')
    ax[0,1].set_title('Roberts filtered Image')
    ax[0,2].imshow(gradient_magnitude, cmap='gray')
    ax[0,2].set_title('Gradient magnitude')

    ax[1,0].imshow(np.log(0.1+np.abs(np.fft.fftshift(tf_orig))), cmap='gray')
    ax[1,0].set_title('Original Image / FFT')
    ax[1,1].imshow(np.log(0.1+np.abs(np.fft.fftshift(tf_blur))), cmap='gray')
    ax[1,1].set_title('Blurred Image / FFT')
    ax[1,2].imshow(tf_diff_log, cmap='gray')
    ax[1,2].set_title('Difference / FFT')
    plt.show()