import sys
sys.path.append("../_libs/")

from camera_lib import init_camera, convert_image, COLOR_MODE, EXPOSURE_TIME
from image_lib import display_image, scale_image
from form_detection import detect_contours, display_contours
import process_lib as pcv
from marker_finding import *

x0, y0, x1, y1 = 500, 200, 1200, 800
x0, y0, x1, y1 = 0, 0, 1900, 1200
xx_delta = 74
yy_delta = 74
dx1 = 11
dy1 = 11
dx2 = 21
dy2 = 21

dir_path = '../_data_marker/'
ref_path = dir_path + 'mire_rep.png'
image_ref1 = cv2.imread(ref_path, cv2.IMREAD_GRAYSCALE)
image_ref1 = scale_image(image_ref1, 1.83)

# GRID DEFINITION
xx_delta = 74
yy_delta = 74
dx1 = 11
dy1 = 11
dx2 = 21
dy2 = 21

# Display grid
def display_grid(image, points, min_distance=20, disp=True):

	selected = []
	for x, y, score in points:
		too_close = False
		for sx, sy, _ in selected:
			distance = np.sqrt((x - sx)**2 + (y - sy)**2)
			if distance < min_distance:
				too_close = True
				break
		if not too_close:
			selected.append((x, y, score))
	
	if len(selected) == 3:
		r_x1 = min(selected[0][0], selected[1][0], selected[2][0])
		r_x2 = max(selected[0][0], selected[1][0], selected[2][0])
		r_y1 = min(selected[0][1], selected[1][1], selected[2][1])
		r_y3 = max(selected[0][1], selected[1][1], selected[2][1])
		# --- Grid ---
		scale_grid_x = (r_x2 - r_x1) / xx_delta
		scale_grid_y = (r_y3 - r_y1) / yy_delta
		x_c1 = int((r_x1 + ((dx1 + 0*dx2) * scale_grid_x)))
		y_c1 = int((r_y1 + ((dy1 + 0*dy2) * scale_grid_y)))
		x_c2 = int((r_x1 + ((dx1 + 1*dx2) * scale_grid_x)))
		y_c2 = int((r_y1 + ((dy1 + 1*dy2) * scale_grid_y)))
		x_c3 = int((r_x1 + ((dx1 + 2*dx2) * scale_grid_x)))
		y_c3 = int((r_y1 + ((dy1 + 2*dy2) * scale_grid_y)))
		x_c4 = int((r_x1 + ((dx1 + 3*dx2) * scale_grid_x)))
		y_c4 = int((r_y1 + ((dy1 + 3*dy2) * scale_grid_y)))
		if disp:
			cv2.circle(image, (x_c1, y_c1), 10, (255, 0, 0), -1)
			cv2.rectangle(image, (x_c1, y_c1), (x_c2, y_c2), (255, 0, 0), 2)
			cv2.rectangle(image, (x_c1, y_c2), (x_c2, y_c3), (255, 0, 0), 2)
			cv2.rectangle(image, (x_c1, y_c3), (x_c2, y_c4), (255, 0, 0), 2)

			cv2.rectangle(image, (x_c2, y_c1), (x_c3, y_c2), (255, 0, 0), 2)
			cv2.rectangle(image, (x_c2, y_c2), (x_c3, y_c3), (255, 0, 0), 2)
			cv2.rectangle(image, (x_c2, y_c3), (x_c3, y_c4), (255, 0, 0), 2)

			cv2.rectangle(image, (x_c3, y_c1), (x_c4, y_c2), (255, 0, 0), 2)
			cv2.rectangle(image, (x_c3, y_c2), (x_c4, y_c3), (255, 0, 0), 2)
			cv2.rectangle(image, (x_c3, y_c3), (x_c4, y_c4), (255, 0, 0), 2)
		return (x_c1, y_c1), (x_c2, y_c2), (x_c3, y_c3), (x_c4, y_c4)
	else:
		return None, None, None, None


