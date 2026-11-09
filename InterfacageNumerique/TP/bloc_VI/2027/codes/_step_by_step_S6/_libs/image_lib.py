import cv2
import numpy as np
from lensepy.utils.images import get_screen_size

DISPLAY_RATIO = 0.8

def display_image(image, disp_ratio=DISPLAY_RATIO):
    height, width = get_screen_size()
    # --- Image display ---
    max_w = int(width * disp_ratio)
    max_h = int(height * disp_ratio)
    h_src, w_src = image.shape[:2]
    scale = min(max_w / w_src, max_h / h_src)
    new_w = int(w_src * scale)
    new_h = int(h_src * scale)
    display = cv2.resize(image, (new_w, new_h))
    return display, scale
    
   
def generate_histogram(image, gray=False, thickness=2, width=512, height=400):
    """
    Generate an image representing the histogram.
    """
    if image is None or image.size == 0:
        raise ValueError("Image vide ou invalide.")

    hist_img = np.zeros((height, width, 3), dtype=np.uint8)
    colors = [(255, 255, 255)]  # Gris : tracé blanc

    if image.ndim == 3:
        colors = [
            (255, 0, 0),    # Blue
            (0, 255, 0),    # Green
            (0, 0, 255)     # Red
        ]

    channels = [0] if image.ndim == 2 else range(image.shape[2])
    bar_width = width / 256

    for channel in channels:
        hist = cv2.calcHist([image], [channel], None, [256], [0, 256])
        hist = cv2.normalize(hist, None, 0, height - 20,
                             cv2.NORM_MINMAX)

        points = []
        for i in range(256):
            x = int(i * width / 256)
            y = height - 1 - int(hist[i, 0])
            points.append((x, y))

        cv2.polylines(
            hist_img,
            [np.array(points, dtype=np.int32)],
            False,
            colors[channel],
            thickness,
            cv2.LINE_AA
        )

    return hist_img


def rotate_image(image, angle):
    # Initial size
    (h, w) = image.shape[:2]
    center = (w / 2, h / 2)
    # Rotation matrix
    M = cv2.getRotationMatrix2D(center, angle, 1.0)

    # New dimensions
    cos = abs(M[0, 0])
    sin = abs(M[0, 1])
    new_w = int(h * sin + w * cos)
    new_h = int(h * cos + w * sin)

    # Translation from initial to new image
    M[0, 2] += (new_w / 2) - center[0]
    M[1, 2] += (new_h / 2) - center[1]

    # Rotation with white background
    rotated = cv2.warpAffine(
        image,
        M,
        (new_w, new_h),
        flags=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=(255, 255, 255)
    )

    return rotated


def scale_image(image, scale):
    """
    Modify scale of the image.
    :param image:   Image to modify
    :param scale:   Scale as a real.
    :return:    New image.
    """
    return cv2.resize(image, None, fx=scale, fy=scale)