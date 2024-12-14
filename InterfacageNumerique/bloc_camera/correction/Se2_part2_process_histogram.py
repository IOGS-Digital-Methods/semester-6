# -*- coding: utf-8 -*-
"""*Se1_part2_process_histogram.py* file.

This file contains a script to open an image with OpenCV and generate a histogram of the image.

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
    # Display the image
    cv2.imshow('Grayscale image', image_gray)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    # Access image parameters
    print(f'Size of the image = {image_gray.shape}')
    print(f'Type of an element of the image = {image_gray.dtype}')
    
    # Process and display histogram
    image_bits_depth = 8
    bins = np.linspace(0, 2 ** image_bits_depth, 2 ** image_bits_depth+1)
    bins, data = process_hist_from_array(image_gray, bins)
    display_hist(image_gray, data, bins)
    