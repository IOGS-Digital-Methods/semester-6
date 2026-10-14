import sys
sys.path.append("../_libs/")

import cv2
from image_lib import display_image, generate_histogram
from form_detection import *


# Parameters
dir_image_path = '../_data/'
DISP_RATIO = 0.6

file_path = dir_image_path+'forms_vi.png'
file_path2 = dir_image_path+'formes_blanc_30ms.png'
MIN_AREA = 1000
APPROX_FACTOR = 0.01


def main():
    # ---
    img_gray = cv2.imread(file_path2, cv2.IMREAD_GRAYSCALE)

    # --- Output image (color) ---
    img_out = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2BGR)

    # --- Contours detection ---
    contours, nb_contours = detect_contours(img_gray)
    print(f'Number of contours: {nb_contours}')

    img_out = display_contours(img_out, contours, MIN_AREA, APPROX_FACTOR, print_out=False)

    # Display
    img_gray_disp, _ = display_image(img_gray, disp_ratio=DISP_RATIO)
    img_out_disp_contour, _ = display_image(img_out, disp_ratio=DISP_RATIO)

    # --- Circle detection ---
    circles, nb_circles = detect_circles(img_gray)
    print(f'Number of circles {nb_circles}')

    img_out = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2BGR)
    img_out = display_circles(img_out, circles)
    img_out_disp_circle, _ = display_image(img_out, disp_ratio=DISP_RATIO)

    cv2.imshow("Initial image / GRAY", img_gray_disp)
    cv2.imshow("Output image / Contour", img_out_disp_contour)
    cv2.imshow("Output image / Circle", img_out_disp_circle)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

