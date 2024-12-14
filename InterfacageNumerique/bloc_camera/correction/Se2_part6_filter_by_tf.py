# -*- coding: utf-8 -*-
"""*Se2_part6_filter_by_tf.py* file.

This file contains a script to apply a filter on an image by using the Fourier transform and a mask.

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

    ### TF
    tf_orig = np.fft.fft2(image_gray)
    tf_mask = circular_mask(100, np.fft.fftshift(tf_orig))#, inverted=True)

    # Final image
    image_final = np.real(np.fft.ifft2(np.fft.fftshift(tf_mask)))

    # Display all
    fig, ax = plt.subplots(nrows=2, ncols=2)
    # Plot data in each subplot
    ax[0,0].imshow(image_gray, cmap='gray')
    ax[0,0].set_title('Original Image')
    ax[0,1].imshow(image_final, cmap='gray')
    ax[0,1].set_title('Filtered Image')

    ax[1,0].imshow(np.log(0.1+np.abs(np.fft.fftshift(tf_orig))), cmap='gray')
    ax[1,0].set_title('Original Image / FFT')
    ax[1,1].imshow(np.log(0.1+np.abs(tf_mask)), cmap='gray')
    ax[1,1].set_title('Masked FFT')
    plt.show()