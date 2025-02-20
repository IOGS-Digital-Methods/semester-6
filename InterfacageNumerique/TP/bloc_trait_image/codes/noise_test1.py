# -*- coding: utf-8 -*-
"""*noise_test1.py* file.

*noise_test1* file contains an example of noise generation in 2D (images processing).

Gaussian distribution of noise.

This file is attached to a 1st year of engineer training labwork in digital interface development.

.. note:: LEnsE - Institut d'Optique - version 0.1

.. moduleauthor:: Julien VILLEMEJANE <julien.villemejane@institutoptique.fr>
.. creation:: 22/nov/2024
"""

from images_manipulation import *
from matplotlib import pyplot as plt

height = 200
width = 300
# Gaussian Noise
gauss_noise = generate_gaussian_noise_image(height, width)
plt.figure()
plt.imshow(gauss_noise, cmap='gray')
plt.show()

# Histogram 
bins = np.linspace(-5, 5, 20)
bins, data = process_hist_from_array(gauss_noise, bins)
display_hist(gauss_noise, data[1:], bins[1:])
