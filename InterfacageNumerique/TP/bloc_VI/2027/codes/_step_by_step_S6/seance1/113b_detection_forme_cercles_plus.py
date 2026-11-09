import sys
sys.path.append("../_libs/")

import cv2
from image_lib import display_image, generate_histogram
from form_detection import *


# Parameters
dir_image_path = '../_data/'
DISP_RATIO = 0.6
N_SIZE = 3

file_path = dir_image_path+'forms_vi.png'
file_path2 = dir_image_path+'formes_blanc_30ms.png'


def main():
    # ---
    img_gray = cv2.imread(file_path2, cv2.IMREAD_GRAYSCALE)
    img_blur = cv2.GaussianBlur(img_gray, (N_SIZE, N_SIZE), 2)

    # Display
    img_gray_disp, _ = display_image(img_gray, disp_ratio=DISP_RATIO)

    # --- Circle detection ---
    circles, nb_circles = detect_circles(img_blur)
    print(f'Number of circles {nb_circles}')

    img_out = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2BGR)
    img_out = display_circles(img_out, circles)
    img_out_disp_circle, _ = display_image(img_out, disp_ratio=DISP_RATIO)

    cv2.imshow("Initial image / GRAY", img_gray_disp)
    cv2.imshow("Output image / Circle (Blur)", img_out_disp_circle)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

