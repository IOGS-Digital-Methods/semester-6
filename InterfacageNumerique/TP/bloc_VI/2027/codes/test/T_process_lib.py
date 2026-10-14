"""T_process_lib.py
Test of the process_lib library (OpenCV)
.. moduleauthor:: Julien VILLEMEJANE <julien.villemejane@institutoptique.fr>
"""
import sys
sys.path.append("../_libs/")

import cv2
import numpy as np

from image_lib import display_image, generate_histogram
import process_lib as pcv

# Parameters
img_dir_path = '../_data/'
DISP_RATIO = 0.6

img_gray = cv2.imread(img_dir_path+'forms_vi.png', cv2.IMREAD_GRAYSCALE)
img_gray_disp, _ = display_image(img_gray, disp_ratio=DISP_RATIO)


# Canny process
image_canny = pcv.canny(img_gray)
image_canny_disp, _ = display_image(image_canny, disp_ratio=DISP_RATIO)

image_invert = pcv.invert_image(img_gray)
image_invert_disp, _ = display_image(image_invert, disp_ratio=DISP_RATIO)

# Display
cv2.imshow("Initial image / GRAY", img_gray_disp)
cv2.imshow("Processed image - Canny / GRAY", image_canny_disp)
cv2.imshow("Processed image - INV / GRAY", image_invert_disp)
cv2.waitKey(0)
cv2.destroyAllWindows()