def detect_zone(image, p1, p2, p3, p4, disp=True):
	MIN_AREA = 1000
	APPROX_FACTOR = 0.05
	PIXEL_CORRECTION = 20
	zone_1_1 = image[p1[1]+PIXEL_CORRECTION:p2[1]-PIXEL_CORRECTION, 
					p1[0]+PIXEL_CORRECTION:p2[0]-PIXEL_CORRECTION]
	zone_1_2 = image[p2[1]+PIXEL_CORRECTION:p3[1]-PIXEL_CORRECTION,
					p1[0]+PIXEL_CORRECTION:p2[0]-PIXEL_CORRECTION]
	zone_1_3 = image[p3[1]+PIXEL_CORRECTION:p4[1]-PIXEL_CORRECTION, 
					p1[0]+PIXEL_CORRECTION:p2[0]-PIXEL_CORRECTION]
	zone_2_1 = image[p1[1]+PIXEL_CORRECTION:p2[1]-PIXEL_CORRECTION, 
					p2[0]+PIXEL_CORRECTION:p3[0]-PIXEL_CORRECTION]
	zone_2_2 = image[p2[1]:p3[1], p2[0]:p3[0]]
	zone_2_3 = image[p3[1]:p4[1], p2[0]:p3[0]]
	zone_3_1 = image[p1[1]:p2[1], p3[0]:p4[0]]
	zone_3_2 = image[p2[1]:p3[1], p3[0]:p4[0]]
	zone_3_3 = image[p3[1]:p4[1], p3[0]:p4[0]]
	
	# Form Detection 
	_, img_thresh = cv2.threshold(
        zone_1_1, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
	)
	contours_op, nb_contours_op = detect_contours(img_thresh)
	img_1_1 = display_contours(zone_1_1, contours_op, MIN_AREA, APPROX_FACTOR)
	
	_, img_thresh = cv2.threshold(
        zone_1_3, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
	)
	contours_op, nb_contours_op = detect_contours(img_thresh)
	img_1_3 = display_contours(zone_1_3, contours_op, MIN_AREA, APPROX_FACTOR)

	_, img_thresh = cv2.threshold(
        zone_2_1, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
	)
	contours_op, nb_contours_op = detect_contours(img_thresh)
	img_2_1 = display_contours(zone_2_2, contours_op, MIN_AREA, APPROX_FACTOR)
	
	
	# Display	
	if disp:
		cv2.imshow("Zone 1/1", img_1_1)
		cv2.imshow("Zone 1/3", img_1_3)
		cv2.imshow("Zone 2/1", img_thresh)
		'''
		cv2.imshow("Zone 1/2", zone_1_2)
		cv2.imshow("Zone 1/3", zone_1_3)
		cv2.imshow("Zone 2/1", zone_2_1)
		cv2.imshow("Zone 2/2", zone_2_2)
		cv2.imshow("Zone 2/3", zone_2_3)
		cv2.imshow("Zone 3/1", zone_3_1)
		cv2.imshow("Zone 3/2", zone_3_2)
		cv2.imshow("Zone 3/3", zone_3_3)
		'''
	


def main():
	# ---
	mode = 'z'

	camera = init_camera(expo=4000)
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
		final_output = frame8

		# --- Marker Detection ---
		result = cv2.matchTemplate(frame8_gray, image_ref1, cv2.TM_CCOEFF_NORMED)
		print(f'Max Correlation = {np.max(result)}')
		# CORRELATION Threshold
		threshold = 0.89
		# Positions where corr > thresh
		ys, xs = np.where(result >= threshold)

		matches = [(x, y, result[y, x]) for x, y in zip(xs, ys)]

		# --- Image display ---
		for m in matches:
			r_x1 = m[0]
			r_y1 = m[1]
			cv2.circle(final_output, (r_x1, r_y1), 5, (0, 0, 255), -1)
		
		p1, p2, p3, p4 = display_grid(final_output, matches)
		print(p1, p2)
        
		# --- Zone detection ---
		if p1 is not None:
			detect_zone(frame8_gray, p1, p2, p3, p4)
			
		# --- Display ---
		image_disp, scale = display_image(final_output, disp_ratio=0.3)
		cv2.putText(image_disp, f'Sc={scale}', (10, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
		cv2.imshow("Flux / Camera", image_disp)
		cv2.imwrite("test.png", image_disp)

        # --- Mode management ---
		key = cv2.waitKey(1) & 0xFF
		if key == ord('q'):
			camera.camera_acquiring = False
			camera.close()
		elif key != 255:  # No key
			mode = key

	camera.close()
	cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
