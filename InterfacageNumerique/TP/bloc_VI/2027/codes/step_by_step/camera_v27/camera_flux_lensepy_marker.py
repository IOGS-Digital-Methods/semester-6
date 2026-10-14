"""camera_flux.py
Basler Camera video flux display (OpenCV)
.. moduleauthor:: Julien VILLEMEJANE <julien.villemejane@institutoptique.fr>
"""

import sys
sys.path.append("../../_libs/")

import cv2
import numpy as np
from camera_lib import init_camera, convert_image, COLOR_MODE, EXPOSURE_TIME
from image_lib import display_image
import process_lib as pcv
from marker_finding import *

x0, y0, x1, y1 = 500, 200, 1200, 800
xx_delta = 74
yy_delta = 74
dx1 = 11
dy1 = 11
dx2 = 21
dy2 = 21

dir_path = '../../_data_marker/'
ref_path = dir_path+'mire_rep_V2_1.png'
image_ref1 = cv2.imread(ref_path, cv2.IMREAD_GRAYSCALE)
ref_path = dir_path+'mire_rep_V2_2.png'
image_ref2 = cv2.imread(ref_path, cv2.IMREAD_GRAYSCALE)
ref_path = dir_path+'mire_rep_V2_3.png'
image_ref3 = cv2.imread(ref_path, cv2.IMREAD_GRAYSCALE)



def main():
	# ---
    mode = 'z'

    camera = init_camera(expo=1000)
    print("Appuyez sur 'q' pour quitter - dans la fenêtre d'OpenCV")
    
    # --- Boucle d'acquisition ---
    while camera.camera_acquiring:
        # --- Get Image ---
        frame_raw = camera.get_image()
        # --- Image conversion ---
        frame8 = convert_image(frame_raw, COLOR_MODE)
		
		# --- ROI ---
        frame8 = frame8[y0:y1, x0:x1, :]
        frame8_gray = cv2.cvtColor(frame8, cv2.COLOR_RGB2GRAY)

        # --- Processing ---
        if mode == ord('a'):    # Canny
            final_output = cv2.Canny(frame8, 100, 150)
        elif mode == ord('g'):  # Gaussian Blur
            final_output = cv2.GaussianBlur(frame8, (15, 15), 4)
        elif mode == ord('i'):  # Inverse image
            final_output = 255 - frame8
        elif mode == ord('c'):  # Inverse image
            final_output = frame8[:, :, [2, 1, 0]]
        else:
            final_output = frame8

        # --- Marker Detection ---
        matches1 = find_all_matches_multiscale(frame8_gray, image_ref1)
        matches2 = find_all_matches_multiscale(frame8_gray, image_ref2)
        matches3 = find_all_matches_multiscale(frame8_gray, image_ref3)
		
        # --- Image display ---
        image_disp, scale = display_image(final_output)
        for m in matches1:
            r_x1 = m['x']
            r_y1 = m['y']
            r_x1_s = int(m['x']*scale)
            r_y1_s = int(m['y']*scale)
            cv2.circle(image_disp, (r_x1_s, r_y1_s), 5, (0, 0, 255), -1)
        for m in matches2:
            r_x2 = m['x']
            r_y2 = m['y']
            r_x2_s = int(m['x']*scale)
            r_y2_s = int(m['y']*scale)
            cv2.circle(image_disp, (r_x2_s, r_y2_s), 5, (0, 255, 255), -1)
        for m in matches3:
            r_x3 = m['x']
            r_y3 = m['y']
            r_x3_s = int(m['x']*scale)
            r_y3_s = int(m['y']*scale)
            cv2.circle(image_disp, (r_x3_s, r_y3_s), 5, (0, 255, 0), -1)
        cv2.putText(image_disp, f'Sc={scale}', (10, 15), 
				cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
		
		# --- Grid ---
        scale_grid_x = (r_x2 - r_x1) / xx_delta
        scale_grid_y = (r_y3 - r_y1) / yy_delta
        x_c1 = int((r_x1 + ((dx1 + 0*dx2) * scale_grid_x))*scale)
        y_c1 = int((r_y1 + ((dy1 + 0*dy2) * scale_grid_y))*scale)
        x_c2 = int((r_x1 + ((dx1 + 1*dx2) * scale_grid_x))*scale)
        y_c2 = int((r_y1 + ((dy1 + 1*dy2) * scale_grid_y))*scale)
        x_c3 = int((r_x1 + ((dx1 + 2*dx2) * scale_grid_x))*scale)
        y_c3 = int((r_y1 + ((dy1 + 2*dy2) * scale_grid_y))*scale)
        x_c4 = int((r_x1 + ((dx1 + 3*dx2) * scale_grid_x))*scale)
        y_c4 = int((r_y1 + ((dy1 + 3*dy2) * scale_grid_y))*scale)
        cv2.circle(image_disp, (x_c1, y_c1), 10, (255, 0, 0), -1)
        cv2.rectangle(image_disp, (x_c1, y_c1), (x_c2, y_c2), (255, 0, 0), 2)
        cv2.rectangle(image_disp, (x_c1, y_c2), (x_c2, y_c3), (255, 0, 0), 2)
        cv2.rectangle(image_disp, (x_c1, y_c3), (x_c2, y_c4), (255, 0, 0), 2)
        
        cv2.rectangle(image_disp, (x_c2, y_c1), (x_c3, y_c2), (255, 0, 0), 2)
        cv2.rectangle(image_disp, (x_c2, y_c2), (x_c3, y_c3), (255, 0, 0), 2)
        cv2.rectangle(image_disp, (x_c2, y_c3), (x_c3, y_c4), (255, 0, 0), 2)
        
        cv2.rectangle(image_disp, (x_c3, y_c1), (x_c4, y_c2), (255, 0, 0), 2)
        cv2.rectangle(image_disp, (x_c3, y_c2), (x_c4, y_c3), (255, 0, 0), 2)
        cv2.rectangle(image_disp, (x_c3, y_c3), (x_c4, y_c4), (255, 0, 0), 2)
        
        # --- Display ---
        cv2.imshow("Flux Basler a2A1920", image_disp)
        
        # --- Crop zone 1 ---
        zone1 = frame8[int(y_c1/scale):int(y_c2/scale), 
                int(x_c1/scale):int(x_c2/scale), :]
        cv2.imshow("Zone 1 - Grid", zone1)
        # --- Crop zone 2 ---
        zone2 = frame8[int(y_c2/scale):int(y_c3/scale), 
                int(x_c1/scale):int(x_c2/scale), :]
        cv2.imshow("Zone 2 - Grid", zone2)
		
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
