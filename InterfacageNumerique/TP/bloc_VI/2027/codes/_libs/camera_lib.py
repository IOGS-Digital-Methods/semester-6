
import cv2
import numpy as np
from pypylon import pylon
from lensepy_app.modules.camera.basler.basler_models import init_first_camera

COLOR_MODE = "BayerRG8"  # "BayerRG8" / "Mono12"
EXPOSURE_TIME = 3000       # integer in us

def init_camera(expo=EXPOSURE_TIME, color_mode=COLOR_MODE):
    # --- Find camera
    camera = init_first_camera('./config/camera_vi.ini')
    if camera is None:
        cv2.destroyAllWindows()
        return
    # --- Camera parameters
    camera.set_parameter('PixelFormat', color_mode)
    camera.set_parameter('ExposureTime', expo)
    # --- Start acquisition
    camera.open()
    camera.camera_acquiring = True

    return camera

def convert_image(frame_raw, color_mode):
    if color_mode == 'Mono12':
        # Conversion 12 bits to 8 bits
        return (frame_raw / 16).astype(np.uint8)
    elif COLOR_MODE == 'BayerRG8':
        return cv2.cvtColor(frame_raw, cv2.COLOR_BGR2RGB)
    else:
        return frame_raw