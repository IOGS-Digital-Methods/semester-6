# -*- coding: utf-8 -*-
"""*display_graph.py* file.

*display_graph* file contains an example for displaying images in a 1 x 3 subplots.
This code cannot be executed alone !

This file is attached to a 1st year of engineer training labwork in digital interface development.

.. note:: LEnsE - Institut d'Optique - version 0.1

.. moduleauthor:: Julien VILLEMEJANE <julien.villemejane@institutoptique.fr>
.. creation:: 15/jan/2025
"""

from matplotlib import pyplot as plt

fig, ax = plt.subplots(nrows=1, ncols=3)    
ax[0].imshow(image_data_1, cmap='gray')
ax[0].set_title('Title Image 1')  
ax[1].imshow(image_data_2, cmap='gray')
ax[1].set_title('Title Image 2')
ax[2].imshow(image_data_3, cmap='gray')
ax[2].set_title('Title Image 3')