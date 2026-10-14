import cv2
import numpy as np

def detect_contours(image):
    """
    :param image:     Contour fourni par la fonction cv2.findContours
    :param min_area:    Surface minimale à détecter
    :param approx_factor:   Facteur d'approximation des formes
    :return:            contours, len of contours
    """
    contours, _ = cv2.findContours(image, cv2.RETR_LIST, cv2.CHAIN_APPROX_TC89_KCOS)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    return contours, len(contours)

def display_contours(img_out, contours, min_area=20, approx_factor=0.1, print_out=True):
    # Results preparation
    for cnt in contours:
        shape, approx, peri, area = detect_shape(cnt, min_area, approx_factor=approx_factor)
        if shape is not None:
            cv2.drawContours(img_out, [approx], -1, (255, 0, 0), 2)

            # Centre du contour
            M = cv2.moments(cnt)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                if print_out:
                    print(f'Shape : {shape} / cX: {cX} - cY: {cY} / Area = {area}')
                cv2.putText(img_out, shape, (cX - 30, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    return img_out


def detect_shape(contour, min_area=20, approx_factor=0.1):
    """
    :param contour:     Contour fourni par la fonction cv2.findContours
    :param min_area:    Surface minimale à détecter
    :param approx_factor:   Facteur d'approximation des formes
    :return:            shape, approx, peri, area
    """
    area = cv2.contourArea(contour)
    if area < min_area:
        return None, None, None,  None

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

    return shape, approx, peri, area


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
    return circles, len(circles)


def display_circles(img_out, circles):
    # Results preparation
    for (x, y, r) in circles:
        cv2.circle(img_out, (x, y), r, (0, 255, 0), 3)
        cv2.putText(img_out, "Cercle", (x - 20, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    return img_out