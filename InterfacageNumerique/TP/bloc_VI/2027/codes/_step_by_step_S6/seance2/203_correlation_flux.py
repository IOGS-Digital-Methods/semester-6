import sys
sys.path.append("../_libs/")

from camera_lib import init_camera, convert_image, COLOR_MODE, EXPOSURE_TIME
from image_lib import display_image, scale_image
import process_lib as pcv
from marker_finding import *

x0, y0, x1, y1 = 500, 200, 1200, 800
xx_delta = 74
yy_delta = 74
dx1 = 11
dy1 = 11
dx2 = 21
dy2 = 21

dir_path = '../_data_marker/'
ref_path = dir_path + 'mire_rep.png'
image_ref1 = cv2.imread(ref_path, cv2.IMREAD_GRAYSCALE)
image_ref1 = scale_image(image_ref1, 0.91)

def main():
    # ---
    mode = 'z'

    camera = init_camera(expo=2000)
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
        threshold = 0.8
        # Positions where corr > thresh
        ys, xs = np.where(result >= threshold)

        matches = [(x, y, result[y, x]) for x, y in zip(xs, ys)]

        # --- Image display ---
        image_disp, scale = display_image(final_output)
        for m in matches:
            r_x1 = m[0]
            r_y1 = m[1]
            r_x1_s = int(m[0] * scale)
            r_y1_s = int(m[1] * scale)
            cv2.circle(image_disp, (r_x1_s, r_y1_s), 5, (0, 0, 255), -1)
        cv2.putText(image_disp, f'Sc={scale}', (10, 15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # --- Display ---
        cv2.imshow("Flux / Camera", image_disp)
        cv2.imshow("Correlation", result)

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
