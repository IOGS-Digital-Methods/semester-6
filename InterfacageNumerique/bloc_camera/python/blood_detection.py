# -*- coding: utf-8 -*-
"""*blood_detection.py* file.

*blood_detection* file contains a script to detect blood on
hand images.
6 images are necessary :
 - 3 "white background" images in R, G and B lighting
 - 3 "hand" images in R, G and B lighting

This file is attached to a 1st year of engineer training labwork in digital interface development.

.. note:: LEnsE - Institut d'Optique - version 0.1

.. moduleauthor:: Julien VILLEMEJANE <julien.villemejane@institutoptique.fr>
.. creation:: 08/jan/2025

Based on an idea of Julien MOREAU <julien.moreau@institutoptique.fr>
"""

import cv2
import numpy as np
from matplotlib import pyplot as plt

grayscale_image = cv2.imread('bricks2.jpg', cv2.IMREAD_GRAYSCALE)
print(grayscale_image.shape)

plt.imshow(grayscale_image, cmap='gray')
plt.show()