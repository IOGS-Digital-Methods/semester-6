"""camera_flux.py
Basler Camera video flux display (OpenCV)
.. moduleauthor:: Julien VILLEMEJANE <julien.villemejane@institutoptique.fr>
"""

from pypylon import pylon
import cv2
import numpy as np

from lensepy.utils import get_screen_size
from lensepy.modules.basler.basler_models import init_first_camera

COLOR_MODE = "BGR8"  # "BGR8" / "Mono12"
GAUSS_SIZE = (7, 7)         # Taille du flou gaussien
GAUSS_SIGMA = 1.9

def main():
    # --- 
    height, width = get_screen_size()
    mode = 'z'
    
    camera = init_first_camera('./camera_vi.ini')
    if camera is None:
        cv2.destroyAllWindows()
        return
    
    camera.set_parameter('PixelFormat', COLOR_MODE)
    camera.open()
    camera.camera_acquiring = True
    
    print("Appuyez sur 'q' pour quitter")
    
    # --- Boucle d'acquisition ---
    while camera.camera_acquiring:
        # --- Get Image ---
        frame_raw = camera.get_image()
        # --- Processing ---
        if mode == 'a': # Canny
            if COLOR_MODE == 'Mono12':
                # Conversion 12 bits → 8 bits
                frame8 = (frame_raw / 16).astype(np.uint8)
            else:
                frame8 = frame_raw
            
            blur_frame8 = cv2.GaussianBlur(frame8, GAUSS_SIZE, GAUSS_SIGMA)
            # Canny
            final_output = cv2.Canny(blur_frame8, 50, 150)
        else:
            if COLOR_MODE == 'Mono12':
                # Conversion 12 bits → 8 bits
                frame8 = (frame_raw / 16).astype(np.uint8)
            else:
                frame8 = frame_raw
            final_output = frame8
        # Redimensionnement
        display = cv2.resize(final_output, (width//2, height//2))
        cv2.imshow("Flux Basler a2A1920", display)

        # --- Mode management ---
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            camera.camera_acquiring = False
            camera.close()
        elif key == ord('a'):
            mode = 'a'
        elif key == ord('z'):
            mode = 'z'
                            
        # --- Histogramme ---
        hist = cv2.calcHist([frame8],[0],None,[256],[0,256])
        hist_norm = cv2.normalize(hist, None, 0, 200, cv2.NORM_MINMAX)
        hist_img = np.full((200, 256), 255, dtype=np.uint8)

        for x in range(256):
            value = int(hist_norm[x].item())   # ✔ Conversion safe, plus de warning
            cv2.line(hist_img, (x, 200), (x, 200 - value), 0, 1)

        cv2.imshow("Histogramme", hist_img)

        #grab.Release()

    camera.close()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
