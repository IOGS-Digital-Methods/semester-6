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
    crop_x, crop_y = 300, 200
    crop_w, crop_h = 200, 400

    # ---
    img_gray = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
    img_crop = img_gray[crop_y:crop_y+crop_h, crop_x:crop_x+crop_w]

    # --- Output image (color) ---
    img_out = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2BGR)
    cv2.rectangle(img_out, (crop_x, crop_y), (crop_x+crop_w, crop_y+crop_h), (0, 255, 0), 2)

    # Display
    img_gray_disp, _ = display_image(img_out, disp_ratio=DISP_RATIO)

    cv2.imshow("Initial image / GRAY", img_gray_disp)
    cv2.imshow("Crop / GRAY", img_crop)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main2()
