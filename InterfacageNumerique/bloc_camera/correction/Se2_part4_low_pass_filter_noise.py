# -*- coding: utf-8 -*-
"""*Se2_part4_low_pass_filter_noise.py* file.

This file contains a script to apply a low-pass (gaussian) filter on an image.
Adding noise on images.

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
    image_noise = generate_gaussian_noise_image_percent(image_gray.shape[0], image_gray.shape[1],
                                                        100, 50, 20)
    image_noise = image_noise # + image_gray

    image_bits_depth = 8
    bins = np.linspace(0, 2 ** image_bits_depth, 2 ** image_bits_depth + 1)
    bins, data_hist = process_hist_from_array(image_noise, bins)
    #display_hist(image_noise, data_hist, bins)

    # Gaussian filter
    kernel_size = (45, 45)

    blurred_image_5_gauss = cv2.GaussianBlur(image_noise, kernel_size, 0)

    ### TF
    tf_orig = np.fft.fft2(image_noise)
    tf_blur = np.fft.fft2(blurred_image_5_gauss)
    tf_diff_log = np.log(0.1+np.abs(np.fft.fftshift(tf_orig)))-np.log(0.1+np.abs(np.fft.fftshift(tf_blur)))

    # Display all
    fig, ax = plt.subplots(nrows=2, ncols=3)
    # Plot data in each subplot
    ax[0,0].imshow(image_noise, cmap='gray')
    ax[0,0].set_title('Original Image')
    ax[0,1].imshow(blurred_image_5_gauss, cmap='gray')
    ax[0,1].set_title('Blurred Image')
    ax[0,2].imshow(image_noise-blurred_image_5_gauss, cmap='gray')
    ax[0,2].set_title('Difference')

    ax[1,0].imshow(np.log(0.1+np.abs(np.fft.fftshift(tf_orig))), cmap='gray')
    ax[1,0].set_title('Original Image / FFT')
    ax[1,1].imshow(np.log(0.1+np.abs(np.fft.fftshift(tf_blur))), cmap='gray')
    ax[1,1].set_title('Blurred Image / FFT')
    ax[1,2].imshow(tf_diff_log, cmap='gray')
    ax[1,2].set_title('Difference / FFT')
    plt.show()
