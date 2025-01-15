# -*- coding: utf-8 -*-
"""*watershed_steps.py* file.

*watershed_steps* file contains code of Watershed segmentation method.
This code cannot be executed alone !

This file is attached to a 1st year of engineer training labwork in digital interface development.

.. note:: LEnsE - Institut d'Optique - version 0.1

.. moduleauthor:: Julien VILLEMEJANE <julien.villemejane@institutoptique.fr>
.. creation:: 15/jan/2025
"""

## STEP 3
# sure background area
sure_bg = cv2.dilate(opening, kernel, iterations=1)

# Finding sure foreground area
k_dist = 0.4
dist_transform = cv2.distanceTransform(opening, cv2.DIST_L1, 5)
ret, sure_fg = cv2.threshold(dist_transform, 
			k_dist * dist_transform.max(), 255, 0)

# Finding unknown region
sure_fg = np.uint8(sure_fg)
unknown = cv2.subtract(sure_bg, sure_fg)



## STEP 4
# Marker labelling
ret, markers = cv2.connectedComponents(sure_fg)
# Add one to all labels so that sure background is not 0, but 1
markers = markers + 1
# Now, mark the region of unknown with zero
markers[unknown == 255] = 0


## STEP 5
image_rgb2 = image_rgb.copy()
markers2 = cv2.watershed(image_rgb, markers)
image_rgb[markers2 == -1] = [255, 0, 0]