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
import process_lib as pcv

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

        # --- Processing ---
        if mode == ord('a'):    # Canny
            final_output = pcv.canny(frame8)
        elif mode == ord('g'):  # Gaussian Blur
            final_output = cv2.GaussianBlur(frame8, (15, 15), 4)
        elif mode == ord('i'):  # Inverse image
            final_output = pcv.invert_image(frame8)
        elif mode == ord('c'):  # Swap channels
            if frame8.ndim == 3:
                final_output = frame8[:, :, [2, 1, 0]]
            else:
                final_output = frame8
        else:
            final_output = frame8
        
        # --- Image display ---
        image_disp, scale = display_image(final_output)
        cv2.imshow("Flux Basler a2A1920", image_disp)

        # --- Mode management ---
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            camera.camera_acquiring = False
            camera.close()
        elif key != 255:    # No key
            mode = key

    camera.close()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
