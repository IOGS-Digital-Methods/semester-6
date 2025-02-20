# -*- coding: utf-8 -*-
"""*noise_test2.py* file.

*noise_test2* file contains an example of noise generation in 2D (images processing).

Uniform distribution of noise.

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
uniform_noise = generate_uniform_noise_image(height, width, 10, 20)
plt.figure()
plt.imshow(uniform_noise, cmap='gray')
plt.show()

# Histogram 
bins = np.linspace(0, 25, 100)
bins, data = process_hist_from_array(uniform_noise, bins)
display_hist(uniform_noise, data[1:], bins[1:])
