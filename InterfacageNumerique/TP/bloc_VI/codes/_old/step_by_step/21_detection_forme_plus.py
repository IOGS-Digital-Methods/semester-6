import cv2
import numpy as np
from matplotlib import pyplot as plt
from form_detection import detect_shape


# Parameters
MIN_AREA = 1
APPROX_FACTOR = 0.01

img_gray = cv2.imread('./_data/formes_blanc_30ms.png', cv2.IMREAD_GRAYSCALE)

_, img_thresh = cv2.threshold(
    img_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
)

# Image de sortie (couleur)
img_out = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2BGR)

# Détection Contours
contours, _ = cv2.findContours(img_thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_TC89_KCOS)

# Tri des contours
contours = sorted(contours, key=cv2.contourArea, reverse=True)

print(f'Number of contours: {len(contours)}')

# Traitement de tous les contours
for cnt in contours:
    area = cv2.contourArea(cnt)
    shape, approx, peri = detect_shape(cnt, min_area=MIN_AREA, approx_factor=APPROX_FACTOR)
    if shape is not None:
        cv2.drawContours(img_out, [approx], -1, (255, 0, 0), 2)

        # Centre du contour
        M = cv2.moments(cnt)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            print(f'Shape : {shape} / cX: {cX} - cY: {cY} / Area : {area}')
            cv2.putText(img_out, shape, (cX - 30, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

# =========================
#   AFFICHAGE
# =========================
plt.figure()
plt.imshow(img_gray, cmap='gray')
plt.title("Image Initiale")

plt.figure()
plt.imshow(img_thresh, cmap='gray')
plt.title("Seuil Otsu")

plt.figure()
plt.imshow(img_out)
plt.title("Formes détectées (polygones + cercles)")

plt.show()
