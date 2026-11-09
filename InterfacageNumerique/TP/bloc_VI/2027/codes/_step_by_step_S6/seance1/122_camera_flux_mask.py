"""camera_flux.py
Basler Camera video flux display (OpenCV)
.. moduleauthor:: Julien VILLEMEJANE <julien.villemejane@institutoptique.fr>
"""

import sys
sys.path.append("../_libs/")

import cv2
import numpy as np
from camera_lib import init_camera, convert_image, COLOR_MODE, EXPOSURE_TIME
from image_lib import display_image
from form_detection import detect_contours, display_contours, get_masks_contours

# Parameters
crop_x, crop_y = 300, 200
crop_w, crop_h = 200, 400

def main():
    # ---
    mode = 'z'

    camera = init_camera(expo=1000)
    print("Click on 'q' to leave the application - in OpenCV window")
    
    # --- Acquisition Loop ---
    while camera.camera_acquiring:
        # --- Get Image ---
        frame_raw = camera.get_image()
        # --- Image conversion ---
        frame8 = convert_image(frame_raw, COLOR_MODE)

        img_crop = frame8[crop_y:crop_y + crop_h, crop_x:crop_x + crop_w]
        
        # --- Image display ---
        image_disp, scale = display_image(frame8)
        cv2.rectangle(image_disp, (crop_x, crop_y), (crop_x + crop_w, crop_y + crop_h), (0, 255, 0), 2)
        cv2.imshow("Flux Basler a2A1920", image_disp)

        cv2.imshow("Flux Basler / CROP", img_crop)

        # --- Mode management ---
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            camera.camera_acquiring = False
            camera.close()
        elif key != 255:    # No key
            mode = key

    camera.close()
    cv2.destroyAllWindows()

def main2():
    # Parameters
    dir_image_path = '../_data/'
    DISP_RATIO = 0.6

    file_path = dir_image_path + 'forms_vi.png'
    file_path2 = dir_image_path + 'formes_bruit.png'
    MIN_AREA = 100
    APPROX_FACTOR = 0.01

    # ---
    img_gray = cv2.imread(file_path2, cv2.IMREAD_GRAYSCALE)
    img_bgr = cv2.imread(file_path2, cv2.IMREAD_UNCHANGED)

    # --- Optimization ?
    _, img_thresh = cv2.threshold(
        img_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    # --- Output image (color) ---
    img_out = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2BGR)

    # --- Contours detection ---
    contours, nb_contours = detect_contours(img_thresh)
    masks = get_masks_contours(contours, img_gray)

    # Display
    img_gray_disp, _ = display_image(img_bgr, disp_ratio=DISP_RATIO)
    img_out = display_contours(img_out, contours, MIN_AREA, APPROX_FACTOR)
    img_out_disp_contour, _ = display_image(img_out, disp_ratio=DISP_RATIO)
    mask_disp, _ = display_image(masks[0], disp_ratio=DISP_RATIO)

    mean_bgr = cv2.mean(img_bgr, mask=masks[0])[:3]
    print(f'mean_bgr: {mean_bgr}')

    cv2.imshow("Initial image / GRAY", img_gray_disp)
    cv2.imshow("Crop / GRAY", img_out_disp_contour)
    cv2.imshow("First Mask / GRAY", mask_disp)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main2()
