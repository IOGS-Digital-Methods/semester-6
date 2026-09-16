import cv2
import numpy as np


def detect_shape(contour, min_area=20, approx_factor=0.1):
    """
    :param contour:     Contour fourni par la fonction cv2.findContours
    :param min_area:    Surface minimale à détecter
    :param approx_factor:   Facteur d'approximation des formes
    :return:            shape, approx, peri
    """
    area = cv2.contourArea(contour)
    if area < min_area:
        return None, None, None

    peri = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, approx_factor * peri, True)
    n = len(approx)

    if n == 3:
        shape = "Triangle"
    elif n == 4:
        rect = cv2.minAreaRect(contour)
        w, h = rect[1]
        if h == 0 or w == 0:
            shape = "Inconnu"
        else:
            ratio = max(w, h) / min(w, h)
            shape = "Carre" if 0.90 < ratio < 1.10 else "Rectangle"
    elif n == 5:
        shape = "Pentagone"
    else:
        shape = f"{n}-gon"

    return shape, approx, peri


def detect_circles(image, minDist=30, minRadius=10, maxRadius=100):
    """
    :param image:   Image en nuance de gris dans laquelle on cherche des cercles
    :param minDist: Distance minimale entre les cercles
    :return:        Retourne une liste des coordonnées des centres et du rayon  (x, y, r)
    """
    circles = cv2.HoughCircles(
        image,
        cv2.HOUGH_GRADIENT,
        dp=1.2,
        minDist=minDist,
        param1=50,
        param2=30,
        minRadius=minRadius,
        maxRadius=maxRadius
    )
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
    return circles