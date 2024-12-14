# -*- coding: utf-8 -*-
"""*Se1_part1_ouvrir_image.py* file.

This file contains a script to open an image with OpenCV.

This file is attached to a 1st year of engineer training labwork in digital interface development.

For tutorials on image processing, see : https://iogs-lense-training.github.io/image-processing/

.. note:: LEnsE - Institut d'Optique - version 0.1

.. moduleauthor:: Julien VILLEMEJANE <julien.villemejane@institutoptique.fr>
.. creation:: 20/oct/2024
"""

import cv2
import numpy as np


if __name__ == "__main__":
    # Open an image - RGB
    image_RGB = cv2.imread('../../_images/robot.jpg')
    # Display the image
    cv2.imshow('RGB image', image_RGB)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    # Access image parameters
    print(f'Size of the image = {image_RGB.shape}')
    print(f'Type of an element of the image = {image_RGB.dtype}')
    
    # Open an image - Grayscale
    image_gray = cv2.imread('../../_images/robot.jpg', cv2.IMREAD_GRAYSCALE)
    # Display the image
    cv2.imshow('Grayscale image', image_gray)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    # Access image parameters
    print(f'Size of the image = {image_gray.shape}')
    print(f'Type of an element of the image = {image_gray.dtype}')
    