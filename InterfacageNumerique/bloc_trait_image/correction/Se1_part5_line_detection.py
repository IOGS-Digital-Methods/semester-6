# -*- coding: utf-8 -*-
"""*Se1_part5_line_detection.py* file.

This file contains a script to open an image with OpenCV and to process line detection (vertical or horizontal) on an image.

This file is attached to a 1st year of engineer training labwork in digital interface development.

For tutorials on image processing, see : https://iogs-lense-training.github.io/image-processing/

.. note:: LEnsE - Institut d'Optique - version 0.1

.. moduleauthor:: Julien VILLEMEJANE <julien.villemejane@institutoptique.fr>
.. creation:: 22/nov/2024
"""

import cv2
import numpy as np
from matplotlib import pyplot as plt


if __name__ == "__main__":
    # Open an image - Grayscale
    image_gray = cv2.imread('../../_images/forms_opening_closing.png', cv2.IMREAD_GRAYSCALE)
    
    #Display the image
    plt.figure()
    plt.imshow(image_gray, cmap='gray')
    plt.title('Original Image')
    
    # Transform image in binary image
    (T, image_bw) = cv2.threshold(image_gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    plt.figure()
    plt.imshow(image_bw, cmap='gray')
    plt.title('Binary Image') 
 
    # Create the kernel for horizontal lines detection
    hor_size = 10
    hor_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (hor_size, 1))
    
    # Apply erosion and dilation
    horizontal1 = cv2.erode(image_bw, hor_kernel)
    horizontal2 = cv2.dilate(horizontal1, hor_kernel)
    
    plt.figure()
    plt.imshow(horizontal1, cmap='gray')
    plt.title('Image after erosion')
    
    plt.figure()
    plt.imshow(horizontal2, cmap='gray')
    plt.title('Image after erosion and dilation')
    
    plt.show()
  
    

    