# -*- coding: utf-8 -*-
"""*Se2_part4_low_pass_filter.py* file.

This file contains a script to apply a low-pass (gaussian) filter on an image.

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

    # Display the image
    '''
    plt.figure()
    plt.imshow(image_gray, cmap='gray')
    plt.show()
    '''

    # Gaussian filter
    kernel_size = (15, 15)

    blurred_image_5_gauss = cv2.GaussianBlur(image_gray, kernel_size, 0)

    # Display two images
    '''
    fig, ax = plt.subplots(nrows=1, ncols=2)
    # Plot data in each subplot
    ax[0].imshow(image_gray, cmap='gray')
    ax[0].set_title('Original Image')
    ax[1].imshow(blurred_image_5_gauss, cmap='gray')
    ax[1].set_title('Blurred Image')
    plt.show()
    '''

    ### TF
    tf_orig = np.fft.fft2(image_gray)
    tf_blur = np.fft.fft2(blurred_image_5_gauss)
    tf_diff_log = np.log(0.1+np.abs(np.fft.fftshift(tf_orig)))-np.log(0.1+np.abs(np.fft.fftshift(tf_blur)))

    # Display TF
    '''
    fig, ax = plt.subplots(nrows=1, ncols=3)
    # Plot data in each subplot
    ax[0].imshow(np.log(0.1+np.abs(np.fft.fftshift(tf_orig))), cmap='gray')
    ax[0].set_title('Original Image / FFT')
    ax[1].imshow(np.log(0.1+np.abs(np.fft.fftshift(tf_blur))), cmap='gray')
    ax[1].set_title('Blurred Image / FFT')
    ax[2].imshow(tf_diff_log, cmap='gray')
    ax[2].set_title('Difference / FFT')
    plt.show()
    '''

    # Display all
    fig, ax = plt.subplots(nrows=2, ncols=3)
    # Plot data in each subplot
    ax[0,0].imshow(image_gray, cmap='gray')
    ax[0,0].set_title('Original Image')
    ax[0,1].imshow(blurred_image_5_gauss, cmap='gray')
    ax[0,1].set_title('Blurred Image')
    ax[0,2].imshow(image_gray-blurred_image_5_gauss, cmap='gray')
    ax[0,2].set_title('Difference')

    ax[1,0].imshow(np.log(0.1+np.abs(np.fft.fftshift(tf_orig))), cmap='gray')
    ax[1,0].set_title('Original Image / FFT')
    ax[1,1].imshow(np.log(0.1+np.abs(np.fft.fftshift(tf_blur))), cmap='gray')
    ax[1,1].set_title('Blurred Image / FFT')
    ax[1,2].imshow(tf_diff_log, cmap='gray')
    ax[1,2].set_title('Difference / FFT')
    plt.show()

    compare_blur_fft('../../_images/bricks2.jpg')