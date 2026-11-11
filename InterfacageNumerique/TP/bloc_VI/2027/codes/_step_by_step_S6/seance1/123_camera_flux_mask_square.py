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
from form_detection import (
	detect_contours, display_contours_dict, 
	get_masks_contours_dict, detect_shape, sort_square
)

# Parameters
crop_x, crop_y = 300, 200
crop_w, crop_h = 500, 600


def main():
	# ---
	mode = 'z'
	MIN_AREA = 1000
	APPROX_FACTOR = 0.01

	camera = init_camera(expo=2000)
	print("Click on 'q' to leave the application - in OpenCV window")

	# --- Acquisition Loop ---
	while camera.camera_acquiring:
		# --- Get Image ---
		frame_raw = camera.get_image()
		# --- Image conversion ---
		frame8 = convert_image(frame_raw, COLOR_MODE)

		img_crop = frame8[crop_y:crop_y + crop_h, crop_x:crop_x + crop_w]
		img_crop_gray = cv2.cvtColor(img_crop, cv2.COLOR_BGR2GRAY)
		
		# --- Optimization ?
		_, img_thresh = cv2.threshold(
			img_crop_gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
		)

		cv2.rectangle(frame8, (crop_x, crop_y), (crop_x + crop_w, crop_y + crop_h), (0, 255, 0), 2)

		# --- Image display ---
		image_disp, scale = display_image(frame8)

		# --- Contours detection ---
		contours, nb_contours = detect_contours(img_thresh)
		new_contours = sort_square(contours, min_area=MIN_AREA)
		masks = get_masks_contours_dict(new_contours, img_crop_gray)
		print(len(masks))

		# Display
		img_out = display_contours_dict(img_crop, new_contours)

		if(len(masks) >= 1):
			mean_bgr = cv2.mean(img_crop, mask=masks[0])[:3]
			print(f'mean_bgr: {mean_bgr}')
			cv2.imshow("Mask", masks[0])
		elif cv2.getWindowProperty("Mask", cv2.WND_PROP_VISIBLE) > 0:
			cv2.destroyWindow("Mask")

		cv2.imshow("CROP", img_out)

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
