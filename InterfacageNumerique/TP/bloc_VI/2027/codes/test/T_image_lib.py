"""T_image_lib.py
Test of the image_lib library (OpenCV)
.. moduleauthor:: Julien VILLEMEJANE <julien.villemejane@institutoptique.fr>
"""
import sys
sys.path.append("../_libs/")

import cv2
import numpy as np

from image_lib import display_image, generate_histogram

# Parameters
img_dir_path = '../_data/'

img_gray = cv2.imread(img_dir_path+'noise_vi.png', cv2.IMREAD_GRAYSCALE)
img_rgb = cv2.imread(img_dir_path+'formes_bruit.png', cv2.IMREAD_UNCHANGED)
img_gray_disp, _ = display_image(img_gray, disp_ratio=0.3)
img_rgb_disp, _ = display_image(img_rgb, disp_ratio=0.3)

# Histogram process
hist_gray = generate_histogram(img_gray)
hist_rgb = generate_histogram(img_rgb)

# Display
cv2.imshow("Initial image / GRAY", img_gray_disp)
cv2.imshow("Histogram of Gray Image", hist_gray)
cv2.waitKey(0)
cv2.imshow("Initial image / BGR", img_rgb_disp)
cv2.imshow("Histogram of BGR Image", hist_rgb)
cv2.waitKey(0)
cv2.destroyAllWindows()
