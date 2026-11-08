"""141_colorspace.py
YUV colorspace
.. moduleauthor:: Julien VILLEMEJANE <julien.villemejane@institutoptique.fr>
"""
import cv2
import numpy as np
from matplotlib import pyplot as plt

# Parameters
dir_image_path = '../_data/'

image_rgb = cv2.imread(dir_image_path+'couleurs_4.png', cv2.IMREAD_UNCHANGED)
image_rgb = cv2.cvtColor(image_rgb, cv2.COLOR_BGR2RGB)

image_gray = cv2.imread(dir_image_path+'couleurs_4.png', cv2.IMREAD_GRAYSCALE)

# RGB to Gray
image_gray_mean = (image_rgb[:,:,0]/3 + image_rgb[:,:,1]/3 + image_rgb[:,:,2]/3).astype(np.uint8)

plt.figure()
plt.imshow(image_rgb)
plt.figure()
plt.imshow(image_gray, cmap='gray')
plt.figure()
plt.imshow(image_gray_mean, cmap='gray')

plt.show()
