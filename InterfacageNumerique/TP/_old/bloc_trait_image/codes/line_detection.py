# -*- coding: utf-8 -*-
"""*line_detection.py* file.

This file contains a script to open an image with OpenCV and to process line detection (horizontal) on an image.

This file is attached to a 1st year of engineer training labwork in digital interface development.

For tutorials on image processing, see : https://iogs-lense-training.github.io/image-processing/

.. note:: LEnsE - Institut d'Optique - version 0.1

.. moduleauthor:: Julien VILLEMEJANE <julien.villemejane@institutoptique.fr>
.. creation:: 22/nov/2024
"""

import cv2
import numpy as np

if __name__ == "__main__":
    # Open an image - Grayscale
    image_gray = cv2.imread('forms_opening_closing.png', cv2.IMREAD_GRAYSCALE)
    
    # Transform image in binary image
    (T, image_bw) = cv2.threshold(image_gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU) 
 
    # Create the kernel for horizontal lines detection
    hor_size = 20
    hor_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (hor_size, 1))
    
    # Apply erosion and dilation
    horizontal1 = cv2.erode(image_bw, hor_kernel)
    horizontal2 = cv2.dilate(horizontal1, hor_kernel)

  
    

    