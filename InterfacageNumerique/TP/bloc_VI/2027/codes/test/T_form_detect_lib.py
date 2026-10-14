"""T_form_detect_lib.py
Test of the form_detection library (OpenCV)
.. moduleauthor:: Julien VILLEMEJANE <julien.villemejane@institutoptique.fr>
"""
import sys
sys.path.append("../_libs/")

import cv2
from image_lib import display_image, generate_histogram
from form_detection import (detect_contours, display_contours,
                            detect_circles, display_circles)


# Parameters
dir_image_path = '../_data/'
DISP_RATIO = 0.6

file_path = dir_image_path+'forms_vi.png'
MIN_AREA = 100
APPROX_FACTOR = 0.01


img_gray = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
img_gray_disp, _ = display_image(img_gray, disp_ratio=DISP_RATIO)

img_out = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2BGR)

# Contour detection
contours, nb_contours = detect_contours(img_gray)
print(f'Number of contours: {nb_contours}')

img_out = display_contours(img_out, contours, MIN_AREA, APPROX_FACTOR)
img_out_disp_contour, _ = display_image(img_out, disp_ratio=DISP_RATIO)


img_out = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2BGR)

# Circle detection
circles_res, nb_circles = detect_circles(img_gray)
print(f'Number of circles: {nb_circles}')
img_out = display_circles(img_out, circles_res)

img_out_disp_circle, _ = display_image(img_out, disp_ratio=DISP_RATIO)

# Display
cv2.imshow("Initial image / GRAY", img_gray_disp)
cv2.imshow("Output image", img_out_disp_contour)
cv2.waitKey(0)

cv2.imshow("Output image", img_out_disp_circle)
cv2.waitKey(0)
cv2.destroyAllWindows()


